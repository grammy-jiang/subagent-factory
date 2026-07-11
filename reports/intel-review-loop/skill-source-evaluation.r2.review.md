# Review (r2): `source-evaluation/SKILL.md`

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/source-evaluation/SKILL.md`
**Grounding:** `docs/intelligence-analysis/PIPELINE-grounded.md`
**Lens 1 — agent-skills-advisor:** SKILL.md authoring quality (a METHOD skill, not a reviewer).
**Lens 2 — ai-agent-engineering-reviewer:** the skill as an executable agent METHOD — procedure soundness, delegation correctness, over-reach, handoff contracts.

Two independent passes. Both cross-checked citations against source `principles.yaml` / `references/grounding.md` and found the analytic procedure sound and accurately grounded. All findings below are about **method mechanics and skill-authoring hygiene**, not the analytic content. Findings that overlap between lenses are merged.

---

## MUST_FIX

### M1 — Grade revision (proc Step 6) has no persistence path; will error against the real tool contract *(engineering)*
Proc Step 6 requires revising the already-written Step-3 grade after corroboration / plantability findings. The **Persistence** section names only `grade_evidence`. Per `mcp_servers/evidence_ledger/server.py:60-95`, `grade_evidence` **errors if a grade already exists** — the revision path is a distinct tool `update_grade` (requires a `reason` arg; appends a superseding grade, never edits). The skill never mentions `update_grade`, so an agent following Persistence literally either hits a hard tool error on the second write or silently leaves the ledger holding the pre-revision grade.
**Fix:** Persistence must state — *"If proc Step 6 revises the grade after it was already written, call `update_grade` (not `grade_evidence` again) with a `reason` capturing what changed."*

### M2 — `judgment_source` (required, trust-gating) is never set by the procedure *(engineering)*
`grade_evidence`/`update_grade` require `judgment_source: "model_draft" | "analyst_confirmed"` (`server.py:65,85`). It is **self-asserted, not server-verified**, gates whether the grade feeds the cross-case trust record and whether `ach-engine.score_matrix` will trust the cell. The skill names the field once in passing but never says which value to pass. This skill runs **before** the Step-10 human-approval gate, so anything but `model_draft` violates `structured-analysis` invariant 1 and can poison the source-trust record.
**Fix:** state explicitly — *"Pass `judgment_source=\"model_draft\"` for every grade this skill produces; `analyst_confirmed` is set only by the human-approval gate, never here."*

### M3 — `source-trust-registry` store framing contradicts both the real architecture and the orchestrator's capability contract *(engineering + skills, merged)*
Two coupled problems:
- **Architecture:** Persistence frames `source-trust-registry` and `evidence-ledger` as *"two distinct MCP stores."* Per `docs/design/phase3-mcp-design.md:36`, source-trust-registry is **folded into evidence-ledger as a cross-case read (not a separate server)**; `get_source_history` is one tool on the `evidence-ledger` server (`server.py:116-121`). There is no `source-trust-registry:get_source_history` namespace.
- **Availability:** the deployed orchestrator `structured-analysis/SKILL.md` lists `source-trust-registry` under **"Deferred (not in this phase)"** and whitelists only `evidence-ledger:add_evidence, evidence-ledger:grade_evidence` in `allowed-tools` — not `get_source_history`. As written, proc Step 2's "call `get_source_history` first" cannot execute under that permission set.

The two skills currently disagree about whether this read exists and under what name — a real handoff break.
**Fix:** reconcile — either (a) update `structured-analysis` `allowed-tools` + Deferred section to add `evidence-ledger:get_source_history` and drop "not built," or (b) make proc Step 2 conditional (*"if `evidence-ledger:get_source_history` is enabled this phase; else grade from present evidence alone and note the gap"*). Correct the framing to **one server (`evidence-ledger`), two tool categories**: cross-case `get_source_history` read + per-case `add_evidence`/`grade_evidence` write.

### M4 — `allowed-tools` frontmatter is missing entirely *(skills)*
Frontmatter has only `name` + `description`, yet the body calls three MCP tools across the stores in M3. Sibling skills declare them: `structured-analysis/SKILL.md:4` grants the same `evidence-ledger` tools; `calibrated-forecasting/SKILL.md:4` grants its MCP tool. Per [P048], an undeclared tool risks being unavailable or forcing a per-call confirmation prompt.
**Fix:** add `allowed-tools:` listing exactly the tools the reconciled M3 decision keeps — e.g. `evidence-ledger:get_source_history, evidence-ledger:add_evidence, evidence-ledger:grade_evidence, evidence-ledger:update_grade`. (Note: the correct namespace and the `update_grade`/`get_source_history` membership depend on the M1–M3 fixes — resolve those first, then declare.)

### M5 — In-body tool references are unqualified (bare name), not `server:tool` *(skills)*
Proc Step 2 writes `get_source_history(source_id)`; Persistence writes `add_evidence`, `grade_evidence` — no server prefix, despite straddling (per M3) multiple tool categories. [P056] requires fully-qualified `ServerName:tool_name` to avoid ambiguous dispatch when multiple MCP servers exist; `structured-analysis` already writes them qualified (`evidence-ledger:add_evidence` etc.).
**Fix:** rewrite every in-body reference as `evidence-ledger:get_source_history(source_id)`, `evidence-ledger:add_evidence`, `evidence-ledger:grade_evidence` (+ `update_grade` per M1).

### M6 — The A–F / 1–6 grading scale is defined only at its endpoints *(skills)*
The skill's entire deliverable is a standardized, repeatable grade, but only A/E/F and 1/5/6 are named — B/C/D and 2/3/4 appear nowhere in the package (nor elsewhere in the repo). This invites run-to-run invention of middle-band wording, defeating the skill's own "grade consistently, regardless of fit" guardrail. [P014]/[P047]: state the recipe concretely enough to work across models, not by parametric recall of FM 2-22.3.
**Fix:** spell out the full 6-point scale for both axes — inline in proc Step 3 (one line each) or in a small `references/grading-scale.md` linked from Step 3, sourced from the FM 2-22.3 claim already cited.

---

## SHOULD_FIX

### S1 — "Step-8 deception-reviewer" is the wrong step number in the deployed pipeline *(engineering)*
Output section points at "the Step-8 deception-reviewer." That matches the abstract 12-step `PIPELINE-grounded.md`, but in the deployed `structured-analysis/SKILL.md` the `deception-detection-reviewer` runs under **Step 7** ("Independent critique"); Step 8 there is "Loop back and revise." A live reader lands on the wrong step.
**Fix:** point at the deployed numbering — *"confirmed by the `deception-detection-reviewer`, run under Step 7, gated on a security review."*

### S2 — Internal 1–7 procedure numbering collides with pipeline/orchestrator step numbers *(engineering)*
The skill's own 7-step procedure, `PIPELINE-grounded.md` (12 steps), and `structured-analysis` (11 steps) all use bare "Step N." Internal refs ("revise the Step 3 grade," "Step 6") sit beside external ones ("Step-3 grading method," "Step-8 deception-reviewer") with no distinguishing prefix — a live source of misreads (compounds S1).
**Fix:** prefix external refs ("pipeline Step 3", "structured-analysis Step 7") and letter/rename the internal list (e.g. "grading step 3 of 7") so the two numbering spaces never collide unlabeled.

### S3 — "carry each into the matrix as evidence in its own right" overstates this skill's write scope *(engineering)*
Proc Step 7 says finalized absence records are "carried into the matrix." Writing ACH cells is `ach-engine:rate_cell`, owned by pipeline Step 4; Persistence only writes to `evidence-ledger`. As worded it reads like this skill populates the matrix.
**Fix:** reword to *"...and include each in the EvidenceItem[] output so the Step-4 ACH-matrix build treats it as evidence in its own right"* — output, not a direct write.

### S4 — No worked input→output example *(skills)*
Has `## Inputs` / `## Output` shape sections but no concrete one-item walk-through (raw report → graded EvidenceItem) across classify → grade → diagnosticity → corroborate → deception-check → finalize. [P014]/[P059]/[P046] call for a worked example for a procedure this nuanced (two independent axes + provisional→final revision across three steps).
**Fix:** add a short worked example inline or as `references/example.md`.

### S5 — `description` frontmatter carries no explicit boundary/exclusion clause *(skills)*
All three "when not to use" exclusions (produce the judgment / critique an existing grade / collect the OSINT) live only in the body, read only *after* the description has already triggered a load. [P002]/[P049]: the description is the sole discovery-time signal and should carry scope boundaries.
**Fix:** append e.g. *"; not for producing the analytic judgment, critiquing an existing grade, or collecting the raw material."*

---

## NICE

- **N1** *(engineering)* — "owning HUMINT authority" (proc Step 6 boundary) references a component absent from `PIPELINE-grounded.md` and the deployed roster. Correctly restrictive, but the handoff target is unnamed — name the concrete owner or drop the aside.
- **N2** *(engineering)* — proc Step 5's corroboration query could name the backing tool `evidence-ledger:list_evidence(case_id, ...)` (`server.py:108-113`), matching the mechanical precision used elsewhere.
- **N3** *(skills)* — minor A–F/1–6 restatement duplication between proc Step 3 and `## Output`; acceptable as an I/O contract, could tighten.
- **N4** *(skills)* — `description` is dense (~72 words / 6 clauses); within limits, could trim for token economy.

---

## Preserve (not findings)
Scope discipline is strong on both lenses: correctly defers collection to `osint-investigation`, defers bias/method/deception critique to reviewer subagents without invoking them, treats its grade and deception flag as **provisional** (respecting the Step-8/Step-7 reviewers and the human gate), uses F/6 "cannot be judged" as built-in handling for ungradeable evidence, and never touches the human-approval gate or loop-back — those stay with `structured-analysis`. Cross-package principle citations `(method P009)`, `(bias P001/P022/P073)` were spot-checked and match their source statements exactly. Progressive disclosure is well-executed (93-line body, per-step traceability in `references/grounding.md`).

The six MUST_FIX items are all about the **mechanics of declaring, persisting, and revising the grade**, plus the undefined mid-scale — not the analytic method, which is sound.

MUST_FIX_COUNT: 6
