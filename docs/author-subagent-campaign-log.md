# Author-Subagent Hardening Campaign Log

Batch run of `/author-subagent` over the `awesome-book-collection` PDFs, processed
**simplest → most complex** (by file size as a length/complexity proxy). Each PDF is
handled by a **fresh subagent** (Claude Opus 4.8, max effort) that:

1. runs the `author-subagent` skill end-to-end on the source PDF,
2. critically reviews the workflow / tooling / skill for defects or improvements
   surfaced during that run,
3. implements the highest-value fix(es) in the factory source,
4. validates (`cli validate` + `make verify`),
5. commits the new package and any factory fixes,
6. appends a dated entry below.

- **Total PDFs:** 165
- **Campaign started:** 2026-06-09
- **Already done before this campaign run:** `domain-driven-design-reviewer`,
  `java-concurrency-reviewer`, `kafka-benchmarking-advisor`,
  `kafka-client-performance-advisor`, `software-design-reviewer`

---

## Processing order (smallest unprocessed first)

| # | Size | Source PDF | Status |
|---|------|-----------|--------|
| 1 | 131 KB | Software Architecture/microservices/MicroservicePatternLanguage.pdf | done (Run 1) → `microservice-patterns-advisor` |
| 2 | 226 KB | System Design/Payment Systems … (1989) | pending |
| 3 | 411 KB | Software Testing/load-testing/k6-guideline.pdf | pending |
| 4 | 498 KB | Operating Systems/a simple, Unix-like teaching operating system.pdf | pending |
| 5 | 526 KB | Soft Skills/negotiating/Never Split the Difference (summary) | pending |
| 6 | 606 KB | Soft Skills/Strengths Finder 2.0 | pending |
| 7 | 643 KB | programming/clean-code/Code Simplicity | pending |

(Order continues by size; table extended as the campaign proceeds.)

---

## Run entries

<!-- Each subagent appends one `### Run N — <slug>` section below, newest last. -->

### Run 1 — microservice-patterns-advisor — 2026-06-09

**Source PDF:** `Software Architecture/microservices/MicroservicePatternLanguage.pdf`
(Chris Richardson, © 2020 Chris Richardson Consulting, Inc., "All rights reserved").
This is the microservices.io **pattern language map** — a one-page taxonomy of the
microservice pattern catalogue, not a prose book.

- **Detected rights:** `distillation-only` (copyright "all rights reserved", no
  open license). Quote scan: clean (no verbatim quotation).
- **Final slug:** `microservice-patterns-advisor` (CREATE NEW).
- **Create/update decision:** create-new. Step 3 search top similarity was **0.24**
  (java-concurrency-reviewer / kafka-client-performance-advisor), far below the 0.55
  "ask" floor and the 0.80 update threshold; no collision with any of the 5 existing
  slugs. Logged and proceeded as create-new per the documented default.
- **Modes:** `advise`, `compare` (both with source evidence; the map presents grouped
  alternative patterns, justifying advise + compare; no produce/review/patch evidence).

**Pipeline outcome**
- Ingestion: `conversion_status=ok`, converter `markitdown`, 1 page, 856 words,
  `is_scanned=False`, `noise_ratio=0.0`. No `needs-ocr` / `needs_auth` / `failed`,
  no human-review-queue entry. (`anchors=0` — the diagram has no Markdown headings;
  expected, not a blocker.)
- Phase 8 self-check (deterministic gate): **PASS** (all checks PASS/INFO, body
  ~610 words). `tests/test-results.md` written.
- `cli validate microservice-patterns-advisor`: **VALIDATION PASSED** (every check OK).
- `make verify`: **OK** — ruff clean, bandit clean, detect-secrets clean,
  pytest **117 passed** (108 prior + the new export regression tests).

**Workflow review (friction points hit this run)**
1. **No sub-agent spawner available.** SKILL Steps 6 & 7 mandate delegation via
   `Agent(subagent_type="source-interrogator" | "profile-deriver")`, but this harness
   exposed no `Task`/`Agent` tool. Applied the SKILL's own documented fallback
   ("write the file in the main thread") for *both* steps: ran the Q1–Q18
   interrogation and the Phase-5 derivation in the main thread, writing
   `interrogation-records.yaml`, `profile.yaml`, `provenance-ledger.md`,
   `CHANGELOG.md`, `README.md`, `tests/golden-tests.yaml` directly, then let the
   deterministic `selfcheck`/`validate` gates (the real authority) verify the output.
   *Gap:* the SKILL handles "agent ran but didn't write the file" but has no explicit
   "cannot spawn sub-agents at all" branch — worth a one-line note in a future skill pass.
2. **Adapter `description` had an unbalanced parenthesis** (the chosen factory fix —
   see below). Reproduced deterministically; affected 4 of 6 packages.
3. The factory sub-agent definitions declare `model: sonnet`; the campaign asks for
   `opus`. Moot this run (no spawner), but a latent mismatch for runs that can delegate.
4. Minor/environmental (not fixed): `extract-sample` output for a 2-D diagram PDF is
   garbled interleaved table fragments (content still recoverable from the ingested
   markdown); every CLI call prints a `RequestsDependencyWarning` (urllib3/chardet)
   on stderr; `fitz`/PyMuPDF is not installed so the last-resort converter is a no-op
   on this machine (markitdown succeeded, so no impact).

**Factory change made**
- `fix: drop dangling unbalanced parenthesis in adapter description` — commit
  **`c26ecc8`**. Added `_drop_dangling_open_paren` in
  `tools/subagent_factory/export_claude_agent.py`, applied at the end of
  `_clean_clause`, so a clause clipped inside a "(...)" group is truncated back to a
  balanced boundary (a balanced inner group is preserved; a dangling outer "(" is
  dropped) and any re-exposed trailing connector is stripped. Added regression tests
  in `tests/subagent_factory/test_export_claude_agent.py`. Strictly non-regressive:
  the 2 already-balanced existing descriptions are unchanged; the 4 broken ones now
  read cleanly (and kafka-benchmarking even regained room for a second well-formed
  trigger). This improves the single most routing-relevant adapter field for the
  whole corpus.

**Packaging / version-control note**
- `subagents/*/` and `.claude/agents/generated/*.md` are **gitignored by design**
  (factory OUTPUT, not source — see `.gitignore` lines 22/26), matching the 5 prior
  packages which are likewise on-disk-only. The new package and its installed adapter
  therefore live on disk, fully validated, but are not committed. Only the factory
  fix + this log are version-controlled, matching prior campaign-commit precedent.
- The 4 existing packages with the old (broken-paren) descriptions were **not**
  re-exported this run (kept the change surgical; their profiles were untouched and
  their installed adapters still match their canonical adapters). They will pick up
  the improved description on their next legitimate re-export. **Follow-up:** re-export
  `domain-driven-design-reviewer`, `kafka-benchmarking-advisor`, and
  `kafka-client-performance-advisor` to refresh their router descriptions.

**Human-review / unauthored stubs left as `status: draft`**
- `subagents/microservice-patterns-advisor/skills/pattern-selection-walkthrough/SKILL.md`
  (STATUS: STUB)
- `subagents/microservice-patterns-advisor/references/microservice-pattern-language-map.md`
  (STATUS: STUB)
- Package stays `status: draft` until both are authored. Recorded evidence gap: the
  one-page map names patterns but gives no per-pattern prose, so per-pattern mechanics
  are out of scope for v0 and must not be fabricated.

### Run 2 — employee-payment-scheme-advisor — 2026-06-09

**Source**
- `awesome-book-collection/System Design/Payment Systems and Performance Improvement_
  Participation in Payment System Design (1989) - Bowey, Angela_ Thorpe, Richard.pdf`
- Actually a 4-page Emerald journal article (*Employee Relations*, Vol. 11 Iss. 1,
  pp. 17–20, DOI 10.1108/EUM0000000001014), **not** software/financial system design.
  Detected rights: **distillation-only** (copyrighted journal, subscription access,
  `permissions@emeraldinsight.com`).

**Role-inference trap (handled correctly)**
- The file sits under `System Design/` but the content is a management / employee-relations
  piece on the **participative design and implementation of employee incentive payment
  (reward) schemes for performance improvement**. Role inferred from the article text
  (extract-sample + full ingested markdown), not from the folder/filename. Slug deliberately
  uses `employee-payment-scheme` to disambiguate from fintech/software payment systems; the
  first `when_not_to_use` exclusion and a `forbidden_behaviour` encode that boundary, and a
  negative-routing golden test (NR-001) locks it in.
- Content was genuinely sufficient for a coherent expert role (~2000 words of recoverable
  body: the participation-over-structure thesis, two named failure modes, the
  participation→productivity→pay relationship, the cross-level participative-group method,
  and the negotiation-boundary rule). Did **not** force a bad package and did **not** stop.

**Create/update decision**
- `search` similarity max **0.13** (`software-design-reviewer`), far below the 0.55 ask /
  0.80 update thresholds. Unambiguous **CREATE NEW**.

**Pipeline outcome**
- `conversion_status=ok` (converter: **markitdown** fallback; Docling unavailable). **Not**
  scanned — no `needs-ocr`. `page_count=5`, `word_count=4748`.
- Phase 8 deterministic `selfcheck`: **PASS** (after trimming the body from 843→797 words to
  clear the 800-word budget — see friction #1 below).
- `cli validate`: **VALIDATION PASSED** (every check OK, including quote-scan = no verbatim
  quotation from the distillation-only source, and adapter-sync).
- `make verify`: **OK** — ruff clean, bandit clean, detect-secrets clean, pytest
  **120 passed** (117 prior + 3 net new self-check tests).
- Stubs scaffolded: 4 skills + 2 references (all `STATUS: STUB`).

**Workflow review (friction points hit this run)**
1. **The 800-word body budget is a per-run tax with no targeting help** (the chosen factory
   fix — see below). `selfcheck` reported only the *total* body word count, so closing the
   `body-size` WARNING was pure trial-and-error: it took ~6 edit/re-run cycles to trim
   843→797 words while blind-guessing which fields were heaviest. Over a 165-book campaign,
   rich sources will routinely exceed 800; this friction recurs every time.
2. **Two-column journal PDF interleaves at the line level** under the markitdown fallback
   (Docling unavailable). Individual sentences came out column-interleaved and the two
   figures were unreadable; the thesis, failure modes, and method were still unambiguous
   from context. Recorded as an evidence gap, not a blocker. (Same class of converter-fidelity
   friction noted in Run 1; fixing it means enabling Docling via `bootstrap`, an environment
   change, not a surgical source fix — out of scope this run.)
3. **Stale cached CLI help in the context index** showed only 5 commands; the live CLI has 10
   (`bootstrap`, `doctor`, `score`, `selfcheck`, `stubs` were missing from the cache). A
   context-mode caching artifact, not a factory bug — verified against the live `--help`.
4. Cosmetic: every CLI call still prints `RequestsDependencyWarning` (urllib3/chardet version
   mismatch); environmental, not factory source.

**Factory change made**
- **What:** `tools/subagent_factory/profile_self_check.py` — when check 14 (`body-size`)
  exceeds the warn/fail budget, the finding message now names the **3 heaviest profile
  sections with their word counts** (e.g. `heaviest: when_to_use 153w, modes 146w,
  quality_bar 132w`) and how many words it is over the 800-word budget. Refactored the body
  fields into a labelled `body_groups` dict; the flattened `body_fields` list (and therefore
  check 13) is byte-for-byte unchanged. **Purely additive to the WARNING/FAIL message** — the
  PASS path, all thresholds, and all verdicts are untouched.
- **Why:** turns closing the most common authoring WARNING from blind trial-and-error into a
  targeted edit. Directly addresses friction #1, which every content-rich run in this campaign
  will hit.
- **Files:** `tools/subagent_factory/profile_self_check.py`,
  `tests/subagent_factory/test_profile_self_check.py` (+3 tests: PASS keeps the compact
  message with no breakdown; over-WARN and over-FAIL both surface the heaviest-section
  breakdown).
- **Non-breaking proof:** all 6 existing packages re-checked — verdicts unchanged. The 4 that
  PASSed still PASS with identical compact messages; the 2 already-WARNING kafka packages
  (911w, 860w) now show the new breakdown but keep their WARNING verdict.
- **Commit:** `ae7bbcc`

**Human-review / unauthored stubs left as `status: draft`**
- `subagents/employee-payment-scheme-advisor/skills/participative-scheme-design-programme/SKILL.md`
- `subagents/employee-payment-scheme-advisor/skills/participative-working-groups/SKILL.md`
- `subagents/employee-payment-scheme-advisor/skills/scheme-subversion-and-decay-diagnosis/SKILL.md`
- `subagents/employee-payment-scheme-advisor/skills/pilot-and-extension/SKILL.md`
- `subagents/employee-payment-scheme-advisor/references/research-base.md`
- `subagents/employee-payment-scheme-advisor/references/cited-literature.md`
- All `STATUS: STUB`; package stays `status: draft` until authored. Evidence gaps recorded in
  the provenance ledger: the source is a condensed 4-page account of a larger research
  programme, so deep procedural detail and the two figures are summarised, not fully
  specified — must not be fabricated.
- **No needs-ocr block this run.**

### Run 3 — k6-load-test-scripting-advisor — 2026-06-09

**Source PDF:** `Software Testing/load-testing/k6-guideline.pdf` — "Most commonly used
terms in K6" by Anshita Bhasin. A single-author cheat sheet / glossary of ~24 numbered
k6 load-testing terms (test lifecycle, VU, iterations, duration, stages, target,
percentiles, checks, metrics, thresholds, status, error, error_code, scenarios, ramping,
ramping-vus executor, requests). Not a methodology book — a reference of k6 script
configuration vocabulary.

- **Detected rights:** `distillation-only`. The PDF has **no license/copyright notice** —
  only "Author: Anshita Bhasin" + a LinkedIn link. Classified conservatively as an authored
  work (copyrighted by default), not `unknown` (see friction #1 / the factory fix). Quote
  scan: clean (no verbatim quotation).
- **Final slug:** `k6-load-test-scripting-advisor` (CREATE NEW).
- **Create/update decision:** create-new. Step 3 search top similarity **0.28**
  (`java-concurrency-reviewer`), then `kafka-benchmarking-advisor` **0.24**. The flagged
  0.55–0.79 band vs `kafka-benchmarking-advisor` did **not** trigger (0.24, far below the
  0.55 ask floor and 0.80 update threshold). No collision with any of the 7 existing slugs.
- **Modes:** `advise`, `compare` (both with source evidence). `advise` — the whole doc
  explains/recommends k6 options configuration. `compare` — the source explicitly contrasts
  P90 vs P95, the four metric types (Counters/Gauges/Rates/Trends), and checks vs thresholds
  ("the only difference in checks is that a failed test case does not halt execution"). No
  review/validate/produce/extract/patch-suggest — the glossary defines and contrasts concepts
  but presents no procedure for auditing or gating an existing script (logged as an evidence gap).

**Pipeline outcome**
- Ingestion: `conversion_status=ok`, converter `markitdown` (Docling unavailable),
  `page_count=16`, `word_count=1233`, `is_scanned=False` (pdftotext recovered 2195 words of
  real text — the markitdown word-gluing is a spacing artifact, **not** OCR garbage),
  `anchor_count=0` (the cheat sheet uses "(1) Term" labels, not Markdown headings; expected
  for this format, not a blocker). No `needs-ocr` / `needs_auth` / `failed`.
- Phase 8 deterministic `selfcheck`: **PASS** (body ~687 words, under the 800 budget on the
  first pass; 5 triggers, 3 exclusions, 4 evidence-citing quality-bar checks, 3 golden + 1
  negative).
- `cli export` + `cli stubs`: adapter installed; 4 skill stubs + 1 reference stub written.
- `cli validate`: **VALIDATION PASSED** (every check OK — adapter-sync matches canonical,
  Phase 8 PASS, quote-scan clean).
- `make verify`: **OK** — ruff clean, bandit clean, detect-secrets clean, pytest **120 passed**.

**Workflow review (friction points hit this run)**
1. **Rights-classification contradiction for unlicensed authored works** (the chosen factory
   fix — see below). `SKILL.md:39` mapped "no copyright notice found → `unknown`", while
   `rights-and-quotation-policy.md:12` defines `unknown` as **"block distillation until
   resolved"**, and `SKILL.md:140` sets the Step 5 default to `distillation-only`. This source
   (an authored cheat sheet with no license line) lands exactly in that contradiction: the
   skill literally tells you to mark it `unknown` → which **blocks the pipeline**. The CLI does
   not enforce the block (it just records the rights string), so the deterministic gates do
   **not** catch this — it is purely a decision trap that the agent must resolve by improvising.
   Over a 165-book copyrighted collection (none of which ship explicit license notices) a literal
   run would halt on the majority. Resolved this run by classifying conservatively as
   `distillation-only`.
2. **Rights not always detectable from `extract-sample`.** When a source carries no notice at
   all (as here), there is nothing in the sample to detect — the decision is "absence of a
   notice", which the skill did not previously give a rule for. Folded into fix #1.
3. Cosmetic/environmental (not factory source, unchanged from prior runs): every CLI call
   prints `RequestsDependencyWarning` (urllib3/chardet mismatch) on stderr; Docling is not
   installed so markitdown is the converter (fidelity is adequate here — the content is plain
   prose + small code blocks). `fitz`/PyMuPDF last-resort converter remains a no-op on this box.
4. **No sub-agent spawner** (as in Runs 1–2): ran Steps 6 & 7 in-thread per the SKILL's
   documented no-spawner branch (now explicit since `3f11980`). Wrote `interrogation-records.yaml`,
   `profile.yaml`, `provenance-ledger.md`, `CHANGELOG.md`, `README.md`, `tests/golden-tests.yaml`
   directly; the deterministic `selfcheck`/`validate` gates verified the output. No friction —
   the branch is now clearly documented.

**Factory change made**
- **What:** Replaced the single ambiguous bullet `No copyright notice found → unknown` in
  `author-subagent/SKILL.md` Step 2a with an explicit decision tree: an **authored work with no
  explicit license** → `distillation-only` (copyrighted-by-default conservative floor; record
  the "no notice" observation in the provenance ledger), and reserve `unknown` for genuinely
  unattributable provenance. Added a blockquote stating that **`unknown` is a blocking state, not
  a value to pass through** — never `ingest --rights unknown`; resolve to `distillation-only`
  first (which is why Step 5's default is `distillation-only`, never `unknown`).
- **Why:** Removes a real, repeatable contradiction between the skill and the rights policy that
  would otherwise (per a literal reading) block distillation on most of the book collection. The
  deterministic gates cannot catch it because the CLI does not enforce the block — so the fix has
  to live in the decision documentation.
- **Paths:** `.claude/skills/author-subagent/SKILL.md` (Step 2a). Documentation-only — no Python,
  schema, or template touched, so the 7 existing packages and all 120 tests are unaffected
  (`make verify` green).
- **Commit:** `75976ae`

**Human-review / unauthored stubs left as `status: draft`**
- `subagents/k6-load-test-scripting-advisor/skills/k6-options-and-stages-configuration/SKILL.md`
- `subagents/k6-load-test-scripting-advisor/skills/k6-thresholds-and-checks/SKILL.md`
- `subagents/k6-load-test-scripting-advisor/skills/k6-scenarios-and-executors/SKILL.md`
- `subagents/k6-load-test-scripting-advisor/skills/k6-metrics-interpretation/SKILL.md`
- `subagents/k6-load-test-scripting-advisor/references/k6-terminology-glossary.md`
- All `STATUS: STUB`; package stays `status: draft` until authored. Evidence gaps recorded in the
  provenance ledger: no license notice (rights set conservatively); modes limited to advise +
  compare; downstream owner inferred (the k6 script owner). Source is undated and defers to the
  official k6 docs (k6.io) for the full metrics reference — option/metric names should be
  re-verified against current k6 releases (annual cadence).
- **No needs-ocr block this run.**
