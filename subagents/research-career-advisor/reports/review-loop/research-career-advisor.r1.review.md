# Review r1 — research-career-advisor

Single review pass. Deterministic gates + 4 reviewer lenses (agent-skills, profile,
faithfulness, ai-agent-engineering), consolidated and deduped.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (all `[OK]`; 7 `[WARN]` injection-scan only) |
| `quote_scan` | **PASS** — no verbatim quotation |
| truncation grep (`…` / severed invariant) | clean, no hits |

Injection-scan WARNs are all on `sources/markdown/hamming-meta-5bf0ea64.md` (role-override
lexical hits + de-obfuscation reveals). Per `untrusted-source-policy.md` these are
**triaged-benign source data, WARN not FAIL** (source content is data, not instruction) —
Hamming's "You and Your Research" prose ("you should do your job in such a fashion...").
**Not a must-fix.** No new instruction-like span introduced by this package.

## Findings (most-severe first)

### must-fix

**1. Adapter frontmatter `description` is truncated — routing signal drops the
empirical-methods domain and all sibling-advisor exclusions.**
- Where: `.claude/agents/generated/research-career-advisor.md:3` (vs `profile.yaml:8-11` `router_description`).
- Problem: the frontmatter `description` (the string Claude Code routes on) is a mechanical
  `role — Use when: [when_to_use[0..1]] — Not for: [when_not_to_use[0]]` concatenation. It
  carries only 2 of 5 `when_to_use` domains and 1 of 6 `when_not_to_use`, then stops. It
  **drops `when_to_use[4]`** ("Designing or reviewing an empirical study, metric, or
  measurement for soundness") — the domain backing 2 of 8 skills
  (`experimental-design-and-measurement`, `evaluation-metrics-and-research-judgment`) and a
  third of `quality_bar` — and **drops the sibling-advisor exclusions** (craft-writing →
  `research-writing-advisor`; integrity/reproducibility audit →
  `research-integrity-reproducibility-advisor`), so a router has no signal to steer those
  requests elsewhere. The profile already carries a complete, purpose-built
  `router_description` (all five domains + advice-only boundary, `profile.yaml:8-11`) that the
  renderer does not use. Partial mitigation: the leading `role` clause does say
  "methodologically sound research", so the methods domain is faintly signaled.
- **SYSTEMIC** — confirmed identical truncation in `research-writing-advisor.md:3` and
  `research-integrity-reproducibility-advisor.md:3` (both merged, PR#95/#97). This is a
  factory-renderer convention, not a hand-edit; the adapter is a faithful deterministic render
  (`adapter-fresh` gate PASSES) and is DO-NOT-EDIT.
- Fix: **upstream, in the adapter renderer** — build the frontmatter `description` from
  `router_description` (or fall back to it), instead of truncating `role` + first-N list items.
  At minimum the rendered description must name all five `when_to_use` domains (incl.
  empirical-study/metric soundness) and the two sibling-advisor exclusions. Re-export all three
  research-methods adapters after the template fix. No per-package hand-edit possible.

### should-fix

**2. `forbidden_behaviours[0-2]` read as principle-grounded but are structural house-policy —
profile is not self-disclosing.**
- Where: `profile.yaml:84-89`.
- Problem: the ledger (`provenance-ledger.md:9-14`) discloses that `forbidden_behaviours[0]`
  (P017,P013), `[1]` (P010,P021), `[2]` (P026) are structural advice-only house-policy whose
  citations are "topically-nearest for provenance," not grounding — but nothing in
  `profile.yaml` itself signals this; the citations look identical to the genuinely-grounded
  `[3-4]`. The sibling field `handoff_rules[2]` (`:101`) already carries the inline qualifier
  "structural house-policy, not principle-derived."
- Fix: add the same inline qualifier to `forbidden_behaviours[0-2]` (e.g. "(structural
  house-policy — advice-only boundary; P017, P013)") for self-consistency.

**3. Faithfulness report does not cover `knowledge_partition.always_on` or `examples` — the
densest citation surface is unaudited.**
- Where: `reports/faithfulness-report.yaml` (coverage gap, not an active over-claim).
- Problem: the report's `findings` review `quality_bar`, `forbidden_behaviours`, `when_to_use`,
  `outputs.primary_format`, `handoff_rules`, `source_of_truth_policy.precedence` — but have
  **zero entries for the 8 `always_on` skill-grounding blocks** (which carry nearly all of
  P001-P048) and **zero for the 3 `examples`**. Independent walk of all 8 blocks + 3 examples
  vs `principles.yaml` found them **currently within scope** (no over-claim today), but the
  artifact does not establish that, so future drift in `always_on` (dense 5-6-principle
  paraphrase per block) would go uncaught.
- Fix: add `rule_ref` entries for each `always_on[i]` block and each `examples[i]` so report
  coverage matches the profile's actual rule surface.

**4. `when_to_use[4]` vs `when_not_to_use[4]` boundary on p-hacking is not crisp.**
- Where: `profile.yaml:28-29` vs `:39-41`.
- Problem: `when_to_use[4]` puts null-hypothesis-test soundness in scope and `quality_bar[4]`
  (P040) is definitionally the p-hacking check, yet `when_not_to_use[4]` excludes "p-hacking"
  as an integrity audit. "Did we p-hack this?" sits ambiguously on both sides. (Already
  tightened once in review r2 per ledger — residual edge, not unaddressed.)
- Fix: add a clause to `when_not_to_use[4]` distinguishing "reviewing whether a stated test
  procedure is statistically valid" (in-scope) from "adjudicating whether misconduct/p-hacking
  occurred" (out-of-scope), or add a boundary `example`.

**5. Skill `## Purpose` sections are filler in 7 of 8 skills.**
- Where: all skills except `evaluation-metrics-and-research-judgment/SKILL.md` — e.g.
  `choosing-advisers-groups-and-positions/SKILL.md:44-46`,
  `experimental-design-and-measurement/SKILL.md:45-48`,
  `research-program-and-problem-selection/SKILL.md:51-53` (+4 more).
- Problem: Purpose restates the description then adds a content-free pointer ("`## When to
  use` and `## Procedure` carry the specific checks") — names no content, costs tokens.
  `evaluation-metrics-and-research-judgment` shows the good pattern (substantive 2-sentence
  purpose, no pointer).
- Fix: replace the filler sentence in the 7 skills with a content-bearing purpose naming what
  the skill actually checks; drop the "carries the specific checks" pointer.

**6. Only 1 of 8 skill descriptions states a negative-scope boundary → over-trigger risk.**
- Where: skill frontmatter `description` in 7 of 8 skills (all except
  `evaluation-metrics-and-research-judgment/SKILL.md:12-13`).
- Problem: skills with generic false-trigger surfaces (e.g.
  `experimental-design-and-measurement` ↔ generic stats/QA;
  `funding-grants-and-research-proposals` ↔ generic business grant-writing) carry no "Not for"
  clause; trigger precision depends on the description alone at load time.
- Fix: add a short "Not for [generic X with no research-career dimension]" clause to the
  most-exposed skill descriptions, mirroring the proven pattern.

### nice

**7.** Repeated verbatim per-skill boilerplate (`## Output` disclaimer sentence, `## Inputs`
2nd bullet, `## Provenance` paragraph) is byte-identical across all 8 skills and restates the
always-loaded agent-level Forbidden-behaviours boundary — trim to a short pointer + principle/
claim ids, defer full source description to `references/research-career-principles-index.md`.

**8.** Description convention drift: 6 of 8 skills open "Guides X…", 2
(`early-career-positioning-and-negotiation`, `presenting-and-engaging-with-research`) open
"Use when…" — normalize for family scanability.

**9.** Worked examples cover only 3 of 8 lenses (problem-selection, empirical-evaluation,
adviser-choice); funding, publication-strategy, evaluation-metrics have none, in either the
profile `examples` or skill bodies. Add 1 compact example per uncovered lens.

**10.** `role` clause "methodological soundness is a condition of research survival
(Cohen, Hamming)" is the one absolute-sounding, author-attributed (not `Pxxx`-cited) claim in
the profile — cite the grounding principle or soften register to match the rest.

**11.** `always_on` block 4 says "moving on if timely credited progress cannot be protected";
P019's scope is the narrower "move groups" (change group/position, not change problem) — tighten
wording to match P019 exactly.

**12.** `source_of_truth_policy.canonical_owner` (`profile.yaml:104-109`) is a substantive
authority statement with no principle citation and is not in the ledger's descriptive-field
no-tag exemption list — add it to the exemption list or note its grounding for ledger
consistency.

## Dedup notes

- Adapter-description truncation (must-fix #1) surfaced by ai-agent-engineering-reviewer; the
  reviewer's "should-fix" naming concern (name signals career only, not methods) is the same
  root cause (routing discoverability of the methods domain) — folded into #1's fix.
- No cross-lens duplicate findings otherwise; profile/faithfulness/skill lenses reported
  disjoint surfaces.

MUST_FIX_COUNT: 1
