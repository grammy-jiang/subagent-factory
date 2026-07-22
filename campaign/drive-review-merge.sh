#!/usr/bin/env bash
# drive-review-merge.sh <slug> [<slug> ...]
#
# MANAGER (campaign layer) that drives /review-subagent to a MERGED PR, per slug, autonomously:
#
#   quota-gate -> isolated git worktree -> hardened review loop (converge to must-fix=0 + validate
#   PASS) -> ADVERSARIAL-VERIFY gate (faithfulness + domain lenses on the CHANGED package, Step 6) ->
#   fix+re-verify until the verify pass is clean or VMAX -> push -> PR -> poll CI green -> squash-merge
#   -> remove worktree. On any gate failure it STOPS that slug and leaves the worktree for triage.
#
# WHY a worktree per slug: the loop's fix edits must never sit uncommitted in the SHARED main tree,
# where a concurrent `git checkout` (a human merging sibling PRs) discarded them once. The loop runs
# with REPO=<worktree> + NO_BRANCH=1 and commits every round that validates.
#
# WHY a quota gate (this is an OPS concern, deliberately NOT in the review-subagent skill): a heavy
# multi-round review cap-killed mid-run corrupts state. Before each heavy engine step we block until
# the 5-hour window has headroom, so a review is never started into an about-to-cap window.
#
# Launch (survivable):  bash campaign/detach.sh bash campaign/drive-review-merge.sh <slug> [<slug>...]
# Env: MAXROUNDS(3) VMAX(2) QUOTA_MAX(70) MODEL(claude-opus-4-8) BASE(origin/master)
#      DOMAIN_REVIEWERS("")  DRY_RUN("" = merge; 1 = stop before push)
set -uo pipefail

REPO="/home/grammy-jiang/projects/subagent-factory"; cd "$REPO"
# shellcheck source=/dev/null
source "$REPO/campaign/_claude_run.sh"

[ "$#" -ge 1 ] || { echo "usage: drive-review-merge.sh <slug> [<slug>...]" >&2; exit 2; }
SLUGS=("$@")
MAXROUNDS="${MAXROUNDS:-5}"       # rounds inside each review-loop invocation (fresh bare-spine
                                 # subagents need >3 — the DRY_RUN capped at 3 with residual)
VMAX="${VMAX:-3}"                # convergence cycles: each = full loop -> adversarial verify (+vfix)
QUOTA_MAX="${QUOTA_MAX:-70}"      # block a review while five_hour.utilization >= this (%)
MODEL="${MODEL:-claude-opus-4-8}"
BASE="${BASE:-origin/master}"
DOMAIN_REVIEWERS="${DOMAIN_REVIEWERS:-}"
DRY_RUN="${DRY_RUN:-}"
WT_ROOT="$REPO/.worktrees"
LOGDIR="$REPO/campaign/logs"; mkdir -p "$LOGDIR" "$WT_ROOT"
LOG="$LOGDIR/drive-review.log"
say(){ printf '[drive] %s\n' "$*" | tee -a "$LOG"; }

# ------------------------------------------------------------------ quota gate
quota_util(){ ~/bin/claude-usage --json 2>/dev/null \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["five_hour"]["utilization"])' 2>/dev/null; }
quota_reset(){ ~/bin/claude-usage --json 2>/dev/null \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["five_hour"]["resets_at"])' 2>/dev/null; }

quota_gate(){ # block until five_hour.utilization < QUOTA_MAX (or the usage tool is unavailable)
  local util reset
  while :; do
    util="$(quota_util)" || { say "quota: usage check failed — proceeding"; return 0; }
    [ -n "$util" ] || { say "quota: no reading — proceeding"; return 0; }
    if awk "BEGIN{exit !($util < $QUOTA_MAX)}"; then
      say "quota OK (5h util=${util}% < ${QUOTA_MAX}%)"; return 0
    fi
    reset="$(quota_reset)"
    say "quota HIGH (5h util=${util}% >= ${QUOTA_MAX}%) — waiting for reset at ${reset}"
    sleep 600
  done
}

# ------------------------------------------------------------------ adversarial verify (Step 6)
verify_prompt(){ # SLUG WORKTREE ROUND
  local slug="$1" wt="$2" vr="$3" dblock="" r
  for r in $DOMAIN_REVIEWERS; do
    dblock="$dblock$(printf '\n  - %s — domain accuracy of the CHANGED principles/skills/profile' "$r")"
  done
  cat <<EOF
You are the ADVERSARIAL VERIFY gate (Step 6 of /review-subagent) for the JUST-CONVERGED package
subagents/$slug/ (cwd = $wt). The review loop reached must-fix=0; do NOT trust that. Independently,
adversarially re-check the package for surviving or newly-introduced defects. EDIT NOTHING except the
one verify report named below.

Spawn these reviewers via Task, IN PARALLEL, each returning findings with a MUST_FIX_COUNT, scoped:
  - faithfulness-reviewer — every profile rule vs principles/principles.yaml: any rule STRONGER than
    its cited principle (SCOPE_BROADENED / HEDGING_REMOVED / CONTRADICTED). Re-derive, don't trust the
    authored grades.
  - a safety/adapter check — read .claude/agents/generated/$slug.md "Operating invariants": any
    invariant truncated ("…" or a line ending "(e.g") or contradicting the advice-only role.$dblock

CONSOLIDATE most-severe-first into EXACTLY: subagents/$slug/reports/review-loop/$slug.verify$3.md
End with a line exactly: MUST_FIX_COUNT: <n>  (real must-fix only). Then STOP.
EOF
}

vfix_prompt(){ # SLUG WORKTREE VERIFYREPORT
  cat <<EOF
FIX the adversarial-verify findings for subagents/$1/ (cwd = $2), STRICTLY grounded — introduce NO
claim not already in principles/principles.yaml; weaken any over-claim to its cited principle; keep a
safety hedge complete. READ: $3. Then bump agent_version + CHANGELOG + provenance-ledger, re-export
(python -m tools.subagent_factory.cli export $1), and run validate until 0 FAIL. Touch no other
subagent. When validate PASSES write subagents/$1/reports/review-loop/$1.vfix.done ("FIXED" + summary).
EOF
}

mustfix_of(){ grep -oiE 'MUST_FIX_COUNT:[[:space:]]*[0-9]+' "$1" 2>/dev/null | tail -1 | grep -oE '[0-9]+' || echo 999; }
run_claude(){ local eff="$1" prompt="$2" log="$3" perm="${5:-author}" argv
  # $4 = --add-dir (worktree); $5 = permission profile (author|review). A verify session is
  # read-only + its own report, so it runs `review` (Edit denied); a vfix session needs `author`.
  CLAUDE_PERM_PROFILE="$perm" build_claude_argv argv "$MODEL" "$eff" "$4"
  printf '%s' "$prompt" | "${argv[@]}" >"$log" 2>&1; }

# ------------------------------------------------------------------ per-slug pipeline
review_one(){
  local slug="$1" wt v mf vr clean converged
  wt="$WT_ROOT/review-$slug"
  [ -f "$REPO/subagents/$slug/profile.yaml" ] || { say "$slug: no package — skip"; return 1; }
  git fetch origin master >>"$LOG" 2>&1 || true
  git worktree remove --force "$wt" 2>/dev/null || true
  git worktree add -B "review/$slug" "$wt" "$BASE" >>"$LOG" 2>&1 \
    || { say "$slug: worktree add failed — skip"; return 1; }
  say "=== $slug: worktree $wt on review/$slug @ $BASE ==="

  # CONVERGENCE (full-auto gate): cycle [ full review loop -> INDEPENDENT adversarial verify ] until
  # BOTH the loop reaches must-fix=0 (its .CLEAN marker = full-panel mf=0 AND validate PASS) AND the
  # adversarial verify reaches must-fix=0. Merge ONLY on that joint gate. A loop that caps with
  # residual is NOT converged (the DRY_RUN lesson: gating on validate alone would merge residual
  # must-fix) — after VMAX cycles without joint convergence the slug STOPS for human triage.
  clean="$wt/subagents/$slug/reports/review-loop/$slug.CLEAN"
  converged=0
  for v in $(seq 1 "$VMAX"); do
    quota_gate
    rm -f "$clean"
    say "$slug: converge cycle $v/$VMAX (review loop, maxrounds=$MAXROUNDS)"
    REPO="$wt" NO_BRANCH=1 MAXROUNDS="$MAXROUNDS" DOMAIN_REVIEWERS="$DOMAIN_REVIEWERS" \
      bash "$REPO/campaign/review-subagent-loop.sh" "$slug" >>"$LOG" 2>&1 || true
    if [ ! -f "$clean" ]; then
      say "$slug: cycle $v — loop capped with RESIDUAL must-fix (not converged)"
      [ "$v" = "$VMAX" ] && { say "$slug: NOT converged after $VMAX cycles — STOP, NOT merging (triage $wt)"; return 1; }
      continue   # next cycle re-runs the loop, which keeps fixing (it commits each round it validates)
    fi
    quota_gate
    vr="$wt/subagents/$slug/reports/review-loop/$slug.verify$v.md"
    say "$slug: cycle $v — loop reached must-fix=0; INDEPENDENT adversarial verify"
    run_claude high "$(verify_prompt "$slug" "$wt" "$v")" "$LOG.$slug.verify$v" "$wt" review || true
    [ -f "$vr" ] || { say "$slug: verify $v produced no report — STOP (triage $wt)"; return 1; }
    mf="$(mustfix_of "$vr")"
    say "$slug: verify$v MUST_FIX=$mf"
    if [ "$mf" = "0" ]; then converged=1; break; fi
    [ "$v" = "$VMAX" ] && { say "$slug: verify still mf=$mf at VMAX — STOP (triage $wt)"; return 1; }
    quota_gate
    say "$slug: verify-fix cycle $v (grounded)"
    run_claude high "$(vfix_prompt "$slug" "$wt" "$vr")" "$LOG.$slug.vfix$v" "$wt" || true
    ( cd "$wt" && git add -A "subagents/$slug" ".claude/agents/generated/$slug.md" \
      && git reset -q -- "subagents/$slug/sources/markdown" "subagents/$slug/sources/assets" \
        "subagents/$slug/sources/original" "subagents/$slug/sources/maps" 2>/dev/null; \
      git commit --no-verify -m "review($slug): adversarial-verify fix cycle $v" ) >>"$LOG" 2>&1 || true
    # next cycle re-runs the FULL loop to re-confirm must-fix=0 after the vfix
  done
  [ "$converged" = "1" ] || { say "$slug: not converged — STOP (triage $wt)"; return 1; }

  # hard gate: validate PASS on disk (belt-and-suspenders; the loop .CLEAN already implies it)
  ( cd "$wt" && python -m tools.subagent_factory.validate_generated_package "subagents/$slug" ) >>"$LOG" 2>&1 \
    || { say "$slug: NOT validate-clean — STOP, NOT merging (triage $wt)"; return 1; }

  if [ -n "$DRY_RUN" ]; then say "$slug: DRY_RUN — CONVERGED (loop mf=0 AND verify mf=0), stopping before push ($wt)"; return 0; fi

  # 4) push -> PR -> CI -> squash-merge
  ( cd "$wt" && git push --no-verify -u origin "review/$slug" ) >>"$LOG" 2>&1 \
    || { say "$slug: push failed — STOP"; return 1; }
  local pr
  pr="$( cd "$wt" && gh pr create --base master --head "review/$slug" \
    --title "review($slug): /review-subagent converge to must-fix=0 (adversarial-verified)" \
    --body "Headless review→fix→adversarial-verify to must-fix=0; validate + quote_scan + CI gated. Driven by campaign/drive-review-merge.sh." 2>>"$LOG" \
    | grep -oE '/pull/[0-9]+' | grep -oE '[0-9]+' | tail -1)"
  [ -n "$pr" ] || { say "$slug: PR create failed — STOP"; return 1; }
  say "$slug: PR #$pr — polling CI"
  local i total pend
  for i in $(seq 1 80); do
    total="$(gh pr checks "$pr" --json bucket 2>/dev/null | python3 -c 'import sys,json;d=json.load(sys.stdin);print(len(d))' 2>/dev/null || echo 0)"
    pend="$(gh pr checks "$pr" --json bucket 2>/dev/null | python3 -c 'import sys,json;print(sum(1 for c in json.load(sys.stdin) if c["bucket"]=="pending"))' 2>/dev/null || echo 1)"
    [ "$total" -gt 0 ] && [ "$pend" = "0" ] && break
    sleep 30
  done
  if gh pr checks "$pr" >/dev/null 2>&1; then
    gh pr merge "$pr" --squash >>"$LOG" 2>&1 && say "=== $slug: MERGED PR #$pr ===" \
      && { git worktree remove --force "$wt" 2>/dev/null || true; return 0; }
    say "$slug: merge command failed on PR #$pr — STOP"; return 1
  else
    say "$slug: CI FAILED on PR #$pr — NOT merging (triage)"; gh pr checks "$pr" >>"$LOG" 2>&1; return 1
  fi
}

for SLUG in "${SLUGS[@]}"; do
  review_one "$SLUG" || say "=== $SLUG: STOPPED (see $LOG + worktree) ==="
done
say "ALL SLUGS PROCESSED: ${SLUGS[*]}"
