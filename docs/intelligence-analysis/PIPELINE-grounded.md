# The analysis pipeline — grounded (12 steps, data contracts, components)

> Single source of truth for the intelligence-analysis workflow. **Every step's scope, its I/O formats, and
> its store reads/writes cite a source claim.** The only non-groundable items — pure software plumbing — are
> quarantined in the last section and are NOT part of the grounded design. Citations: `<book> <claim_id>`,
> or `ACH Step N` (Heuer's numbered source text), or `<Technique> method` (CIA Tradecraft Primer).
> Companions: `BLUEPRINT-intel-analysis-agent.md` (what/why/decisions), `DESIGN-SPEC-intel-analysis-agent.md`
> (build detail). Sources MAPped in `inputs/intelligence-analysis-advisor/` (2,084 principles / 11 books).

## Grounding discipline
- **(a) source-grounded** — the *what/why/format* traces to a claim. Everything in this doc except the last section.
- **(b) build-plumbing** — form/serialization the 1949–2015 sources can't state; quarantined below, deferred to build time.
- Rule: default to finding the claim; verify against `cache/book-extracts/<sha>/claims.jsonl`, not recall.

## The 12 steps — scope, four I/O legs, component
Legs: **↑ upstream-in** (pipeline) · **⟲ store-read** (self/local DB) · **↓ downstream-out** (pipeline) · **⟳ store-write**.

| # | step (scope, grounded) | ↑ upstream-in | ⟲ store-read | ↓ downstream-out | ⟳ store-write | component |
|---|---|---|---|---|---|---|
| 1 | **Frame** — input → precise question + sub-questions + purpose *(Kent C012, C020; Tetlock C150)* | raw input | reference-class / base-rate ("outside view", Tetlock **C155**) | Question | case-workspace | skill: SAT + calibrated-forecasting |
| 2 | **Hypotheses** — enumerate ALL competing hypotheses *(Heuer C102)* | Question | — | HypothesisSet | case-workspace | skill: SAT |
| 3 | **Collect + grade** — gather evidence; grade objectively *(FM C023, C027)* | Question | **source-trust-registry** — source's credibility history (Masterman **C044**; scale FM **C428**) | EvidenceItem[] | evidence-ledger | skill: source-evaluation / osint-investigation |
| 4 | **ACH matrix** — hyp×evidence, rate consistency *(Heuer C234; ACH Step 3)* | HypothesisSet + EvidenceItem[] | — | ACHMatrix | ach-engine | tool: ach-engine + skill supplies ratings |
| 5 | **Key assumptions** — surface + test load-bearing premises *(Primer C009)* | analysis so far | — | KeyAssumptions[] | case-workspace | skill: SAT |
| 6 | **Conclude by disproving** — rank by least-inconsistency *(Heuer ACH Step 5)* | ACHMatrix | — | Ranking | ach-engine | tool: ach-engine + skill interprets |
| 7 | **Bias / misperception check** *(Kahneman C009; Jervis C006)* | case state | — | ReviewFinding[](bias) | case-workspace: audit trail | **subagent** bias-perception-reviewer |
| 8 | **Contrarian + deception** — devil's-advocate + D&D sensitivity *(Primer C051; Masterman C002; ACH Step 6)* | case state | — | ReviewFinding[](method/deception) | case-workspace: audit trail | **subagent** method-reviewer (+deferred deception-reviewer) |
| 9 | **Calibrated judgment** — numeric probability + confidence *(Tetlock C076/C077; EPJ C041)* | Ranking + ReviewFinding[] | **calibration-tracker** — own track record (Tetlock **C239**, EPJ **C005**); base-rate (**C155**) | Judgment | calibration-tracker: log forecast | skill: calibrated-forecasting + subagent audits |
| 10 | **Report + approve** — assemble assessment; human decides *(Heuer ACH Step 7; Kent C012, C020, C167)* | Judgment + all | — | Assessment | case-workspace | skill: production + human gate |
| 11 | **Indicators** — observables to monitor going forward *(Primer C032)* | Assessment | — | Indicator[] | case-workspace: watch-list | skill: SAT |
| 12 | **Score + feedback** — Brier-score; update track-records *(Tetlock C086)* | Judgment (later) + outcome | calibration-tracker (logged forecast); evidence-ledger (its sources) | Score | **calibration-tracker** (Brier C086) + **source-trust-registry** (update credibility, C044) | tool: calibration-tracker + source-trust-registry |

## Artifact formats — as the sources DEFINE them (not invented)
- **Question** — question + sub-questions (Tetlock C150) + policy purpose: outgoing/defensive (Kent C020).
- **HypothesisSet** — all hypotheses (Heuer C102); status candidate/unproven/disproved (Heuer C241, keep unproven≠disproved alive).
- **EvidenceItem[]** — Heuer **ACH Step 2**: beyond concrete reporting, include (1) the analyst's own assumptions/deductions, (2) per hypothesis "if true, what should I see or NOT see?", (3) the **absence of evidence** ("the dog that did not bark"); + reliability **A–F** / credibility **1–6** (FM **C428**).
- **ACHMatrix** — Heuer **ACH Step 3/5**: hypotheses across top, evidence down side, per-cell consistency; across rows (Step 3) then down columns (Step 5); refine/delete non-diagnostic (Step 4).
- **KeyAssumptions[]** — Primer **Key-Assumptions-Check method**: analytic line; all premises (stated+unstated); challenge each; refined must-be-true list + failure conditions; per-assumption confidence + what-would-undermine.
- **Ranking** — Heuer **ACH Step 5**: hypotheses ordered, leading = fewest inconsistencies.
- **ReviewFinding[]** — the critique: the best case for an alternative (Primer C051) / D&D risk (Masterman C002) / a flagged bias (Kahneman C009, Jervis C006).
- **Judgment** — probability as an explicit **number** (Tetlock C076/C077); calibration + discrimination (EPJ C041); + confidence, dissent.
- **Assessment** — Heuer **ACH Step 7**: relative likelihood of ALL hypotheses + specific confidence + alternatives-considered-and-why-rejected; the finished product (Kent C012).
- **Indicator[]** — Primer **Indicators method**: per-scenario expected observables, a Topics×Indicators×time matrix + triggers; maintain + regularly review (C032).
- **Score** — Brier = distance forecast↔outcome (Tetlock **C086**).

## Persistent stores — two scopes (both source-grounded as artifacts)
- **Per-case (one case file):** `case-workspace` (question/hypotheses/assumptions/conclusion/assessment/audit-trail/watch-list) · `evidence-ledger` (items + A–F/1–6 grades, FM C428) · `ach-engine` (the matrix, Heuer C234).
- **Cross-case (institutional memory / the "learning" layer):** `calibration-tracker` (keep score over time, Tetlock C086 — 60 claim hits) · `source-trust-registry` (a source's credibility built over time, Masterman C044 — source-reliability = 114 hits across FM/Heuer/Masterman).
- The learning leg: read the source's history to grade (step 3, C044); read base-rates/own-calibration to judge (step 9, C155/C239); write outcomes back (step 12, C086/C044).

## Loop-back & human gate — goal grounded, mechanism deferred
- **Loop-back / revise:** the process iterates — refine the matrix, reconsider hypotheses, keep unproven alive (Heuer C249, ACH Step 4; C241). *(retry-cap/escalation counter = plumbing.)*
- **Human before commit:** intelligence serves the decisionmaker; the analyst produces, the human owns (Kent C020; analyst's judgment Heuer C167). *(the approval-gate surface = plumbing.)*

## PURE BUILD-PLUMBING — quarantined, NOT part of the grounded design
Introduced only at build time, justified by engineering best-practice (mcp-security / mcp-quality reviews),
never by the corpus:
- Delivery-FORM labels (skill / subagent / MCP server); JSON/serialization shape; `id`/`case_id`/timestamps/links.
- Persistence mechanics: append-only, hash-chain, cross-server staleness/invalidation, `is_error` convention.
- Loop-back retry-cap + escalation counter; approval-gate surface; ReviewFinding severity/resolution bookkeeping.

**Everything above this section traces to the sources; everything in it is deferred plumbing. No third category.**
