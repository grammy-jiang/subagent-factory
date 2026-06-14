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
#   bash docs/Research/run_research.sh            # launch all topics (detached) on Claude
#   TOPICS_FILTER=<folder> bash docs/Research/run_research.sh           # one topic, Claude
#   ENGINE=copilot TOPICS_FILTER=<folder> bash docs/Research/run_research.sh  # one topic, Copilot
#
# Parallel across both engines/budgets (run each via the harness's own backgrounding, DETACH=0):
#   DETACH=0 ENGINE=claude  TOPICS_FILTER=topic-a bash docs/Research/run_research.sh   # Claude
#   DETACH=0 ENGINE=copilot TOPICS_FILTER=topic-b bash docs/Research/run_research.sh   # Copilot
#
set -euo pipefail

# ── Config (override via env) ────────────────────────────────────────────────
# ENGINE selects the CLI that runs the (identical) research-pipeline skill. Both `claude` and
# `copilot` have the skill + paper-screener/analyzer/synthesizer agents + research-pipeline MCP
# installed (the shared `research-pipeline` pipx package symlinks skill_data/agent_data into both
# ~/.claude and ~/.copilot), so the SAME prompt template drives either — only the launch flags differ.
# Run two engines on two TOPICS in parallel to use both budgets (Claude spend + Copilot premium).
ENGINE="${ENGINE:-claude}"                             # claude | copilot
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"   # real binary, NOT the shell alias
COPILOT_BIN="${COPILOT_BIN:-$HOME/.local/bin/copilot}"
COPILOT_MODEL="${COPILOT_MODEL:-claude-opus-4.8}"      # latest Opus on Copilot (probe-confirmed)
COPILOT_EFFORT="${COPILOT_EFFORT:-high}"               # Copilot's max effort is "high" (no "max")
SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills/research-pipeline}"
CFG="${CFG:-$SKILL_DIR/config.toml}"
RUNNER="$SKILL_DIR/runners/runner.py"
PROFILE="${PROFILE:-deep}"
MODEL="${MODEL:-opus}"                                 # claude worker model
EFFORT="${EFFORT:-max}"                                # claude reasoning effort level
RESEARCH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # docs/Research
TOPICS_FILTER="${TOPICS_FILTER:-}"                     # optional: run only this folder
DETACH="${DETACH:-1}"                                  # 1=setsid detach; 0=foreground (let the
                                                       #   caller, e.g. harness run_in_background,
                                                       #   own + track the process — setsid wedges it)

# ── Topic registry:  folder | topic | seed-keywords | downstream-use ─────────
declare -a TOPICS=(
"prompt-injection-defense|Indirect prompt-injection defenses for LLM systems that ingest untrusted documents: detection, content isolation and spotlighting, sanitization, and benchmarks|indirect prompt injection; injection detection; untrusted content; spotlighting; data-marking defense; jailbreak detection; LLM security benchmark; content sanitization; data exfiltration|Feeds a deterministic prompt-injection scan (regex/heuristics over ingested source markdown), an adapter-policy scan, an untrusted-source policy rule, and attack fixtures for a factory that turns arbitrary PDFs/HTML into agent behaviour."
"argument-mining-claim-extraction|Argument mining and atomic claim extraction from long-form technical and scientific documents: claim and premise detection, claim typing, condition and exception extraction, and evidence linking|argument mining; claim detection; premise extraction; argument component classification; claim typing; scientific claim extraction; evidence linking; discourse segmentation; key-point extraction|Feeds a claims schema (claim/premise/condition/exception/type taxonomy), an LLM claim-extraction prompt, and claim fixtures used to distill expert principles from books/papers into subagents."
"factual-consistency-faithfulness|Factual consistency and faithfulness evaluation of LLM-generated text against source documents: hallucination and overgeneralization detection, claim verification, and entailment- and QA-based metrics|faithfulness evaluation; factual consistency; hallucination detection; claim verification; natural language inference; textual entailment; QA-based factuality; overclaiming detection; attribution faithfulness|Feeds a faithfulness rubric and a 'generated rule stronger than its source evidence' detection method, plus a faithfulness-report schema and fixtures, to stop a subagent factory from over-claiming beyond its sources."
"long-document-structure-mapping|Hierarchical reading of long technical and scientific documents for distillation: long-document and hierarchical summarisation, topic and discourse segmentation, document-structure extraction, and candidate knowledge-unit identification over 200+ page books|long-document summarization; hierarchical summarization; discourse segmentation; topic segmentation; TextTiling; document structure extraction; section and chapter segmentation; key-point extraction; candidate unit extraction; semantic chunking; book-length summarization; long-context document reading|Feeds a Tier-1 source-structure-mapping preprocessing step (Phase 2A/2B) for the subagent factory: before claim extraction, build a hierarchical map of a 200+ page book (part -> chapter -> section -> key passage) and segment it into candidate knowledge units, so claim and principle extraction reads structure-aware instead of flat-reading the whole text. Aim: higher recall and precision of extracted claims/principles/skills on long books (e.g. a 131k-word concurrency book already processed). Keep it a literature review of methods and how to apply them, not a product build."
"knowledge-fusion-conflict-detection|Cross-document knowledge fusion and contradiction detection for merging expert principles distilled from multiple source documents: cross-document concept and entity alignment, alias and duplicate clustering across documents, cross-document contradiction and conflict detection, and claim/knowledge reconciliation with conflict resolution|cross-document contradiction detection; knowledge fusion; conflicting information across documents; cross-document entity and event coreference; concept alignment; ontology and knowledge-graph alignment and fusion; claim deduplication; truth discovery; conflicting evidence aggregation; stance detection across documents; knowledge conflict resolution; defeasible reasoning|Feeds Step 7 multi-source synthesis in the subagent factory: merge 2+ books' distilled principles into one model — cluster co-expressed concepts across sources (alias/dedup), detect cross-source contradictions, and reconcile/record a principle graph. SCOPE: only the CROSS-document layer; the intra-document argument-relation vocabulary (claim/premise, stance support/contest, Pollock rebut/undercut) is already covered by the argument-mining research and must NOT be re-covered. Literature review of methods + how to apply (deterministic-seed vs LLM split), not a product build."
"instruction-induction-agent-distillation|Instruction induction and agent distillation: converting distilled expert principles into crisp behavioural rules, decision policies, and few-shot worked examples for an LLM agent persona|instruction induction; instruction generation; agent distillation; principle to rule conversion; behavioural rule generation; few-shot exemplar selection; demonstration selection; in-context example construction; system-prompt and persona design; constitutional rules; policy distillation; skill and procedure induction; decision policy extraction|Feeds Phase 5/9: convert promoted principles into the adapter's behavioural rules + worked examples that make a generated expert ACT well, not merely describe knowledge. Output-quality goal: crisper rules, well-chosen few-shot examples, explicit decision policies. The adapter-quality gate already checks examples EXIST; this informs making them GOOD. Literature review, not a product build."
"agent-benchmarking-output-evaluation|Benchmarking and runtime quality evaluation of LLM agents and expert assistants: LLM-as-judge methodology and biases, rubric-based evaluation, pairwise and Elo comparison, and reference-free quality scoring of free-form advisory/review output|LLM-as-a-judge; agent benchmarking; rubric-based evaluation; pairwise comparison; Elo and win-rate; judge bias and calibration; position bias; reference-free evaluation; meta-evaluation; inter-rater agreement; G-Eval; checklist evaluation; assistant evaluation harness|Feeds Phase 10: a rigorous output-quality evaluation harness for generated subagents. Formalise the ad-hoc eval (run subagent on a real doc, score vs rubric, deterministic grounding-check) into reliable LLM-as-judge rubrics, judge-bias mitigation, pairwise/Elo for comparing versions (1-source vs 2-source), and reference-free scoring. Literature review, not a product build."
"knowledge-graph-ontology-construction|Knowledge graph and ontology construction from text for representing expert principles: concept/entity extraction, taxonomy and ontology induction, relationship and alias modelling, and a principle graph linking and deduplicating concepts|knowledge graph construction; ontology learning; ontology induction from text; taxonomy induction; concept extraction; relation extraction; entity alias and synonym detection; schema and ontology alignment; concept hierarchy; node and edge typing; provenance in knowledge graphs; principle graph|Feeds Phase 7A (graph half of Step 7): represent merged principles as a graph (nodes = principles/concepts, edges = refines/supports/specialises/alias with provenance) + induce a lightweight taxonomy and aliases. SCOPE: graph/ontology representation + alias/relationship induction; cross-document CONTRADICTION detection is the sibling knowledge-fusion spike's job, not re-covered. Literature review, not a product build."
"prompt-optimization-eval|Automatic prompt and instruction optimization for LLM agents against an evaluation signal: optimizing system prompts, instructions, decision rules, and few-shot demonstrations to maximize a task/behaviour metric|prompt optimization; instruction optimization; DSPy; OPRO optimization by prompting; TextGrad textual gradients; GEPA reflective prompt evolution; APE automatic prompt engineering; few-shot demonstration selection; bootstrap few-shot; instruction search; LLM-as-optimizer; metric-guided prompt tuning; prompt program compilation; reflective self-improvement|Feeds a NEW optimize-adapter step: after build (Steps 1-9) and measure (the replay engine + semantic LLM grader + behaviour-tests, Phase 10), automatically optimize the generated adapter/skill prompts to MAXIMIZE the package's behaviour-test score — propose rule/example variants, score via replay+grader, keep the winner (the replay gate is the assess-before-merge primitive). DISTINCT from instruction-INDUCTION (already covered: mine rules from principles); this TUNES the adapter against an eval objective. Literature review of methods + how to apply (deterministic-gate vs LLM split, cost control), not a product build."
"behaviour-test-generation|Automatic generation of behavioural test suites for evaluating LLM agents and expert assistants: golden, negative-routing, and edge-case test synthesis, checklist and rubric construction, coverage-guided and metamorphic test generation, and adversarial red-team prompts for a specialised persona|test case generation; LLM unit tests; checklist generation; behavioral testing; metamorphic testing; coverage-guided test synthesis; adversarial test generation; red-teaming prompts; negative and routing tests; edge case discovery; CheckList; specification-based test generation; evaluation suite construction|Feeds the behaviour-test step (golden / negative-routing / missing-context tests in tests/*.yaml) that the eval harness (replay engine + semantic grader) and the optimize-adapter step score against. Goal: generate HIGH-COVERAGE, adversarial, well-scoped behaviour tests from a profile/principles spec, so the eval objective is strong (the optimizer is only as good as its tests). DISTINCT from agent-benchmarking (judge methodology) and prompt-optimization (tuning against tests); this generates the TESTS. Literature review of methods + how to apply (deterministic gen vs LLM, coverage metrics), not a product build."
"calibration-abstention|Calibration and selective prediction for LLM agents: when an advisory agent should answer vs abstain or ask for missing context — confidence calibration, selective prediction and answerability, the reject/ask option, and clarification-question generation|confidence calibration; selective prediction; selective classification; abstention; reject option; risk-coverage curve; answerability; unanswerable question detection; know what you don't know; out-of-scope detection; clarification question generation; ask vs answer; underspecification detection; calibration of LLM confidence; expected calibration error|Feeds the ask-gate / missing-context behaviour the factory tests and rewards (Step-11 missing_context_tests, behaviour_replay must_ask_for, Step-12 optimization target): when should a generated advisor abstain or ask for the decision-relevant input rather than commit to an answer, and how to gate that deterministically vs with an LLM. Also informs judge/eval calibration (this codebase measured an LLM judge as n=1-unreliable; selective-prediction methods bear on when to trust a judge verdict). Literature review of methods + how to apply (deterministic gate vs LLM split), not a product build."
"rag-graphrag|Retrieval-augmented generation and GraphRAG for an expert agent's runtime knowledge: when to bake distilled knowledge into the system prompt vs retrieve it at runtime from an evidence/reference/principle-graph store, retrieval over a knowledge graph, chunking and indexing, reranking, and grounded citation at answer time|retrieval augmented generation; RAG; GraphRAG; knowledge graph retrieval; vector retrieval; hybrid retrieval; reranking; chunking strategy; index construction; query-focused retrieval; grounding and citation; retrieval vs parametric knowledge; long-context vs RAG; agentic retrieval; provenance-grounded answers|Feeds the knowledge_partition decision + a possible Phase-9 adapter retrieval layer (§20 topic #10, never run): the factory bakes always_on rules into the adapter and lists skills/references as files, deciding BY HAND what is distilled vs retrieved. This is the distill-vs-retrieve architecture question — when should a generated expert carry knowledge in-prompt vs retrieve at runtime from its evidence/reference/principle-graph store, and how to ground+cite. SCOPE: runtime retrieval architecture for the generated agent, NOT the authoring-time pipeline (which knowledge-fusion/knowledge-graph already cover). Literature review of methods + how to apply (deterministic index/gate vs LLM), not a product build."
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
  local prompt; prompt="$(cat "$dir/PROMPT.md")"

  # Build the per-engine command (same prompt; both CLIs carry the research-pipeline skill).
  local -a cmd
  if [ "$ENGINE" = "copilot" ]; then
    cmd=( "$COPILOT_BIN" -p "$prompt" --model "$COPILOT_MODEL" --effort "$COPILOT_EFFORT" --allow-all )
  else
    cmd=( "$CLAUDE_BIN" -p "$prompt" --model "$MODEL" --effort "$EFFORT" --dangerously-skip-permissions --verbose )
  fi

  if [ "$DETACH" = "1" ]; then
    # setsid + </dev/null fully detaches so runs survive the launching shell.
    ( cd "$dir" && setsid "${cmd[@]}" </dev/null >"$dir/run.log" 2>&1 & echo $! >"$dir/run.pid" )
    echo "launched (detached, $ENGINE) ${folder}  pid=$(cat "$dir/run.pid")  log=${dir}/run.log"
  else
    # Foreground: no setsid — the caller owns the process (so the harness can track it and notify
    # on completion). Blocks until this topic's run finishes.
    echo "running (foreground, $ENGINE) ${folder}  log=${dir}/run.log"
    ( cd "$dir" && "${cmd[@]}" >"$dir/run.log" 2>&1 )
  fi
}

main () {
  echo "research root: $RESEARCH_ROOT"
  echo "engine       : $ENGINE"
  if [ "$ENGINE" = "copilot" ]; then
    echo "copilot      : $COPILOT_BIN  model=$COPILOT_MODEL effort=$COPILOT_EFFORT"
  else
    echo "claude       : $CLAUDE_BIN  model=$MODEL effort=$EFFORT (profile=$PROFILE)"
  fi
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
