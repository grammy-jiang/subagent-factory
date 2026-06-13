Research the following topic using the research-pipeline skill, deep profile. This is an independent, unattended run.

TOPIC:
Knowledge graph and ontology construction from text for representing expert principles: concept and entity extraction, taxonomy and ontology induction, relationship and alias modelling, and building a principle graph that links and deduplicates concepts across a body of knowledge

SEED KEYWORDS (focus the query plan; edit plan/query_plan.json if recall is weak):
knowledge graph construction; ontology learning; ontology induction from text; taxonomy induction; concept extraction; relation extraction; entity alias and synonym detection; schema and ontology alignment; concept hierarchy; node and edge typing; provenance in knowledge graphs; principle graph

DOWNSTREAM USE (anchor scope to this application; keep it a literature review, not a product build):
Feeds Phase 7A of the subagent factory (the GRAPH half of Step 7 multi-source synthesis): represent merged principles as a graph (nodes = principles/concepts, edges = relationships such as refines/supports/specialises/alias, with provenance) and induce a lightweight taxonomy and aliases. SCOPE: graph/ontology representation + alias/relationship/taxonomy induction; the cross-document CONTRADICTION-detection layer is the sibling knowledge-fusion spike's job and must NOT be re-covered. Literature review + how to apply (deterministic vs LLM split), not a product build.

HOW TO RUN:
- Launch via the runner, never bypass it. Round 1:
    python3 $HOME/.claude/skills/research-pipeline/runners/runner.py "Knowledge graph and ontology construction from text for representing expert principles: concept and entity extraction, taxonomy and ontology induction, relationship and alias modelling, and building a principle graph that links and deduplicates concepts across a body of knowledge" --profile deep --config $HOME/.claude/skills/research-pipeline/config.toml
- Follow the research-pipeline SKILL rules: when the runner prints DELEGATE TO SUB-AGENT, run the named sub-agent (paper-screener / paper-analyzer / paper-synthesizer) with the printed contract, set that task to accepted, and re-run. Honor reviewer gates (on 'rejected': fix, reset task to pending, re-run).
- Write the final report only after validate-report is accepted.
- DO NOT STOP AFTER ROUND 1. If the validated report still lists any HIGH-severity ACADEMIC gap and round < 4, run gap-closure round(s) per references/iterative-synthesis.md until every HIGH academic gap is closed or reclassified, or the 4-round hard cap is reached. ENGINEERING gaps are resolved inline.

OUTPUT / SANDBOX RULES (hard):
- Your current working directory is this topic folder. Put EVERY artifact here: plan/, search/, screen/, download/, convert/, extract/, summarize/, workflow_state.json, gaps.json, and the final <topic-slug>-research-report.md.
- Do NOT modify, create, or delete any file outside this folder. The ONLY permitted external location is the shared pipeline cache under ~/.cache.
- Do not edit anything in the subagent-factory repository.

WHEN DONE — ALWAYS, as your final action — write SUMMARY.md here containing: (1) final report filename; (2) Round History table; (3) every remaining open gap with classification + severity + one line; (4) the 5-10 findings most relevant to the DOWNSTREAM USE above, each with paper IDs.
Then print exactly: RESEARCH RUN COMPLETE: <report filename>
