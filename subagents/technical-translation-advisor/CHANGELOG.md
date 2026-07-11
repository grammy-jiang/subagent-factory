# Changelog — technical-translation-advisor

All notable changes to this generated subagent package.

## 1.1.0 — 2026-07-12

### Changed
- Review-loop convergence **plus independent adversarial verification** (`/review-subagent`): resolved every must-fix from the structural + domain panel across two passes — the headless review loop, then a 6-lens adversarial re-verify (faithfulness + documentation-as-code + ux-design + the translation-equivalence / descriptive-translation / translation-quality domain reviewers) that caught real holes the loop missed — each fix grounded in the existing spine.
- **MF1 (adapter render, safety)** — the invariant compiler (`compile_invariants.py`) truncated each must-hold rule to 160 chars, gutting P146's warning-severity hedge (and P141, P102) from the *deployed adapter*; it now renders each invariant as a complete first sentence and `validate` fails on any truncated (`…`) invariant.
- **MF2** — regenerated all 10 skill bodies without the fixed-length truncation that had severed Procedure steps mid-clause; the generator now renders full statements and rejects any body containing a truncation ellipsis.
- **MF3 (P146, safety)** — rewrote so the first sentence carries the complete duty to verify the notice-severity hierarchy against the market's governing warning-label standard (ANSI Z535, ISO 3864, IEC 82079-1); Byrne's table is now a clearly-bracketed example with an explicit flag that its Warning/Caution assignment is the reverse of the common standard ranking (DANGER > WARNING > CAUTION > NOTICE).
- **MF8 (P003 + adapter template)** — de-imperative'd P003, and fixed the shared adapter template so the Operating-invariants section is explicitly subordinate to the role boundary and Forbidden behaviours, resolving the invariants-vs-boundary contradiction.
- **MF4** — added a forbidden behaviour against certifying/signing off safety-critical or legally-mandated content (grounded in the commissioner's sign-off remit, P090).
- **Faithfulness** — dropped a manufactured evidence anchor (P045) from precedence; restored P133's client-permission caveat and P104's hedge; narrowed the source-deficiency escalation to safety-critical content in **both** quality_bar[5] and forbidden_behaviours[3]; softened 'every'→'nearly every' in **both** quality_bar[0] and always_on[0]; kept Latin nomenclature audience-conditional (P071) and footnote-avoidance scoped to queries (P139); corrected the P078 handoff citation; and graded the precedence rule and all 10 always_on bullets.
- **Domain accuracy** — scoped precedence so documentary (P035) and form-priority (P089) translations keep literal fidelity, with P133's reorder threshold corrected; P070 now names adaptation as the fourth oblique procedure (P131); P042 distinguishes concurrent from retrospective think-aloud (C00379); P018 prefers a pre-tested questionnaire (C00387); P080 is scoped to marketing case studies with a genre-check flag (P072/P128).
- **SF9/SF10/NH1** — added routing triggers for the iconic-linkage and document-type skills, a sibling-disambiguation when-not-to-use line, reframed web/EUR-Lex consultation as advice to the caller (Read/Grep/Glob toolset), and fixed the skill Purpose grammar.

## 1.0.0 — 2026-07-11

### Added
- Initial LLM-authored layer over the deterministically-valid distilled spine (150 principles from 2 distillation-only sources by Jody Byrne).
- `profile.yaml` (tier 2, advice-only) with role, when-to-use/not, three modes (advise/review/compare), quality bar, forbidden behaviours, handoff rules, and a 10-skill / 2-reference knowledge partition — every rule grounded in cited principle ids.
- `reports/faithfulness-report.yaml`: every load-bearing profile rule graded against the principles/claims (EXACT_SUPPORT or deliberate WITHIN_SCOPE narrowing; no over-claim).
- 10 authored skills and 2 references, each with resolving principle/claim/evidence provenance.
- `tests/`: golden tests (6 positive, 3 negative-routing, 2 missing-context) and principle-behaviour tests covering all 150 principles.
- Claude Code adapter exported and installed.
