# Provenance Ledger - ai-agent-engineering-reviewer

**Profile version:** 0.2.0
**Generated:** 2026-07-03

## Version History

- **0.3.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

- `0.2.0` - Rebuilt the LLM-authored layer from the current claims, evidence records, and principles. Distilled artifacts were treated as the source of truth.

## Distillation Log

| Profile field | Source IDs | Principle / claim basis | Note |
|---|---|---|---|
| display_name, role | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P008, P011, P014, P019, P022, P051 | Synthesizes the package role around AI-agent engineering review rather than any single source. |
| when_to_use | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P003-P054 high-confidence profile-rule principles | Triggers cover design review, trace diagnosis, evaluation, retrieval/tool use, and release risk. |
| when_not_to_use | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | Scope boundary from source coverage | Excludes implementation ownership, non-agent advice, and unsupported live/vendor facts. |
| inputs.required | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P004, P008, P019, P020, P022, P051 | Requires the reviewed artifact plus task, tools, safety constraints, and decision need. |
| outputs and modes | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P008/P010/P011, P019/P020, P022/P024/P051/P053 | Defines review, advise, and gate outputs without granting patch or deployment authority. |
| quality_bar | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P008, P010, P011, P012, P014, P019, P020, P021, P022, P024, P030, P040, P048, P051, P053, P054 | Falsifiable checks group the highest-confidence operational principles. |
| forbidden_behaviours | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P011, P016, P017, P021, P023, P024, P025, P029, P043, P047, P050, P051 | Prevents over-claiming, unsafe safety shortcuts, aggregate-only reporting, and unjustified tool recommendations. |
| source_of_truth_policy | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | source-pack.manifest.yaml; evidence/evidence-records.yaml; principles/principles.yaml | Names the deterministic spine as the package behaviour authority and caller artifacts as implementation authority. |
| knowledge_partition | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | operational_mapping.skill/reference are null in current principles | No skill/reference files were invented; always-on summaries preserve core review rules. |
| examples | lewis-rag-a4fb490b, yao-react-0285c0b6, schick-toolformer-1f1b3be1, park-generative-agen-f505bd2a, wang-llm-agents-surv-6dd22ee2, mohammadi-llm-agent-a39afdcf, mitchell-model-cards-d06c3bb5, zhang-agent-safetybe-fe01c6f4 | P004, P008, P024, P051; scope boundary | Includes one happy-path review and one failure-recovery redirect. |

## Rights Notes

All eight sources are marked `distillation-only`; generated package prose is paraphrased and no source passage is quoted.
