---
name: evidence-integrity-and-claims
description: >-
  Checks that claims are scoped to exactly what the evidence supports and never presented more
  strongly than warranted, that weaknesses, negative results, and limitations are reported as
  visibly as strengths, that statistics and methods are interpreted as evidence rather than
  certainty, that alternative explanations and increasingly severe disproof attempts are tried
  against a favored hypothesis, that the evidence chain and records are auditable and preserved,
  and that authorship credit tracks substantive contribution. Use when a claim, conclusion, or
  achievement must be scoped and hedged to the evidence; when negative, unexpected, or limiting
  results must be reported honestly rather than buried; when statistics, models, or methods need
  sound interpretation and their assumptions or baselines validated; or when the evidence chain,
  records, or authorship must be made auditable and properly credited.
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

Route to the subsection for the concern under review: the evidence chain, whether claims are scoped to evidence, handling of alternatives and negatives, or research conduct and records. Order findings highest-impact first.

### Evidence chain and auditability

1. Build credibility through an unbroken chain from prior work to conclusions — cited sources, described methods, clear data, appropriate statistics, and conclusions grown from the data — using concreteness rather than hype, because a break anywhere in the chain loses credibility (P015).
2. Support a novel algorithm with the literature, stated limitations, credible implementation, appropriate data, sufficient tests, and an objective explanation that lets skeptical readers judge novelty, sense, and effectiveness (P018).
3. Make the evidence chain auditable by identifying collectors and methods, using near-primary sources, citing completely, and accepting responsibility for every selection and transformation between underlying data and the report (P168).

### Claims scoped to evidence and statistics

4. Audit conventional research-language formulations for concealed evidential defects rather than allowing euphemism to hide missing support, failed work, selective samples, unreadable evidence, or poor agreement (P042).
5. Hedge with precision rather than vagueness: state the proposition and scope clearly, limit broad claims to the observed sample or search, and treat visual prominence separately from epistemic certainty (P067).
6. Present weaknesses, bias, and methodological limits as visibly as strengths, incorporate them into alternative explanations, keep achievement claims proportional, and hedge only claims whose uncertainty warrants it (P081).
7. Replace inflated scientific language with operational definitions and scrutinize work that evades evidence, ignores contrary advances, fails to develop under new data, or reports implausibly perfect outcomes (P092).
8. Choose significance thresholds for context, interpret significance as evidence against the null rather than certainty, and interpret nonsignificance as inconclusive rather than proof of the null or equivalence (P093).
9. Scope conclusions to tested cases and factors, avoid untested rankings or informal equivalence, and interpret quantitative differences only according to the metric's measurement scale (P104).
10. Signal a supported achievement explicitly and explain its value, using emphatic language rarely and only at strength accepted by the discipline and justified by the evidence (P136).

### Alternatives, negatives, and disproof

11. Test alternative explanations, interpret negative results as possible failures of test or implementation as well as hypothesis, and sanity-check outputs against invariants, totals, boundaries, expectations, and seeded cases (P034).
12. Use proofs, models, simulations, and real experiments as complementary but bounded evidence: validate their assumptions and correspondence, label each accurately, and never generalize beyond what it tested (P036).
13. Report credible negative and unexpected results explicitly, distinguishing informative absence from invalid data caused by procedural failure (P147).
14. Challenge a favored hypothesis with plausibility checks and increasingly severe attempts at disproof, checking early contradictions but abandoning or reformulating the claim when evidence shows it false (P172).

### Research conduct and records

15. Grant authorship only for significant intellectual contribution to conception, execution, or interpretation; directed coding, proofreading, funding, management, reward, or favor does not qualify by itself (P069).
16. Let the intended measurement determine experimental software scope, building the simplest probe that preserves realistic behavior rather than an unnecessary complete system (P105).
17. Keep conventional research reports focused on evidence-bearing material, omitting routine false starts unless a failure itself yields an important lesson or the genre explicitly calls for reflection (P120).
18. Maintain an immutable dated record of methods, versions, inputs, parameters, outputs, interpretations, decisions, and failures, and share code and data when rights and constraints permit (P133).
19. Treat every method as good when done well, because bad is a matter of interpretation — a method may be bad for measuring one thing but good for a slightly different thing — so explain why your methods give the information you need (P150).

## Inputs

- The claims, data, statistics, methods, and records under review and the strength of support each actually has.
- The reasoning offered for the decision under review: the goal, the audience and venue, the draft or plan in place, and any claim of clarity, rigor, or readiness made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research writing and presentation; it does not write the paper, section, slides, or talk for the caller, guarantee acceptance or publication, or rule on the domain-science correctness of the research.

## Anti-patterns to flag

### Evidence chain and auditability

- A step in the credibility chain is missing or vague — a conclusion asserted without the cited sources, described method, or clear data that would ground it, or concreteness replaced by hype (P015).
- A novel-algorithm claim omits one of its required pillars: no positioning against the literature, no stated limitations, a vaguely described implementation, thin or unrepresentative data, too few tests, or advocacy language that pre-empts the skeptical reader's own judgment (P018).
- The chain from underlying data to the report cannot be audited: the collector or method is unidentified, a source is farther from primary than necessary, a citation is incomplete, or a selection or transformation step has no accountable owner (P168).

### Claims scoped to evidence and statistics

- Stock research phrasing ("promising results," "broadly consistent") is used where it actually conceals missing support, a selective sample, unreadable evidence, or poor agreement (P042).
- A hedge is vague rather than precise: the proposition or its scope is left unstated, a claim about the observed sample is generalized beyond it, or a figure's or heading's visual prominence is allowed to imply more certainty than the wording states (P067).
- Limitations are present but visually or rhetorically buried relative to the strengths, left out of the alternative-explanations discussion, or an achievement claim is stated more strongly than the acknowledged limits and uncertainty support (P081).
- Inflated language stands in for an operational definition, or a result that is implausibly perfect, unresponsive to new data, or silent on contrary advances passes without scrutiny (P092).
- A significant result is treated as certainty rather than evidence against the null, or a nonsignificant result is reported as proof of the null or of equivalence rather than as inconclusive (P093).
- A conclusion is generalized to cases or factors that were not tested, an untested ranking or informal equivalence is asserted, or a quantitative difference is interpreted without regard to the metric's actual measurement scale (P104).
- Emphatic language ("groundbreaking," "definitively shows") is used routinely or at a strength the discipline would not accept for the evidence presented, or a genuinely supported achievement is left unsignaled (P136).

### Alternatives, negatives, and disproof

- A negative result is read only as refuting the hypothesis, with no check of whether the test or implementation itself failed, and no sanity check of outputs against known invariants, totals, boundaries, or seeded cases (P034).
- A simulation, model, or proof result is generalized beyond what it actually tested, or its type is mislabeled — a simulated result presented as if it were a real experiment — without its assumptions validated (P036).
- A negative or unexpected result is omitted from the report, or its interpretation conflates an informative absence with invalid data caused by a procedural failure (P147).
- A favored hypothesis is defended past the point where evidence contradicts it, with no increasingly severe disproof attempts made and no willingness to abandon or reformulate the claim (P172).

### Research conduct and records

- An author credit is extended for directed coding, proofreading, funding, management, or reward or favor alone, with no significant intellectual contribution to conception, execution, or interpretation (P069).
- Experimental software is built out as an unnecessarily complete system beyond what the intended measurement requires, or is simplified so far that it no longer preserves the realistic behavior being measured (P105).
- A conventional research report includes routine false starts or narrative detours with no evidentiary payoff, crowding out evidence-bearing material, in a genre that does not call for reflection (P120).
- No dated, immutable record exists of the methods, versions, parameters, interpretations, or decisions behind a result, or code and data that rights and constraints would permit sharing are withheld without cause (P133).
- A method is dismissed as simply "bad" without asking what it is good for, or the report never explains why the chosen methods actually give the information the claim needs (P150).

## References

Consult `../../references/research-writing-principles-index.md` only when a finding's principle needs its full source-grounded statement, or when the issue may belong to a sibling skill and you need to confirm which skill owns it. Consult `../../references/research-writing-evidence-notes.md` only when the caller disputes a finding's grounding and you need its source basis.

## Provenance

Derived from P015, P018, P034, P036, P042, P067, P069, P081, P092, P093, P104, P105, P120, P133, P136, P147, P150, P168, P172, grounded in the nine distillation-only sources (*The Craft of Research*; *Writing for Computer Science*; *Writing Science*; *English for Writing Research Papers*; *Science Research Writing for Non-Native Speakers of English*; *How to Write a Lot*; *How to Take Smart Notes*; *Presentation Zen Design*; and *TED Talks: The Official TED Guide to Public Speaking*). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
