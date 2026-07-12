---
name: russian-corpus-and-interpreting-research
kind: skill
status: ready
description: Review corpus-based translation and interpreting work in the Russian
  field, where corpus scarcity and fragmentation are hard design constraints — pressing
  for multifactorial modelling, significance testing with effect sizes, metadata-rich
  corpora, and inclusion of the Russian research tradition. Use when a Russian-field
  corpus or interpreting study is under review; general corpus design goes to corpus-design-and-methodology.
provenance:
  principles:
  - P019
  - P020
  - P029
  - P051
  - P052
  - P056
  - P057
  - P058
  - P146
  - P147
  - P148
  claims:
  - C00629
  - C00630
  - C00631
  - C00632
  - C00633
  - C00634
  - C00635
  - C00636
  - C00637
  - C00638
  - C00639
  - C00640
  - C00641
  - C00642
  - C00643
  - C00644
  evidence: []
  source_anchors: []
  authored_from_digest: ef1b4ba7fb8bc4af68fa6da9fc7bb83da684cc796e1767977ab6ba0e89f47944
---

# Russian Corpus And Interpreting Research

## Purpose

This skill reviews corpus-based translation and interpreting work in the Russian field, where corpus availability is a hard design constraint — scarcity, fragmentation, missing historical data, and little standardization. It presses for multifactorial modelling over isolated frequencies, significance testing with effect sizes, metadata-rich corpora recording direction, mode, and delivery, and inclusion of the Russian research tradition rather than assuming the field is only Anglophone.

## When to use

- Russian translation/interpreting corpus scarcity, fragmentation, or lack of standardization is being ignored as a design constraint.
- A complex variation claim rests on isolated frequencies or concordances instead of multifactorial modelling with significance testing and effect sizes.
- A Polish-Russian or Russian-Polish study lacks metadata recording translation direction, delivery, and mode.
- A survey assumes the field is represented only by Anglophone research, or draws strong Russian interpreting generalisations from thin data.

## Procedure

1. For Russian interpreting research, treat corpus availability as a design constraint: expect scarcity, fragmentation, missing historical data, and no default Europarl Russian component (P019).
2. Prioritize corpus construction and study designs for underexplored Russian varieties, especially constrained communication, amateur translation, post-edited translation, second-language translation, translator qualifications, and non-English language pairs (P020).
3. When surveying Russian translation and interpreting corpora, include the Russian research tradition rather than assuming the field is represented only by better-known English, French, German, or Spanish work (P029).
4. When recommending Russian interpreting data sources, describe UN Web TV, SIREN, and COINCOUT with their acquisition, transcription, size, domain, and access limitations (P051).
5. Recommend supervised or unsupervised machine learning for Russian translation/interpreting only when the corpus is large, feature-rich, and metadata-suitable, and frame the result as pattern detection or classification rather than automatic explanation (P052).
6. For complex variation in translation or interpreting, discourage explanation from isolated frequencies or concordances and recommend multifactorial modelling when multiple explanatory variables are plausible (P056).
7. In mode or producer comparisons, operationalize linguistic markers clearly and pair descriptive indicators with significance testing and effect sizes before interpreting group differences (P057).
8. For Polish-Russian or Russian-Polish multifactorial studies, require metadata-rich corpora that record factors such as translation direction, delivery mode, and text variety before making explanatory claims (P058).
9. When evaluating universals or strategies, check patterns across lexical, syntactic, and discourse levels and avoid strong Russian interpreting generalizations until independent corpora replicate them (P146).
10. Encourage Russian translationese studies to move beyond newspapers by using larger corpora and feature sets spanning lexical, morphological, syntactic, and genre-sensitive evidence (P147).
11. For advanced computational or process-oriented Russian corpus research, encourage interdisciplinary collaboration across linguistic, literary, computational, NLP, and psychological expertise (P148).

## Inputs

- The Russian-field corpus study, its data sources and metadata, and the modelling and generalisation claims made.
- The reasoning offered for the decision under review: the corpus, the orientation, the brief, and any quality claim made.

## Output

Per finding: flaw, principle, correction, trade-off, next step, highest-impact first — reviews the analysis, not the finished translation or the publication decision.

## Anti-patterns to flag

- Treating corpus scarcity or fragmentation as an excuse to drop the research question instead of a constraint that should redirect effort toward underexplored Russian varieties — constrained communication, amateur/post-edited/second-language translation, translator qualifications, non-English pairs — where scarcity is precisely what makes new data valuable (P019, P020).
- Explaining complex translation/interpreting variation from isolated frequency counts or concordance lines when several explanatory variables are plausible and multifactorial modelling was never attempted (P056).
- Reporting a mode or producer comparison as a real difference from descriptive indicators alone: a clearly operationalized marker is still an incomplete claim without a paired significance test and effect size (P057).
- Presenting a machine-learning result on Russian data as an explanation ("the model shows X causes Y") rather than what it actually is — pattern detection or classification, and only reliable at that once the corpus is large, feature-rich, and metadata-suitable (P052).
- Promoting a single-corpus finding to a Russian interpreting "universal" or "strategy" without checking it across lexical, syntactic, and discourse levels or waiting for independent replication (P146).
- Presenting a bounded source as if it were the whole picture: surveying Russian corpora from Anglophone scholarship alone (P029); recommending UN Web TV, SIREN, or COINCOUT without their acquisition, transcription, or access caveats (P051); confining Russian translationese work to newspaper text and a narrow feature set (P147); accepting a Polish-Russian multifactorial claim from a corpus missing direction, mode, or variety metadata (P058); or reviewing advanced computational Russian corpus work without flagging the need for interdisciplinary input (P148).

## References

See `../../references/translation-quality-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/translation-quality-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P019, P020, P029, P051, P052, P056, P057, P058, P146, P147, P148, grounded in the distillation-only source Dayter & Grabowski (eds.), corpus-based translation and interpreting studies in the Russian field. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
