# Review — presentation-design-advisor (round 1)

Package: `subagents/presentation-design-advisor/`
Reviewers: deterministic gates + 4 LLM lenses (skill-authoring, profile release-readiness,
faithfulness/over-claim, agent design).
Mode: **review only** — no package file was modified.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** — 0 FAIL, 1 WARN (see F6) |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| ellipsis truncation grep (`…` in skills + adapter) | no hits |
| severed-parenthetical grep (adapter invariants) | no hits |

Zero deterministic FAILs. Note: the two truncation greps are **clean but not exonerating** — the
real truncation in this package is silent (no ellipsis, closes with a `(Pxxx).` citation), so it
slips past both patterns. See F2.

## Findings

Most severe first. Deduped across lenses.

---

### F1 — Anti-pattern lists hard-capped at 7 entries, dropping up to 8 principles per skill
**Where:** `skills/*/SKILL.md`, `## Anti-patterns to flag` — 10 of 13 skills.
Worst: `rehearsal-and-extemporaneous-delivery/SKILL.md:87-93`,
`slide-density-and-signal-to-noise/SKILL.md:80-88`,
`assertion-evidence-slide-structure/SKILL.md:79-87`,
`format-choice-and-preparation-planning/SKILL.md:77-84`.
**Severity: must-fix** (confirmed deterministically)

**Problem.** Every anti-pattern section stops at exactly `min(7, N)` entries regardless of how many
principles the skill carries, while the frontmatter `provenance.principles` list is always complete.
Measured principles-vs-anti-patterns per skill:

```
rehearsal-and-extemporaneous-delivery       15 → 7   (8 dropped)
assertion-evidence-slide-structure          12 → 7   (5 dropped)
slide-density-and-signal-to-noise           12 → 7   (5 dropped)
format-choice-and-preparation-planning      11 → 7   (4 dropped)
audience-analysis-and-persona-design        10 → 7   (3 dropped)
talk-organisation-transitions-and-emphasis  10 → 7   (3 dropped)
persuasion-ethos-pathos-and-logos            9 → 7   (2 dropped)
story-structure-and-the-big-idea             9 → 7   (2 dropped)
typography-colour-and-slide-layout           9 → 7   (2 dropped)
visual-evidence-analogies-and-graphics       9 → 7   (2 dropped)
equipment-venue-and-contingency              4 → 4   ok
questions-challenge-and-composure            4 → 4   ok
opening-closing-and-framing-slides           6 → 6   ok
```

Every skill at or under 7 principles is complete; every skill over 7 is truncated to exactly 7 —
a generator cap, not an authoring judgment. Behavioural impact: `rehearsal-and-extemporaneous-delivery`
loses the anti-patterns for most of its actual delivery content (P094, P095, P105, P106, P107, P108,
P110, P111 — composure, confidence, eye contact, room control), so an agent scanning a submitted talk
against that skill's checklist cannot flag violations of over half its principles.

**Fix.** Regenerate `## Anti-patterns to flag` from the full `provenance.principles` list — one entry
per principle, no `min(7, N)` cap — matching the completeness the closing `Provenance` line already has.

---

### F2 — Procedure and anti-pattern bullets truncated mid-clause, producing ungrammatical instructions
**Where:** `skills/format-choice-and-preparation-planning/SKILL.md:57`;
`skills/persuasion-ethos-pathos-and-logos/SKILL.md:60,81`;
`skills/story-structure-and-the-big-idea/SKILL.md:59,61,75,79,80`;
`skills/slide-density-and-signal-to-noise/SKILL.md:64`;
`skills/visual-evidence-analogies-and-graphics/SKILL.md:59`;
`skills/audience-analysis-and-persona-design/SKILL.md:81`.
**Severity: must-fix** (confirmed by reading the lines)

**Problem.** Bullets are cut at a fixed character length (~230-240 chars for Procedure, ~150 for
anti-patterns) with **no ellipsis** — the text just stops and the `(Pxxx).` citation is appended, so
the line looks well-formed to a grep but is a broken sentence. Confirmed instances:

- `format-choice…:57` — "…and combining strong (P010)." — combining strong *what*?
- `persuasion…:60` — "…at every stage through careful (P113)." — through careful *what*?
- `story-structure…:59` — "…recording how the presenter felt as each (P064)."
- `story-structure…:61` — "…and everything after (P116)."
- `slide-density…:64` — "…splitting without sequencing (P073)." — drops the actual point, which the
  Purpose section states as: splitting without sequencing "does not by itself solve density".
- `visual-evidence…:59` — "…supply the background warrants without (P091)."
- `audience-analysis…:81` — "…keeping the persona slide at."
- `story-structure…:75,80` — anti-patterns for P060 / P064 end "…conveys what." / "…sketching."

This is worse than a cosmetic defect: the qualifying clause is where the substantive guidance lives,
and an agent quoting these lines to a caller emits meaningless text.

**Fix.** Regenerate Procedure/anti-pattern bodies without a character-count truncation. If a length
bound is required, cut to the nearest complete clause and *summarize* the tail rather than severing it.
Add a generator-side guard: reject any bullet whose text before the `(Pxxx)` citation does not end at a
clause boundary — the existing `…` and severed-parenthetical greps do not catch this shape.

---

### F3 — Faithfulness report never audits `knowledge_partition.always_on` (the bulk of the profile)
**Where:** `reports/faithfulness-report.yaml` (whole file) vs `profile.yaml:113-313` (`always_on`,
13 paragraphs) and `profile.yaml:333-389` (`examples`).
**Severity: must-fix** (confirmed: `grep -c 'always_on\|knowledge_partition'` → **0**)

**Problem.** The report carries `rule_ref` entries for only these keys:
`quality_bar`, `forbidden_behaviours`, `when_to_use`, `when_not_to_use`, `outputs`, `handoff_rules`,
`source_of_truth_policy`, `minimum_useful_output` — 29 rule locations, all
`WITHIN_SCOPE` / `accept_with_note`. There is **zero** coverage of `always_on` or `examples`.

`always_on` is the largest section of the profile (~2,000 words) and carries essentially every
concrete, checkable claim: numeric thresholds (28pt type, 120-140 wpm, four-item groupings,
"over twenty or thirty seconds", "within an hour"), audience-effect claims, and the one place a
principle explicitly excluded from profile-rule status still appears as an operative directive (F4).
A report that never opens the section cannot support the "faithfulness reviewed" gate it exists to
provide — it is thin relative to its own stated method ("per rule, assign a verdict").

**Fix.** Extend the report with a finding per `always_on` paragraph (and the `examples`), checking each
numeric and mechanical claim against its cited principles' exact wording *and* `applies_when`
conditions — not only the top-level quality-bar / forbidden-behaviour summaries.

---

### F4 — P048 is operative in both the profile and a skill despite `profile_rule: false`
**Where:** `profile.yaml:296-298` (`always_on`, format/prep paragraph) and
`skills/format-choice-and-preparation-planning/SKILL.md:61` (Procedure step 6), vs
`principles/principles.yaml:856-872` (`P048`).
**Severity: should-fix** — claim strength **SCOPE_BROADENED**

**Problem.** P048's own `operational_mapping.profile_rule` is `false`, and a sweep of
`principles.yaml` confirms it is the **only** principle in the file marked that way — the
principle-promotion step deliberately excluded it from profile-operative content (it is a descriptive
claim about institutional adoption timelines, not an actionable design instruction; matches the
evidence-protocol exclusion for background with no operational value). It nevertheless appears twice
as an active directive: the profile's `always_on` says the skill "plans for slow institutional
adoption of a better slide structure… (P048)", and the skill's Procedure step 6 reads
"Plan for slow adoption of a better slide structure (P048)." This re-admits a principle past its own
metadata gate — exactly the leak F3's blind spot would have to catch.

**Fix.** Drop the P048 citation from both loci, or restate it as descriptive context rather than an
operative "plan for…" instruction. Then add a generator/validator check that no `profile_rule: false`
principle is cited by a profile rule or skill Procedure step.

---

### F5 — Governance clauses cite principles that do not carry the claim
**Where:** `profile.yaml:90-91` (`forbidden_behaviours[2]`) and `profile.yaml:109-112`
(`source_of_truth_policy.precedence`).
**Severity: should-fix** — claim strength **SCOPE_BROADENED** (invented grounding)

**Problem.** `forbidden_behaviours[2]` — "Certifying the underlying result or business case as
correct… (P001, P091)" — cites two *craft* principles (fix the main assertion before graphing it;
build a chain of evidenced sub-assertions). Neither states or implies a prohibition on certifying
truth. Likewise "Where two principles conflict, the audience's comprehension decides (P012, P056)"
cites decluttering an overloaded slide and audience-centred design; neither states a meta-rule for
arbitrating principle conflicts. Both clauses are sound authored policy — the defect is that the
`(Pxxx, Pyyy)` citations claim principle-level grounding the principles don't carry.

**Fix.** Either re-cite to principles that actually state a certification boundary / conflict-arbitration
rule, or mark both as authored-policy overlays with no principle citation rather than attaching
citations that don't support them.

---

### F6 — Quote-scan rights gate could not run (validator WARN)
**Where:** `validate_generated_package` output; `sources/markdown/` absent by design
(3 `distillation-only` sources).
**Severity: should-fix**

**Problem.** `[WARN] quote-scan: rights NOT verified — 3 restricted source(s) but no source text
available (no sources/markdown/, no warm cache module); verbatim-quote gate could not run.` The
standalone `quote_scan` reports PASS, but that PASS is vacuous — with no source text there is nothing
to compare against. Given three `distillation-only` sources (Alley + Duarte ×2), the no-verbatim-quotation
rule in `.claude/rules/rights-and-quotation-policy.md` is currently **unverified**, not satisfied.

**Fix.** Run the quote scan once against a warm markdown cache (or a temporary re-conversion) and record
the verified result in the package, so the rights-clean export carries evidence rather than an
unrunnable gate. Not a FAIL, but it is the one gate this package cannot currently self-attest.

---

### F7 — `always_on` block carries all 13 topic areas into every invocation
**Where:** `.claude/agents/generated/presentation-design-advisor.md:26-254`
(mirrors `profile.yaml:114-313`); skill list at adapter lines 392-416.
**Severity: should-fix**

**Problem.** The operating-invariants block reproduces ~120 principles near-verbatim, and that content
maps almost one-to-one onto the 13 separate skill files. Every invocation — a font-choice question or
a Q&A-tactics question alike — always loads slide structure, story arc, persuasion, delivery, *and*
equipment logistics into the system prompt. That defeats the point of granular on-demand skills and
dilutes attention with material irrelevant to the query.

**Fix.** Shrink `always_on` to genuinely cross-cutting non-negotiables (the advice-only boundary, the
"never violate" rules), and leave the topic-specific technique detail to the skill files that already
carry it. Re-export the adapter after the profile change.

---

### F8 — Read/Grep/Glob granted but never mentioned in the instructions
**Where:** adapter frontmatter line 4 (`tools: Read, Grep, Glob`); no corresponding instruction in the
body (lines 17-421) or in `profile.yaml`.
**Severity: should-fix**

**Problem.** `review` mode triggers on "the caller submits a deck, slide, talk outline… for critique",
but nothing tells the model when to Read a caller-supplied path versus rely on pasted text, or that
Grep/Glob are for locating a named file rather than browsing. The tools are either dead weight or used
without a boundary.

**Fix.** Add one instruction: when the caller references a deck/outline by path rather than pasting it,
use Read to load the actual content before critiquing; use Grep/Glob only to locate a referenced file,
never to browse unrelated material.

---

### F9 — Anti-patterns are restatements of Procedure steps, not failure signatures
**Where:** all 13 `skills/*/SKILL.md`, `## Anti-patterns to flag`
(e.g. `assertion-evidence-slide-structure/SKILL.md:81-87`).
**Severity: should-fix**

**Problem.** Every entry is literally "Overlooking P0XX: `<the same imperative sentence as the matching
Procedure step>`." None describes an observable failure in a submitted deck (e.g. "headline is a topic
phrase like 'Results' rather than a claim sentence"; "slide has five bullets but the speaker will voice
only two"). The section is a lossy duplicate of Procedure — and, given F2, sometimes a strictly worse
duplicate.

**Fix.** Author anti-patterns as observable symptoms distinct from the positive instruction, giving a
reviewing agent two lenses (what to do / what a violation looks like) instead of one repeated.

---

### F10 — `rehearsal-and-extemporaneous-delivery` fuses two unrelated lenses (15 principles)
**Where:** `skills/rehearsal-and-extemporaneous-delivery/SKILL.md` (whole file; package median ≈9).
**Severity: should-fix**

**Problem.** It merges rehearsal/memorisation mechanics (P020, P052, P054, P094, P095, P105) with
in-room delivery technique (eye contact P107, room control P106, composure P108, confidence P110,
pacing P111) and general delivery-style judgment (P016, P066, P072, P079). It is also the worst victim
of F1 — which is itself a symptom of one file covering too much ground.

**Fix.** Split into `rehearsal-and-memorisation` (practice method, notes vs no-notes, script vs
organisation-memorisation) and an in-room delivery/composure skill (eye contact, room control,
confidence, mid-talk recovery). Both lists then fit without hitting any cap.

---

### F11 — "composure" triggers two skills with disjoint principles
**Where:** `skills/questions-challenge-and-composure/SKILL.md:44` vs
`skills/rehearsal-and-extemporaneous-delivery/SKILL.md:55`.
**Severity: should-fix**

**Problem.** Both use "composure" as trigger language — Q&A/attack context (P029, P055, P093, P109)
and general mid-talk nervousness (P108, P110). A caller asking "I lost my composure mid-talk, how do
I recover" gives no clean signal for which skill applies.

**Fix.** State the distinguishing condition in each `When to use` bullet: challenge/Q&A-triggered
composure vs general mid-delivery mishap or nervousness.

---

### F12 — `format-choice-and-preparation-planning` carries two off-lens principles
**Where:** `skills/format-choice-and-preparation-planning/SKILL.md:44-45,52,60,65` (P036, P074).
**Severity: should-fix**

**Problem.** The name promises format choice and prep planning (document-vs-presentation, specialised
styles, illustrator briefing, prep scheduling), but P036 ("critique a talk from four separate
perspectives") and P074 ("refuse to treat slides as an extension of the presenter's persona") are
general review-methodology / ethics guidance. A caller asking "meeting or deck?" gets unrelated
content; a caller wanting talk-critique method won't look here. (P048's presence in the same skill is
covered separately in F4.)

**Fix.** Re-home P036/P074 to the shared quality-bar framing, or rename the skill to match its actual
broader scope.

---

### F13 — Provenance ledger exempts four profile fields from the repo's traceability hard rule
**Where:** `provenance-ledger.md:9-10` vs `.claude/rules/rights-and-quotation-policy.md`
("Every profile field must be traceable to a source and QID… No orphan field values").
**Severity: should-fix**

**Problem.** The ledger states that `role`, `when_to_use`, `inputs`, `outputs` "carry no inline tags,
per repo convention", but those fields (`profile.yaml:8-23, 24-34, 44-47, 48-64`) hold substantive
claims — the 13-topic role summary, the required-inputs list — with no citation trail. By the letter of
the rule they are orphans; the ledger declares an exception to a rule that admits none.

**Fix.** Either add QID pointers for the descriptive fields' factual claims, or amend the policy to scope
the traceability requirement to load-bearing rule fields (`quality_bar`, `forbidden_behaviours`,
`handoff_rules`, `knowledge_partition`, `source_of_truth_policy`) so the carve-out is policy-consistent.

---

### F14 — `inputs.required` bundles seven facts as uniformly mandatory
**Where:** `profile.yaml:44-47`.
**Severity: should-fix**

**Problem.** One `required` bullet makes all of artifact, occasion, audience, post-talk action, slot
length, prep time, and room conditions strictly mandatory — broader than the triggers need. `when_to_use`
bullet 1 (does each slide assert and evidence something?) needs neither room conditions nor prep time;
bullet 2 (diagnose a flop) may need only audience plus what happened. Gating on all seven risks stalling
on requests the advisor could partly answer.

**Fix.** Split into a minimal `required` set (artifact/topic + audience) and a `recommended` set
(occasion, post-talk action, slot length, prep time, room conditions) that sharpens advice without gating.

---

### F15 — P006 widened from "science" to "technical work"
**Where:** `profile.yaml:206` vs `principles/principles.yaml:99-118` (P006).
**Severity: nice** — claim strength **SCOPE_BROADENED** (minor)

**Problem.** P006 is scoped to "science"/"scientists" (Alley's domain); the profile generalises to
"technical work" broadly. Probably intended cross-source synthesis with Duarte, but it is a silent
widening of P006's own evidence base.

**Fix.** Cite a Duarte-derived principle alongside P006 to carry the broader domain explicitly.

---

### F16 — Post-mortem diagnosis trigger maps to no output mode
**Where:** `profile.yaml:52-64` (`outputs.modes`) vs `profile.yaml:27-28` (`when_to_use` bullet 2).
**Severity: nice**

**Problem.** `when_to_use` bullet 2 describes diagnosing why a talk didn't land — a narrated post-mortem
with no artifact — but `review` mode's trigger is "the caller submits a deck, slide, talk outline, or
delivery for critique" (artifact in hand) and `advise` is framed as a forward-looking decision. Neither
mode cleanly names the case.

**Fix.** Broaden `review`'s trigger to include "or a description of what happened", or add a diagnostic
clause to `advise`.

---

### F17 — No example demonstrates two of the three refusal categories
**Where:** `profile.yaml:371-389` (`examples`) vs `profile.yaml:38-39` (`when_not_to_use` items 2, 3).
**Severity: nice**

**Problem.** Three examples exist (two happy-path, one failure-recovery refusing to inflate a weak
result), but none demonstrates declining to rule on whether the underlying result/business case is
correct, or declining to guarantee funding/approval.

**Fix.** Add an example where the caller asks "is our data solid enough to greenlight this" or "will the
board approve this", showing an in-scope-help-while-declining response.

---

### F18 — `multisource_synthesis: deferred` is unexplained
**Where:** `profile.yaml:7`; not mentioned anywhere in `provenance-ledger.md`.
**Severity: nice**

**Problem.** An auditor cannot tell why synthesis across the three sources (Alley vs the two Duarte
books) was deferred, or what "deferred" is meant to trigger later.

**Fix.** Add one ledger line (Distillation or Version History) giving the rationale — e.g. single-pass P0
authored layer, cross-source synthesis planned for a later minor version.

---

### F19 — In-scope/out-of-scope both hinge on the word "case"
**Where:** adapter lines 259-267 vs 270-281 (`profile.yaml:24-43`).
**Severity: nice**

**Problem.** "Judging whether a persuasive case covers evidence, emotional appeal, and speaker
credibility" (in scope) sits next to "a ruling on whether the underlying result, data, method, or
business case is correct" (out of scope). A router doing keyword matching can blur "is the case well
presented" with "is the case true".

**Fix.** Add a clause to the in-scope bullet: "…judging whether the case is *presented* persuasively —
not whether the underlying data or business case is valid."

---

### F20 — Procedure steps ordered by principle ID, not by workflow dependency
**Where:** all 13 `skills/*/SKILL.md`, `## Procedure`.
**Severity: nice**

**Problem.** Step order matches ascending `provenance.principles` order in every skill, so Procedure is
a per-principle restatement of Purpose rather than a sequenced process. Each step is individually
actionable, but the section doesn't encode dependencies.

**Fix.** Where a genuine causal order exists (assertion-evidence: identify assertion → draft headline →
apply mechanics → check evidence-first exceptions), re-sequence to reflect it. Not needed where the
principles are independent checks.

---

### F21 — Two Procedure steps drop the condition their principle carries
**Where:** `skills/format-choice-and-preparation-planning/SKILL.md:58` (P027);
`skills/visual-evidence-analogies-and-graphics/SKILL.md:61` (P102).
**Severity: nice**

**Problem.** "Reserve the Lessig style (P027)." and "Put a short reference listing (P102)." compress a
conditional principle into a bare imperative, dropping the condition stated in the skill's own Purpose
(Lessig style is for "keynotes and after-dinner talks reused on multiple occasions"; the reference must
be "visible on every slide carrying another group's work"). Read in isolation they aren't actionable.
Related to F2 but distinct: these are grammatical, just under-specified.

**Fix.** Fold the triggering condition into the Procedure line so each step stands alone.

---

## Summary

| Severity | Count |
|----------|-------|
| must-fix | 3 (F1, F2, F3) |
| should-fix | 11 (F4-F14) |
| nice | 7 (F15-F21) |

All three must-fix findings were independently confirmed against the files, not accepted on a
reviewer's word: the 7-entry anti-pattern cap by counting principles vs anti-patterns per skill, the
mid-clause truncation by reading the cited lines, and the faithfulness gap by grepping
`reports/faithfulness-report.yaml` for `always_on`/`knowledge_partition` (0 hits) plus confirming P048
is the sole `profile_rule: false` principle.

Deterministic gates contributed **0** must-fix (validation passed; the single WARN is F6). The package
validates but is not yet trustworthy: F1 and F2 mean the skill bodies under-deliver against their own
declared principle coverage, and F3 means the faithfulness gate never inspected the section of the
profile carrying nearly all the checkable claims.

MUST_FIX_COUNT: 3
