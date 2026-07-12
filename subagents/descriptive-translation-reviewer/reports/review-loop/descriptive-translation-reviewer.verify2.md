# Adversarial Verify (Step 6) — descriptive-translation-reviewer

Independent adversarial re-check of the just-converged package (review loop claimed
must-fix=0). Five reviewers spawned in parallel; findings re-adjudicated against the
on-disk `principles/principles.yaml` and adapter — authored grades NOT trusted.

Package version at verify: profile.yaml `agent_version: 1.8.0`.

---

## MUST-FIX (survives adjudication)

### 1. Liturgical-verse example cites out-of-scope principles (faithfulness — SCOPE_BROADENED)

- **Location:** `profile.yaml`, `examples` → "Compare a formal against a dynamic rendering
  for a liturgical verse", `ideal_response`, the formal-orientation clause:
  *"The formal orientation preserves the source's syntactic and formal features and its
  foreignness but risks unidiomatic, opaque target lines **(P104, P162)**"*.
- **Defect:** Both cited principles are the wrong support for this clause.
  - **P162** is scoped verbatim to *"legal documents and equally valid multilingual
    treaties"* (`principles.yaml:3373`), and its actual content is about grammatical
    divergence causing "legal confusion, loopholes, or interpretive discrepancy" — nothing
    to do with a liturgical verse or with "unidiomatic, opaque target lines." Applying a
    legal/treaty-scoped principle to a liturgical text is SCOPE_BROADENED.
  - **P104** concerns obligatorily-forced grammatical categories / reserving the
    "untranslatable" verdict for poetry — it does not assert that formal orientation
    produces opacity.
- **Confirmed by:** faithfulness-reviewer (must-fix, SCOPE_BROADENED, high severity);
  independently flagged by translation-equivalence-advisor (P162 out-of-scope) and noted by
  technical-translation-advisor ("looser fit than P036 would have been … citation-precision").
- **Note:** The *claim itself is domain-correct* — two domain reviewers confirmed the
  formal-vs-dynamic trade-off and the sacred-text exception are textbook Nida. This is a
  **grounding/provenance** defect (a shipped example modelling reviewer output cites a
  principle outside its stated domain), not a theory error.
- **Fix (reground, no claim change):** cite **P105** (formal equivalence "matches source
  form and content closely … for academic or legal texts," `principles.yaml:2339` — already
  cited on the dynamic side of this same example) for the "preserves source form" part, and
  ground the opacity/unidiomatic risk in **P036** (sacred/sensitive-text word-and-syntax
  attention) or drop that risk clause. Remove **P162** unless the example is changed to an
  actual legal/treaty text.

---

## Adjudicated NOT must-fix

### A. "Reiss text types conflate Koller's equivalence relations" — FALSE POSITIVE

- translation-equivalence-advisor graded this a must-fix (misattribution). **Rejected on
  verification.** The changed principle is **P121** (`principles.yaml:2607`), whose statement
  reads *"Koller's denotative, connotative, text-normative, pragmatic, and formal
  (formal-aesthetic/expressive) kinds"* — correctly attributed to **Koller's** five
  equivalence relations, NOT to Reiss's text-type typology. Reiss's types
  (informative/expressive/operative) live separately and correctly in
  `skills/text-type-skopos-and-the-brief` (P060/P128/P129).
- The false positive was induced by the verify prompt's own framing ("Reiss text types");
  translation-quality-reviewer and technical-translation-advisor both read the file directly
  and independently confirmed the two typologies are correctly kept separate. No defect.

### B. House TQA / register-skill sibling-boundary overlap — DEFER (owner-decide)

- translation-quality-reviewer flagged that `register-discourse-and-audiovisual-constraints`
  (P064/P065/P021) implements House's overt/covert + field-tenor-mode quality judgement,
  which overlaps the `translation-quality-reviewer` sibling; the v1.8.0 routing fix only
  patched the applied-studies/corpus-scoring seam, not this one.
- **Not counted as must-fix for this package:** (i) it is a *pre-existing* design seam, not
  introduced by the loop; (ii) it is not an over-claim or domain error — House's model
  legitimately grounds register-based quality assessment as a descriptive method; (iii) the
  reviewer's own remedy is a *reciprocal boundary sentence on the sibling package*, which
  this package cannot edit. Route to the loop/family owner as a sibling-boundary refinement,
  not a convergence blocker.

---

## Clean

- **Adapter safety** (`.claude/agents/generated/descriptive-translation-reviewer.md`): all
  158 Operating-invariant lines intact — no truncation, no dangling `(e.g` / `…`, no unclosed
  parens; review-only boundary + all 5 forbidden behaviours present and uncut; DO-NOT-EDIT
  header at line 8; profile `forbidden_behaviours` map 1:1 to adapter with citations
  preserved. The `compile_invariants` truncation bug did **not** recur here. **0 must-fix.**
- **technical-translation-advisor:** routing boundary to `technical-translation-advisor`
  correctly scoped; Toury initial norm, operative-leaflet, and liturgical examples
  domain-accurate. **0 must-fix.**

---

## Reviewer tallies (raw, pre-adjudication)

| Reviewer | Raw | Adjudicated |
|---|---|---|
| faithfulness | 1 | **1 (kept)** |
| adapter/safety | 0 | 0 |
| translation-equivalence-advisor | 1 | 0 (false positive — Koller, not Reiss) |
| translation-quality-reviewer | 1 | 0 (defer — sibling boundary) |
| technical-translation-advisor | 0 | 0 |

MUST_FIX_COUNT: 1
