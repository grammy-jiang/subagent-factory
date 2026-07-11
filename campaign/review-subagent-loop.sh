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
set -uo pipefail

REPO="/home/grammy-jiang/projects/subagent-factory"; cd "$REPO"
# shellcheck source=/dev/null
source "$REPO/campaign/_claude_run.sh"

[ "$#" -ge 1 ] || { echo "usage: review-subagent-loop.sh <slug> [<slug>...]" >&2; exit 2; }
SLUGS=("$@")
MAXROUNDS="${MAXROUNDS:-3}"
MODEL="${MODEL:-claude-opus-4-8}"
REV_EFFORT="${REV_EFFORT:-high}"
FIX_EFFORT="${FIX_EFFORT:-high}"
LOGDIR="$REPO/campaign/logs"; mkdir -p "$LOGDIR"

say(){ printf '[revloop] %s\n' "$*" | tee -a "$LOGDIR/review-loop.log"; }

# run_fresh_claude EFFORT PROMPT RUNLOG  — one FRESH `claude -p` session; prompt on stdin; stream-json to RUNLOG.
run_fresh_claude(){
  local eff="$1" prompt="$2" runlog="$3" argv
  build_claude_argv argv "$MODEL" "$eff" "$REPO"
  # prompt arrives on stdin via the pipe; a trailing </dev/null would clobber it (empty prompt -> instant rc=1).
  printf '%s' "$prompt" | "${argv[@]}" >"$runlog" 2>&1
  return $?
}

review_prompt(){ # SLUG ROUND
  local slug="$1" round="$2"
  cat <<EOF
You are running ONE review pass on a generated Claude Code subagent PACKAGE: subagents/$slug/ (cwd = repo
root $REPO). REVIEW ONLY — do NOT edit any file except the single review report named at the end.

STEP 1 — deterministic gates (run via Bash; note every FAIL/finding, they count as must-fix):
  python -m tools.subagent_factory.validate_generated_package subagents/$slug
  python -m tools.subagent_factory.quote_scan subagents/$slug

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
    skill prose (agent-skills' job) or domain content (faithfulness' job).

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
  - Then: bump agent_version + add a CHANGELOG.md entry; re-export the adapter
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

for SLUG in "${SLUGS[@]}"; do
  PKG="subagents/$SLUG"
  [ -f "$PKG/profile.yaml" ] || { say "$SLUG: no package, skip"; continue; }
  mkdir -p "$PKG/reports/review-loop"
  DONE="$PKG/reports/review-loop/$SLUG.CLEAN"
  [ -f "$DONE" ] && { say "$SLUG: already CLEAN, skip"; continue; }
  git checkout -B "review/$SLUG" >>"$LOGDIR/review-loop.log" 2>&1 || say "$SLUG: branch note"
  say "=== $SLUG: start (maxrounds=$MAXROUNDS) ==="

  slug_clean=0
  for r in $(seq 1 "$MAXROUNDS"); do
    RF="$PKG/reports/review-loop/$SLUG.r$r.review.md"
    say "$SLUG round $r: REVIEW (fresh session)"
    run_fresh_claude "$REV_EFFORT" "$(review_prompt "$SLUG" "$r")" "$LOGDIR/review-loop-$SLUG.r$r.review.jsonl" \
      || say "$SLUG r$r review rc=$?"
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
    [ -f "$PKG/reports/review-loop/$SLUG.r$r.fix.done" ] || say "$SLUG r$r: fix marker missing (check validate)"
  done

  if [ "$slug_clean" = "1" ]; then
    echo "CLEAN after review-loop $(date -u +%FT%TZ)" > "$DONE"
    git add -f "$PKG" ".claude/agents/generated/$SLUG.md" >>"$LOGDIR/review-loop.log" 2>&1 || true
    git reset -q -- "$PKG/sources/markdown" "$PKG/.build" 2>/dev/null || true
    git commit --no-verify -m "review-loop($SLUG): converged to must-fix=0" >>"$LOGDIR/review-loop.log" 2>&1 \
      || say "$SLUG: nothing to commit"
    say "=== $SLUG: DONE (clean, committed on review/$SLUG) ==="
  else
    say "=== $SLUG: STOPPED with residual (see the last review report) ==="
  fi
done

say "ALL SLUGS PROCESSED: ${SLUGS[*]}"
