---
name: evidence-integrity-and-claims
kind: skill
status: ready
provenance:
  principles:
  - P015
  - P018
  - P034
  - P036
  - P042
  - P067
  - P069
  - P081
  - P092
  - P093
  - P104
  - P105
  - P120
  - P133
  - P136
  - P147
  - P150
  - P168
  - P172
  claims:
  - C00147
  - C00148
  - C00149
  - C00150
  - C00151
  - C00152
  - C00153
  - C00154
  - C00180
  - C00181
  - C00182
  - C00197
  - C00198
  - C00199
  - C00200
  - C00221
  evidence: []
  source_anchors: []
  authored_from_digest: c9c402714bc73d392b76c3dcb15939c963f20fc737f918792e5297ef43f77d26
---


# Evidence Integrity And Claims

## Purpose

This skill guides honest claims and a sound evidence base. It checks that claims are scoped to what the data supports and never presented more strongly than warranted, that weaknesses, negative results, and limitations are reported as visibly as strengths, that statistics are interpreted as evidence rather than certainty, that alternative explanations and severe disproof are tried, that methods and records are auditable and preserved, and that authorship credit tracks substantive contribution.

## When to use

- A claim, conclusion, or achievement must be scoped and hedged to exactly what the evidence supports.
- Negative, unexpected, or limiting results must be reported honestly rather than buried.
- Statistics, models, or methods need interpreting soundly and their assumptions and baselines validated.
- The evidence chain, records, and authorship must be auditable and credited to substantive contribution.

## Procedure

1. Build credibility through an unbroken chain from prior work to conclusions (P015).
2. Support a novel algorithm with the literature, stated limitations, credible implementation, appropriate data, sufficient tests, and an objective explanation that lets skeptical readers judge novelty, sense, and effectiveness (P018).
3. Test alternative explanations, interpret negative results as possible failures of test or implementation as well as hypothesis, and sanity-check outputs against invariants, totals, boundaries, expectations, and seeded cases (P034).
4. Use proofs, models, simulations, and real experiments as complementary but bounded evidence (P036).
5. Audit conventional research-language formulations for concealed evidential defects rather than allowing euphemism to hide missing support, failed work, selective samples, unreadable evidence, or poor agreement (P042).
6. Hedge with precision rather than vagueness (P067).
7. Grant authorship only for significant intellectual contribution to conception, execution, or interpretation; directed coding, proofreading, funding, management, reward, or favor does not qualify by itself (P069).
8. Present weaknesses, bias, and methodological limits as visibly as strengths, incorporate them into alternative explanations, keep achievement claims proportional, and hedge only claims whose uncertainty warrants it (P081).
9. Replace inflated scientific language with operational definitions and scrutinize work that evades evidence, ignores contrary advances, fails to develop under new data, or reports implausibly perfect outcomes (P092).
10. Choose significance thresholds for context, interpret significance as evidence against the null rather than certainty, and interpret nonsignificance as inconclusive rather than proof of the null or equivalence (P093).
11. Scope conclusions to tested cases and factors, avoid untested rankings or informal equivalence, and interpret quantitative differences only according to the metric's measurement scale (P104).
12. Let the intended measurement determine experimental software scope, building the simplest probe that preserves realistic behavior rather than an unnecessary complete system (P105).
13. Keep conventional research reports focused on evidence-bearing material, omitting routine false starts unless a failure itself yields an important lesson or the genre explicitly calls for reflection (P120).
14. Maintain an immutable dated record of methods, versions, inputs, parameters, outputs, interpretations, decisions, and failures, and share code and data when rights and constraints permit (P133).
15. Signal a supported achievement explicitly and explain its value, using emphatic language rarely and only at strength accepted by the discipline and justified by the evidence (P136).
16. Report credible negative and unexpected results explicitly, distinguishing informative absence from invalid data caused by procedural failure (P147).
17. Treat every method as good when done well (P150).
18. Make the evidence chain auditable by identifying collectors and methods, using near-primary sources, citing completely, and accepting responsibility for every selection and transformation between underlying data and the report (P168).
19. Challenge a favored hypothesis with plausibility checks and increasingly severe attempts at disproof, checking early contradictions but abandoning or reformulating the claim when evidence shows it false (P172).

## Inputs

- The claims, data, statistics, methods, and records under review and the strength of support each actually has.
- The reasoning offered for the decision under review: the goal, the audience and venue, the draft or plan in place, and any claim of clarity, rigor, or readiness made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research writing and presentation; it does not write the paper, section, slides, or talk for the caller, guarantee acceptance or publication, or rule on the domain-science correctness of the research.

## Anti-patterns to flag

- Overlooking P015: Build credibility through an unbroken chain from prior work to conclusions.
- Overlooking P018: Support a novel algorithm with the literature, stated limitations, credible implementation, appropriate data, sufficient tests, and an objective.
- Overlooking P034: Test alternative explanations, interpret negative results as possible failures of test or implementation as well as hypothesis, and sanity-check.
- Overlooking P036: Use proofs, models, simulations, and real experiments as complementary but bounded evidence.
- Overlooking P042: Audit conventional research-language formulations for concealed evidential defects rather than allowing euphemism to hide missing support, failed.
- Overlooking P067: Hedge with precision rather than vagueness.
- Overlooking P069: Grant authorship only for significant intellectual contribution to conception, execution, or interpretation; directed coding, proofreading, funding.

## References

See `../../references/research-writing-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/research-writing-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P015, P018, P034, P036, P042, P067, P069, P081, P092, P093, P104, P105, P120, P133, P136, P147, P150, P168, P172, grounded in the nine distillation-only sources (*The Craft of Research*; *Writing for Computer Science*; *Writing Science*; *English for Writing Research Papers*; *Science Research Writing for Non-Native Speakers of English*; *How to Write a Lot*; *How to Take Smart Notes*; *Presentation Zen Design*; and *TED Talks: The Official TED Guide to Public Speaking*). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
