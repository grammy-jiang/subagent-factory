# Review — subagent `analytic-method-reviewer` (R2, review-only)

Package: `subagents/analytic-method-reviewer/` · profile `agent_version: 1.1.0`

## Gate (deterministic — authoritative)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). 3 injection-scan WARNs on
  `sources/markdown/thinking-fast-and-sl-d88ef771.md` = untrusted-source triage (role-override /
  fake-completion in the *source book text*), not package defects. Stale-maintenance = re-stamp
  hints only (no baseline digest), non-blocking.
- `quote_scan` → **PASS** — no verbatim quotation.

No gate FAIL. Must-fix below = BLOCKER + HIGH consolidated across the 4 review lenses.

---

## MUST-FIX (BLOCKER + HIGH)

### B1 · BLOCKER — provenance ledger missing the 1.1.0 version entry
`provenance-ledger.md` Version History only documents 1.0.0, but `profile.yaml:5` is `1.1.0` and
`CHANGELOG.md` records a substantive R1 change (body trimmed; `quality_bar`/`forbidden_behaviours`
re-scoped with P080/P010; `when_not_to_use` reordered). Violates the supersession rule in
`.claude/rules/generated-artifact-policy.md`.
**Fix:** add `### 1.1.0 — 2026-07-11` ledger entry summarizing the R1 fix-pass + updated grounding.

### H1 — ledger field→grounding table stale vs the 1.1.0 profile
Same root as B1 (ledger not refreshed on bump). Two stale rows:
- `provenance-ledger.md:34` (`quality_bar[4]` row) lists `P004,P006,P020,P058` — profile now also
  cites **P080**.
- `provenance-ledger.md:36` (`forbidden_behaviours` row) omits **P010**, which profile now cites.

**Fix:** add P080 and P010 to the respective rows (do together with B1).

### H2 — adapter frontmatter `description` truncation drops routing keywords
`.claude/agents/generated/analytic-method-reviewer.md:3`. Claude Code auto-routing reads only this
string. Lost inclusion keys "assumptions, uncertainty" (under-invokes) and lost exclusion keys
"interrogation, targeting, covert action" — kept only "collection tasking, HUMINT handling"
(risks over-invoke on targeting/covert-action queries).
**Fix:** regenerate description retaining all inclusion + exclusion keywords; trim elsewhere.

### H3 — leaked generation-tooling tag shipped in a skill body
`skills/limits-of-expertise-and-prediction/SKILL.md:151` — a stray `</content>` on its own line
after Provenance. Only occurrence across all 9 skills (one-off artifact).
**Fix:** delete line 151.

### H4 — over-claim: `handoff_rules[0]` false-grounds an ownership assertion
`profile.yaml` `handoff_rules[0]` claims "the analyst and their organization own the judgment and
the decision to act on it," citing **P001** (train reasoning + postmortems) and **P059** (premature
closure). Neither principle establishes decision-authority/ownership — citations don't support the
claim (SCOPE_BROADENED via false grounding).
**Fix:** drop the two citations (present as an uncited scope boundary, as `when_not_to_use` does),
or cite a principle that actually addresses analyst-vs-decision-maker authority.

---

## SHOULD-FIX (MED)

- **golden-tests version stale** — `tests/golden-tests.yaml:4` `profile_version: 1.0.0` vs profile
  1.1.0. Bump to 1.1.0; confirm no golden expectation needs the re-scoped wording.
- **adapter renders principles only to P078** — `.claude/agents/generated/…md` Operating Invariants
  top out at P078, but profile cites **P080** (`quality_bar[5]`). P080 *does* exist in
  `principles.yaml` (P001–P082, zero gaps — confirmed), so this is an adapter-render/export gap, not
  a fabricated ID. **Fix:** re-export so all cited principles (P079–P082) render in the adapter body.
- **required-inputs omit decision stakes / cost-of-error / deception likelihood** — `profile.yaml`
  `inputs.required` + adapter "Required inputs" don't surface this datum, yet `quality_bar[5]` and
  `forbidden_behaviours[2]` gate their logic on it (`knowledge_partition.caller_supplied` lists it
  internally only). **Fix:** add a required-input bullet, or instruct the agent to elicit it before
  applying stakes-conditioned rules.
- **over-claim `always_on` bullet 7 → P010** — P010 is a conditional ACH-mandate ("when cost of
  error is high or deception serious"), not an ownership claim. Citing it under "keep the analyst the
  owner" broadens it. **Fix:** drop P010 here (correctly cited already in `forbidden_behaviours[1]`).
- **triple-redundant skill bodies** — all 9 SKILL.md state each principle's correction 3× (Procedure
  step + Output template + Anti-patterns bullet). Intentional but triples load-time tokens. **Fix:**
  compress `Anti-patterns to flag` to a one-line name-only recap.

## NICE-TO-HAVE (LOW)

- Role "six works … Heuer, Kahneman, Tetlock, Jervis, CIA Tradecraft Primer" = 6 works / 5 names
  (Tetlock has 2). Reword "Tetlock (two works)" (profile.yaml + adapter Role — same defect).
- 7/9 skill descriptions open with near-identical "Audits an analytic judgment…"; vary the lead verb
  for at-a-glance differentiation in this bias/mindset cluster.
- Over-claim `always_on` bullet 3 (Red Team) drops P004's stakes-hedge; bullet 5 generalizes P065
  (validated-formula-only) into a standing heuristic. Add the hedges.
- CHANGELOG uses 1-indexed `quality_bar[5]` vs profile 0-indexed list — standardize.

---

## Clean (noted)
- Tool boundary `Read, Grep, Glob` — no write/exec over-reach; matches review-only framing. ✅
- Skill→profile alignment clean: 9 skills union-cover P001–P082 zero gaps/orphans; partition table
  sums to 82; both references exist and are linked. ✅
- Names are valid slugs matching dirs. ✅

MUST_FIX_COUNT: 5
