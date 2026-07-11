# Provenance Ledger — k6-load-test-scripting-advisor

## Source pack

| source_id | title | author | rights_status | authority | conversion |
|-----------|-------|--------|---------------|-----------|------------|
| `k6-guideline-20260612112658` | Most commonly used terms in K6 | Anshita Bhasin | distillation-only | secondary | ok (Docling, 52 heading anchors h0000–h0063) |

- sha256: `abd331966f5b1fc3f587a368f1e8d358d6158a21e276328b311de750bf1d075b`
- page_count: 16, word_count: ~1233, anchor_count: 64 (h0000–h0063), asset_count: varies
- Rights note: the PDF carries no license or copyright notice — only "Author: Anshita Bhasin" and a LinkedIn link. An authored work with no stated open license is copyrighted by default. Classified conservatively as `distillation-only`: distillation allowed, no verbatim quotation. Unchanged from prior conversion; confirmed in interrogation-records.yaml evidence_gaps item 1.

## Field provenance (profile.yaml → QID → source evidence, v0.3.0)

All provenance re-anchored to real Docling heading anchors (h0000–h0063).

| Profile field | QID | Source evidence |
|---------------|-----|-----------------|
| `display_name` | Q1 | Anchor h0000 ("Most commonly used terms in K6"); anchor h0062 names "k6" as the open-source load-testing tool. |
| `role` | Q1, Q2 | Anchors h0001–h0058 define 23 k6 terms with options-object examples (vus, iterations, duration, stages, scenarios, thresholds, checks, metrics). |
| `when_to_use[0]` | Q3 | Anchors h0006 (VU), h0008 (Iterations), h0010 (Duration), h0012 (Stages), h0016 (Target): define the load-profile options. |
| `when_to_use[1]` | Q3 | Anchors h0027 (Thresholds), h0022 (Checks), code block c0029 (threshold examples). |
| `when_to_use[2]` | Q3 | Anchors h0040 (Scenario), h0056 (Ramping), h0057 (Ramping VUs): executor-level ramping configuration. |
| `when_to_use[3]` | Q3 | Anchor h0026 (Metrics): Counters/Gauges/Rates/Trends; built-in http/iteration/vu metrics. |
| `when_to_use[4]` | Q3 | Anchors h0000 (intro), h0020 (90 Percentile), h0021 (95 Percentile), h0038 (Error_Code): glossary use-case. |
| `when_not_to_use[0]` | Q4 | Anchor h0062 conclusion: source is k6-only, no cross-tool comparison. |
| `when_not_to_use[1]` | Q4 | Absence of content: source covers scripting the test, not tuning the SUT. |
| `when_not_to_use[2]` | Q4 | Absence of content: distributed/cloud exec, xk6, custom metrics, CI — not present in anchors h0000–h0063. |
| `inputs.required` | Q5 | Anchors h0007, h0009, h0011, h0013, h0017, h0023, h0028, h0041, h0055, h0058: each section pairs concept with options-object context. |
| `outputs.primary_format` | Q6 | Anchors h0001–h0058: every numbered section delivers prose definition + options-object example. |
| `modes[advise]` | Q9 | Entire cheat sheet is actionable how-to: explains, recommends, and shows configuration for each k6 option and construct. |
| `modes[compare]` | Q9 | Anchors h0020–h0021 (P90 vs P95), h0026 (four metric types), h0022 + h0027 (checks vs thresholds distinction). |
| `quality_bar[0]` | Q7 | Principles k6-p001, k6-p002, k6-p004 (checks/thresholds/stages documented meanings). |
| `quality_bar[1]` | Q7 | Principle k6-p003 (checks vs thresholds must not be conflated). |
| `quality_bar[2]` | Q7 | Principles k6-p005, k6-p007 (metric types and primary built-in metrics). |
| `quality_bar[3]` | Q7 | Evidence gap note from interrogation: gaps in coverage are stated, not invented. |
| `minimum_useful_output` | Q11 | Shortest source unit: one-paragraph term definition + code/image example (e.g. VU definition at anchor h0006/h0007). |
| `forbidden_behaviours[0]` | Q10 | Scope boundary at anchors h0000–h0062; faithfulness constraint from k6-p001–k6-p008. |
| `forbidden_behaviours[1]` | Q10 | Anchor h0062 conclusion: source is k6-only. |
| `forbidden_behaviours[2]` | Q10 | Principle k6-p002 scope note: source shows threshold examples, not mandated values. |
| `handoff_rules` / `canonical_owner` | Q8 | Anchor h0062 names "QAs and Developers" as audience; downstream owner (script owner) inferred from context. |
| `source_of_truth_policy.precedence` | Q8, Q17 | Anchor h0026 "refer to the Metrics reference"; anchor h0062 "Ref: https://k6.io/docs/". |
| `knowledge_partition.always_on[0]` | Q12 | Anchors h0002 (init), h0003 (setup), h0004 (VU), h0005 (teardown): lifecycle stages. |
| `knowledge_partition.always_on[1]` | Q12 | Anchors h0006 (vus), h0008 (iterations), h0010 (duration), h0012 (stages), h0016 (target): options object. |
| `knowledge_partition.always_on[2]` | Q12 | Anchors h0027 (thresholds, principle k6-p002), h0022 (checks, principle k6-p001). |
| `knowledge_partition.always_on[3]` | Q12 | Anchor h0026 (metric types, principle k6-p007). |
| `knowledge_partition.skills` | Q13 | Options/stages, thresholds/checks, scenarios/executors, metrics: all actionable detailed topics. |
| `knowledge_partition.references` | Q14 | 23-term glossary is reference material (entire cheat sheet). |
| `knowledge_partition.mcp` / `caller_supplied` | Q15, Q16 | None — no tool retrieval or per-project runtime context required. |
| `tier` | — | Tier 1: atomic evidence-backed principles (k6-p001–k6-p008) derived from claims (k6-c013–k6-c050) with full provenance chain. |

## Mode decision log

- **advise** — assigned. Verb: explain/recommend; deliverable: the k6 options/scenario/threshold/check configuration. Pervasive in source (anchors h0001–h0058). Grounded in principles k6-p001, k6-p002, k6-p004, k6-p005, k6-p006, k6-p007, k6-p008.
- **compare** — assigned. Verb: contrast; deliverable: documented distinction used to choose a construct. Grounded in principles k6-p003, k6-p006, k6-p007 (anchors h0020, h0021, h0022, h0026, h0027).
- **review, validate, produce, extract, patch-suggest** — NOT assigned. The cheat sheet defines and contrasts concepts but presents no procedure for auditing, gating, drafting from scratch, extracting, or proposing a bounded change to an existing script. No deliverable evidence → withheld per the mode-evidence rule. No patch-policy.yaml required.

## Conflicts and gaps

- No multi-source conflicts (single source).
- Evidence gaps (from interrogation-records.yaml):
  1. No license/copyright notice → rights set to `distillation-only` conservatively.
  2. Q9 limited to advise + compare (no review/validate evidence in source).
  3. Q8 downstream owner inferred (script owner), not named explicitly in source.
  4. Several example sections reference images (image placeholders) not converted by Docling; code details from VU example (h0007), iterations (h0009), duration (h0011), scenario (h0041), requests (h0043), cookies (h0045), ramping-vus (h0058) are unavailable from images.

## Quotation policy

`distillation-only`: no verbatim quotation in any generated artifact. Profile prose is paraphrase/restructure of definitions. Run `quote_scan` before release.

## Review schedule

- Volatility: low; cadence: annual (Q18). k6 option/executor/metric names drift across k6 releases; re-verify against current k6 docs. Source is undated.

## Version history

| Version | Date | Change | Supersedes |
|---------|------|--------|------------|
| 0.3.0 | 2026-06-12 | SUPERSESSION re-author. Prior source conversion (k6-guideline-20260608232906) used MarkItDown and produced 0 heading anchors (empty-anchor), making all field provenance unanchored. Re-ingested as k6-guideline-20260612112658 with Docling, yielding 52 real heading anchors (h0000–h0063). All profile-field provenance re-anchored to real section headings. Interrogation re-run (Q1–Q18). Tier set to 1: atomic principles k6-p001–k6-p008 derived from claims layer with full provenance chain. quality_bar and forbidden_behaviours grounded in principle IDs. always_on fields cite new heading anchors. | 0.2.0 |
| 0.2.0 | 2026-06-11 | Authored all 4 skill bodies and the k6-terminology-glossary reference. Promoted package from draft to ready. Skills grounded in profile always_on/when_to_use rules and the source cheat sheet (Tier 0, no principle/claim layer). | 0.1.0 |
| 0.1.0 | 2026-06-09 | Initial derivation from the k6 cheat sheet (MarkItDown conversion, 0 anchors). advise + compare modes. Stub skills and reference. status: draft. | — |
| 0.4.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |
