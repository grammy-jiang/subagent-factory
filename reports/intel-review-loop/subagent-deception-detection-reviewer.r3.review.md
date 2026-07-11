# Review Loop r3 — deception-detection-reviewer

Package: `subagents/deception-detection-reviewer/`
Pass: single review (REVIEW ONLY, no edits)
Date: 2026-07-11

## Bash gate — PASS (no must-fix from gate)

- `validate_generated_package` → **VALIDATION PASSED** (only non-fatal `phase8` self-check WARNING).
- `quote_scan` → **PASS** — no potential verbatim quotation.

## Reviewers run (parallel, each own scope)

| Reviewer | Scope | must-fix |
|---|---|---|
| agent-skills-advisor | skills/*/SKILL.md + profile routing | 1 |
| profile-reviewer | profile.yaml + provenance-ledger.md | 0 |
| faithfulness-reviewer | profile rules vs principles.yaml | 1 |
| ai-agent-engineering-reviewer | adapter + profile (agent-design) | 1 |

---

## MUST-FIX (CRITICAL + HIGH), severe-first

### H1 — Invariants written in operator voice can override the reviewer-only restriction (authority-escalation path)
`.claude/agents/generated/deception-detection-reviewer.md:21-24` vs `:26-156`; mirrored `profile.yaml:118-129` forbidden_behaviours + `:153-231` knowledge_partition.
Precedence rule (line 23) says operating invariants outrank the "softer guidance below; do not override them" — but many invariants are first-person operational imperatives (P001 "Stage a controlled act of sabotage…" :26; P015 "Confirm that you control an entire enemy network…" :54; P018 steer investigation/press :60; P041 "Build a planted deception carried by a corpse…" :106), while the "no operational plan against a real-world target" restriction lives textually BELOW in forbidden_behaviours = the "softer guidance" the invariants are declared to outrank. Caller can invoke "apply P001/P041" and the doc's own precedence favors the operator-voice invariant over the reviewer-only boundary.
Fix: reframe every invariant in review-criteria voice ("Check whether the plan does/avoids X…", not "Do X"), OR explicitly except forbidden_behaviours + the "does not run the operation" role clause from invariant precedence. Requires profile.yaml edit → re-export adapter → version bump + changelog.

### H2 — `always_on[3]` / P004 over-claim (SCOPE_BROADENED) — stronger than source
`profile.yaml` knowledge_partition.always_on[3]: "read a handler's deep personal investment as the strongest guarantor of the case" (cites P004).
P004 carries explicit `applies_when: ["the enemy service is trusted by its own high command"]`. Masterman's point holds ONLY when the handler's superiors credit him, not universally. Profile drops the condition → presents unconditional guidance, contradicting the same bullet's own header ("assess belief on evidence, never assumption"). NOT already in faithfulness-report.yaml.
Fix: restore the condition — "…strongest guarantor of the case *where the enemy service itself credits that handler internally*."

### H3 — governance-approval skill bundles unauthorized self-audit scope
`subagents/deception-detection-reviewer/skills/governance-approval-and-organization/SKILL.md:3-7` + Procedure steps 2-5,8,10-11 (lines 89-90,94-95,98-100,105-106,116-117,121-126).
Skill fuses two review objects: (a) auditing the *case's* governance evidence (in scope) AND (b) auditing "the reviewing team's own governance hygiene," case policy, approval routing, personal integrity — not authorized in profile.yaml role/when_to_use/outputs.modes/forbidden/handoff (which hand policy/legal/process to "the owning specialist"). Unilateral scope expansion invented at skill layer; no sibling skill self-audits the review team.
Fix: split self-audit content into an optional appendix (or drop) and keep skill scoped to the evidence-chain-under-review's governance/approval machinery, matching the other 7 skills' single-direction framing.

---

## Should-fix (MEDIUM)

### M1 — P042 citation mismatch on the most safety-critical rule
`adapter:237` vs `:108` (mirror `profile.yaml:129` vs `:203`). Forbidden "Producing an operational plan to harm/sabotage/deceive a specific real-world target" cites **(P042)**, but P042 is actually the personal-integrity principle — unrelated. The load-bearing scope boundary is anchored to the wrong principle ID, breaking the "traceable to source principle" guarantee for the rule that matters most.
Fix: correct citation to the principle that truly grounds the no-real-world-attack-plan rule (verify against full index), or restate without an anchor if none supports it. (Related to faithfulness L3 below — same P042 over-attribution family.)

### M2 — golden-tests.yaml profile_version stale
`tests/golden-tests.yaml:4` `profile_version: 1.0.0` vs `profile.yaml:5` `agent_version: "1.0.2"`. CHANGELOG, provenance Version History, adapter header all correctly 1.0.2; only test metadata lagged after R1/R2.
Fix: bump to 1.0.2, re-verify golden prompts still exercise R2-adjusted wording (P035/P063 hedges).

### M3 — profile body ~986 words, ~14 below the 1000-word FAIL line (phase8 WARNING is real)
`profile.yaml` body. Both R1/R2 rounds ADDED text (new quality_bar bullet :109-112, new precedence clause :146-151) with nothing trimmed. quality_bar alone ≈214 words / 6 bullets vs checker's "expect 3-5". One more remediation round of this shape tips WARNING→FAIL and blocks export.
Fix: consolidate/shorten densest sections (merge 2 of 6 quality_bar bullets; shorten precedence) to rebuild headroom under 800 words BEFORE next remediation touches this profile.

### M4 — governance skill trigger is dead-weight routing text
`governance-approval-and-organization/SKILL.md:7` — "when a reviewer is hesitating to raise an unwelcome deduction" is introspective; a caller prompt won't phrase it so. Doesn't function as a routing signal.
Fix: remove from frontmatter description; keep in body "When to use" only if at all.

### M5 — governance step 7 overlaps strategic-stewardship skill, no frontmatter routing signal
`governance-.../SKILL.md:110-113` (P027 husband-for-long-game) vs `strategic-stewardship-and-timing/SKILL.md` (P052/P040/P053/P083/P093). Disambiguated only in References footer, not in either description → "spend now or hold" query has no routing signal.
Fix: add clause narrowing governance P027 to approval-level spend, or move P027 into strategic-stewardship.

---

## Nits (LOW) — optional owner cleanup

- **L1** `always_on[0]` cites P001 (staged sabotage) — belongs to always_on[6] physical-craft bullet, not "turn/run controlled agent." Stray citation; drop it (P055 already covers infiltrator-turn). (faithfulness)
- **L2** `quality_bar[5]` cites (P037,P041,P044,P046,P081) but P037/P044/P046 don't support the three clauses; "staged sabotage" clause is grounded by **P018** (uncited here, correct in always_on[6]). Replace P037/P044/P046 with P018 or trim clauses. (faithfulness)
- **L3** `handoff_rules[1]` cites (P016,P042); neither grounds "hand off collection plumbing to owning specialist" — inferred policy overlay mislabeled as principle-grounded. Mark policy-derived or drop the "collection plumbing" example. (faithfulness; see M1)
- **L4** `physical-and-technical-deception-craft/SKILL.md:3-10` description enumerates 7 trigger objects — front-load single unifying trigger ("physical/technical evidence behind a plant"), move list to body. (skills)
- **L5** `assessing-enemy-trust-and-belief/SKILL.md:3-10` description = 560-char run-on; trim to primary + one disambiguating clause vs counter-deception-and-the-mirror. (skills)
- **L6** all 8 SKILL.md — "Anti-patterns to flag" is near-complete negative restatement of "Procedure"; consider collapsing to compact table for shorter skills. (skills)
- **L7** `adapter:3` frontmatter routing description grammatically truncated ("…history of Britain's WWII — Use when…" drops "double-agent system"). Restore full noun phrase. (agent-design)

## Positives (no fix)
- Tool boundary exactly `Read, Grep, Glob`; `mcp: []`, `caller_supplied: []` — no capability grant. Scope-discipline denials present in role/when_not_to_use/forbidden/handoff; both worked examples correctly decline operational asks and hand decision to case owner.
- All 94 principle IDs cited across profile resolve to real principle_ids (P001-P094 spot-checked) — no orphan citations.
- Frontmatter third-person + valid on all 8 skills; uniform actionable body structure; trust-vs-mirror split explicitly disambiguated bidirectionally; all reference links resolve.

MUST_FIX_COUNT: 3
