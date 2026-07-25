# research-career-advisor — Review Loop Round 3 (re-run, v1.4.0)

One review pass over `subagents/research-career-advisor/` (profile v1.4.0). REVIEW ONLY.
Panel: deterministic gates + 4 reviewer lenses (agent-skills-advisor, profile-reviewer,
faithfulness-reviewer, ai-agent-engineering-reviewer). Findings deduped, most-severe first.

Note: this supersedes the prior r3 report, which reviewed v1.2.0 and carried 2 must-fix
(false P026/P010 grounding on `forbidden_behaviours`). Both are **confirmed fixed** in
v1.3.0/v1.4.0 — those rules now carry only the "(structural house-policy)" qualifier and no
principle citation (verified by direct read, not just changelog).

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (adapter installed/sync/fresh; tests+results present; skill-authoring 8/8 + 2 refs; tier-consistency ok) |
| `quote_scan` | **PASS** — no potential verbatim quotation |
| `profile_self_check` check-14 body-size | **WARNING** — 998 words (>800 budget; FAIL threshold >1000, not crossed) |
| injection-scan | 7 WARN (triage only) — benign frozen-source Hamming prose ("you are now at the lower levels…"); correctly quarantined per untrusted-source-policy, not a defect |
| truncation gates (`…` / severed invariant) | clean — no hits |

**Deterministic FAILs: 0.** The profile lens escalated body-size to "must-fix pending
mechanical verification"; the deterministic tool resolves it to **WARNING (998w)** —
should-fix, not FAIL.

## Consolidated findings (deduped across lenses; most-severe first)

### should-fix

1. **Profile body over budget — `profile.yaml` (check-14 field set)**
   998 words vs 800 budget (198 over); only 2 words under the >1000 FAIL cutoff, and it has
   drifted up across v1.3.0/v1.4.0 with no compensating trim. No headroom.
   *Fix:* trim heaviest sections — `quality_bar` (193w) and `when_not_to_use` (148w) — under 800.

2. **`when_to_use[4]` invites "produce the study design" misread — `profile.yaml:31-32`**
   (carried unaddressed from prior r3 #12). "Designing or reviewing an empirical study, metric,
   or measurement for soundness" sits adjacent to forbidden "running the study for the caller."
   *Fix:* "Advising on or reviewing the design of an empirical study, metric, or measurement
   for soundness."

3. **Evaluator-side scope undeclared — `profile.yaml` (skill-8 always_on vs when_to_use/when_not_to_use)**
   `evaluation-metrics-and-research-judgment` always_on covers ranking *other people* for scarce
   roles (committee side), but when_to_use/when_not_to_use only scope the researcher's *own*
   decisions. The process-help vs outcome-decision line near `forbidden_behaviours` is undrawn.
   *Fix:* add a when_to_use bullet for "advising on designing a fair, gameability-checked
   evaluation/ranking process the caller does not personally decide," plus a when_not_to_use
   reinforcement that the advisor never renders the ranking or outcome.

4. **Missing worked examples for 5 of 8 skill areas — `profile.yaml` examples**
   Examples cover only problem-selection, experimental-design, adviser-choice. No input→output
   model for early-career-negotiation, funding-grants, presenting, evaluation-metrics,
   writing-and-publishing.
   *Fix:* add one short worked example per uncovered skill, following the existing 3-example pattern.

5. **Reference paths not Markdown links — all 8 `skills/*/SKILL.md` References**
   (carried unaddressed from prior r3 #11). Paths rendered as inline code
   (`` `../../references/...md` ``), not links; an unlinked resource is never loaded by
   progressive disclosure.
   *Fix:* convert to `[research-career-principles-index.md](../../references/research-career-principles-index.md)`
   (+ evidence-notes equivalent) in all 8 files.

6. **Negative-routing test gap — `tests/golden-tests.yaml`**
   (carried unaddressed from prior r3 #10). Only NR-001 (produce-the-paper) + NR-002
   (pure domain-science). No coverage for the two most collision-prone sibling exclusions.
   *Fix:* add NR-003 (craft-writing → `research-writing-advisor`) and NR-004
   (integrity/fabrication → `research-integrity-reproducibility-advisor`), both `do_not_invoke`.

7. **Faithfulness coverage gap — `reports/faithfulness-report.yaml`**
   (carried partially from prior r3 #6). No `rule_ref` entries for `when_not_to_use[*]`, `role`,
   or `router_description`. `when_not_to_use` carries the sibling-routing claims and has never
   been over-claim-audited.
   *Fix:* add coverage entries for `when_not_to_use[0-5]`, `role`, `router_description`.

8. **Duplicated boilerplate across all 8 skills — `skills/*/SKILL.md` `## Output` + `## Provenance`**
   Three-mode output description and full four-source provenance paragraph copy-pasted verbatim
   into every skill; both already live in `profile.yaml` (charter, always loaded). ~15-20 dup
   lines/skill.
   *Fix:* trim `## Output` to a one-line pointer to the mode contract; trim `## Provenance` to
   `Derived from P0xx…; see provenance-ledger.md`.

9. **Role coherence — career identity vs bundled empirical-methods scope**
   3 of 8 skills are pure empirical-methods/statistics (problem-selection, experimental-design,
   evaluation-metrics) with no necessary career dimension; the *name* signals only "career," so a
   methods-only caller has nothing to key off (only the router description carries it).
   *Fix:* either surface the dual scope in the identity (e.g. rename
   `research-strategy-and-methods-advisor`) OR add one Role sentence stating the fusion is
   deliberate and confirm the router description is the durable discoverability mechanism.

10. **Reciprocal routing missing (family-level) — sibling profiles**
    `research-career-advisor` routes craft-writing/integrity out to the two siblings, but neither
    `research-writing-advisor` nor `research-integrity-reproducibility-advisor` names
    `research-career-advisor` back for career/adviser/funding/job-market questions (grep: 0 hits).
    Routing graph is asymmetric. *Out of scope for this package's own profile — blocks full-family
    release-readiness.*
    *Fix:* add symmetric `when_not_to_use` + `handoff_rules` entry to both sibling profiles;
    re-export/re-version those adapters.

### nice

11. **P044 qualifier dropped (SCOPE_BROADENED) — `profile.yaml` `always_on[5]` funding block**
    Profile: creativity judged "rather than novelty, execution difficulty, or **popularity** alone";
    P044 says "immediate popularity alone." The source hedge "immediate" was removed.
    *Fix:* restore "…or immediate popularity alone."

12. **Dense description fields — `research-program-and-problem-selection`, `evaluation-metrics-and-research-judgment` SKILL.md**
    ~14 / ~10 lines of semicolon-joined prose (under the 1024-char ceiling), content restated in
    body `## When to use`.
    *Fix:* tighten description to strongest trigger + primary "Not for"; leave sub-cases to body.

13. **Skill frontmatter carries full provenance block — all 8 SKILL.md**
    `provenance:` (principles/claims/evidence/anchors/digest) beyond name+description on every skill;
    weight depends on whether discovery indexes full frontmatter.
    *Fix:* confirm adapter-export discovery parses only name/description; if so move bookkeeping to
    body/manifest.

14. **Role paragraph mixes identity with inline self-justification — `profile.yaml` Role**
    "Empirical-methods and evaluation review belong inside this remit…" defends the scope-bundling
    inside the identity statement.
    *Fix:* if scope kept, move the justification to `source_of_truth_policy` / a design note.

15. **No `compare` mode despite comparison-shaped example — `profile.yaml` modes**
    Modes are advise/review/plan; example 1 ("three possible thesis problems") is a comparison folded
    into advise; sibling advisors use an explicit `compare` mode for this shape.
    *Fix:* optional — add `compare` mode, or leave as-is.

16. **Skill description template inconsistent — 8 SKILL.md**
    (carried from prior r3 #16). 6 use "Guides X. Use when Y."; `presenting-and-engaging-with-research`
    + `early-career-positioning-and-negotiation` invert. Cosmetic.
    *Fix:* normalize to the majority template.

## Verdict

Deterministic gates PASS (one body-size WARNING, non-blocking). The 2 prior-r3 must-fix
(false-citation groundings) are fixed. All four LLM lenses returned **0 must-fix** after
mechanical verification of the one escalated item (998w = WARNING, not FAIL). Remaining findings
are release-quality polish and family-level routing symmetry — no correctness, faithfulness,
tool-boundary, or authority-creep defect survives. Tool boundary (Read/Grep/Glob),
forbidden-behaviours, and outbound sibling routing are sound.

MUST_FIX_COUNT: 0
