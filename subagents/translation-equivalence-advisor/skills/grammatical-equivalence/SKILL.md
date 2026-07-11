---
name: grammatical-equivalence
description: Diagnoses and reviews rendering across grammatical systems — obligatory
  categories, voice, gender, number, tense and aspect, modality, and pronouns of address
  — by function rather than form; owns grammar-driven shifts, not information structure,
  which thematic-and-information-structure owns. Use when a caller asks how to handle
  a tense, aspect, gender, number, voice/passive, or politeness form that the target
  forces.
kind: skill
status: ready
provenance:
  principles:
  - P009
  - P015
  - P025
  - P026
  - P045
  - P046
  - P055
  - P057
  - P064
  - P084
  - P085
  claims:
  - C00115
  - C00116
  - C00117
  - C00118
  - C00119
  - C00120
  - C00121
  - C00122
  - C00123
  - C00124
  - C00125
  - C00126
  - C00127
  - C00128
  - C00129
  - C00130
  - C00131
  - C00132
  - C00133
  - C00134
  - C00135
  - C00136
  - C00137
  - C00138
  - C00139
  - C00140
  - C00141
  - C00142
  - C00143
  - C00144
  - C00145
  - C00146
  - C00147
  - C00148
  - C00149
  - C00150
  - C00151
  - C00369
  - C00370
  - C00371
  - C00372
  - C00399
  - C00400
  - C00401
  - C00402
  evidence: []
  source_anchors: []
  authored_from_digest: ed470b54baf63c2a9fca276bfa87d647cd932cc1ff7c1929c96ae928ffbb0257
---

# Grammatical Equivalence

## Purpose

This skill reviews decisions forced by differences in grammar. Its rule is that a language's grammatical system, like its lexicon, determines what must be said, so the translator must render each obligatory category by its function — not copy the source form — and flag where the target grammar forces information the source left open.

## When to use

- The source and target grammars oblige different information (number, gender, tense, voice, definiteness).
- Voice, modality, tense, or aspect must cross between differing systems.
- Pronouns of address cross a T/V, gender, or inclusive/exclusive boundary.
- A grammatical choice must be weighed against a lexical one.

## Procedure

1. Expect grammar to act like a straitjacket: identify the obligatory categories the target forces and remember both lexical and grammatical resources determine what can be said (P025, P045).
2. Translate voice by function, not form — do not preserve an active or passive merely because the source used it (P009).
3. Handle grammatical gender by its function: "masculine as unmarked" describes the source system, not a default to carry into the target, so where the gender distinction is arbitrary or need not be specified, restructure (for example with the passive) rather than defaulting to it; and choose deliberately when moving between a number-marking and a numberless language (P015, P064).
4. Do not map tense and aspect mechanically, and render modality (certainty, possibility, obligation) by its function rather than its literal form (P046, P085).
5. When translating pronouns into a language that marks formality, gender, or inclusive/exclusive reference, resolve what the source leaves implicit deliberately (P026).
6. When weighing a grammatical against a lexical choice, distinguish grammar (morphology and syntax together, a closed, largely obligatory system that rules out alternatives by default) from lexis (an open, largely optional system) (P084).
7. Adapt grammar and lexicon to receptor-language requirements, first classifying terms as ordinary parallels, functional cultural analogues, or culture-specific items — and only then choosing a strategy (e.g. borrowing, paraphrase, cultural substitution) for the culture-specific class, per the word-level skill; always satisfy obligatory receptor features, but flag any forced addition, specification, or omission when the source is silent (P055, P057).

## Inputs

- The source structure and the draft target structure.
- The obligatory categories each grammar marks (number, gender, tense, voice, modality).
- What the source leaves open that the target forces.

## Output

Per finding: name the grammatical category at issue, whether the draft copied form or rendered function, what the target forced that the source left open, and the function-based correction; in compare mode weigh two function-based renderings — including the extra meaning each target form carries — by function (P046). Follow the shared advise/review/compare response protocol in `../../references/translation-equivalence-key-concepts.md`.

## Anti-patterns to flag

- Preserving source voice, tense, or aspect by form when function differs (P009, P046).
- Mapping modality or gender literally instead of by function (P085, P015).
- Silently inventing information the target forces without flagging the forced choice (P057).

## Worked example

Source: "The samples were analyzed" (passive); a draft into a target where that passive reads unnaturally keeps it passive on the grounds the source used it. Diagnosis — voice copied by form, not rendered by function (P009). If the target's natural active rendering forces an agent the source left unstated, that is a forced specification to flag, not to invent silently (P057); where a gender or number the target forces is arbitrary here, restructure rather than default to the unmarked form (P015, P064). Residual loss — the target may add or drop information the source left open; flag each forced choice, and hand the wording back.

## References

See `../../references/translation-equivalence-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/translation-equivalence-key-concepts.md` for the equivalence vocabulary this skill uses.

## Provenance

Derived from principles P009, P015, P025, P026, P045, P046, P055, P057, P064, P084, P085, grounded in the distillation-only sources (Baker, *In Other Words*; Nida, dynamic and formal equivalence). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
