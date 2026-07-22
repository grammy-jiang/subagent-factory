#!/usr/bin/env bash
# review-subagent-loop.sh <slug> [<slug> ...]
#
# Headless REVIEW -> FIX -> RE-REVIEW loop over one or more GENERATED subagent packages, until clean or a
# round cap. EACH review and EACH fix runs in its OWN FRESH `claude -p` session (no session reuse -> no
# context pollution); the loop itself is meant to run DETACHED (setsid) so it never touches an interactive
# context. It gates on small MARKER files (the review report's MUST_FIX_COUNT + `validate` PASS), never on
# transcripts or notifications.
#
# Per round, per slug:
#   1. deterministic gate  (validate_generated_package + quote_scan)   [inside the review session]
#   2. 4 reviewer lenses via Task, in parallel, inside ONE fresh review session:
#        agent-skills-advisor | profile-reviewer | faithfulness-reviewer | ai-agent-engineering-reviewer
#   3. consolidate -> write <pkg>/reports/review-loop/<slug>.rN.review.md ending "MUST_FIX_COUNT: <n>"
#   4. if n==0 AND validate PASS -> slug DONE
#   5. else (fresh FIX session) apply fixes, re-author flagged skills, re-export, re-validate -> next round
#   6. round cap reached with residual -> leave the review report as a TRIAGE artifact, stop that slug
#
# Launch (survivable):  bash campaign/detach.sh bash campaign/review-subagent-loop.sh <slug> [<slug>...]
# Env: MAXROUNDS(3) MODEL(claude-opus-4-8) REV_EFFORT(high) FIX_EFFORT(high)
set -euo pipefail

# REPO is overridable so a manager (e.g. drive-review-merge.sh) can point the whole loop at an
# ISOLATED git worktree: uncommitted fix edits on the main tree were once discarded by a concurrent
# `git checkout` in that shared tree. With REPO=<worktree> every review/fix session, validate, and
# per-round commit happens inside the worktree, immune to main-tree git ops.
REPO="${REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$REPO" || { echo "review-subagent-loop: cannot cd to REPO=$REPO" >&2; exit 3; }
# shellcheck source=/dev/null
source "$REPO/campaign/_claude_run.sh"
# shellcheck source=/dev/null
source "$REPO/campaign/_review_readonly.sh"

[ "$#" -ge 1 ] || { echo "usage: review-subagent-loop.sh <slug> [<slug>...]" >&2; exit 2; }
SLUGS=("$@")
MAXROUNDS="${MAXROUNDS:-3}"
MODEL="${MODEL:-claude-opus-4-8}"
REV_EFFORT="${REV_EFFORT:-high}"
FIX_EFFORT="${FIX_EFFORT:-high}"
# Space-separated agent names for the DOMAIN panel (accuracy cross-check). Chosen DYNAMICALLY by the
# review-subagent skill from the live .claude/agents/ roster + the target's domain; empty = structural-only.
DOMAIN_REVIEWERS="${DOMAIN_REVIEWERS:-}"
LOGDIR="$REPO/campaign/logs"; mkdir -p "$LOGDIR"

say(){ printf '[revloop] %s\n' "$*" | tee -a "$LOGDIR/review-loop.log"; }

# run_fresh_claude EFFORT PROMPT RUNLOG  — one FRESH `claude -p` session; prompt on stdin; stream-json to RUNLOG.
run_fresh_claude(){
  local eff="$1" prompt="$2" runlog="$3" perm="${4:-author}" argv
  # perm (author|review) selects the permission profile; a review session gets Edit denied so it
  # cannot modify the package it is reviewing. Passed as an explicit arg (not a leaked prefix var).
  CLAUDE_PERM_PROFILE="$perm" build_claude_argv argv "$MODEL" "$eff" "$REPO"
  # prompt arrives on stdin via the pipe; a trailing </dev/null would clobber it (empty prompt -> instant rc=1).
  printf '%s' "$prompt" | "${argv[@]}" >"$runlog" 2>&1
  return $?
}

review_prompt(){ # SLUG ROUND
  local slug="$1" round="$2" r dblock=""
  if [ -n "$DOMAIN_REVIEWERS" ]; then
    dblock=$(printf '\n\nPLUS these DOMAIN-expertise reviewers, dynamically selected for the domain of this subagent — each\ngives an INDEPENDENT cross-check that the guidance is correct, complete, and current for that domain; flag\ndomain errors, missing best-practices, or advice a domain expert would dispute. ALTITUDE: domain ACCURACY of\nthe content ONLY (not skill prose / agent design / over-claim, which the four lenses above already own). Spawn\neach via Task; skip any not deployed under .claude/agents/:')
    for r in $DOMAIN_REVIEWERS; do
      dblock="$dblock$(printf '\n  - %s -> subagents/%s/{principles/principles.yaml, skills/*/SKILL.md, profile.yaml}: is the domain guidance accurate and complete?' "$r" "$slug")"
    done
  fi
  cat <<EOF
You are running ONE review pass on a generated Claude Code subagent PACKAGE: subagents/$slug/ (cwd = repo
root $REPO). REVIEW ONLY — do NOT edit any file except the single review report named at the end.

STEP 1 — deterministic gates (run via Bash; note every FAIL/finding, they count as must-fix):
  python -m tools.subagent_factory.validate_generated_package subagents/$slug
  python -m tools.subagent_factory.quote_scan subagents/$slug
  # truncation gate: any hit is a SILENTLY-TRUNCATED skill body or adapter invariant (must-fix) —
  # a "…" ellipsis, or an invariant line severed inside a parenthetical (ending "(e.g").
  grep -rn '…' subagents/$slug/skills/*/SKILL.md subagents/$slug/adapters/claude-code/$slug.md 2>/dev/null
  grep -nE '\(e\.g\$|\([^)]*\$' subagents/$slug/adapters/claude-code/$slug.md 2>/dev/null | grep -F '**['

STEP 2 — spawn these reviewer subagents via the Task tool, IN PARALLEL, each returning findings
severity-ranked (must-fix|should-fix|nice) with a MUST_FIX_COUNT; hand each ONLY its scope:
  - agent-skills-advisor -> subagents/$slug/skills/*/SKILL.md + profile.yaml (charter). SKILL AUTHORING
    QUALITY only (description/triggers/progressive-disclosure/body/anti-patterns/lens-fit). Domain over-claim
    is OUT of scope (faithfulness covers it).
  - profile-reviewer -> subagents/$slug/profile.yaml + provenance-ledger.md. Release-readiness: role,
    when_to_use / when_not_to_use, quality_bar, forbidden_behaviours, outputs, self-check completeness.
  - faithfulness-reviewer -> subagents/$slug/profile.yaml rules vs principles/principles.yaml +
    reports/faithfulness-report.yaml. OVER-CLAIM only: a rule stronger than its source support.
  - ai-agent-engineering-reviewer -> .claude/agents/generated/$slug.md (the adapter) + profile.yaml. The
    subagent's DESIGN AS AN AGENT: role coherence, tool-boundary (Read/Grep/Glob only), when-to/not clarity,
    no over-reach/authority creep. ALTITUDE CONSTRAINT: review the agent design ONLY; do NOT re-litigate
    skill prose (agent-skills' job) or domain content (faithfulness' job).$dblock

STEP 3 — CONSOLIDATE all findings into ONE report (deterministic FAILs ARE must-fix). Dedup across lenses;
most-severe first; for each: where | severity | problem | fix. WRITE it to EXACTLY this path:
  subagents/$slug/reports/review-loop/$slug.r$round.review.md
End the file with a line exactly: MUST_FIX_COUNT: <n>   (n = deterministic FAILs + LLM must-fix, deduped).
Then STOP. Write NO other file. Do not fix anything.
EOF
}

fix_prompt(){ # SLUG ROUND
  local slug="$1" round="$2"
  cat <<EOF
You are FIXING a generated Claude Code subagent PACKAGE: subagents/$slug/ (cwd = repo root $REPO). Apply the
review findings, then re-validate to green. Stay STRICTLY grounded.

READ: subagents/$slug/reports/review-loop/$slug.r$round.review.md — the consolidated findings.

APPLY every must-fix + every high-value should-fix, GROUNDED (introduce NO claim not already in the package's
principles; a skill body must cite ONLY its own principle IDs):
  - Skill-body issues -> re-author each flagged skills/<name>/SKILL.md via the skill-author subagent (Task,
    one per flagged skill) to the GOLD shape: # Title, ## Purpose, ## When to use, ## Procedure (principles
    cited (Pxxx) inline), ## Inputs, ## Output, ## Anti-patterns to flag (skill-specific), ## References,
    ## Provenance; add a description: frontmatter line; DELETE any 'Review checklist' / verbatim 'Principles
    to apply' dump. PRESERVE each skill's frontmatter provenance block VERBATIM.
  - Profile issues -> edit subagents/$slug/profile.yaml (role / when_to_use / etc.).
  - Faithfulness over-claim -> weaken the offending profile rule to match its source support.
  - Then: bump agent_version + add a CHANGELOG.md entry AND a matching provenance-ledger.md Version History
    entry (supersession rule — every bump needs a ledger entry; refresh any field->grounding rows whose principle
    citations changed); re-export the adapter
    (python -m tools.subagent_factory.cli export $slug); if digest WARNs appear, python -m
    tools.subagent_factory.cli stale --stamp $slug; and run
    python -m tools.subagent_factory.validate_generated_package subagents/$slug until it PASSES (0 FAIL).
  - Touch NO other subagent. Do NOT edit the review report.

When validate PASSES, WRITE exactly one file: subagents/$slug/reports/review-loop/$slug.r$round.fix.done
containing "FIXED" + a one-sentence summary of what changed. STOP.
EOF
}

parse_mustfix(){ # REVIEW_FILE -> echoes n (or 999 if missing/unparseable)
  local f="$1" n
  n="$(grep -oiE 'MUST_FIX_COUNT:[[:space:]]*[0-9]+' "$f" 2>/dev/null | tail -1 | grep -oE '[0-9]+' || true)"
  printf '%s' "${n:-999}"
}

validate_pass(){ # SLUG -> 0 if PASS
  python -m tools.subagent_factory.validate_generated_package "subagents/$1" >/dev/null 2>&1
}

commit_round(){ # SLUG ROUND — durably commit this round's package state to the CURRENT branch, so a
  # concurrent main-tree git op cannot discard uncommitted fixes (the lost-fixes bug). Keeps .build
  # (tracked gen.py) but drops the large/distill-only raw sources.
  local slug="$1" r="$2" pkg="subagents/$1"
  git add -f "$pkg" ".claude/agents/generated/$slug.md" >>"$LOGDIR/review-loop.log" 2>&1 || true
  git reset -q -- "$pkg/sources/markdown" "$pkg/sources/assets" "$pkg/sources/original" \
    "$pkg/sources/maps" 2>/dev/null || true
  git commit --no-verify -m "review-loop($slug): round $r (validate PASS)" \
    >>"$LOGDIR/review-loop.log" 2>&1 && say "$slug r$r: committed (validate PASS)" || true
}

for SLUG in "${SLUGS[@]}"; do
  PKG="subagents/$SLUG"
  [ -f "$PKG/profile.yaml" ] || { say "$SLUG: no package, skip"; continue; }
  mkdir -p "$PKG/reports/review-loop"
  DONE="$PKG/reports/review-loop/$SLUG.CLEAN"
  [ -f "$DONE" ] && { say "$SLUG: already CLEAN, skip"; continue; }
  # A manager (drive-review-merge.sh) pre-creates an isolated worktree already on review/$SLUG and
  # sets NO_BRANCH=1; standalone, the loop makes the branch itself in the (main) tree.
  [ -n "${NO_BRANCH:-}" ] || git checkout -B "review/$SLUG" >>"$LOGDIR/review-loop.log" 2>&1 \
    || say "$SLUG: branch note"
  say "=== $SLUG: start on $(git branch --show-current) (maxrounds=$MAXROUNDS) ==="

  slug_clean=0
  for r in $(seq 1 "$MAXROUNDS"); do
    RF="$PKG/reports/review-loop/$SLUG.r$r.review.md"
    say "$SLUG round $r: REVIEW (fresh session)"
    # Snapshot the package BEFORE the review session so the read-only guard below reverts only THIS
    # review's writes (not an uncommitted prior-round fix).
    _before_ut="$(mktemp)"
    _pre="$(review_readonly_snapshot "$PKG" "$_before_ut")"
    run_fresh_claude "$REV_EFFORT" "$(review_prompt "$SLUG" "$r")" "$LOGDIR/review-loop-$SLUG.r$r.review.jsonl" review \
      || say "$SLUG r$r review rc=$?"
    # Read-only enforcement: a review session may only write its report under reports/; revert any
    # other file it touched in the package (Write can't be permission-scoped — see _claude_run.sh).
    _reverted="$(review_readonly_enforce "$PKG" "$_pre" "$_before_ut")"; rm -f "$_before_ut"
    if [ "${_reverted:-0}" -gt 0 ]; then
      say "$SLUG r$r: read-only guard reverted $_reverted non-report file(s) written by the review session"
    fi
    [ -f "$RF" ] || { say "$SLUG r$r: NO review file produced — aborting slug"; break; }
    mf="$(parse_mustfix "$RF")"
    say "$SLUG r$r: MUST_FIX_COUNT=$mf"
    if [ "$mf" = "0" ] && validate_pass "$SLUG"; then
      say "$SLUG: CLEAN at round $r"; slug_clean=1; break
    fi
    if [ "$r" = "$MAXROUNDS" ]; then
      say "$SLUG: round cap reached with residual — TRIAGE artifact = $RF"; break
    fi
    say "$SLUG round $r: FIX (fresh session)"
    run_fresh_claude "$FIX_EFFORT" "$(fix_prompt "$SLUG" "$r")" "$LOGDIR/review-loop-$SLUG.r$r.fix.jsonl" \
      || say "$SLUG r$r fix rc=$?"
    # marker-vs-disk: trust the package's ACTUAL validate state, not the .fix.done marker (a dead or
    # cap-killed fix session can leave a stale/misleading marker — the r1.fix.done that claimed v1.1.0
    # over a v1.0.0 disk). Commit every round that reaches PASS so the work is durable.
    if validate_pass "$SLUG"; then
      commit_round "$SLUG" "$r"
    else
      say "$SLUG r$r: fix left package INVALID on disk (marker $( [ -f "$PKG/reports/review-loop/$SLUG.r$r.fix.done" ] && echo present || echo missing ) — next round re-reviews)"
    fi
  done

  if [ "$slug_clean" = "1" ]; then
    echo "CLEAN after review-loop $(date -u +%FT%TZ)" > "$DONE"
    commit_round "$SLUG" "final"   # commits the .CLEAN marker alongside the converged package
    say "=== $SLUG: DONE (clean, committed on $(git branch --show-current)) ==="
  else
    say "=== $SLUG: STOPPED with residual (see the last review report) ==="
  fi
done

say "ALL SLUGS PROCESSED: ${SLUGS[*]}"
