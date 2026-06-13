Research the following topic using the research-pipeline skill, deep profile. This is an independent, unattended run.

TOPIC:
Instruction induction and agent distillation: converting distilled expert principles into crisp behavioural rules, decision policies, and few-shot worked examples for an LLM agent persona; turning declarative knowledge into operational instructions and exemplars that improve an agent's task behaviour

SEED KEYWORDS (focus the query plan; edit plan/query_plan.json if recall is weak):
instruction induction; instruction generation; agent distillation; principle to rule conversion; behavioural rule generation; few-shot exemplar selection; demonstration selection; in-context example construction; system-prompt and persona design; constitutional rules; policy distillation; skill and procedure induction; decision policy extraction

DOWNSTREAM USE (anchor scope to this application; keep it a literature review, not a product build):
Feeds Phase 5/9 of the subagent factory: convert promoted principles into the adapter's behavioural rules + worked examples that make a generated expert ACT well, not merely describe knowledge. OUTPUT-QUALITY goal: crisper operational rules, well-chosen few-shot examples, explicit decision policies, so the adapter gives concrete actionable advice. The adapter-quality gate already checks that examples EXIST; this informs making them GOOD. Literature review of methods + how to apply (deterministic vs LLM split), not a product build.

HOW TO RUN:
- Launch via the runner, never bypass it. Round 1:
    python3 $HOME/.claude/skills/research-pipeline/runners/runner.py "Instruction induction and agent distillation: converting distilled expert principles into crisp behavioural rules, decision policies, and few-shot worked examples for an LLM agent persona; turning declarative knowledge into operational instructions and exemplars that improve an agent's task behaviour" --profile deep --config $HOME/.claude/skills/research-pipeline/config.toml
- Follow the research-pipeline SKILL rules: when the runner prints DELEGATE TO SUB-AGENT, run the named sub-agent (paper-screener / paper-analyzer / paper-synthesizer) with the printed contract, set that task to accepted, and re-run. Honor reviewer gates (on 'rejected': fix, reset task to pending, re-run).
- Write the final report only after validate-report is accepted.
- DO NOT STOP AFTER ROUND 1. If the validated report still lists any HIGH-severity ACADEMIC gap and round < 4, run gap-closure round(s) per references/iterative-synthesis.md until every HIGH academic gap is closed or reclassified, or the 4-round hard cap is reached. ENGINEERING gaps are resolved inline.

OUTPUT / SANDBOX RULES (hard):
- Your current working directory is this topic folder. Put EVERY artifact here: plan/, search/, screen/, download/, convert/, extract/, summarize/, workflow_state.json, gaps.json, and the final <topic-slug>-research-report.md.
- Do NOT modify, create, or delete any file outside this folder. The ONLY permitted external location is the shared pipeline cache under ~/.cache.
- Do not edit anything in the subagent-factory repository.

WHEN DONE — ALWAYS, as your final action — write SUMMARY.md here containing: (1) final report filename; (2) Round History table; (3) every remaining open gap with classification + severity + one line; (4) the 5-10 findings most relevant to the DOWNSTREAM USE above, each with paper IDs.
Then print exactly: RESEARCH RUN COMPLETE: <report filename>
