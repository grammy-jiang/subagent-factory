# Adversarial verify gate — translation-equivalence-advisor (verify1)

**Package:** `subagents/translation-equivalence-advisor/` (Baker, *In Other Words* 1992 + Nida
dynamic/formal-equivalence extract; 116 principles; v1.2.0)
**Trigger:** Step 6 of `/review-subagent`. Review loop self-reported `must-fix=0` (CLEAN
2026-07-11T18:39:47Z). This gate independently re-checked and does NOT trust that.

**Panel (5 reviewers, parallel):** faithfulness-reviewer (re-derived grades from
`principles/principles.yaml`, not authored report) · safety/adapter check ·
descriptive-translation-reviewer · translation-quality-reviewer · technical-translation-advisor.

**Result: the loop's `must-fix=0` is NOT clean — 2 real must-fix survive.** Both are
principle→skill/profile drift the loop's own resolve-or-defer discipline missed, verified against
the canonical `principles/principles.yaml` (not recall).

---

## MUST-FIX

### MF-1 — `skills/grammatical-equivalence/SKILL.md` step 7 conflates a term-TYPE with a STRATEGY, drifting from cited P055 and contradicting the package's own no-map-to-strategy rule *(domain — translation-quality-reviewer; verdict CONFIRMED)*

- **Written:** *"...first classifying terms as ordinary parallels, functional equivalents, or
  **borrowings**; ... (P055, P057)."*
- **Cited principle P055** (`principles/principles.yaml:1106-1107`, verified): *"...first
  classifying terms as ordinary parallels, functional **cultural analogues**, or
  **culture-specific items**."* (Nida, C00371.)
- **Defect:** the skill silently swaps the diagnostic third category **"culture-specific items"**
  (a term-TYPE: a lexical gap) for **"borrowings"** (a STRATEGY: the loan-word device), and drops
  "cultural" from the second. This collapses Nida's *classification* into one of its *solutions* —
  and directly contradicts this same package's governing rule in
  `word-level-nonequivalence-and-strategies/SKILL.md` step 3 ("diagnose the type... but do not map
  that type to a strategy"). A user follows step 7 and pre-labels a culture-specific item as "a
  borrowing" before any strategy choice, short-circuiting the deliberate-selection discipline the
  rest of the package enforces.
- **Fix (no new source):** restate step 7 to P055's sense — classify as ordinary parallels /
  functional cultural analogues / culture-specific items; only *then* choose a strategy (borrowing,
  paraphrase, cultural substitution) for the culture-specific class, per the word-level skill.
  Re-run faithfulness + validate.

### MF-2 — `profile.yaml` quality_bar[0] broadens word-scoped P037/P001 to "or phrase level" *(faithfulness — independent re-derivation; verdict PLAUSIBLE, grader-dependent)*

- **Written (quality_bar[0]):** *"No one-to-one match at word **or phrase level**: diagnose the
  non-equivalence... choose from an open set... (P037, P001, P103, P106)."*
- **Cited P037** (`principles.yaml:773`, verified): *"Never assume a one-to-one correspondence
  between **words** and meanings across languages..."* — word-scoped. **P001** likewise word-scoped;
  P103/P106 are general strategy-openness, not scoped to word-vs-phrase.
- **Defect:** "or phrase level" is a **SCOPE_BROADENED** extension its citations do not support.
  Phrase/collocation level is governed by different principles (P042/**P043** — judge collocations
  by target **typicality**, which presupposes typical target patterns commonly *do* exist), so
  framing phrase-level rendering as "no one-to-one match" with the same certainty as word-level
  runs against P043 and changes the character of the advice. This is the exact spot the review-loop
  history says it touched; the existing `reports/faithfulness-report.yaml` grades it WITHIN_SCOPE —
  incorrect on re-derivation. Every *other* P037-citing locus (forbidden[1], always_on[0], the
  line-181 example) correctly stays word-scoped; quality_bar[0] is the sole outlier.
- **Factory rule engaged:** `.claude/rules/evidence-protocol.md` — *"No generated rule may be
  stronger than its source support."* This is a strict gate, so counted must-fix despite being
  advice-adjacent rather than advice-reversing.
- **Fix:** narrow to "word level" (match P037/P001), or, if phrase coverage is intended, cite an
  actual phrase-level principle (P042/P043) and reframe away from "no one-to-one match" — or fold
  the phrase content into quality_bar[1]'s collocation/idiom framing.

---

## NICE (not must-fix — recorded, defer or batch)

- **N1 — Grice maxim named "Relevance" not "Relation"** (`pragmatic-equivalence.../SKILL.md`,
  P032/P073). descriptive-reviewer flagged MUST_FIX vs Grice's canonical "Maxim of Relation."
  **Downgraded:** the package is *faithful to its source* — its own grounded P032
  (`principles.yaml:675-676`) reads "Quantity, Quality, **Relevance**, and Manner," Baker's standard
  gloss. Not a factory over-claim and not advice-harmful; a terminology-precision nit. Optional:
  gloss as "Relation (be relevant)".
- **N2 — P023 skill drift** (`dynamic-and-formal-equivalence/SKILL.md` step 4): skill says
  "cultural substitute" where P023 says "receptor-language description" — two different strategies.
  Same drift class as MF-1 but not self-contradicting; low harm. Align wording to P023.
- **N3 — "continuative" folded into Halliday & Hasan's 4-part conjunction taxonomy**
  (`cohesion-and-texture/SKILL.md` step 3, P017). Conflates cohesion-conjunction (additive/
  adversative/causal/temporal) with a distinct textual-Theme category. Taxonomic precision; no
  actionable-advice error.
- **N4 — adapter invariants: 2 ellipsis truncations** (`.md` P038, P058) — cut only the trailing
  "because…" **rationale**, not the must-hold imperative. **Unlike** the sibling-package factory
  bug (which gutted the safety clause), here every load-bearing directive survives. Cosmetic.
- **N5 — "explanatory vs supplemental coherence"** (P070) — could not corroborate as Baker's own
  terms; skills carry `evidence: []`/`source_anchors: []` so no anchor to check. Provenance-check
  before relying on the label pair as citable.
- **N6–N15** — quality_bar[5] P050 motivated-deviation hedge slightly flattened; quality_bar[2]/[1]
  citation-completeness (gender P015/number P064/modality P085/typicality P043 uncited in-bullet);
  precedence "aesthetic" vs P005 "poetic"; plus the r3 NICE backlog (N1–N11 in
  `...r3.review.md`: phrase-scope N1 [= MF-2 escalated here], 被-passive currency, edition note,
  role omits `compare` mode, golden-tests `generated_at` not bumped, DRY boilerplate). Batch or
  defer with reasoning.

---

## Verified clean (adversarially confirmed, no issue)

- **Advisory boundary intact** — tools Read/Grep/Glob only; `mcp: []`, `caller_supplied: []`; never
  delivers final target text, never certifies one correct rendering (Role/When-NOT/Forbidden/
  Handoff/Precedence all present, un-truncated). No tool-grant widening, no escalation tokens.
- **DO-NOT-EDIT generated header** present (adapter lines 8–15). Installed adapter byte-identical to
  canonical `adapters/claude-code/`.
- **Profile→adapter parity** — all 4 forbidden_behaviours, 9 quality_bar, precedence, handoff
  reproduced verbatim; nothing load-bearing dropped in compilation.
- **v1.2.0 MF-1/MF-2 (receptor-response dual-criterion; idiom hedge) genuinely closed** — confirmed
  consistent across profile + skill + key-concepts by technical-translation-advisor.
- **Baker word-level 8-strategy set, meaning types, semantic fields, idiom traps, formal/dynamic
  equivalence, theme/rheme + FSP, register field/tenor/mode** — all domain-accurate as scoped.
- Skopos / DTS-norms / domestication correctly deferred to sibling packages, not mis-asserted.

MUST_FIX_COUNT: 2
