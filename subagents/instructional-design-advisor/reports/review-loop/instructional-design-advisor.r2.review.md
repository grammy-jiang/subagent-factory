# Review — instructional-design-advisor (round 2)

Package: `subagents/instructional-design-advisor/` (agent_version 1.4.0)
Mode: review only — no package file edited by this pass except this report.
Lenses: deterministic gates + agent-skills-advisor, profile-reviewer, faithfulness-reviewer,
ai-agent-engineering-reviewer (run in parallel, each given only its scope).

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — all checks OK, 0 FAIL |
| `quote_scan` | **PASS** — no potential verbatim quotation |
| truncation gate — `…` ellipsis in skill bodies / adapter | **PASS** — 0 hits |
| truncation gate — adapter invariant severed inside a parenthetical | **PASS** — 0 hits |

Deterministic FAILs: **0**. One gate reports informationally,
`phase8: Phase 8 self-check WARNING`, emitted as `[OK]` rather than a FAIL — see S-1.

## Reviewer panel

| Lens | Scope | must-fix |
|------|-------|----------|
| agent-skills-advisor | 13 `skills/*/SKILL.md` + profile as charter | 0 |
| profile-reviewer | `profile.yaml`, `provenance-ledger.md` | 0 |
| faithfulness-reviewer | profile rules vs `principles/principles.yaml` + prior report | 0 |
| ai-agent-engineering-reviewer | installed adapter + profile | 0 |

Positive verifications worth recording — each independently re-derived this round, not taken
on trust from the prior report:

- **Principle partition is clean.** All 200 principle IDs P001–P200 appear in exactly one
  skill's provenance block, and the partition matches `profile.yaml`'s
  `knowledge_partition.skills` exactly.
- **No sibling routing** in `profile.yaml`, `when_not_to_use`, or the adapter — every referral
  names a human role (teacher of record, institution, accrediting body, qualified content
  expert). Complies with the standing subagent-independence rule.
- **Tool boundary holds.** Adapter frontmatter grants `Read, Grep, Glob` only; nothing in the
  role, invariants, modes, quality bar, or worked examples implies write/edit/execute/network
  action by the agent. Imperative worked-example language ("rewrite the unit outcome...") is
  advice addressed to the caller, and both examples close with an explicit ownership statement.
- **Hedges intact.** The load-bearing conditionals survive into the profile unweakened: P153
  ("retention evidence *alone*"), P163 ("*solely* from prior attainment"), P157 ("*in a
  system-paced presentation*"), P165's conditional trigger, P006, P196, P056. No invented
  thresholds leaked — P155's "75 percent more time" and P038's "five to seven chunks" stay in
  the principle layer and are not asserted in the profile.
- **Ledger consistent with the file.** Every citation change the ledger claims for 1.2.0–1.4.0
  matches the current `profile.yaml` text byte-for-byte; supersession is explicit, not silent.
- **Adapter hygiene.** `<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->` at line 8; description
  matches `router_description`; no dangling or truncated invariant lines.

## Findings — most severe first

### must-fix

None.

### should-fix

**S-1 | `profile.yaml` (body) — Phase 8 body-size margin is thin**
Problem: profile body is 935 words against a soft budget of 800 and a hard FAIL at 1000; this is
the source of the `phase8` WARNING. It is a documented, accepted release state
(`provenance-ledger.md:245-257`), but the 65-word margin means the next added citation or clause
hard-fails validation, and the ledger itself records that the "remaining weight is irreducible
without dropping grounded content".
Fix: not a release blocker. Before the next content edit, restructure the body (compress prose,
not citations) to recover margin, rather than trimming reactively at FAIL time.

**S-2 | `profile.yaml:77-78` + `.claude/agents/generated/instructional-design-advisor.md:208-227` — `minimum_useful_output` never reaches the model**
Problem: the canonical profile declares an output floor ("At least one finding that names an
instructional-design practice, its principle, and the residual trade-off or referral to make").
The shared adapter template has no slot for it, so the deployed agent has no floor to self-check
against at runtime. Raised independently by the profile and agent-design lenses.
Fix: render `minimum_useful_output` into the adapter's "Supported modes and outputs" section via
the shared template. **Factory-level template gap, not a package defect** — check whether sibling
adapters drop it too and fix once upstream.

**S-3 | all 13 `skills/*/SKILL.md:3-5` (`description:`) — no triggering-time boundary clause**
Problem: no skill description carries a non-trigger clause, though `forbidden_behaviours`
(`profile.yaml:79-92`) hard-stops "build the deliverable", "grade learners", and "certify
effectiveness". "Build me a rubric for X" reads as a clean on-trigger match for
`assessment-design-and-authentic-tasks` ("Designs and reviews authentic assessment tasks,
rubrics..."). The disambiguation lives only in the body's `Output` section — read *after* load,
so it cannot do triggering-time work.
Fix: append a short boundary clause to the most exposed descriptions — at minimum
`assessment-design-and-authentic-tasks`, `multimedia-and-elearning-design`,
`active-learning-and-group-formats`, `iterative-prototyping-and-development` — e.g.
"(reviews and guides; does not author the artefact itself)".

**S-4 | ~8 of 13 `skills/*/SKILL.md` — mixed British/American spelling**
Problem: `organise/organize`, `recognise/recognize`, `prioritise/prioritize` mixed, sometimes
within one file — `backward-design-and-constructive-alignment/SKILL.md:5` "prioritizing" vs `:75`
"prioritise"; `needs-and-context-analysis/SKILL.md:65,67,68` "organizational" vs `:73,89`
"organisational". Cosmetic, but it breaks an otherwise uniform authored voice.
Fix: normalise to one variant (the corpus leans American) in a single pass across all 13 files.

**S-5 | `provenance-ledger.md:13-26` — structural-policy carve-out documented in the wrong place**
Problem: two profile clauses (the "final authority... rests with the teacher of record and the
institution" sentence in `canonical_owner`, and the advisor-boundary half of
`forbidden_behaviours[0]`) are declared an intentional uncited carve-out from the "No orphan
field values" hard rule in `.claude/rules/rights-and-quotation-policy.md`. The reasoning is sound
— these are authority/ownership statements, not instructional-design claims, and two prior
versions tried and rejected fabricated citations for them — but the exception is declared only in
*this package's* ledger, not in the rule it exempts itself from.
Fix: promote the carve-out into `.claude/rules/rights-and-quotation-policy.md` (or
`evidence-protocol.md`) as a named exception category, so the next package hitting this tension
need not re-derive its legitimacy. Repo-level, not package-level.

### nice

**N-1 | `profile.yaml` `examples[0].ideal_response`, clause (3) — HEDGING_REMOVED in example prose**
Asserts "A multiple-choice quiz *cannot* show understanding". P067 states the weaker claim:
expect evidence of understanding to be "less direct and more complicated" than objective-test
evidence, and a right answer "can" come from rote recall, test-taking skill, or a lucky guess.
The source never says a multiple-choice test *cannot* show understanding.
Not must-fix: illustrative example prose, not a `quality_bar`, `forbidden_behaviours`,
`always_on`, or mode-trigger rule. Still worth fixing — it is exactly the over-claim the
package's own `forbidden_behaviours[2]` forbids.
Fix: "A multiple-choice quiz is weak evidence of understanding — a right answer can come from
rote recall, test-taking skill, or a lucky guess (P067)."

**N-2 | `skills/instructional-strategy-and-events/SKILL.md` — partition imbalance (35 principles)**
More than double the next-largest skill (35 vs 19). Mitigated by internal `###` subsections and
specific `When to use` bullets; already scoped as a deferred split at
`provenance-ledger.md:279-283`. Raised by both the skills and profile lenses.
Fix: if it over-triggers or under-scans in practice, split along the existing subsection
boundaries (sequencing / nine-events vs outcome-type technique matching + scaffolding).

**N-3 | `profile.yaml:45-47` (`outputs.primary_format`) vs adapter**
The "never a bare good/bad verdict" constraint is not rendered as one consolidated adapter
statement, though each of the three modes restates an equivalent clause (adapter lines 214, 220,
226). Coverage is functionally present. Same template root cause as S-2.
Fix: render one top-level anti-verdict statement so the constraint survives a skim that skips a
mode block.

**N-4 | `.claude/agents/generated/instructional-design-advisor.md:26-174` — invariants block size**
62 short imperative bullets with no grouping or priority ordering inside the block (grouping
exists one level up, in the skill files). Large single system-prompt segment, but the three-mode
structure and Quality Bar give the model a usable frame, and the pattern matches already-shipped
sibling packages — not a novel defect.
Fix: none required now; revisit if the block grows.

**N-5 | all 13 `skills/*/SKILL.md` — ~80 words of byte-identical `Inputs`/`Output` boilerplate**
Duplicated across 13 files. Not a context-budget problem (one skill loads at a time), but a
future wording change means 13 hand edits.
Fix: optional — factor into the shared reference with a pointer, or accept as a deliberate
self-containment trade-off (each skill stays independently readable).

## Verdict

Release-ready. Zero deterministic FAILs, zero must-fix across four independent lenses. Of the
five should-fix items, **two (S-2, S-5) are factory/repo-level rather than package defects**, and
one (S-1) is an accepted-and-documented state that constrains the *next* edit rather than this
release.

MUST_FIX_COUNT: 0
