---
name: corpus-design-and-methodology
kind: skill
status: ready
description: Review whether a corpus-based translation study is built to answer its
  question — corpus type (parallel / monolingual comparable / multilingual comparable),
  comparability, metadata, alignment, and frequency normalisation — before any difference
  is attributed to translation status. Use when a corpus design or corpus statistic
  is under review; universals interpretation goes to translation-universals-and-the-third-code,
  applied tooling to applied-corpus-tools-and-textual-devices.
provenance:
  principles:
  - P003
  - P012
  - P050
  - P068
  - P077
  - P078
  - P097
  - P107
  - P108
  - P112
  - P118
  - P122
  - P135
  - P140
  - P141
  claims:
  - C00214
  - C00236
  - C00237
  - C00317
  - C00318
  - C00319
  - C00320
  - C00321
  - C00322
  - C00323
  - C00324
  - C00326
  - C00327
  - C00334
  - C00338
  - C00451
  evidence: []
  source_anchors: []
  authored_from_digest: 8a9727af0a2c70a2cbc8da4010970d442d1610b0f66e381a874c8da3373faca7
---

# Corpus Design And Methodology

## Purpose

This skill reviews whether a corpus-based translation study is built to answer its question:
the corpus type — a parallel corpus for equivalence, shifts, and alignment; a monolingual
comparable corpus (translated versus non-translated texts in the same target language,
matched for domain, register, and period) for translation universals and translationese; or
a multilingual comparable corpus (comparable original texts across several languages) for
cross-linguistic feature contrasts — fits the aim, and comparability, metadata, copyright,
alignment, and frequency normalisation are controlled before any difference is attributed to
translation status. It treats the corpus as one tool inside a wider evidence set and pairs
quantitative patterns with recontextualised interpretation.

## When to use

- A corpus type (parallel, monolingual comparable, or multilingual comparable) is being chosen
  or a difference is attributed to translation status without controlling comparability,
  metadata, or alignment.
- Raw frequencies from unequal subcorpora are being compared without normalisation.
- A corpus statistic is being taken as a final answer rather than a prompt for qualitative,
  contextualised interpretation.
- The measure does not match the research question, or corpus evidence is being used outside a
  broader set of introspective, observational, and textual evidence.

## Procedure

Triage first: steps 1–2 and 10 select the corpus type and frame the study; steps 3, 5, 6, 11,
and 13 set comparability, tooling, and normalisation controls; steps 4, 7, 8, 9, 12, 14, and 15
integrate the corpus evidence with qualitative interpretation and the wider evidence set.

1. Choose the corpus type by the question: a parallel corpus for equivalence, shifts, and
   alignment; a monolingual comparable corpus for translation universals and translationese; a
   multilingual comparable corpus for cross-linguistic feature contrasts (P003).
2. Treat the primary purpose of corpus work in translation studies as explaining what
   translation is (P012).
3. Check comparability, metadata, copyright clearance, and alignment requirements before
   attributing corpus differences to translation status or using parallel-corpus evidence
   (P050).
4. Use carefully designed, contextualized parallel and comparable corpora to generalize and
   verify equivalence claims beyond individual cases (P068).
5. Use explicitly designed machine-readable corpora together with suitable software tools;
   corpus evidence is only useful when it can be searched, counted, displayed, and analysed
   (P077).
6. Match the corpus measure to the research question and control for its limitations before
   comparing texts (P078).
7. Use genre-level corpus comparison to relate an individual text pair to norms and options in
   that genre and language pair (P097).
8. Use corpora as one tool within a broader evidence set that also includes introspection,
   observation, textual analysis, and ethnographic analysis (P107).
9. Combine qualitative and quantitative inquiry by using corpus statistics as prompts for
   recontextualized interpretation rather than as final answers (P108).
10. Frame corpus-based translation studies around explicit hypotheses, varied data, descriptive
    categories, and a methodology that can support both inductive and deductive questions (P112).
11. Use corpus metadata to separate regional variation, dialect, source-language interference,
    translator-mother-tongue effects, institutional profile, team structure, target language,
    and source-text variants (P118).
12. Ground corpus-based translation and interpreting advice in empirical corpus evidence, using
    quantitative patterns together with qualitative interpretation rather than treating either
    as sufficient alone (P122).
13. Normalize corpus frequencies when subcorpora differ in size, and do not infer translation
    influence from frequency alone when item functions differ (P135).
14. Use large computerised corpora to open questions that small-scale studies cannot settle
    (P140).
15. Treat corpus research as an empirical check on intuition; prefer natural-discourse evidence
    when claims about language patterning are disputed or assumed (P141).

## Inputs

- The study's research question, corpus design (type, comparability, metadata, alignment), and
  the measures applied.
- The reasoning offered for the decision under review: the corpus, the orientation, the brief,
  and any quality claim made.

## Output

Per finding: flaw, principle, correction, trade-off, next step — highest-impact first. Reviews
the study or claim, not the finished translation or the publication decision.

## Anti-patterns to flag

- Reaching for a multilingual comparable corpus, or a vaguely-labelled "comparable corpus," to
  study translation universals or translationese, when the question calls for a monolingual
  comparable corpus matched for domain, register, and period in one target language; reserve
  parallel corpora for equivalence, shift, and alignment questions (P003).
- Attributing an observed difference to translation status without using comparability, metadata,
  copyright, and alignment checks to rule out the confounds they exist to catch: regional
  variation, dialect, source-language interference, translator-mother-tongue effects,
  institutional profile, team structure, target-language variety, or source-text variants (P050,
  P118).
- Comparing raw frequencies across differently-sized subcorpora without normalising — and even
  after normalising, crediting a gap to translation influence when the compared items serve
  different functions in each subcorpus (P135).
- Stopping at the frequency or statistic as the finding itself instead of treating it as a
  prompt for qualitative, recontextualized interpretation, and treating the corpus as the sole
  evidence rather than one tool alongside introspection, observation, textual, and ethnographic
  analysis (P107, P108, P122).
- Justifying a corpus project mainly by how much it improves human or machine translation
  output, rather than by what it explains about how translation works — the practical
  improvement is expected to follow from the explanation, not substitute for it (P012).
- Substituting a small-scale, few-text-pair analysis for a large computerised corpus when the
  question — intermediate translation stages, unit-of-translation size, or the level of
  equivalence actually achieved — needs corpus scale to settle (P140).

## References

See `../../references/translation-quality-principles-index.md` for the full principle catalogue
grouped by skill, and `../../references/translation-quality-evidence-notes.md` for how these
principles are grounded and kept faithful to the sources.

## Provenance

Derived from P003, P012, P050, P068, P077, P078, P097, P107, P108, P112, P118, P122, P135, P140,
P141, grounded in the distillation-only sources (Kruger et al., eds., *Corpus-Based Translation
Studies*; House, *Translation Quality Assessment*; Baker, *Corpus Linguistics and Translation
Studies*). The frontmatter `provenance` block lists the exact principle and claim ids, which
resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
