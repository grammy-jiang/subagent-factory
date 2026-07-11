# Changelog — technical-translation-advisor

All notable changes to this generated subagent package.

## 1.1.0 — 2026-07-12

### Changed
- Review-loop convergence (`/review-subagent`): resolved the 8 must-fix from the domain + structural review panel, each grounded in the existing spine.
- **MF2** — regenerated all 10 skill bodies without the fixed-length truncation that had severed Procedure/anti-pattern steps mid-clause; the generator now renders full principle statements and fails if any body still contains a truncation ellipsis.
- **MF3 (P146)** — attributed the notice-severity table to Byrne as one illustrative convention and added a hedge to verify the governing warning-label standard for the target market (e.g. ANSI Z535 / ISO 3864) rather than asserting one ordering as fact.
- **MF8 (P003)** — rephrased the invariant from a first-person production imperative to an advisory statement, and made the advice-only boundary unambiguously override the operating invariants; the invariants list no longer reads as licence to produce a translation.
- **MF4** — added an explicit forbidden behaviour against certifying/signing off safety-critical or legally-mandated content (the role and golden test GT-005 already required it).
- **Faithfulness (MF5/MF6/MF7 + SF)** — dropped a manufactured evidence anchor (P045) from precedence, restored P133's client-permission caveat and P104's hedge, narrowed the source-deficiency escalation duty to safety-critical content, softened 'every'→'nearly every' (P069), corrected the P078 handoff citation, and graded the precedence rule.
- **SF9/SF10** — added routing triggers for the iconic-linkage and document-type skills, a sibling-disambiguation when-not-to-use line, and reframed web/EUR-Lex consultation as advice to the caller (the advisor's tools are Read/Grep/Glob).

## 1.0.0 — 2026-07-11

### Added
- Initial LLM-authored layer over the deterministically-valid distilled spine (150 principles from 2 distillation-only sources by Jody Byrne).
- `profile.yaml` (tier 2, advice-only) with role, when-to-use/not, three modes (advise/review/compare), quality bar, forbidden behaviours, handoff rules, and a 10-skill / 2-reference knowledge partition — every rule grounded in cited principle ids.
- `reports/faithfulness-report.yaml`: every load-bearing profile rule graded against the principles/claims (EXACT_SUPPORT or deliberate WITHIN_SCOPE narrowing; no over-claim).
- 10 authored skills and 2 references, each with resolving principle/claim/evidence provenance.
- `tests/`: golden tests (6 positive, 3 negative-routing, 2 missing-context) and principle-behaviour tests covering all 150 principles.
- Claude Code adapter exported and installed.
