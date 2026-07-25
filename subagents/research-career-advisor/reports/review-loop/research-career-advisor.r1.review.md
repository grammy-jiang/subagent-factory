# Review Loop — research-career-advisor — Round 1

Package: `subagents/research-career-advisor/`
Deterministic gates: `validate` **PASS**, `quote_scan` **PASS**, truncation gate (`…` / severed adapter invariant) **no hits**.
Injection-scan: 8 WARN, all benign (Hamming source prose, e.g. "you are now at the lower levels in your organization" — frozen source, data-not-instruction; NOT must-fix).

Reviewer panel: agent-skills-advisor (2 must-fix), profile-reviewer (0), faithfulness-reviewer (0), ai-agent-engineering-reviewer (0).

Findings consolidated, deduped across lenses, most-severe first.

---

## MUST-FIX

### M1 — Every SKILL.md is missing the `description:` frontmatter field
- **Where**: all 8 `subagents/research-career-advisor/skills/*/SKILL.md` (frontmatter, lines 1–5: only `name`/`kind`/`status`/`provenance`).
- **Problem**: `description` is the sole tier-1 progressive-disclosure / triggering signal in the SKILL.md spec these files imitate. Sibling PASS package `research-writing-advisor` authors a full `description:` on every skill (verified); this package drops it, so "when to use" lives only in the body and any consumer must open the whole file to route. Regression against the factory's own norm.
- **Fix**: Add a 1–2 sentence third-person, trigger-oriented `description:` to each of the 8 frontmatter blocks, front-loading concrete cue phrases (mirror the sibling `research-writing-advisor` skills). Re-export adapter + `stale --stamp` + re-validate after.

### M2 — "Anti-patterns to flag" bullets are truncated mid-clause across ≥6 of 8 skills
- **Where**: e.g. `writing-and-publishing-scientific-work/SKILL.md:72` ("...and disclose known weaknesses **rather.**"), `:74` ("...evaluation and **separating.**"), `:76` ("...unrelated or **merely.**"), `:73` ("...an accurate title, a brief results-focused abstract, and an **introduction.**"); same pattern in `choosing-advisers-groups-and-positions` (`:69`, `:73`), `research-program-and-problem-selection:75`, `experimental-design-and-measurement:66-70`, `evaluation-metrics-and-research-judgment:73-77`, `funding-grants-and-research-proposals:67`.
- **Problem**: Bullets are character-capped substrings of the procedure text with a period appended → grammatically broken, several read as nonsense ("...and separating.", "...or merely."). This is exactly the "truncated skill body" class; the deterministic truncation gate misses it because these end in `.` not `…`.
- **Fix**: Regenerate each "Overlooking PXXX" bullet as a complete sentence — ideally rewrite as a standalone observable failure symptom (see S8) instead of a capped copy of the Procedure step. Re-stamp/re-validate after.

---

## SHOULD-FIX

### S1 — `quality_bar[2]` over-claims P010 (hedge removed)
- **Where**: `profile.yaml:67-69` ("Career moves are evaluated on evidence, not prestige...").
- **Problem**: P010 is conditioned — "prefer an established adviser **when other mentoring qualities are comparable**." `quality_bar[2]` flattens to a blanket "not prestige," a HEDGING_REMOVED distortion. Internally inconsistent: `knowledge_partition.always_on` (lines 132-134) preserves the hedge; the quality_bar line the advisor self-checks against does not. `faithfulness-report.yaml` rates it WITHIN_SCOPE — under-catches.
- **Fix**: Restore the tie-break condition, e.g. "...judged primarily by access, real guidance, credited output, and mobility, with established reputation used only as a tie-breaker when those protection factors are comparable." Update the faithfulness-report verdict accordingly.

### S2 — No authored `router_description:`; installed adapter description under-covers scope
- **Where**: `profile.yaml` (no `router_description:` key) → `.claude/agents/generated/research-career-advisor.md:3` frontmatter `description`.
- **Problem**: `_compose_description()` surfaces only the first 2 of 5 `when_to_use` items + first exclusion → adapter description advertises only problem-selection and adviser/job choice; omits writing/presenting, funding, empirical-design triggers. Export docstring flags exactly this for broad multi-skill advisors; sibling `research-writing-advisor` uses the override, this one doesn't.
- **Fix**: Add `router_description:` (≤320 chars) covering all 5 when-to-use domains + core exclusion; re-export.

### S3 — Undeclared routing overlap with sibling `research-writing-advisor`
- **Where**: `profile.yaml` `when_to_use` item 3 (paper title/abstract/intro, talk/slides, publication strategy) vs `research-writing-advisor` when_to_use items 1 & 4.
- **Problem**: Both advertise title/abstract + talk/slide prep in routing-facing text; altitude split (strategy vs craft) lives only in skill-body prose, so "review my abstract / talk slides" routes ambiguously.
- **Fix**: Narrow item 3 to the strategy slice this agent owns (publication strategy, portfolio/dissertation composition, venue/impact framing); add a `when_not_to_use` / `handoff_rules` pointer to research-writing-advisor for craft-level drafting/clarity/slide design. Mirror reciprocal pointer in the sibling.

### S4 — Profile body word budget borderline against the 1000-word FAIL ceiling
- **Where**: `profile.yaml` counted fields (role + when_to_use + when_not_to_use + inputs.required + outputs.primary_format + minimum_useful_output + modes + quality_bar + forbidden_behaviours + handoff_rules + precedence).
- **Problem**: Reviewer hand-sum ≈998w — one counting error from the hard fail. Highest-weight: quality_bar (~196w), role (~133w).
- **Fix**: Confirm with `profile_self_check`; trim for margin. Note the role's closing sentence duplicates `forbidden_behaviours[0..2]` (~40w) — collapse to a one-line pointer (also raised as S5).

### S5 — Role field duplicates the forbidden-behaviours summary
- **Where**: `profile.yaml:8-17` role closing sentence vs `forbidden_behaviours[0..2]` (lines 82-87). (Raised independently by profile, faithfulness, and ai-agent reviewers.)
- **Problem**: ~40 words of pure duplication; drift risk if the two edit apart; feeds S4 word budget.
- **Fix**: Shorten role's closing to a pointer ("...the advice-only boundary and forbidden behaviours below take precedence."); let `forbidden_behaviours` carry specifics.

### S6 — `multisource_synthesis: deferred` — cross-source conflict pass never run/recorded
- **Where**: `profile.yaml:7`; no `principle-clusters.json` / `principle-graph.json` present.
- **Problem**: Legit validator opt-out, but 4 sources span very different eras/institutions (Hamming Bell-Labs industrial 1997 vs present-day academic job market); latent cross-source tension in career-move guidance unverified. Ledger doesn't record a manual check.
- **Fix**: Either run Step-7 synthesis, or add a line to `provenance-ledger.md` recording a manual cross-source conflict check (found none / noting accepted tensions + how precedence resolves them).

### S7 — Anti-pattern list drops one principle in 2 skills (7 bullets vs 8 provenance principles)
- **Where**: `writing-and-publishing-scientific-work/SKILL.md:70-77` (omits P046); `evaluation-metrics-and-research-judgment/SKILL.md:70-77` (omits P038). Other 6 skills are 1:1.
- **Fix**: Add the missing anti-pattern bullet in each so every provenance principle has a corresponding entry.

### S8 — Several Procedure steps collapse to one-line stubs vs sibling steps in the same file
- **Where**: `presenting-and-engaging-with-research:51` (P039 layers unstated); `choosing-advisers-groups-and-positions:52,54`; `early-career-positioning-and-negotiation:49`; `evaluation-metrics-and-research-judgment:55,57`.
- **Problem**: Bare restatement of the principle with no operative detail, though the concrete criteria already sit in that file's "Purpose" paragraph.
- **Fix**: Expand each stub to restate the concrete criteria already present in Purpose, matching the file's other steps.

### S9 — Anti-pattern bullets restate the rule rather than name a failure symptom
- **Where**: all 8 skills, "Anti-patterns to flag" ("Overlooking PXXX: <positive-practice text>").
- **Problem**: Redundant with Procedure; likely the root cause of the M2 truncation (auto-generated substring of the procedure sentence).
- **Fix**: Rewrite each as a short observable failure symptom independent of the Procedure step (resolving this resolves M2's root cause).

---

## NICE

- **N1** — All 8 skills lack an embedded worked example; profile-level examples cover only 3 of 8 lenses and only `advise`/`review` modes (no `plan`-mode example). Add short scenario+ideal-response per skill, and a `plan`-mode profile example. (`profile.yaml:217-259`)
- **N2** — `quality_bar[1]` cites P046 for "few high-quality papers over many weak" — that content is P012, not P046. Citation-accuracy nit. (`profile.yaml:64-66`)
- **N3** — `knowledge_partition.skills`/`references` are bare, positionally-keyed name lists → adapter "Canonical package" file list is unannotated (generic-pointer smell). Pair each with a one-line "read when..." note. (`profile.yaml:203-214`)
- **N4** — `faithfulness-report.yaml` only covers a subset of fields (skips `knowledge_partition.always_on`, `when_not_to_use`, `examples`, `canonical_owner`); reviewer checked them and found no over-claim, but the report should carry the findings so a future pass need not re-derive.
- **N5** — Per-skill negative/out-of-scope triggers absent (global `when_not_to_use` only in profile/adapter).

---

MUST_FIX_COUNT: 2
