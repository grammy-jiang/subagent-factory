# research-writing-advisor — Review Loop Round 3

Package: `subagents/research-writing-advisor/` (profile v1.2.0)
Review-only pass. Deterministic gates + 4 reviewer lenses (skill-authoring, profile
release-readiness, faithfulness over-claim, agent-design). Findings deduped across lenses,
most-severe first.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL) |
| `quote_scan` | **PASS** — no potential verbatim quotation |
| truncation grep (`…` ellipsis) | clean |
| adapter invariant severed-parenthetical grep | clean |

Injection scan emits 9 `WARN` on `sources/markdown/*` — all benign frozen writing-textbook prose
("You are now ready to begin building a model of…") and reversed/base-normalized false positives
on `english-writing-rese-*`. Known, triage-only, not a FAIL. No action.

**Deterministic FAILs: 0.**

---

## MUST-FIX

### MF1 — `forbidden_behaviours[3]` / `handoff_rules[1]` / `source_of_truth_policy.canonical_owner`: P140 over-claim (invented authority chain + citation stretched to a claim it never grounds)

- **Where:** `profile.yaml:84-86` (`forbidden_behaviours[3]`), echoed at `:94-96`
  (`handoff_rules[1]`) and `:98-102` (`canonical_owner`).
- **Lens:** faithfulness (must-fix). Profile reviewer independently touched the same `(P140)` note
  (its NICE #5) as reading awkwardly.
- **Problem:** P140 (`principles.yaml:4167-4170`) states only: *"Assess both legal rights and
  academic ethics when owning or reusing intellectual creations…"* — its underlying claims
  (C01312, C02016–C02018) frame this as the **author's own** responsibility (assess, credit, check
  self-reuse limits). No principle or claim in the 172-principle corpus establishes an external
  authority chain; a corpus grep for "counsel"/"institution" in an authority sense returned nothing.
  The profile turns *"you (the author) must personally assess this"* into *"this belongs to counsel
  and the institution, and the advisor routes it there"* — a **SCOPE_BROADENED** invention of
  institutional authority, sitting inside a hard boundary (`forbidden_behaviours`) and a handoff
  rule. Separately, the same bullet's *"domain-science correctness … belongs to the researcher and
  domain experts"* clause also cites only `(P140)`, but P140 says nothing about domain-science
  correctness (zero corpus hits) — one citation stretched to ground two distinct claims, neither
  fully supported.
- **Fix:** Reword to what P140 grounds — the advisor does not itself assess/assert
  legal-rights/plagiarism status and prompts the *author* to make that assessment (P140's own
  framing). If the "counsel/institution" routing is wanted as a product-safety default, mark it as
  an explicit engineering/editorial boundary decision, **not** a source-grounded P140 citation. Drop
  the P140 citation from the domain-science-correctness clause, or cite an actual grounding
  principle (none found).

---

## SHOULD-FIX

### SF1 — `handoff_rules[0]` / `canonical_owner`: P080 stretched to ground broad ownership claim

- **Where:** `profile.yaml:91-93` and `:98-102`.
- **Lens:** faithfulness (should-fix).
- **Problem:** P080 (`principles.yaml:2960-2966`) is specifically about **English-correctness
  responsibility** and story-over-grammar priority ("hire an editor for language but not a scientist
  for your science"). It does not cover data ownership, claim-decision authority, or submission
  timing. The faithfulness report itself notes structural P022 was dropped in 1.1.0, leaving one
  narrow principle to carry "own the manuscript, the data, and the substance … what to claim and
  when to submit." SCOPE_BROADENED.
- **Fix:** Narrow wording to what P080 supports (author responsible for correct English / final
  story-language decisions), or cite an actual principle establishing data-ownership and
  submission-timing authority before keeping the broader phrasing.

### SF2 — Adapter drops authored guardrail text: `outputs.primary_format` + `minimum_useful_output` never rendered

- **Where:** `profile.yaml:44-47` (`primary_format`) and `:75-76` (`minimum_useful_output`) vs
  exported adapter "Supported modes and outputs" (`.claude/agents/generated/research-writing-advisor.md:158-177`).
- **Lens:** agent-design (should-fix). **Factory-template gap, not package-unique** — affects every
  generated adapter.
- **Problem:** Profile authors `primary_format` as *"…never a bare verdict, a ghost-written
  deliverable, or a promise of acceptance"* plus a `minimum_useful_output` floor. `export_claude_agent.py`
  computes both variables (lines 350, 353) but the Claude Code Jinja2 template never references
  either, so neither reaches the deployed system prompt. Core ghostwriting/acceptance bans survive
  via `Forbidden behaviours`, but the distinct **"never a bare verdict" quality floor has no
  rendered equivalent** — a minimal, unhelpful one-line answer violates no stated runtime constraint.
- **Fix:** Extend the Claude Code adapter template to render `outputs.primary_format` (lead-in under
  "Supported modes and outputs") and fold in `minimum_useful_output`; re-export; bump `agent_version`.
  Raise as a factory-template defect (all packages affected).

### SF3 — Skill `description` fields duplicate the body `## Purpose` and bury the trigger

- **Where:** all 13 `skills/*/SKILL.md` frontmatter descriptions (systemic).
- **Lens:** skill-authoring (should-fix, combines its findings 1 & 2).
- **Problem:** Description is a near-verbatim copy of the body `## Purpose` paragraph — wastes the
  always-loaded trigger budget and blurs the frontmatter-vs-body split progressive disclosure needs.
  In 11 of 13 the "Use when…" trigger clause sits at the *end* of a 500–900-char paragraph rather
  than front-loaded (only `literature-and-source-use` and `presenting-and-public-speaking` lead with
  it).
- **Fix:** Shrink each description to 2–4 sentences leading with "Use when X, Y, Z…", then the
  what-it-checks detail; keep the fuller explanation only in `## Purpose`. Standardize one pattern
  package-wide.

### SF4 — Two skill descriptions near the 1024-char frontmatter cap

- **Where:** `paper-sections-and-organization/SKILL.md` (~29 description clauses),
  `research-argument-and-contribution/SKILL.md`.
- **Lens:** skill-authoring (should-fix). Unconfirmed exact byte count; thin margin.
- **Fix:** Run an exact char count on both before release; trim under 1024 with headroom (SF3 also
  helps).

### SF5 — Densest skills are flat ID-ordered lists, not task-phase-grouped

- **Where:** `paper-sections-and-organization` (29-item Procedure), `clarity-and-sentence-style`
  (21), `research-argument-and-contribution` / `evidence-integrity-and-claims` (19 each),
  `presenting-and-public-speaking` (15).
- **Lens:** skill-authoring (should-fix).
- **Problem:** Items ordered by principle ID, not task phase. For `paper-sections-and-organization`
  the 29 steps jump between Introduction/Abstract/Results/Discussion/Title/Methods in ID order, so
  an agent reviewing only the Introduction must scan all 29 to find the ~4 relevant ones.
- **Fix:** Add task-phase subheadings (`### Introduction`, `### Methods`, …) grouping existing items,
  or a short routing note at the top of Procedure mapping section → step numbers.

### SF6 — `router_description` has no faithfulness-report entry

- **Where:** `profile.yaml:8-11` vs `reports/faithfulness-report.yaml`.
- **Lens:** profile release-readiness (should-fix).
- **Problem:** `router_description` (the literal router-match text, verified complete/untruncated in
  both adapters) was added in 1.2.0, but the faithfulness report — extended 19→41 entries this same
  round to close coverage — carries no `rule_ref: router_description`. CHANGELOG asserts "grounded
  paraphrase, no new claim" but it's unlogged where every other load-bearing field is logged.
  (Independently checked: WITHIN_SCOPE, no new claim — needs recording, not rewording.)
- **Fix:** Add a `rule_ref: router_description` entry, verdict WITHIN_SCOPE, noting it paraphrases
  role/when_to_use/when_not_to_use with no new claim.

### SF7 — `golden-tests.yaml` `profile_version` stale (1.0.0)

- **Where:** `tests/golden-tests.yaml:4`.
- **Lens:** profile release-readiness (should-fix).
- **Problem:** Declares `profile_version: 1.0.0`; profile is at 1.2.0 across two rounds, one of
  which reworded the exact trigger GT-005 exercises (`when_to_use[4]`).
- **Fix:** Bump to `1.2.0` (or re-stamp via the test generator).

### SF8 — Profile body over 800-word advisory budget (carried, deferred)

- **Where:** profile body fields total ~950–980 words (Phase-8 check 14 WARNING).
- **Lens:** profile release-readiness (should-fix, carried). Under the 1000-word FAIL ceiling; not a
  blocker. Already tracked (CHANGELOG 1.2.0 SF6 deferred — moving the 29 grounded steps to a
  reference risks de-actionalizing them).
- **Fix:** None urgent; keep open. Overlaps SF5 (trimming/grouping the densest skill helps).

---

## NICE-TO-HAVE

- **N1** (skill-authoring #5): `research-argument-and-contribution`, `paper-sections-and-organization`,
  `narrative-structure-and-paragraphs` all cover "framing a knowledge gap as a question" but none
  cross-reference the others; a full introduction review needs all three. Add one boundary sentence
  each naming the adjacent skill(s).
- **N2** (skill-authoring #6): No positive worked example inside individual skills — only the
  profile-level 2-scenario `examples` block + per-skill Anti-patterns. Optionally add one
  before/after per skill (at least the 5 densest).
- **N3** (skill-authoring #7): A few Procedure items (e.g. `paper-sections-and-organization` step 14)
  pack 4–5 sub-instructions into one line. Split into sub-bullets.
- **N4** (agent-design #2): `review` mode's output spec doesn't itself constrain "correction" to a
  directional description vs drafted replacement prose; per-finding across a multi-finding review it
  could cumulatively reconstruct large stretches without technically breaching the "end to end"
  ghostwriting ban. The worked example (adapter:221-225) models the right restraint but is
  illustrative, not binding. Add a clause: "correction" = naming the needed change, not drafting the
  caller's replacement sentence. (Fixing SF2 helps — `primary_format`'s ban would then be visible
  next to the mode table.)
- **N5** (faithfulness #3): `faithfulness-report.yaml` `when_not_to_use[1]` note claims it "restates
  the P140 domain-science boundary" — P140 has no domain-science content; correct the note (the
  bullet itself is a legitimate uncited router-scope decision).

---

## Confirmed fixed / non-issues (from r2)

- MF1 (r2) adapter router-description truncation — **fixed**, complete in both exported and installed
  adapters.
- MF2 (r2) `canonical_owner` orphan field — **fixed** in 1.2.0 (now cites P080/P135/P140; but see MF1
  above re: the *strength* of the P140 citation).
- `role` and `inputs.required` carry no traceability record — repo-wide convention (matches career /
  descriptive-translation siblings); non-issue.

MUST_FIX_COUNT: 1
