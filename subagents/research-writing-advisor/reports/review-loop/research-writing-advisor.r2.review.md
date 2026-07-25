# research-writing-advisor — review loop r2

Review-only pass. Package: `subagents/research-writing-advisor/`. cwd = repo root.
Lenses: deterministic gates + agent-skills, profile, faithfulness, ai-agent-engineering (parallel, scoped).

## Deterministic gates (Step 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** (0 FAIL). 9 injection-scan WARNs — all benign frozen writing-textbook prose ("You are now ready to begin building a model…") + reversed/base64 false-normalization on 2 source markdowns; not runtime injection, not must-fix. |
| `quote_scan` | **PASS** — no potential verbatim quotation. |
| truncation grep (`…` in skills/adapter) | **clean** — no hits. |
| adapter invariant-severed-in-parenthetical grep | **clean** — no hits. |

No deterministic FAIL → 0 must-fix from gates.

## Consolidated findings (most-severe first, deduped across lenses)

### MUST-FIX

**1. Adapter frontmatter `description` is truncated mid-list — under-triggers + weakened boundary signal**
- Where: `.claude/agents/generated/research-writing-advisor.md:3` (YAML `description`) — the field Claude Code's router matches on.
- Problem: Surfaces only 1 of 5 `when_to_use` items (drafting/revising a paper/section); drops slide/talk review, argument/evidence review, note-taking practice. `when_not_to_use` clause cut off mid-list at `"…the paper, section, slides"` — omits "or talk," the "guides the work, does not perform it" clause, and the two exclusions that matter most for authority creep (no domain-science verdict, no acceptance guarantee). Router under-fires on legitimate talk/slide/note requests and gets a weakened exclusion signal.
- Fix: Regenerate `description` as a standalone complete summary, not first-item-plus-truncated-list. Cover the full in-scope span (writing, argument, structure, clarity, figures, sources, claims integrity, presentation/talk) + the advice-only "not for: writing the deliverable, guaranteeing acceptance, ruling on domain-science/legal-rights" boundary, within the generator's length budget. Root cause is generation/rendering (single source → `profile.yaml`), so fix in the export path, not by hand-editing the adapter.

**2. `source_of_truth_policy.canonical_owner` is an orphan field value — contradicts the ledger's own traceability guarantee**
- Where: `subagents/research-writing-advisor/profile.yaml:96-100` vs `provenance-ledger.md:7-9`.
- Problem: `canonical_owner` carries zero principle-ID citations, but the ledger asserts "every `…source_of_truth_policy` value cites the promoted principle(s) it restates." Every sibling field (`precedence`, `handoff_rules`, `quality_bar`, `forbidden_behaviours`) does carry `(Pxxx)` cites; this one doesn't → ledger's own stated rule is false for this field (also trips repo `rights-and-quotation-policy` "No orphan field values").
- Fix: Either (a) add cites to `canonical_owner` reusing IDs already used for the same assertions in `handoff_rules` (author/team → manuscript authority; editors/reviewers → acceptance; counsel/institution → legal-rights/plagiarism), or (b) narrow the ledger's blanket traceability sentence to explicitly exempt `canonical_owner` the same way it already exempts `role`/`when_to_use`/`inputs`/`outputs`.

### SHOULD-FIX

**3. `role` duplicates `forbidden_behaviours` content — DRY violation, un-cited, drift risk**
- Where: `profile.yaml:13-16`. "…never writes the paper or talk, never guarantees acceptance, never rules on domain-science correctness or legal-rights" restates `forbidden_behaviours` bullets 1/2/4 nearly verbatim in an un-cited field with no single source of truth.
- Fix: Compress `role` to a boundary pointer ("invariants below are advisory criteria, not authority to act; see forbidden_behaviours for hard boundaries") and let `forbidden_behaviours` be the one authoritative statement. Also shaves the largest body-size contributor (see #6).

**4. `faithfulness-report.yaml` under-covers the profile's rule surface**
- Where: `reports/faithfulness-report.yaml` (19 scored locations) vs `profile.yaml` `knowledge_partition.always_on[0-12]`, `when_not_to_use`, `minimum_useful_output`, `outputs.modes`, `source_of_truth_policy.canonical_owner`, `examples[0-1]`.
- Problem: The report scores only 19 rule locations and omits the 13 `always_on` skill blurbs — the most heavily-cited rule content (6–24 principles each) — and both worked `examples` (the clearest place an over-claim would surface). Direct sampling of the omitted content (~35 principle IDs spot-checked) found no over-claim (all WITHIN_SCOPE), so the package's "no over-claim" conclusion is TRUE but not fully documented by the shipped report.
- Fix: Extend the report with entries for `always_on[0-12]`, `when_not_to_use`, `minimum_useful_output`, `outputs.modes`, `canonical_owner`, and `examples[0-1]` so it covers "every rule" per the faithfulness contract.

**5. `multisource_synthesis: deferred` is undocumented for a 9-source package**
- Where: `profile.yaml:7`; no matching note in `provenance-ledger.md`.
- Problem: 9 sources declared, synthesis `deferred`, no ledger rationale → Phase-8 check 17 ("no unresolved conflict") unverifiable from the record; reviewer can't tell "handled at cluster stage" from "not done."
- Fix: Add a ledger line stating why synthesis is deferred (e.g. cross-source de-dup done at principle-cluster / reduce stage, not a per-source Phase-7 profile merge).

**6. `paper-sections-and-organization` skill is the family outlier (~29 steps + 29 anti-patterns, ~1.4× next-largest)**
- Where: `skills/paper-sections-and-organization/SKILL.md`. Pushes body toward the progressive-disclosure ceiling.
- Fix: Move least-jointly-needed items (title wording, tool-vs-problem abstract framing, borrowed-method attribution) into the existing `references/research-writing-principles-index.md` entry with an explicit "load this section when reviewing a title/abstract" pointer — don't split the skill (fractures the IMRaD charter).

**7. Skill References footer is identical boilerplate across all 13 skills and never says *when* to open the referenced files (anti-pattern P029)**
- Where: `skills/*/SKILL.md` References section (byte-identical across the family).
- Fix: Replace shared boilerplate with a scoped trigger, e.g. "consult principles-index only if a finding's principle needs its full source-grounded statement or might belong to a sibling skill; consult evidence-notes only if the caller disputes a finding's grounding." Single template/generator fix.

### NICE

- **8.** Profile body ~981 words (Phase-8 check 14 WARNING, > 800 advisory budget, **under the 1000-word FAIL ceiling — confirmed by re-running `profile_self_check`, exit 0**). Not a release blocker; #3 above trims it. (Refutes an earlier ~1040w "over ceiling" read — actual tool count is 981w WARNING.)
- **9.** `faithfulness-report.yaml` note for `forbidden_behaviours[3]` cites "P150/P140" but profile cites only `(P140)`; P150 is unrelated (evidence-integrity list bleed). Report-accuracy slip, not a profile over-claim — correct or drop P150.
- **10.** `role` (`profile.yaml:8-16`) and `inputs.required` (`:38-41`) are dense single run-on sentences; splitting each into 2-3 would aid scanability. No content change.
- **11.** `when_to_use` item 5 ("wants a durable writing practice — scheduled sessions… a note-taking system that feeds drafting") reads close to a build/setup request; tool grant (no Write/Edit/Bash) already blocks overreach, but reword to "…wants recommendations for a durable writing practice…" to keep phrasing unambiguously advisory.
- **12.** Two skills (`paper-sections-and-organization`, `slide-and-visual-design`) use YAML `>` where 11 siblings use `>-`; normalize to `>-`.
- **13.** No skill embeds a worked before/after example in-body; defensible for a 13-way partition, but the two densest skills would gain actionability from one compact snippet each.

## Notes
- Body-size, injection WARNs, and the earlier "over-ceiling" claim were verified against the actual tools, not reviewer word-counts. Only #1 and #2 survive as must-fix; both are single-source-rooted (regenerate adapter / edit profile+ledger), not adapter hand-edits.

MUST_FIX_COUNT: 2
