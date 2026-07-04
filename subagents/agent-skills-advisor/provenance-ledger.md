# Provenance Ledger — Agent Skills Advisor

**Subagent slug:** `agent-skills-advisor`
**Profile version:** 0.1.0
**Generated:** 2026-07-04

This package distills 57 primary and secondary sources on Agent Skills, subagents, MCP,
evaluation, context engineering, and instruction files (across the Claude, OpenAI Codex, and GitHub
Copilot surfaces and the open Agent Skills standard) into an evidence-backed advisor. The distilled
spine — `analysis/claims.jsonl` (C#####), `evidence/evidence-records.yaml` (E#####),
`principles/principles.yaml` (P001–P150), and `sources/anchors/*.anchors.jsonl`
(`<sha12>-cNNNN`) — was assembled by the map→reduce build and is not modified here. This ledger
records how the LLM-authored layer (profile, skills, references, tests, faithfulness report) was
derived from that spine.

---

## Source Registry

| ID | Title | Authority | Rights |
|----|-------|-----------|--------|
| a-harness-for-every-de706ba6 | a-harness-for-every-task-dynamic-workflows-in-claude-code | secondary | distillation-only |
| advanced-tool-use-5e5bb110 | advanced-tool-use | secondary | distillation-only |
| agents-md-standard-fe2afcda | agents-md-standard | secondary | distillation-only |
| agentskills-adding-s-053f470d | agentskills-adding-skills-support | secondary | distillation-only |
| agentskills-best-pra-8e78d596 | agentskills-best-practices | secondary | distillation-only |
| agentskills-evaluati-221fbace | agentskills-evaluating-skills | secondary | distillation-only |
| agentskills-optimizi-2b4357e5 | agentskills-optimizing-descriptions | secondary | distillation-only |
| agentskills-overview-7e0f1b34 | agentskills-overview | secondary | distillation-only |
| agentskills-quicksta-2700eb30 | agentskills-quickstart | secondary | distillation-only |
| agentskills-specific-9d770de8 | agentskills-specification | secondary | distillation-only |
| agentskills-using-sc-f3393478 | agentskills-using-scripts | secondary | distillation-only |
| ai-resistant-technic-78079b86 | ai-resistant-technical-evaluations | secondary | distillation-only |
| building-agents-with-a8659148 | building-agents-with-skills-equipping-agents-for-specialized-work | secondary | distillation-only |
| building-effective-a-bb93dea1 | building-effective-agents | secondary | distillation-only |
| claude-agent-skills-375da9b8 | claude-agent-skills-overview | secondary | distillation-only |
| claude-code-best-pra-24d6de31 | claude-code-best-practices | secondary | distillation-only |
| claude-code-skills-67f80534 | claude-code-skills | secondary | distillation-only |
| claude-skill-authori-2b076b2b | claude-skill-authoring-best-practices | secondary | distillation-only |
| claude-skills-api-gu-52ae38ef | claude-skills-api-guide | secondary | distillation-only |
| claude-skills-api-qu-44948e80 | claude-skills-api-quickstart | secondary | distillation-only |
| claude-think-tool-45823385 | claude-think-tool | secondary | distillation-only |
| code-execution-with-c3493427 | code-execution-with-mcp | secondary | distillation-only |
| codex-agent-skills-df66a50c | codex-agent-skills | secondary | distillation-only |
| codex-agents-md-3d65b6e6 | codex-agents-md | secondary | distillation-only |
| codex-customization-59f8ec5e | codex-customization | secondary | distillation-only |
| complete-guide-to-bu-ea05f66b | complete-guide-to-building-skills | secondary | distillation-only |
| copilot-about-agent-d057d7be | copilot-about-agent-skills | secondary | distillation-only |
| copilot-agent-skills-c86c41e7 | copilot-agent-skills | secondary | distillation-only |
| copilot-cli-add-skil-eaf2ba38 | copilot-cli-add-skills | secondary | distillation-only |
| copilot-custom-instr-e3c9db39 | copilot-custom-instructions | secondary | distillation-only |
| copilot-customizatio-c2aa0db4 | copilot-customization-cheat-sheet | secondary | distillation-only |
| copilot-response-cus-9385a2ff | copilot-response-customization | secondary | distillation-only |
| demystifying-evals-f-ba55f4c0 | demystifying-evals-for-ai-agents | secondary | distillation-only |
| effective-context-en-107bd586 | effective-context-engineering-for-ai-agents | secondary | distillation-only |
| effective-harnesses-f71acdfe | effective-harnesses-for-long-running-agents | secondary | distillation-only |
| equipping-agents-for-b2e7bb6f | equipping-agents-for-the-real-world-with-agent-skills | secondary | distillation-only |
| extending-claude-cap-772a4479 | extending-claude-capabilities-with-skills-mcp-servers | secondary | distillation-only |
| getting-started-with-d12f463d | getting-started-with-loops | secondary | distillation-only |
| harness-design-long-27f56709 | harness-design-long-running-apps | secondary | distillation-only |
| how-anthropic-enable-8375b55a | how-anthropic-enables-self-service-data-analytics-with-claude | secondary | distillation-only |
| how-anthropic-uses-c-f5c48713 | how-anthropic-uses-claude-gtm-engineering | secondary | distillation-only |
| how-claude-code-work-e98da165 | how-claude-code-works-in-large-codebases-best-practices-and-where-to-start | secondary | distillation-only |
| how-to-create-skills-50982633 | how-to-create-skills-key-steps-limitations-and-examples | secondary | distillation-only |
| improving-skill-crea-f86a022e | improving-skill-creator-test-measure-and-refine-agent-skills | secondary | distillation-only |
| infrastructure-noise-00f2d8c4 | infrastructure-noise | secondary | distillation-only |
| lessons-from-buildin-53c9120d | lessons-from-building-claude-code-how-we-use-skills | secondary | distillation-only |
| managed-agents-a3e5d595 | managed-agents | secondary | distillation-only |
| multi-agent-research-da6e3e92 | multi-agent-research-system | secondary | distillation-only |
| obra-anthropic-best-217629b3 | obra-anthropic-best-practices | secondary | distillation-only |
| onboarding-claude-co-2445eb66 | onboarding-claude-code-like-a-new-developer-lessons-from-17-years-of-development | secondary | distillation-only |
| organization-skills-a13b9e9e | organization-skills-and-directory | secondary | distillation-only |
| seeing-like-an-agent-aac4af97 | seeing-like-an-agent | secondary | distillation-only |
| skills-3a6becc3 | skills | secondary | distillation-only |
| skills-explained-0bc9d804 | skills-explained | secondary | distillation-only |
| steering-claude-code-3f36f834 | steering-claude-code-skills-hooks-rules-subagents-and-more | secondary | distillation-only |
| vscode-copilot-agent-4f2d849c | vscode-copilot-agent-skills | secondary | distillation-only |
| writing-tools-for-ag-a0c96ef1 | writing-tools-for-agents | secondary | distillation-only |

---

## Distillation Log

Every profile field is grounded in the package's promoted principles
(`principles/principles.yaml`), which trace to `analysis/claims.jsonl` →
`evidence/evidence-records.yaml` → `sources/anchors/*.anchors.jsonl`. The profile core is kept
platform-neutral; platform-specific mechanics live in the skills and references.

| Field | Grounding principles | Notes |
|-------|----------------------|-------|
| `role` | P001, P002, P005, P006, P010, P053, P088 | Portable SKILL.md capability format; progressive disclosure; skill/subagent/MCP relationship; evaluation. |
| `when_to_use` | P001, P003, P004, P007, P016, P030, P039, P041, P044, P045, P048, P049, P069, P095, P117, P132 | Caller-observable triggers from principle `applies_when`: author, deploy, evaluate, compose, diagnose. |
| `when_not_to_use` | scope boundary (advisor scopes the skill, not the domain work) | Role-scoping decision, not a source claim. |
| `inputs.required` | P002, P008, P047, P095 | Skill + target surface + current SKILL.md/instruction files + observed behaviour. |
| `outputs.modes` | advise: P012, P059, P061; review: P025, P049, P070; eval-guide: P007, P044, P045 | Three read-only advisory modes. |
| `quality_bar` | P001, P002, P004, P005, P007, P016, P025, P029, P030, P043, P044, P045, P048, P049, P070, P088, P095, P117 | Falsifiable checks citing principle ids. |
| `minimum_useful_output` | P002, P025 | One actionable, cited recommendation or a missing-context statement. |
| `forbidden_behaviours` | P007, P015, P025, P034, P044, P088, P105, P114 | Traceable do-not rules (invented mechanisms, unproven claims, untrusted skills, context bloat). |
| `handoff_rules` | precedence (docs supersede sources for versioned APIs) | Defer domain/infra work; defer versioned API detail to official docs. |
| `source_of_truth_policy` | — | Ingested sources govern; official current docs supersede for version-specific API details. |
| `knowledge_partition.skills` | authoring: P001–P005, P012, P014, P019, P024, P025, P029, P032, P034, P035, P038, P040, P088, P092, P093, P112–P115, P120, P135, P150; evaluating: P007, P008, P041, P044, P045, P047, P052, P063, P065, P087, P099, P101, P102, P117, P145; deploying: P004, P009, P016, P020, P030, P036, P037, P048, P050, P053, P055, P060, P077, P095, P096, P122, P124, P133; orchestrating: P006, P010, P013, P033, P039, P051, P054, P056, P066, P068, P069, P089, P116, P121, P126, P143 | Operational recipes. |
| `knowledge_partition.references` | format: P025, P032, P034, P037, P040, P048, P055, P092, P112, P120, P122, P124, P135, P150; platform-matrix: P021, P027, P028, P050, P071, P076, P078, P079, P081, P082, P097, P123, P125, P136–P140; context/harness: P058, P083, P084, P086, P100, P105, P106, P108, P109, P127–P131, P141, P142, P144, P146–P149 | Lookup material. |

---

## Rights & Quotation

Distillation-only sources: no verbatim quotation is emitted in the authored layer. The distilled
spine (claims / evidence / principles / anchors) was not modified. Source metadata `source_type`
was corrected from the invalid `md` to the schema value `markdown` (a defect the map→reduce build
had introduced); no other spine content changed.
