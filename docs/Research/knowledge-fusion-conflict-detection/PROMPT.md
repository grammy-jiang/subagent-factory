Research the following topic using the research-pipeline skill, deep profile. This is an independent, unattended run.

TOPIC:
Cross-document knowledge fusion and contradiction detection for merging expert principles distilled from multiple source documents: cross-document concept and entity alignment, alias and duplicate clustering across documents, cross-document contradiction and conflict detection, claim and knowledge reconciliation with conflict resolution, and aggregation of conflicting evidence across sources.

SEED KEYWORDS (focus the query plan; edit plan/query_plan.json if recall is weak):
cross-document contradiction detection; knowledge fusion; conflicting information across documents; multi-document summarization contradiction; cross-document entity and event coreference; concept alignment; ontology and knowledge-graph alignment and fusion; claim deduplication; truth discovery; conflicting evidence aggregation; stance detection across documents; contradiction detection NLI; knowledge conflict resolution; merging knowledge from multiple sources; defeasible reasoning and undercutting

DOWNSTREAM USE (anchor scope to this application; keep it a literature review, not a product build):
Feeds Step 7 "multi-source synthesis" in a subagent factory: when a subagent is built from 2+ books, merge their distilled principles into ONE knowledge model — (1) cluster co-expressed concepts across sources (alias/duplicate detection: e.g. "don't build for speculative futures" in one book ≈ "tactical vs strategic programming" in another), (2) detect cross-source contradictions (different thresholds, opposed advice), and (3) reconcile / resolve conflicts and record a principle graph. IMPORTANT SCOPE BOUNDARY: the INTRA-document argument-relation vocabulary (claim/premise detection, stance = support/contest/no_relation, Pollock rebutting vs undercutting attacks) is ALREADY covered by a prior argument-mining research report — DO NOT re-cover it. This spike must cover ONLY the CROSS-document / CROSS-source layer: aligning and deduplicating equivalent concepts across documents, and detecting + resolving contradictions BETWEEN sources. Deliver methods + how to apply them (deterministic-seed vs LLM split where possible), not a product build.

HOW TO RUN:
- Launch via the runner, never bypass it. Round 1:
    python3 $HOME/.claude/skills/research-pipeline/runners/runner.py "Cross-document knowledge fusion and contradiction detection for merging expert principles distilled from multiple source documents" --profile deep --config $HOME/.claude/skills/research-pipeline/config.toml
- Follow the research-pipeline SKILL rules: when the runner prints DELEGATE TO SUB-AGENT, run the named sub-agent (paper-screener / paper-analyzer / paper-synthesizer) with the printed contract, set that task to accepted, and re-run. Honor reviewer gates (on 'rejected': fix, reset task to pending, re-run).
- Write the final report only after validate-report is accepted.
- DO NOT STOP AFTER ROUND 1. If the validated report still lists any HIGH-severity ACADEMIC gap and round < 4, run gap-closure round(s) per references/iterative-synthesis.md (new run_id, carry prior_paper_ids, derive a gap-specific topic from the open gap's suggested query) until every HIGH academic gap is closed or reclassified, or the 4-round hard cap is reached. ENGINEERING gaps are resolved inline in the report, never via a new round.

OUTPUT / SANDBOX RULES (hard):
- Your current working directory is this topic folder. Put EVERY artifact here: plan/, search/, screen/, download/, convert/, extract/, summarize/, workflow_state.json, gaps.json, and the final <topic-slug>-research-report.md.
- Do NOT modify, create, or delete any file outside this folder. The ONLY permitted external location is the shared pipeline cache under ~/.cache (PDF + SQLite index).
- Do not edit anything in the subagent-factory repository.

WHEN DONE — ALWAYS, as your final action — write SUMMARY.md in this folder containing:
  1. final report filename;
  2. the Round History table;
  3. every remaining open gap with classification (ACADEMIC / ENGINEERING), severity, and one line on why it is still open;
  4. the 5-10 findings most relevant to the DOWNSTREAM USE above, each with paper IDs.
Then print exactly: RESEARCH RUN COMPLETE: <report filename>
