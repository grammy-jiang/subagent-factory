# Review Loop — research-career-advisor — Round 2

Single review pass. Scope: `subagents/research-career-advisor/`. Review-only; no package files edited.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** (0 FAIL) |
| `quote_scan` | PASS — no verbatim quotation |
| ellipsis-truncation grep | clean |
| adapter invariant-truncation grep | clean |
| injection-scan | 7× WARN, all in `sources/markdown/hamming-meta-*.md` (frozen source, Hamming motivational prose `role-override/body/medium` + normalization artifacts). Benign — triage-not-block per untrusted-source-policy. **Not must-fix.** |

No deterministic FAILs → 0 must-fix from gates.

## Consolidated findings (most-severe first, deduped across 4 lenses)

### must-fix

1. **`skills/evaluation-metrics-and-research-judgment/SKILL.md` (frontmatter description + `## When to use`, lines 4-9, 64-80) — trigger scope drifts outside advisor boundary.**
   Problem: 5 of 8 "when to use" bullets are generic org/management-judgment prose with no research-career anchor (P018 systems judgment, P028 training for changing tools, P030 selection-pipeline design, P037 local-vs-system-value tracing reads as SRE/eng-org language). Profile `when_not_to_use` explicitly excludes "general software engineering unrelated to research" and hiring decisions, yet this skill gives the router no scoping language to distinguish a generic corporate-metrics/hiring question from a research-lab one → risks firing out-of-scope + makes the skill read as a leftover-judgment catch-all (weak lens-fit vs its 7 siblings).
   Fix: Rewrite the description and each bullet to anchor to the research domain (a lab/department productivity or publication metric; screening PhD/postdoc applicants; an expert's judgment carried into a new subfield; a lab's local-optimization anti-pattern) so the trigger cannot be satisfied by a purely generic corporate-metrics/hiring question.
   *Related (same root — the two methods skills sit awkwardly under a career-advisor identity): ai-agent should-fix below (role bundling) and profile should-fix below (boundary-rule citation fit). Fixing the trigger scope here + adding the sibling carve-out addresses the cluster.*

### should-fix

2. **`profile.yaml` — no `when_not_to_use` / `handoff_rules` carve-out vs `research-integrity-reproducibility-advisor` sibling.**
   Problem: `experimental-design-and-measurement` covers null-hypothesis validity, uncertainty/selection-effect accounting, instrument validation — core research-integrity concerns. The writing-advisor overlap has an explicit carve-out (`when_not_to_use[3]`) but the integrity sibling does not, so both subagents can claim the same request.
   Fix: Add a `when_not_to_use` bullet routing integrity/reproducibility audits (misconduct, p-hacking, replication failure) to `research-integrity-reproducibility-advisor` (confirm sibling scope first).

3. **`profile.yaml` — `handoff_rules` (2 items) omits the sibling-agent routing that `when_not_to_use[3]` already declares.**
   Problem: `when_not_to_use[3]` routes craft-level writing to `research-writing-advisor`, but `handoff_rules` (the field designed to carry routing) only lists human owners.
   Fix: Add a third `handoff_rules` entry: craft-level research-writing tasks (sentence clarity, drafting, figure/slide design, academic-English editing) → `research-writing-advisor`.

4. **`profile.yaml:86-91,97-99` — boundary-rule citations are topically adjacent, not source support for the boundary asserted.**
   Problem: `forbidden_behaviours[0]` (P017,P013) / `handoff_rules[0]` (P015,P017) / `forbidden_behaviours[1]` (P010,P021) / `[2]` (P026) assert advisor-vs-researcher ownership and no-prediction-of-outcomes, but the cited principles state dissertation structure / program orientation / milestone decomposition / how-to-choose / negotiate-in-writing — none literally establishes the boundary. Ledger's blanket "every value cites the principle it restates" overstates fidelity here.
   Fix: In `provenance-ledger.md`, relabel these rows as structural/house-policy (advice-only boundary), OR cite a `claims.jsonl` claim that actually states advisor-vs-researcher ownership if one exists.

5. **All 8 `SKILL.md` — `## References` (7 of 8) give a generic pointer, not a load-on-demand condition.**
   Problem: 7 skills use identical "See `../../references/...` for the full catalogue" prose — a pointer, not a trigger. `funding-grants-and-research-proposals` (lines 88-89) does it right: "Consult ... only when a finding's principle needs its full source-grounded statement / when the caller disputes grounding."
   Fix: Adopt the funding skill's conditional phrasing across the other 7 so each reference load is gated by need.

6. **All 8 `SKILL.md` — 4× content redundancy per body (`Purpose` ≈ `When to use` ≈ `Procedure` ≈ `Anti-patterns`).**
   Problem: `## Purpose` near-verbatim copies the profile `always_on` bullet; the other sections restate the same content 3 more times. `## Procedure` is the genuinely distinct actionable content. Under the ~5k-token ceiling (~1.3-1.9k words each) so not a hard budget FAIL, but works against token discipline.
   Fix: Trim `## Purpose` to 1-2 sentences; let `## Procedure` carry the detail.

7. **`skills/funding-grants-and-research-proposals` + `research-program-and-problem-selection` — frontmatter `description` 2-3× longer than siblings; possible 1024-char breach.**
   Problem: 12-14 folded YAML lines (~175 words funding); estimated near/over the 1024-char frontmatter cap, and schemas carry no length check so `validate` won't catch it. Over-long descriptions defeat the cheap always-loaded triggering tier.
   Fix: Extract the field, verify char count, trim both to a single tight paragraph with the concrete trigger phrases.

8. **`profile.yaml` — role bundles two personas (career strategy + general empirical-methodology reviewer) under one identity.**
   Problem: Name/framing centre on career strategy, but 2 of 8 skills are a methodology/statistics soundness reviewer serving a different caller intent; a caller wanting "is this p-value analysis sound" may not invoke a "career advisor." Disclosed up front (not hidden) but reads as two jobs stapled together — routing-coherence risk.
   Fix: (a) document in `role` why methodology-review belongs (empirical rigor as career survival, per Cohen/Hamming), or (b) rebalance `router_description`/`when_to_use` ordering for discoverability, or (c) hive the two methods skills into a dedicated research-methods advisor if a sibling covers it.

### nice

9. `provenance-ledger.md:6-10` — "no orphan" is a blanket assertion, not a field→principle crosswalk table; optional table would surface the #4 citation-fit pattern.
10. `quality_bar[1]` cites P046 alongside P017/P012, but P046 grounds no clause in that bullet (P017+P012 cover it) — citation-hygiene looseness, not over-claim.
11. `presenting-...`, `writing-...`, `funding-...` SKILL.md use unwrapped long lines vs the ~78-char wrap in the other 5 — cosmetic diff-noise.
12. All 8 `## Procedure` steps pack 2-4 clauses per sentence; splitting into sub-bullets improves scannability.
13. `when_to_use[5]` (empirical-study soundness) sits flat among 4 career bullets with no signpost that it invokes a different mental model — cosmetic.

## Faithfulness

No rule at `SCOPE_BROADENED` or worse. All checked rules `WITHIN_SCOPE`/`EXACT_SUPPORT`; the v1.1.0 reputation-as-tie-breaker hedge fix (P010 scope) confirmed still intact. 0 over-claim must-fix.

## Lens must-fix tallies
deterministic 0 · agent-skills 1 · profile 0 · faithfulness 0 · ai-agent 0 → deduped total 1.

MUST_FIX_COUNT: 1
