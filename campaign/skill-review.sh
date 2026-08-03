#!/usr/bin/env bash
# Iterative review of ONE Claude Code Skill by this repo's GENERATED reviewer subagents — each round
# in a FRESH, INDEPENDENT headless `claude -p` instance (no context shared with the fixer session, so
# the review is unbiased by the implementation chat).
#
# Same shape as campaign/dogfood-review.sh (which reviews the factory itself); this one targets an
# arbitrary skill directory, which normally lives OUTSIDE this repo (e.g. ~/.claude/skills/<name>).
# The headless instance still runs with cwd = this repo, because the reviewer subagents are installed
# at .claude/agents/generated/ here; the skill dir is exposed read-only via --add-dir.
#
# One round per invocation:
#   1. render the review prompt for the ACTIVE reviewers,
#   2. snapshot the skill dir (it must come out byte-identical — a review may not fix anything),
#   3. run the prompt in a fresh headless instance (root-safe --allowedTools allowlist, NOT
#      --dangerously-skip-permissions, which the CLI refuses under root),
#   4. restore any stray write to the skill dir,
#   5. digest: print the NEW findings, record them, and DROP converged reviewers.
# Then YOU (the fixer session) read the digest, apply the fixes, and run the next round.
#
# A reviewer is DROPPED from later rounds once its NEW must-fix + should count is 0 (--drop-when
# no-actionable) — that is the token saver: converged reviewers stop being spawned.
#
# Usage:
#   campaign/skill-review.sh --skill <dir> [--round N] [--reviewers a,b,c]
#                            [--model M] [--timeout S] [--dry-run]
# Reset the loop:  rm -rf campaign/skill-review/<skill-name>/
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO" || { echo "skill-review: cannot cd to REPO=$REPO" >&2; exit 3; }

MODEL="${MODEL:-claude-opus-4-8}"
TIMEOUT="${RUN_TIMEOUT:-3000}"
SKILL_DIR=""; ROUND=""; REVIEWERS_ARG=""; DRYRUN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --skill) SKILL_DIR="$2"; shift 2;;
    --round) ROUND="$2"; shift 2;;
    --reviewers) REVIEWERS_ARG="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found on PATH" >&2; exit 3; }

# ── target validation (the restore step deletes files under here — be strict) ────────────────────
[ -n "$SKILL_DIR" ] || { echo "skill-review: --skill <dir> is required" >&2; exit 2; }
SKILL_DIR="$(cd "$SKILL_DIR" 2>/dev/null && pwd)" \
  || { echo "skill-review: --skill dir does not exist" >&2; exit 3; }
case "$SKILL_DIR" in
  /|/home|/home/*/|"$HOME") echo "skill-review: refusing unsafe --skill '$SKILL_DIR'" >&2; exit 3;;
esac
# A skill is either a bare directory holding SKILL.md, or a project that ships
# one alongside the code that backs it — beside the source, or inside the
# package itself so that the checkout and the installed tree are the same paths.
# All are reviewable; the project cases are the more useful targets because the
# reviewers see the code too. An unmatched glob stays literal and fails -f.
SKILL_MD=""
for candidate in "$SKILL_DIR/SKILL.md" "$SKILL_DIR/skill/SKILL.md" \
                 "$SKILL_DIR"/src/*/skill/SKILL.md; do
  [ -f "$candidate" ] || continue
  if [ -n "$SKILL_MD" ]; then
    echo "skill-review: more than one SKILL.md under $SKILL_DIR" >&2
    echo "  $SKILL_MD" >&2
    echo "  $candidate" >&2
    echo "skill-review: point --skill at the one you mean" >&2
    exit 3
  fi
  SKILL_MD="$candidate"
done
if [ -z "$SKILL_MD" ]; then
  echo "skill-review: no SKILL.md under $SKILL_DIR (./, ./skill/, ./src/*/skill/) — not a skill" >&2
  exit 3
fi
SKILL_NAME="$(basename "$SKILL_DIR")"

WORK="$REPO/campaign/skill-review/$SKILL_NAME"
STATE="$WORK/active-reviewers.txt"; SEEN="$WORK/seen.tsv"
mkdir -p "$WORK"

# Reviewer -> the lens it applies to a skill. Seeds the default active set + the prompt's domain hints.
declare -A HINT=(
  [agent-skills-advisor]="SKILL.md as an Agent Skill — frontmatter validity, the description as the ONLY trigger signal (specific enough to fire, bounded enough not to over-fire), progressive disclosure vs context bloat, body structure and step ordering, the bundled-script contract, and whether a skill is even the right primitive here"
  [python-reviewer]="the bundled *.py scripts — idiomatic Python, correctness, error handling, CLI contract, encoding/atomicity, edge cases when called with model-chosen arguments"
  [python-testing-advisor]="tests/ — test design and coverage gaps, weak or tautological assertions, fixtures and isolation, what the suite would fail to catch, and whether the offline stubs (a fake curl on PATH) still exercise the real code path"
  [software-design]="the split across gitignore.py / gitwork.py / render_summary.py / _shared.py — responsibility boundaries, coupling through the facts JSON, duplication, and whether the SKILL.md-vs-script division puts each decision in the right place"
  [application-security-reviewer]="the trust boundary — content fetched from a remote API and written into a repo file, argument/name validation before it reaches a URL or a shell, path handling, and the irreversible git operations (commit/push/--force-with-lease) the skill body prescribes"
  [bash-shell-scripting-advisor]="every shell command the SKILL.md body tells the agent to run — quoting, word-splitting, exit-status checking, git plumbing correctness (rev-parse/rev-list/push semantics), and failure paths that are silently skipped"
  [documentation-as-code-advisor]="SKILL.md as instructions an LLM must execute — ambiguity, unstated preconditions, missing failure branches, Diataxis type confusion, ordering, and whether every step is unambiguously actionable"
  [pragmatic-programming-advisor]="DRY across SKILL.md and the scripts, orthogonality, whether the skill fails loud, and whether any rule is stated in two places that can drift"
  [software-testing-advisor]="tests/ from a technique angle rather than a pytest angle — which cases the specification demands, the coverage criterion actually achieved, the fake-curl test double (right kind? does it still exercise the real path?), and test smells (eager/obscure/fragile tests, assertion roulette)"
  [ux-design-advisor]="the operator experience — the AskUserQuestion prompts, what the user is asked to decide and whether they have enough information at that moment, and the final summary's readability"
)
DEFAULT_REVIEWERS=(agent-skills-advisor python-reviewer python-testing-advisor \
  software-testing-advisor application-security-reviewer bash-shell-scripting-advisor \
  documentation-as-code-advisor software-design ux-design-advisor)

# Active reviewers this round: --reviewers  >  state file  >  default seed (seeded on first run).
if [ -n "$REVIEWERS_ARG" ]; then
  IFS=',' read -ra ACTIVE <<< "$REVIEWERS_ARG"
elif [ -s "$STATE" ]; then
  mapfile -t ACTIVE < <(grep -vE '^[[:space:]]*(#|$)' "$STATE")
else
  ACTIVE=("${DEFAULT_REVIEWERS[@]}"); printf '%s\n' "${ACTIVE[@]}" > "$STATE"
fi
[ "${#ACTIVE[@]}" -gt 0 ] || { echo "[skill-review] no active reviewers left — converged."; exit 0; }
for r in "${ACTIVE[@]}"; do
  [ -f "$REPO/.claude/agents/generated/$r.md" ] \
    || { echo "[skill-review] unknown reviewer subagent: $r" >&2; exit 2; }
done

# Round number: explicit, else max existing round + 1 (claimed atomically via a bare mkdir).
if [ -z "$ROUND" ]; then
  last=0
  for d in "$WORK"/round-*; do
    [ -d "$d" ] || continue; nn="${d##*/round-}"
    case "$nn" in ''|*[!0-9]*) ;; *) [ "$nn" -gt "$last" ] && last="$nn";; esac
  done
  ROUND=$((last + 1))
  while ! mkdir "$WORK/round-$ROUND" 2>/dev/null; do ROUND=$((ROUND + 1)); done
  RDIR="$WORK/round-$ROUND"
else
  RDIR="$WORK/round-$ROUND"; mkdir -p "$RDIR"   # explicit --round N: idempotent (allows re-run)
fi
FINDINGS="$RDIR/findings.json"                  # OUTSIDE the skill dir, so the restore is total

# Prompt inputs: per-reviewer domain block + the prior titles the instance must not repeat.
REVIEWER_BLOCK=""
for r in "${ACTIVE[@]}"; do REVIEWER_BLOCK+="  - ${r}: ${HINT[$r]:-(general review of this skill)}"$'\n'; done
if [ -s "$SEEN" ]; then PRIOR_TITLES="$(awk -F'\t' 'NF>=3{print "  - "$2": "$3}' "$SEEN")"
else PRIOR_TITLES="  (none yet — first round)"; fi

promptfile="$RDIR/prompt.txt"
ROUND="$ROUND" SKILL_NAME="$SKILL_NAME" SKILL_DIR="$SKILL_DIR" REVIEWER_BLOCK="$REVIEWER_BLOCK" \
FINDINGS="$FINDINGS" PRIOR_TITLES="$PRIOR_TITLES" SKILL_MD="$SKILL_MD" \
  python3 "$REPO/campaign/render-prompt.py" "$REPO/campaign/skill-review-prompt.tmpl" > "$promptfile"

echo "[skill-review] skill=$SKILL_NAME  dir=$SKILL_DIR"
echo "[skill-review] round=$ROUND  reviewers=${#ACTIVE[@]} (${ACTIVE[*]})"
echo "[skill-review] model=$MODEL  timeout=${TIMEOUT}s"
echo "[skill-review] findings -> $FINDINGS"

if [ "$DRYRUN" -eq 1 ]; then
  echo "------------------ rendered prompt ------------------"; cat "$promptfile"
  rm -rf -- "$RDIR"   # a dry run must not consume the round number it claimed
  exit 0
fi

# ── refuse to run against a working tree someone is editing ──────────────────────────────────────
# The guard below restores anything that changed during the session, on the
# assumption that only the reviewer could have changed it. That assumption held
# when the target was a docs-only skill directory; against a live repository it
# is false, and the restore silently reverts the author's concurrent edits.
# Requiring a clean tree makes the assumption true again: afterwards, anything
# that differs really is the reviewer's doing.
if git -C "$SKILL_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  tree_dirty="$(git -C "$SKILL_DIR" status --porcelain)"
  if [ -n "$tree_dirty" ]; then
    echo "[skill-review] $SKILL_DIR has uncommitted changes. Commit or stash them first —" >&2
    echo "[skill-review] the read-only guard restores the tree afterwards and would revert them:" >&2
    printf '%s\n' "$tree_dirty" | sed 's/^/  /' >&2
    exit 3
  fi
fi

# ── read-only guard: snapshot the skill dir BEFORE the session ───────────────────────────────────
# `Write` cannot be permission-scoped in this claude version (bare `Write` is allow-all), so the
# review instance is held read-only at the LOOP level: snapshot, then restore anything it touched.
SNAP="$RDIR/.skill-snapshot"
rm -rf -- "$SNAP"; mkdir -p "$SNAP"
# Skip build and cache output: it changes on its own, and snapshotting it buried
# the one line that mattered under a dozen .pyc and .ruff_cache entries.
tar -C "$SKILL_DIR" -cf - \
  --exclude=.git --exclude=__pycache__ --exclude='.*_cache' \
  --exclude=dist --exclude=build --exclude='*.egg-info' . | tar -C "$SNAP" -xf -

log="$RDIR/session.log.jsonl"
echo "[skill-review] launching fresh headless instance…"
rc=0
# Root-safe: an explicit allowlist (Read/Grep/Glob to review, Task to spawn reviewer subagents, Write
# for the findings JSON) runs non-interactively WITHOUT --dangerously-skip-permissions, which the CLI
# refuses under root.
timeout "$TIMEOUT" claude -p \
  --model "$MODEL" \
  --add-dir "$SKILL_DIR" \
  --allowedTools "Read Grep Glob Task Write" \
  --output-format stream-json --verbose \
  < "$promptfile" > "$log" 2>&1 || rc=$?
echo "[skill-review] instance rc=$rc  log=$log"

# ── restore: the skill dir must come out exactly as it went in ───────────────────────────────────
reverted=0
while IFS= read -r -d '' rel; do            # modified or deleted vs the snapshot -> put it back
  if ! cmp -s -- "$SNAP/$rel" "$SKILL_DIR/$rel"; then
    mkdir -p -- "$(dirname -- "$SKILL_DIR/$rel")"
    cp -a -- "$SNAP/$rel" "$SKILL_DIR/$rel"
    echo "[skill-review]   reverted: $rel" >&2; reverted=$((reverted + 1))
  fi
done < <(cd "$SNAP" && find . -type f -printf '%P\0')
while IFS= read -r -d '' rel; do            # created by the session -> remove (named file, no glob)
  if [ ! -e "$SNAP/$rel" ]; then
    rm -f -- "$SKILL_DIR/$rel"
    echo "[skill-review]   removed stray: $rel" >&2; reverted=$((reverted + 1))
  fi
done < <(cd "$SKILL_DIR" && find . -type f \
    -not -path './.git/*' -not -path '*/__pycache__/*' -not -path './.*_cache/*' \
    -not -path './dist/*' -not -path './build/*' -not -path '*.egg-info/*' -printf '%P\0')
if [ "$reverted" -gt 0 ]; then
  echo "[skill-review] WARNING: review instance wrote to the skill dir; $reverted path(s) restored." >&2
else
  echo "[skill-review] skill dir unchanged (read-only honoured)."
fi
rm -rf -- "$SNAP"

[ -f "$FINDINGS" ] || { echo "[skill-review] NO findings.json produced — inspect $log (rc=$rc)."; exit 4; }

# Digest: NEW vs prior rounds, print the fix-list, record seen titles, drop converged reviewers.
# --drop-when no-actionable: a reviewer whose new must-fix + should count is 0 stops being spawned.
python3 "$REPO/campaign/dogfood_digest.py" \
  --round "$ROUND" --findings "$FINDINGS" --seen "$SEEN" --state "$STATE" \
  --active "$(IFS=,; echo "${ACTIVE[*]}")" \
  --label "SKILL REVIEW ($SKILL_NAME)" --drop-when no-actionable

echo "[skill-review] round $ROUND done. Fix the findings above, then re-run for the next round."
