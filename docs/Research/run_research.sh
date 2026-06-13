#!/usr/bin/env bash
#
# run_research.sh — launch independent headless Claude research runs.
#
# Why a script + `claude -p` (not the Agent tool): a spawned sub-agent cannot
# spawn its own sub-agents, but the research-pipeline `deep` profile requires
# sub-agents (paper-screener / paper-analyzer / paper-synthesizer). Each
# `claude -p` invocation is a real TOP-LEVEL session that CAN spawn them.
#
# Each topic runs fully sandboxed to its own subfolder. Every artifact lands in
# that folder. The only permitted external location is the shared pipeline cache
# under ~/.cache (PDF + SQLite index) — that is by design.
#
# Usage:
#   bash docs/Research/run_research.sh            # launch all 3 in background
#   MODEL=opus bash docs/Research/run_research.sh # higher-quality (pricier) workers
#   TOPICS_FILTER=prompt-injection-defense bash docs/Research/run_research.sh  # one topic
#
set -euo pipefail

# ── Config (override via env) ────────────────────────────────────────────────
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"   # real binary, NOT the shell alias
SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills/research-pipeline}"
CFG="${CFG:-$SKILL_DIR/config.toml}"
RUNNER="$SKILL_DIR/runners/runner.py"
PROFILE="${PROFILE:-deep}"
MODEL="${MODEL:-opus}"                                 # worker model
EFFORT="${EFFORT:-max}"                                # reasoning effort level
RESEARCH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # docs/Research
TOPICS_FILTER="${TOPICS_FILTER:-}"                     # optional: run only this folder

# ── Topic registry:  folder | topic | seed-keywords | downstream-use ─────────
declare -a TOPICS=(
"prompt-injection-defense|Indirect prompt-injection defenses for LLM systems that ingest untrusted documents: detection, content isolation and spotlighting, sanitization, and benchmarks|indirect prompt injection; injection detection; untrusted content; spotlighting; data-marking defense; jailbreak detection; LLM security benchmark; content sanitization; data exfiltration|Feeds a deterministic prompt-injection scan (regex/heuristics over ingested source markdown), an adapter-policy scan, an untrusted-source policy rule, and attack fixtures for a factory that turns arbitrary PDFs/HTML into agent behaviour."
"argument-mining-claim-extraction|Argument mining and atomic claim extraction from long-form technical and scientific documents: claim and premise detection, claim typing, condition and exception extraction, and evidence linking|argument mining; claim detection; premise extraction; argument component classification; claim typing; scientific claim extraction; evidence linking; discourse segmentation; key-point extraction|Feeds a claims schema (claim/premise/condition/exception/type taxonomy), an LLM claim-extraction prompt, and claim fixtures used to distill expert principles from books/papers into subagents."
"factual-consistency-faithfulness|Factual consistency and faithfulness evaluation of LLM-generated text against source documents: hallucination and overgeneralization detection, claim verification, and entailment- and QA-based metrics|faithfulness evaluation; factual consistency; hallucination detection; claim verification; natural language inference; textual entailment; QA-based factuality; overclaiming detection; attribution faithfulness|Feeds a faithfulness rubric and a 'generated rule stronger than its source evidence' detection method, plus a faithfulness-report schema and fixtures, to stop a subagent factory from over-claiming beyond its sources."
"long-document-structure-mapping|Hierarchical reading of long technical and scientific documents for distillation: long-document and hierarchical summarisation, topic and discourse segmentation, document-structure extraction, and candidate knowledge-unit identification over 200+ page books|long-document summarization; hierarchical summarization; discourse segmentation; topic segmentation; TextTiling; document structure extraction; section and chapter segmentation; key-point extraction; candidate unit extraction; semantic chunking; book-length summarization; long-context document reading|Feeds a Tier-1 source-structure-mapping preprocessing step (Phase 2A/2B) for the subagent factory: before claim extraction, build a hierarchical map of a 200+ page book (part -> chapter -> section -> key passage) and segment it into candidate knowledge units, so claim and principle extraction reads structure-aware instead of flat-reading the whole text. Aim: higher recall and precision of extracted claims/principles/skills on long books (e.g. a 131k-word concurrency book already processed). Keep it a literature review of methods and how to apply them, not a product build."
"knowledge-fusion-conflict-detection|Cross-document knowledge fusion and contradiction detection for merging expert principles distilled from multiple source documents: cross-document concept and entity alignment, alias and duplicate clustering across documents, cross-document contradiction and conflict detection, and claim/knowledge reconciliation with conflict resolution|cross-document contradiction detection; knowledge fusion; conflicting information across documents; cross-document entity and event coreference; concept alignment; ontology and knowledge-graph alignment and fusion; claim deduplication; truth discovery; conflicting evidence aggregation; stance detection across documents; knowledge conflict resolution; defeasible reasoning|Feeds Step 7 multi-source synthesis in the subagent factory: merge 2+ books' distilled principles into one model — cluster co-expressed concepts across sources (alias/dedup), detect cross-source contradictions, and reconcile/record a principle graph. SCOPE: only the CROSS-document layer; the intra-document argument-relation vocabulary (claim/premise, stance support/contest, Pollock rebut/undercut) is already covered by the argument-mining research and must NOT be re-covered. Literature review of methods + how to apply (deterministic-seed vs LLM split), not a product build."
)

# ── Prompt builder ───────────────────────────────────────────────────────────
build_prompt () {
  local topic="$1" keywords="$2" why="$3"
  cat <<EOF
Research the following topic using the research-pipeline skill, ${PROFILE} profile. This is an independent, unattended run.

TOPIC:
${topic}

SEED KEYWORDS (focus the query plan; edit plan/query_plan.json if recall is weak):
${keywords}

DOWNSTREAM USE (anchor scope to this application; keep it a literature review, not a product build):
${why}

HOW TO RUN:
- Launch via the runner, never bypass it. Round 1:
    python3 ${RUNNER} "${topic}" --profile ${PROFILE} --config ${CFG}
- Follow the research-pipeline SKILL rules: when the runner prints DELEGATE TO SUB-AGENT, run the named sub-agent (paper-screener / paper-analyzer / paper-synthesizer) with the printed contract, set that task to accepted, and re-run. Honor reviewer gates (on 'rejected': fix, reset task to pending, re-run).
- Write the final report only after validate-report is accepted.
- DO NOT STOP AFTER ROUND 1. If the validated report still lists any HIGH-severity ACADEMIC gap and round < 4, you MUST run gap-closure round(s) per references/iterative-synthesis.md (new run_id, carry prior_paper_ids, derive a gap-specific topic from the open gap's suggested query) until every HIGH academic gap is closed or reclassified, or the 4-round hard cap is reached. ENGINEERING gaps are resolved inline in the report, never via a new round.

OUTPUT / SANDBOX RULES (hard):
- Your current working directory is this topic folder. Put EVERY artifact here: plan/, search/, screen/, download/, convert/, extract/, summarize/, workflow_state.json, gaps.json, and the final <topic-slug>-research-report.md.
- Do NOT modify, create, or delete any file outside this folder. The ONLY permitted external location is the shared pipeline cache under ~/.cache (PDF + SQLite index) — that is expected.
- Do not edit anything in the subagent-factory repository.

WHEN DONE — ALWAYS, as your final action, even if you believe the task is already complete — write SUMMARY.md in this folder containing:
  1. final report filename;
  2. the Round History table;
  3. every remaining open gap with classification (ACADEMIC / ENGINEERING), severity, and one line on why it is still open;
  4. the 5-10 findings most relevant to the DOWNSTREAM USE above, each with paper IDs.
Then print exactly: RESEARCH RUN COMPLETE: <report filename>
EOF
}

# ── Launcher ─────────────────────────────────────────────────────────────────
launch () {
  local folder="$1" topic="$2" keywords="$3" why="$4"
  local dir="$RESEARCH_ROOT/$folder"
  mkdir -p "$dir"
  build_prompt "$topic" "$keywords" "$why" > "$dir/PROMPT.md"
  # setsid + </dev/null fully detaches so runs survive the launching shell.
  ( cd "$dir" && setsid "$CLAUDE_BIN" -p "$(cat "$dir/PROMPT.md")" \
        --model "$MODEL" --effort "$EFFORT" --dangerously-skip-permissions --verbose \
        </dev/null >"$dir/run.log" 2>&1 & echo $! >"$dir/run.pid" )
  echo "launched ${folder}  pid=$(cat "$dir/run.pid")  log=${dir}/run.log"
}

main () {
  echo "research root: $RESEARCH_ROOT"
  echo "claude bin   : $CLAUDE_BIN"
  echo "profile/model: $PROFILE / $MODEL (effort=$EFFORT)"
  echo
  for entry in "${TOPICS[@]}"; do
    IFS='|' read -r folder topic keywords why <<< "$entry"
    [ -n "$TOPICS_FILTER" ] && [ "$TOPICS_FILTER" != "$folder" ] && continue
    launch "$folder" "$topic" "$keywords" "$why"
  done
  echo
  echo "Launched in background. Monitor with:"
  echo "  tail -f $RESEARCH_ROOT/*/run.log"
  echo "  for d in $RESEARCH_ROOT/*/; do echo \"\$d -> \$(tail -n1 \"\$d/run.log\" 2>/dev/null)\"; done"
}

main "$@"
