---
name: quality-assessment-and-error-analysis
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P013
  - P016
  - P030
  - P031
  - P055
  - P060
  - P078
  - P088
  - P089
  - P092
  - P135
  - P136
  - P137
  - P138
  - P140
  claims:
  - C00183
  - C00184
  - C00185
  - C00189
  - C00192
  - C00205
  - C00206
  - C00212
  - C00213
  - C00222
  - C00223
  - C00229
  - C00231
  - C00246
  - C00247
  - C00248
  evidence: []
  source_anchors: []
  authored_from_digest: 8f6378d75390346b41ea2ad971b37d2dd5b519d604b32823dbbf5e5948b5fcf8
---

# Quality Assessment And Error Analysis

## Purpose

This skill reviews translation-quality assessment and error analysis. It requires evaluation by comparison against the source in the source language, built from a source-text profile of the function to be sought; treats quality as probabilistic, not deterministic; classifies overt errors and covert (cultural-filter) mismatches; and weights errors by source-profile priorities rather than counting them flat.

## When to use

- A translation is being scored without comparison against the source in the source language.
- Quality is being treated as a single verdict rather than a range of valid answers.
- Overt errors and covert (cultural-filter) versions are being conflated, or errors counted without weighting.
- An assessment lacks a source-text profile of the function the target should seek.

## Procedure

1. Decide whether a translation is overt (P003).
2. For overt translation, aim at second-level access to the source function, preserve the source as intact as possible, and balance necessary explanation against replacement of source-culture markedness (P013).
3. Build the quality comparison from a detailed source-text profile that specifies the function to be sought in the target text (P016).
4. Use micro-, macro-, and superstructural levels to judge error seriousness only as part of a specified, text-context-sensitive procedure (P030).
5. Treat preservation of factual content as insufficient when target choices weaken addressee involvement, flattery, reassurance, indirectness, responsibility management, hedging, or interpersonal force (P031).
6. Evaluate a translation by comparing it against the source in the source language, giving priority to the elements where error silently distorts or reverses the argument (P055).
7. Do not accept target-only, reception-only, or response-only evaluations as sufficient when they cannot explain the source-translation relation or distinguish translation from adaptation (P060).
8. Judge translation quality by probabilistic, not deterministic, rules (P078).
9. Allow analyst judgement only as argued, evidence-constrained hypotheses, acknowledging that equivalence and TQA retain non-absolute and subjective elements (P088).
10. Classify unjustified cultural-filter changes as covert versions, and classify added special-audience or special-purpose renderings as overt versions rather than ordinary translations (P089).
11. In Mode analysis of mission statements, distinguish oral-rhetorical writtenness from plain information delivery and evaluate repetition, parallelism, rhetorical macrostructure, and summative closure (P092).
12. Classify overt errors separately as denotative omissions, additions, substitutions, wrong selections or combinations, ungrammaticality, and questionable acceptability (P135).
13. State the assumptions and exceptions behind dimensional error judgements, including cultural comparability, intertranslatability, and whether the target has an added special function (P136).
14. Weight errors by source-profile priorities, evaluation objective, and functional component, treating denotative mismatches as especially serious when ideational function is central (P137).
15. Measure revised-model quality by analogous source and target profile/function analysis while distinguishing dimensional from non-dimensional mismatches (P138).
16. Do not treat local cohesion as sufficient when translation loses source macrostructural parallelism, rhetorical guidance, oral-rhetorical effect, or summative closure (P140).

## Inputs

- The quality claim or TQA analysis under review and the source it should be measured against.
- The reasoning offered for the decision under review: the orientation, strategy, brief, and any quality claim made.

## Output

Per finding: name the flaw and the principle it violates, apply the correction, state the residual uncertainty and the trade-off it reflects, and end with a concrete next step. Order findings highest-impact first. This skill reviews a translation, a translation choice, or a translation-studies analysis; it does not produce the finished translation or make the publication decision.

## Anti-patterns to flag

- The analysis fails to decide whether a translation is overt (P003).
- The analysis fails to for overt translation, aim at second-level access to the source function, preserve the source as intact as possible, and balance necessary explanation against (P013).
- The analysis fails to build the quality comparison from a detailed source-text profile that specifies the function to be sought in the target text (P016).
- The analysis fails to use micro-, macro-, and superstructural levels to judge error seriousness only as part of a specified, text-context-sensitive procedure (P030).
- The analysis fails to treat preservation of factual content as insufficient when target choices weaken addressee involvement, flattery, reassurance, indirectness, responsibility management (P031).
- The analysis fails to evaluate a translation by comparing it against the source in the source language, giving priority to the elements where error silently distorts or reverses the argument (P055).
- The analysis fails to do not accept target-only, reception-only, or response-only evaluations as sufficient when they cannot explain the source-translation relation or distinguish translation (P060).

## References

See `../../references/translation-faithfulness-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/translation-faithfulness-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P003, P013, P016, P030, P031, P055, P060, P078, P088, P089, P092, P135, P136, P137, P138, P140, grounded in the eight distillation-only sources (Nida, *Principles of Correspondence*; Toury, *The Nature and Role of Norms in Translation*; House, *Translation Quality Assessment*; Byrne, *Technical Translation* and *Scientific and Technical Translation Explained*; Baker, *In Other Words*; Munday, *Introducing Translation Studies*; Venuti, ed., *The Translation Studies Reader*). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
