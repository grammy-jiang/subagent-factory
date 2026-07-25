# Review Loop r1 — research-writing-advisor

Single fresh review pass over the current package. REVIEW ONLY — no package files edited.
Reviewers: deterministic gates + 4 LLM lenses (agent-skills, profile, faithfulness, ai-agent-engineering). Deduped, most-severe first.

> Note: a prior r1 report existed at this path against an earlier package state; its lead must-fix
> (skill Procedure/anti-pattern lines severed mid-clause) is **resolved** in the current bodies —
> the cited lines now render complete sentences, and a severed-clause sweep of all 13 skills is clean.
> This report supersedes it and reflects the current package.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASSED** (0 FAIL). Only WARN-triage injection-scan hits — all benign: source text quoting writing instructions ("You are now ready to begin building a model of Introductions by writing…") + normalization-layer reveals on 2 source files. Triage, not block, per `untrusted-source-policy.md`. |
| `quote_scan` | **PASS** — no verbatim quotation. |
| ellipsis `…` grep (skills + adapter) | **clean**. |
| severed-invariant / mid-clause sweep | **clean** (2 grep hits verified grammatically complete). |

Deterministic FAIL count: **0**.

## Consolidated findings

### MUST-FIX

**M1 — Version stamp / provenance mismatch: `agent_version: 1.2.1` but ledger has no 1.2.1 entry** *(profile-reviewer; verified)*
- Where: `profile.yaml:4` (`1.2.1`) vs `provenance-ledger.md:47-49` Version History (newest entry `1.2.0`, 2026-07-25).
- Problem: Fails Phase 8 #16; violates `generated-artifact-policy.md` rules 4–5 + supersession rule. No record of what changed 1.2.0→1.2.1 or whether the bump was intentional.
- Fix: (a) add a `1.2.1` Version History entry documenting the delta (fields/principles touched, superseded rows) + current Phase 8 verdict + re-run body-size (#14) word count; or (b) if clerical, revert `profile.yaml:4` to `1.2.0` so the files agree.

**M2 — No real progressive disclosure: full principle detail inlined in every skill body** *(agent-skills-advisor)*
- Where: package-wide; worst in `paper-sections-and-organization/SKILL.md` (29 Procedure + ~29 mirrored Anti-pattern items), `evidence-integrity-and-claims` (19+19), `clarity-and-sentence-style` (21+21), `research-argument-and-contribution` (19+19). Bodies ~2,500–3,500+ words.
- Problem: `## Procedure` restates each principle's full content; `## Anti-patterns` restates nearly the same as negations. Nothing deferred to `references/` for routine use. Contradicts the quality bar ("keep SKILL.md concise and within its context budget") and the progressive-disclosure invariant.
- Fix: For skills with >~12 principles, keep a short routing table in SKILL.md (principle ID → one-line cue → maps-to) and move the elaborated Procedure/Anti-pattern bullets into a per-skill reference (e.g. `references/paper-sections-checklist.md`) loaded on demand. [P002, P005, P022, P057, P072]

**M3 — Large skills use one flat undifferentiated numbered list, no internal routing** *(agent-skills-advisor)*
- Where: `paper-sections-and-organization/SKILL.md` (steps interleave Introduction/Methods/Results/Discussion/Abstract/Title in arbitrary principle order); same shape in `evidence-integrity-and-claims`, `research-argument-and-contribution`, `clarity-and-sentence-style`.
- Problem: A caller wanting only the Discussion (or only hedging) must scan the whole list — no subheading/decision routing by task type.
- Fix: Add subheadings inside `## Procedure` (`### Introduction`, `### Methods`, …) grouping existing numbered steps; mirror in `## Anti-patterns`. Reorganization, not rewrite — drop no content. [P054]

### SHOULD-FIX

**S1 — P080 citation over-reach: language-editing responsibility stretched into a broad ownership/authority doctrine** *(faithfulness-reviewer)*
- Where: `source_of_truth_policy.canonical_owner`, `handoff_rules[0]`, `forbidden_behaviours[0]`, `when_not_to_use[0]`, `source_of_truth_policy.precedence` — all cite **P080** for "author/team own the manuscript, the data, the argument's substance, and what to claim and when to submit."
- Problem: P080's text is narrow — author is responsible for correct English and for the story/science that can't be outsourced to a language editor. "The data," "argument's substance," "when to submit" appear nowhere in P080; no other principle grounds data-ownership or submission-timing authority (corpus grepped). `SCOPE_BROADENED`, repeated across 5 load-bearing fields. (Secondary: P024 cited for "advisor guides, does not author" is a defensible inference but stretched past its literal text.)
- Fix: (a) narrow the P080-cited sentence to what P080 supports, dropping data/substance/submission; or (b) keep the broader authority statement but mark it an advisor design default, not a source-derived claim — matching how `role` frames invariants as advisory.

**S2 — "Domain experts" named as an owner but never routed to** *(ai-agent-engineering-reviewer)*
- Where: `when_not_to_use` bullet 2 + `forbidden_behaviours[4]` name domain experts as owning domain-science correctness, but `handoff_rules` and `source_of_truth_policy.canonical_owner` name only author/team + editors/reviewers. Mirrored in adapter.
- Problem: Incomplete routing contract for the sharpest edge of scope — asserted as co-owner in one place, dropped from the two sections that formalize ownership.
- Fix: Add a third handoff line routing domain-science correctness to the researcher + domain experts (flag, don't rule), and add that owner to `source_of_truth_policy.canonical_owner`, so all three boundary statements name the same owners.

**S3 — Body-size (Phase 8 #14) not re-verified for current version** *(profile-reviewer)*
- Where: last recorded count ~981 w at v1.1.0 (`provenance-ledger.md:79-81`); v1.2.0 added `router_description` + citations; v1.2.1 undocumented.
- Problem: Only ~19 w under the 1000-w FAIL ceiling before two content additions — unverified risk of now exceeding it.
- Fix: Re-run #14 (`profile_self_check` / body-size gate) against the current profile; record count + verdict in the next ledger entry before export. (Folds into M1's ledger entry.)

**S4 — Shared boilerplate duplicated verbatim across all 13 skills (DRY)** *(agent-skills-advisor)*
- Where: second `## Inputs` bullet + full `## Output` + full `## References` are byte-identical in all 13 SKILL.md.
- Problem: One output-contract fact repeated 13×; any change needs 13 synced hand-edits; +~100–150 w per body.
- Fix: Move the shared Output contract + References policy to a shared reference and point to it, or document that the text is intentionally mirrored from `profile.yaml outputs.primary_format` and regenerated from that single source.

**S5 — CHANGELOG.md requirement unverified** *(profile-reviewer)*
- Where: `generated-artifact-policy.md` rule 5 requires a CHANGELOG.md entry per bump — distinct from the ledger Version History; out of reviewed scope.
- Fix: Confirm a CHANGELOG.md entry exists for 1.2.0/1.2.1, or state in the ledger header that Version History is this package's canonical changelog.

**S6 — Methods-reproducibility content overlaps two sibling skills, no cross-reference** *(agent-skills-advisor)*
- Where: `paper-sections-and-organization` step (P050, author-time completeness) vs `revision-editing-and-peer-review` step (P149, revision-time audit).
- Fix: Add one clause to each description distinguishing authoring vs auditing Methods, cross-referencing the sibling by name.

**S7 — Description-opening pattern inconsistent across 13 skills** *(agent-skills-advisor)*
- Where: `figures-tables-and-data-display`, `literature-and-source-use`, `presenting-and-public-speaking` diverge from the "what-it-does then Use-when" pattern of the other 10.
- Fix: Re-lead all three with a one-clause "what this skill does" before the trigger list. [P056, P083]

**S8 — Dense descriptions run 2–3× the frontmatter guideline** *(agent-skills-advisor)*
- Where: `paper-sections-and-organization` (~150 w), `research-argument-and-contribution` (~150 w) — under the 1024-char cap but restate nearly every constituent principle inline.
- Fix: Trim to 3–5 representative trigger phrases + a one-sentence summary; move exhaustive per-principle restatement out of frontmatter.

### NICE

- **N1** — `outputs.primary_format` cites only (P022, P047) for "never a ghost-written deliverable or promise of acceptance"; those sub-claims are grounded elsewhere (P080/P024/P083/P135). Fix: drop the parenthetical or extend the citation list. *(faithfulness)*
- **N2** — Examples skew to `review` mode; `advise`/`plan` have no worked example. Optionally add one. *(profile)*
- **N3** — `revision-editing-and-peer-review` H1 uses a comma (`# Revision, Editing And Peer Review`) unlike the 12 comma-free siblings. *(agent-skills)*
- **N4** — figures/tables vs slide-visual naming proximity; a poster/infographic could match either. Add a one-clause mutual exclusion. *(agent-skills)*
- **N5** — "pure code, data analysis, or non-writing project work" boundary is soft for adjacent technical-writing artifacts (README/API docs). Optional sharpening. *(ai-agent)*

## Solid — no issue found
- **Tool boundary correct:** adapter `tools: Read, Grep, Glob` only — no Write/Edit/Bash/MCP despite an available `research-pipeline` server.
- **Advisory framing coherent:** role frames invariants as "advisory criteria, not authority to act"; `outputs.primary_format` bars bare verdicts, ghost-written deliverables, acceptance promises; `may_edit_canonical: false`; forbidden_behaviours override every invariant. Both worked examples enforce the no-deliverable boundary.

## Per-lens must-fix tally
- deterministic gates: 0
- agent-skills-advisor: 2 (M2, M3)
- profile-reviewer: 1 (M1)
- faithfulness-reviewer: 0
- ai-agent-engineering-reviewer: 0

MUST_FIX_COUNT: 3
