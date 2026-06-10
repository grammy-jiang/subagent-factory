Research the following topic using the research-pipeline skill, deep profile. This is an independent, unattended run.

TOPIC:
Factual consistency and faithfulness evaluation of LLM-generated text against source documents: hallucination and overgeneralization detection, claim verification, and entailment- and QA-based metrics

SEED KEYWORDS (focus the query plan; edit plan/query_plan.json if recall is weak):
faithfulness evaluation; factual consistency; hallucination detection; claim verification; natural language inference; textual entailment; QA-based factuality; overclaiming detection; attribution faithfulness

DOWNSTREAM USE (anchor scope to this application; keep it a literature review, not a product build):
Feeds a faithfulness rubric and a 'generated rule stronger than its source evidence' detection method, plus a faithfulness-report schema and fixtures, to stop a subagent factory from over-claiming beyond its sources.

HOW TO RUN:
- Launch via the runner, never bypass it. Round 1:
    python3 /home/grammy-jiang/.claude/skills/research-pipeline/runners/runner.py "Factual consistency and faithfulness evaluation of LLM-generated text against source documents: hallucination and overgeneralization detection, claim verification, and entailment- and QA-based metrics" --profile deep --config /home/grammy-jiang/.claude/skills/research-pipeline/config.toml
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
