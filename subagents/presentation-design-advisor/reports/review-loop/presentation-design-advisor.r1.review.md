# Review — presentation-design-advisor (round r1)

Package: `subagents/presentation-design-advisor/` @ `agent_version: 1.2.1`
Date: 2026-07-27
Mode: review only — no files changed except this report.

## 1. Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASSED** — 0 FAIL, 1 WARN |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| Truncation gate: `…` ellipsis in skill bodies / adapter | clean — 0 hits |
| Truncation gate: adapter invariant severed inside a parenthetical | clean — 0 hits |

Deterministic FAILs: **0**.

Two non-FAIL signals carried forward as findings below:

- `[WARN] quote-scan: rights NOT verified — 3 restricted source(s) but no source text available (no sources/markdown/, no warm cache module); verbatim-quote gate could not run`
- `[OK  ] phase8: Phase 8 self-check WARNING`

## 2. Reviewer panel

Four lenses run in parallel, each scoped to its own surface:

| Lens | Surface | MUST_FIX |
|------|---------|----------|
| agent-skills-advisor | `skills/*/SKILL.md` (14) | 0 |
| profile-reviewer | `profile.yaml`, `provenance-ledger.md` | 1 |
| faithfulness-reviewer | profile rules vs `principles/principles.yaml` | 1 |
| ai-agent-engineering-reviewer | exported adapter + profile (agent design) | 0 |

## 3. Consolidated findings — most severe first

### F1 — must-fix — over-claim: Duarte persuasive narrative arc stated as universal planning law

- **where** `profile.yaml:178-192` (`knowledge_partition.always_on[4]`, story-structure paragraph); also rendered into `.claude/agents/generated/presentation-design-advisor.md`
- **lens** faithfulness (SCOPE_BROADENED)
- **problem** The paragraph asserts the *Resonate* arc unconditionally — "It opens by stating what is… it makes the turning point an explicit, memorable call to adventure… and it lands the ending on a higher plane than the beginning." Each of the three principles carrying that arc is scoped by the source to a persuasive / change-seeking talk:
  - P087 `applies_when: the presenter is about to propose something new`
  - P059 `applies_when: writing the final movement of a persuasive presentation`
  - P116 `applies_when: the audience must be moved from complacency into wanting a different reality`

  All three conditions are dropped. The paragraph is always-on for any "planning from scratch" task (`when_to_use[2]`), which per `router_description` includes Alley-domain scientific-conference talks and lectures that report findings without proposing anything or needing a call to adventure. This is precisely the cross-source failure mode the package is exposed to: Duarte persuasion technique promoted to universal presentation law. `reports/faithfulness-report.yaml:381-390` audits P041's scope for this rule but is silent on P087/P059/P116 — i.e. the existing report is lenient on exactly this rule.
- **fix** Either (a) restore the condition — "where the talk proposes something new or seeks a decision, it opens by stating what is… and lands the ending on a higher plane"; or (b) split the paragraph so the genuinely general big-idea/ideation content (P005, P035, P060, P118) stays unconditional and the narrative-arc content (P087, P059, P116) is explicitly scoped to persuasive / change-seeking talks. Then update the `knowledge_partition.always_on[4]` entry in `reports/faithfulness-report.yaml`, bump `agent_version`, re-export the adapter, re-validate.

### F2 — must-fix — `status: ready` declared over a self-check gap the ledger itself records as open

- **where** `provenance-ledger.md:71-75` (1.2.1 entry) vs `profile.yaml:5` (`status: ready`); corresponds to the validator's `phase8: Phase 8 self-check WARNING`
- **lens** profile / release-readiness
- **problem** The ledger's own 1.2.1 entry records an unresolved process finding: the authored `reports/faithfulness-report.yaml` audits `profile.yaml` fields only — **zero entries cover `knowledge_partition.skills` or any `SKILL.md` body** — "which is why (b) and (c) survived a `must-fix = 0` verdict. The faithfulness surface should extend to skill bodies." That is the coverage hole behind the Phase 8 WARNING: 14 skill bodies carry inline `## Procedure` citations but their prose and anti-pattern text is unaudited. Two round-1 self-check defects escaped and were only caught by the next cycle — direct evidence the surface is insufficient *today*, not hypothetically. The package was nonetheless versioned forward 1.2.0→1.2.1 with `status: ready`, and the gap is written as a changelog note that reads closed but is not. F1 above is a live instance of what this hole misses.
- **fix** Either (a) extend `reports/faithfulness-report.yaml` to cover every `SKILL.md` body and re-run Phase 8 before shipping this version; or (b) if deferring is deliberate, drop `status: ready` for an explicit provisional status and raise a tracked follow-up rather than a changelog note.

### F3 — should-fix — `P031` cited in the adapter but never defined in it

- **where** `.claude/agents/generated/presentation-design-advisor.md:357` (Handoff rules, "(P009, P031)"); source `profile.yaml:107`
- **lens** agent design
- **problem** The adapter's Operating Invariants section is the one place that spells out principle text, and it claims each invariant is "traceable to its source principle" — but it jumps P030 → P032, so P031 is never defined in the document, while being cited in the handoff bullet on channel choice. P009's text supports the "change the format" half; the second citation is unresolvable from the adapter alone. Verified: P031 **does** exist in `principles/principles.yaml:564` and is legitimately cited at `profile.yaml:311`, so this is a rendering/selection gap in the must-hold invariant tier, not a dangling ID — it degrades the traceability guarantee the invariants section makes about itself. All other three-digit citations spot-checked (P062, P100–P120) resolve.
- **fix** Add P031's statement to the Operating Invariants tier so the citation resolves within the adapter, or drop the citation from the handoff bullet if P031 was deliberately excluded from must-hold. Fix in `profile.yaml` and re-export — never edit the adapter.

### F4 — should-fix — `quality_bar[8]` is an ungrounded orphan field

- **where** `profile.yaml:86-87` ("Nothing falls below the output floor…") vs `provenance-ledger.md:18-26` (field-grounding table)
- **lens** profile / provenance
- **problem** Every other uncited profile field is either tagged inline `(authored boundary; no source principle states it)` (see `forbidden_behaviours[0]` at :91-92, `[2]` at :95-96, `handoff_rules[0]` at :103-105) or named in the ledger's grounding table (e.g. `outputs.primary_format`, `minimum_useful_output` at ledger:24). `quality_bar[8]` has neither: no `(Pxxx)`, no authored tag, and no `quality_bar` row in the grounding table — despite the 1.2.0 entry (ledger:93-94) explaining it was added deliberately as an authored floor duplicating `minimum_useful_output`. Orphan field value under the provenance requirement.
- **fix** Tag it inline `(authored output floor; no source principle states it)` and add a one-line `quality_bar` row to the ledger table cross-referencing `minimum_useful_output`.

### F5 — should-fix — verbatim-quote gate could not run (rights not verified)

- **where** validator WARN; `sources/markdown/` absent by design (3 `distillation-only` sources, rights-clean export)
- **lens** deterministic gate
- **problem** `quote_scan` returned PASS, but the validator separately warns the rights check was **not verified**: with no source text and no warm cache module, the 40+-consecutive-word verbatim gate had nothing to compare against. The standalone `quote_scan` PASS is therefore not evidence that no verbatim quotation exists — it is evidence that nothing was checked. For three `distillation-only` sources (Alley, Duarte ×2), verbatim quotation is a hard policy bar.
- **fix** Re-run `quote_scan` once against a warm MAP cache or a temporarily restored `sources/markdown/`, record the verified result in `reports/`, and cite it at release. If a rights-clean export permanently precludes this, record the last verified-clean run's version so the WARN is explicitly accounted for rather than silently carried.

### F6 — nice — `when_to_use[5]` drops the live-presentation anchor

- **where** `profile.yaml:33` / adapter `:267` — "Judging whether a persuasive case covers evidence, emotion, and speaker credibility for its audience."
- **lens** agent design (routing)
- **problem** Every other `when_to_use` bullet is anchored to a talk / deck / slide / delivery context, and `when_not_to_use` explicitly excludes "a written document … with no live-presentation dimension." Bullet 5 alone reads as generic persuasion review (essay, ad, memo), a small misrouting risk against the package's own stated exclusion.
- **fix** "Judging whether a persuasive **talk or pitch** covers evidence, emotion, and speaker credibility for its audience."

### F7 — nice — same condition-dropping in the persuasion paragraph

- **where** `profile.yaml:212-229` (`knowledge_partition.always_on[6]`)
- **lens** faithfulness (SCOPE_BROADENED, low risk)
- **problem** Same pattern as F1 — "It engineers contrast…", "builds the character appeal deliberately…", "builds common ground…" stated unconditionally, while P040 / P092 / P115 each carry an `applies_when`. Lower risk because this paragraph only fires inside the persuasion skill, where the conditions are near-always satisfied.
- **fix** Optional consistency tightening once F1 is fixed — restate each clause with its source condition.

### F8 — nice — `quality_bar[2]` citation incomplete on "bold type"

- **where** `profile.yaml:73-75`
- **lens** faithfulness (citation completeness, not a strength violation)
- **problem** Cites (P007, P098, P099, P011, P004), but the bullet's "bold type" is grounded in P049 (boldface for larger rooms), which is not in this bar's citation list. P049 is correctly cited elsewhere at `knowledge_partition.always_on[3]`.
- **fix** Add P049 to the citation list, or drop "bold" from the compressed bullet and leave it to the typography paragraph.

### F9 — nice — adjacent skills lack mutual disambiguation

- **where** `skills/audience-analysis-and-persona-design/SKILL.md:59-61` and `skills/persuasion-ethos-pathos-and-logos/SKILL.md:49-52`
- **lens** skill authoring
- **problem** Both cover "tuning emotional appeal to the audience" from adjacent angles. Principle ownership is clean (no ID overlap), but neither description nor "When to use" cross-references the other — unlike the rehearsal / in-room-delivery / questions-challenge triad, which disambiguates itself well. A caller diagnosing "the pitch didn't land emotionally" gets no signal which to open first, and the profile's own worked example draws on both.
- **fix** Add a one-line pointer in each "When to use", mirroring the existing triad pattern.

### F10 — nice — three meta-level skills lack an explicit trigger clause

- **where** `skills/story-structure-and-the-big-idea/`, `skills/format-choice-and-preparation-planning/`, `skills/talk-organisation-transitions-and-emphasis/` — frontmatter `description`
- **lens** skill authoring
- **problem** Descriptions are imperative capability statements rather than trigger-oriented. Most skills compensate with concrete domain nouns ("typeface", "palette", "sticky-note story order") that should still fire; the three meta-level skills have no such anchor and no "Use when…" symptom clause.
- **fix** Append an explicit symptom trigger, e.g. for `talk-organisation-transitions-and-emphasis`: "Use when a talk feels shapeless, loses the audience mid-way, or key details aren't landing despite sound content."

### F11 — nice — "Not owned by a skill" section breaks index reading order

- **where** `references/presentation-design-principles-index.md:332-337`
- **lens** skill authoring
- **problem** The P036 / P048 section sits mid-document between two skill sections, interrupting the skill-by-skill order the 14 SKILL.md cross-references imply.
- **fix** Move it to the end of the index.

### F12 — nice — boundary sentence duplicated verbatim across 14 skill Output sections

- **where** all `skills/*/SKILL.md` "## Output" (e.g. `assertion-evidence-slide-structure/SKILL.md:77-79`)
- **lens** skill authoring
- **problem** The advice-only boundary sentence is copy-pasted into all 14 files. No load-time cost (only the matched skill loads), but a DRY liability: a future edit to the profile's `forbidden_behaviours` wording must be propagated to all 14 or they drift from canonical language.
- **fix** No functional change now; note the propagation requirement for maintainers.

## 4. What checked out (no finding)

- All 14 skills: frontmatter `provenance.principles` matches exactly the IDs cited in each body's Procedure and Anti-patterns. 118 skill-owned principles partition with **zero duplicate IDs**; P036/P048 documented as unowned. Bodies 79–174 lines, well within budget. All relative links to `references/` resolve.
- Adapter frontmatter well-formed; `tools: Read, Grep, Glob`; description byte-identical to `router_description`; DO-NOT-EDIT header present in first 20 lines naming source profile and version 1.2.1, matching `agent_version`.
- Tool boundary respected: every agent-directed instruction maps to Read/Grep/Glob; all write/build/produce/deliver verbs are either explicitly forbidden behaviours or domain content describing what the *presenter* does.
- **Subagent-independence rule holds** — no "route to `<other>-advisor`" text anywhere; out-of-scope is stated by capability. The two adjacent phrases ("your methods reviewer rules on whether the claim is true") are boundary statements about who is not this agent, not delegation.
- No authority creep: forbidden behaviours bar certifying results, guaranteeing outcomes, and prescribing one correct delivery style; worked examples reinforce it in practice.
- Version consistency: `profile.yaml:4` 1.2.1 matches ledger top entry (:55); three prior entries with explicit supersession reasoning — supersession rule satisfied.
- Ledger field-grounding table covers every uncited profile field except `quality_bar[8]` (F4).
- Not verified this pass (out of every lens's read scope): `CHANGELOG.md` has a matching 1.2.1 entry per `generated-artifact-policy.md` rule 5. The release owner should confirm separately.

## 5. Tally

- Deterministic FAILs: 0
- LLM must-fix (deduped): 2 — F1 (faithfulness), F2 (profile / Phase 8)
- should-fix: 3 — F3, F4, F5
- nice: 7 — F6–F12

F1 and F2 are related but distinct and both must be closed: F2 is the missing audit surface, F1 is a live over-claim that surface would have caught.

MUST_FIX_COUNT: 2
