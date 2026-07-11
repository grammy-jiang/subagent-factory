#!/usr/bin/env bash
# review-intel-loop.sh [target ...]
#
# Headless REVIEW -> FIX -> RE-REVIEW loop over the intelligence-analysis artifacts of THREE kinds:
#   subagent  (factory package under subagents/<slug>)
#   skill     (product SKILL.md under <product>/.claude/skills/<name>)
#   mcp       (product FastMCP server under <product>/mcp_servers/<pkg>)
# Each kind gets its own reviewer panel, fix recipe, and gate. EACH review and EACH fix runs in its OWN
# FRESH `claude -p` session (no reuse -> no context pollution). Run DETACHED (setsid). Gate on MARKER files
# (MUST_FIX_COUNT + the kind's deterministic gate), never transcripts.
#
# All sessions run FROM the factory repo (reviewer subagents live here) and --add-dir the product (to read/fix
# product files). Review reports + markers land in $FACTORY/reports/intel-review-loop (product stays clean).
#
# Targets default to all 12; override by passing "type:id" args, e.g.  mcp:ach_engine  skill:source-evaluation
# Launch:  bash campaign/detach.sh bash campaign/review-intel-loop.sh
# Env: MAXROUNDS(3) MODEL(claude-opus-4-8) REV_EFFORT(high) FIX_EFFORT(high)
set -uo pipefail

FACTORY="/home/grammy-jiang/projects/subagent-factory"
PRODUCT="/home/grammy-jiang/projects/intelligence-analysis-agent"
cd "$FACTORY"
# shellcheck source=/dev/null
source "$FACTORY/campaign/_claude_run.sh"

MAXROUNDS="${MAXROUNDS:-3}"; MODEL="${MODEL:-claude-opus-4-8}"
REV_EFFORT="${REV_EFFORT:-high}"; FIX_EFFORT="${FIX_EFFORT:-high}"
REVDIR="$FACTORY/reports/intel-review-loop"; LOG="$FACTORY/campaign/logs/review-intel-loop.log"
mkdir -p "$REVDIR" "$(dirname "$LOG")"
say(){ printf '[intel-revloop] %s\n' "$*" | tee -a "$LOG"; }

DEFAULT_TARGETS=(
  subagent:bias-perception-reviewer subagent:analytic-method-reviewer
  subagent:calibration-forecasting-reviewer subagent:deception-detection-reviewer
  skill:structured-analysis skill:calibrated-forecasting skill:source-evaluation skill:osint-investigation
  mcp:calibration_tracker mcp:evidence_ledger mcp:ach_engine mcp:osint_toolkit
)
TARGETS=("$@"); [ "${#TARGETS[@]}" -ge 1 ] || TARGETS=("${DEFAULT_TARGETS[@]}")

# All fixes land on a review branch in EACH repo (never master); commit + inspect after the loop.
git -C "$FACTORY" checkout -B review/intel-review >>"$LOG" 2>&1 || say "factory branch note"
git -C "$PRODUCT" checkout -B review/intel-review >>"$LOG" 2>&1 || say "product branch note"
say "review branches: factory review/intel-review + product review/intel-review"

run_fresh_claude(){ # EFFORT PROMPT RUNLOG  — one fresh session; --add-dir factory + product
  local eff="$1" prompt="$2" runlog="$3" argv
  build_claude_argv argv "$MODEL" "$eff" "$FACTORY" "$PRODUCT"
  # prompt arrives on stdin via the pipe; do NOT add </dev/null here — it would clobber the pipe (empty prompt).
  printf '%s' "$prompt" | "${argv[@]}" >"$runlog" 2>&1
}
parse_mf(){ grep -oiE 'MUST_FIX_COUNT:[[:space:]]*[0-9]+' "$1" 2>/dev/null | tail -1 | grep -oE '[0-9]+' || printf 999; }

# ---- per-kind REVIEW body ----
review_body(){ local kind="$1" id="$2" round="$3" rf="$4"; case "$kind" in
 subagent) cat <<EOF
ONE review pass on a generated subagent PACKAGE subagents/$id/ (cwd=$FACTORY). REVIEW ONLY.
Bash gate: python -m tools.subagent_factory.validate_generated_package subagents/$id ; python -m tools.subagent_factory.quote_scan subagents/$id  (FAILs = must-fix).
Task (parallel), each its own scope:
- agent-skills-advisor -> subagents/$id/skills/*/SKILL.md + profile.yaml. Skill authoring quality only.
- profile-reviewer -> subagents/$id/profile.yaml + provenance-ledger.md. Release-readiness (role/when_to/not/quality_bar/forbidden/self-check).
- faithfulness-reviewer -> profile rules vs principles/principles.yaml + reports/faithfulness-report.yaml. Over-claim only.
- ai-agent-engineering-reviewer -> .claude/agents/generated/$id.md + profile.yaml. Agent-design only (role/tool-boundary Read,Grep,Glob/no over-reach); ALTITUDE: not skill prose, not domain content.
Consolidate (dedup, severe-first) -> WRITE $rf ending "MUST_FIX_COUNT: <n>". STOP; write no other file.
EOF
 ;; skill) cat <<EOF
ONE review pass on a product METHOD skill $PRODUCT/.claude/skills/$id/SKILL.md (cwd=$FACTORY; product is --add-dir'd). REVIEW ONLY. This skill is the *method the intel-analysis agent runs*, grounded in $FACTORY/docs/intelligence-analysis/PIPELINE-grounded.md.
Task (parallel):
- agent-skills-advisor -> the SKILL.md. Authoring quality: description/triggers/progressive-disclosure/body/skill-specific anti-patterns. (A METHOD skill, not a reviewer.)
- ai-agent-engineering-reviewer -> the SKILL.md. The skill as a METHOD: procedure sound+actionable, correct delegation (reviewer subagents via Task + the MCP tools; the human-approval gate + loop-back for structured-analysis), no over-reach. ALTITUDE: method-design, not prose nits.
Consolidate -> WRITE $rf ending "MUST_FIX_COUNT: <n>". STOP; write no other file.
EOF
 ;; mcp) cat <<EOF
ONE review pass on a FastMCP server $PRODUCT/mcp_servers/$id/ (cwd=$FACTORY; product --add-dir'd). REVIEW ONLY.
Bash gate: cd $PRODUCT && python -m pytest tests/ -q   (test FAILs = must-fix).
Task (parallel), reading $PRODUCT/mcp_servers/$id/{server,store,models}.py (+ common.py/staleness.py if used):
- mcp-protocol-advisor -> tool defs/schemas/structured-output/read-back/error handling/stdio.
- mcp-security-advisor -> input validation, injection, the append-only hash-chain + verify_chain, judgment/collect-then-grade boundaries, no-egress (except osint), secrets.
- mcp-quality-advisor -> tool names/descriptions/schemas/granularity/agent-usability; judgment-input-vs-computed boundary clarity.
- python-reviewer -> store/server/models .py. Pythonic correctness, idiom, error handling, SQL parameterization.
Consolidate (test FAILs ARE must-fix; dedup) -> WRITE $rf ending "MUST_FIX_COUNT: <n>". STOP; write no other file.
EOF
 ;; esac; }

# ---- per-kind FIX body ----
fix_body(){ local kind="$1" id="$2" round="$3" rf="$4" done="$5"; case "$kind" in
 subagent) cat <<EOF
FIX subagent package subagents/$id/ (cwd=$FACTORY) per $rf. Grounded (no new claim; a skill body cites only its own principle IDs).
- Skill issues -> re-author flagged skills/<name>/SKILL.md via skill-author (Task, one/skill) to gold shape (Purpose/When-to-use/Procedure-cited-inline/Inputs/Output/skill-specific-Anti-patterns/References/Provenance + description:; drop Review-checklist/verbatim dump; preserve provenance frontmatter verbatim).
- Profile issues -> edit profile.yaml. Faithfulness over-claim -> weaken the rule to its source.
- On ANY version bump: increment agent_version AND add BOTH a CHANGELOG.md entry AND a matching provenance-ledger.md Version History entry (supersession rule — every bump needs a ledger entry; also refresh any field->grounding rows whose principle citations changed, e.g. quality_bar/forbidden_behaviours). Then python -m tools.subagent_factory.cli export $id ; cli stale --stamp $id if digest WARNs; run validate_generated_package subagents/$id until 0 FAIL.
Touch no other subagent. WRITE $done = "FIXED" + 1-sentence summary. STOP.
EOF
 ;; skill) cat <<EOF
FIX product skill $PRODUCT/.claude/skills/$id/SKILL.md (cwd=$FACTORY; product --add-dir'd) per $rf. Grounded in $FACTORY/docs/intelligence-analysis/PIPELINE-grounded.md (cite claims; introduce no ungrounded rule). Apply must-fix + high-value should-fix to the SKILL.md directly (or via skill-author Task). Keep the frontmatter name; keep/insert a crisp description. Do NOT change what the skill delegates to (the reviewer subagents / MCP tools) unless the review says the wiring is wrong.
WRITE $done = "FIXED" + 1-sentence summary. STOP.
EOF
 ;; mcp) cat <<EOF
FIX FastMCP server $PRODUCT/mcp_servers/$id/ (cwd=$FACTORY; product --add-dir'd) per $rf. Apply must-fix + high-value should-fix to the .py. Preserve the design invariants (analyst supplies judgment; append-only + hash-chain; bound-param SQL; no-egress except osint). After edits: cd $PRODUCT && python -m pytest tests/ -q until ALL PASS (add a regression test for any behavioural fix). Do NOT weaken a security control to make a test pass.
WRITE $done = "FIXED" + 1-sentence summary. STOP.
EOF
 ;; esac; }

# ---- per-kind deterministic GATE (0 = pass) ----
gate(){ local kind="$1" id="$2"; case "$kind" in
 subagent) python -m tools.subagent_factory.validate_generated_package "subagents/$id" >/dev/null 2>&1 ;;
 skill) grep -q '^name:' "$PRODUCT/.claude/skills/$id/SKILL.md" 2>/dev/null && grep -q '^description:' "$PRODUCT/.claude/skills/$id/SKILL.md" 2>/dev/null ;;
 mcp) ( cd "$PRODUCT" && python -m pytest tests/ -q >/dev/null 2>&1 ) ;;
esac; }

for T in "${TARGETS[@]}"; do
  KIND="${T%%:*}"; ID="${T#*:}"; TAG="$KIND-$ID"
  DONEMARK="$REVDIR/$TAG.CLEAN"; [ -f "$DONEMARK" ] && { say "$TAG already CLEAN, skip"; continue; }
  say "=== $TAG: start (maxrounds=$MAXROUNDS) ==="
  clean=0
  for r in $(seq 1 "$MAXROUNDS"); do
    RF="$REVDIR/$TAG.r$r.review.md"; FD="$REVDIR/$TAG.r$r.fix.done"
    say "$TAG r$r: REVIEW (fresh session)"
    run_fresh_claude "$REV_EFFORT" "$(review_body "$KIND" "$ID" "$r" "$RF")" "$REVDIR/$TAG.r$r.review.jsonl" || say "$TAG r$r review rc=$?"
    [ -f "$RF" ] || { say "$TAG r$r: NO review file — abort target"; break; }
    mf="$(parse_mf "$RF")"; say "$TAG r$r: MUST_FIX_COUNT=$mf"
    if [ "$mf" = "0" ] && gate "$KIND" "$ID"; then say "$TAG: CLEAN at r$r"; clean=1; break; fi
    [ "$r" = "$MAXROUNDS" ] && { say "$TAG: cap reached, residual -> triage $RF"; break; }
    say "$TAG r$r: FIX (fresh session)"
    run_fresh_claude "$FIX_EFFORT" "$(fix_body "$KIND" "$ID" "$r" "$RF" "$FD")" "$REVDIR/$TAG.r$r.fix.jsonl" || say "$TAG r$r fix rc=$?"
    [ -f "$FD" ] || say "$TAG r$r: fix marker missing (check gate)"
  done
  if [ "$clean" = 1 ]; then echo "CLEAN $(date -u +%FT%TZ)" > "$DONEMARK"; say "=== $TAG: DONE clean ==="
  else say "=== $TAG: STOPPED with residual ==="; fi
done
say "ALL TARGETS PROCESSED (${#TARGETS[@]}): ${TARGETS[*]}"
say "commit review branches manually after inspecting $REVDIR (factory: subagents; product: skills/mcp)."
