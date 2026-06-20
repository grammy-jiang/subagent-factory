# Resume + polish + gap-close — knowledge-fusion research report (unattended)

You are a fresh autonomous research engineer. There is NO human watching: never ask, never wait;
apply the documented default, note it, and proceed. Permissions are pre-approved — just act.

## What this is — NOT a from-scratch run
An existing knowledge-fusion research run already completed and **validated PASS 0.83** (19 papers).
Your job is two things: **(A) polish** the degraded final report, and **(B) close two HIGH academic
gaps** the prior run could not close because the pipeline's arXiv search is recency-locked (~2026).

- Working directory: THIS folder (the `knowledge-fusion-conflict-detection` topic folder).
- Canonical complete run: **run_id `57e857a93e69`** — good synthesis artifacts already exist at
  `57e857a93e69/summarize/` (`synthesis.md`, `synthesis_report.md`, per-paper `*.summary.json`) and
  `57e857a93e69/analysis/`. Those 19 paper IDs are the prior corpus. Do NOT re-search them.
- Problem: the top-level `cross-document-...-research-report.md` rendered in **template-fallback** —
  it is full of `structured LLM extraction` / `not_reported` placeholders, ~171 auto `CON-###`
  negation-spam lines, and empty Assumption/Operational/Design sections. The research is fine; the
  report FILE is not.

## Read first (fresh from disk)
- `~/.claude/skills/research-pipeline/SKILL.md` + references: `command-reference.md` (the exact
  `expand` / paper-id injection flags + MCP tool map), `iterative-synthesis.md` (gap-closure rounds),
  `output-templates.md` + `final-report-contract.yaml` (report shape), `troubleshooting.md` (if
  structured extraction falls back again).
- This folder's prior `SUMMARY.md` and `gaps.json` (the real findings + the open gaps G1/G3).
- **Always launch via the runner; never bypass it.** Honor reviewer `rejected` gates (fix → reset to
  pending → re-run; never override).

## JOB A — polish the report
Regenerate the final report from the canonical run's synthesis artifacts (resume-on-top:
`research-pipeline report` for run_id `57e857a93e69`, or `runner.py --run-id 57e857a93e69 --state ...`).
Snapshot the old report to `cross-document-...-research-report.2026-06-20.md` before overwriting.

**Acceptance (HARD).** The regenerated report MUST be substantive. It MUST NOT contain any of:
the literal `structured LLM extraction` placeholder, a `not_reported`-filled Evidence Matrix, auto
`CON-###` negation-spam, or empty Assumption / Operational / Design sections. If it still falls back,
the analyze/summarize stage was optimistic-accepted WITHOUT running — drive it explicitly: run the
`paper-analyzer` / `paper-synthesizer` sub-agents with their printed contracts, and only mark a task
`accepted` AFTER its tool actually produced the artifact. Then regenerate and re-check.

## JOB B — close G1 and G3 by arXiv-ID injection (recency-lock workaround)
The pipeline arXiv search returns only ~2026 papers, so rounds 2–3 found 0 foundational papers for
these two gaps. **Bypass the search by injecting specific foundational papers by arXiv ID** (direct
ID fetch/download is NOT recency-locked).

1. For each gap, identify the canonical FOUNDATIONAL papers BY TITLE using your OWN web/arXiv access
   (NOT the locked pipeline search). **Verify every arXiv ID resolves to the real paper before using
   it — do NOT invent IDs; skip any you cannot verify.**
   - **G3 — cross-document contradiction detection across independent documents:** DocNLI;
     cross-document NLI; stance detection across documents; long-document / cross-document
     contradiction & knowledge-conflict benchmarks.
   - **G1 — reconciling normative / prescriptive principles ("prefer X" / "avoid Y"):** truth
     discovery for subjective / opinion claims; social-choice / preference aggregation; AGM belief
     revision & belief merging.
2. Inject the verified IDs into the corpus with the skill's documented mechanism
   (`research-pipeline expand --paper-ids <id1,id2,...>` — confirm exact flag in
   `command-reference.md`), then download + convert + **analyze** them (paper-analyzer) so they carry
   real structured extraction.
3. Run gap-closure round(s) per `iterative-synthesis.md`: new `run_id`, `context.prior_paper_ids` =
   the 19 canonical IDs, `--profile standard`, via `runner.py --state workflow_state.json`. Integrate
   the injected papers, re-summarize, and regenerate the report so **G1 and G3 are RESOLVED (with
   citations to the injected papers) or explicitly RECLASSIFIED** (e.g. ACADEMIC-HIGH → resolved, or
   → ACADEMIC-LOW with reason). Engineering gaps stay resolved inline. Respect the 4-round hard cap.

## Output / sandbox (HARD)
- Every artifact stays in THIS folder. The only permitted external location is the shared `~/.cache`
  pipeline cache (PDF + SQLite index). Do NOT edit, create, or delete anything in the
  subagent-factory repository.
- Write the final report only after `validate-report` is `accepted`.

## When done — ALWAYS, as the final action
Update `SUMMARY.md` with: final report filename; the Round History table (incl. the new injection
round(s)); every remaining open gap (classification + severity + one-line why); and the 5–10 findings
most relevant to the downstream use — Step-7 multi-source synthesis = merging distilled principles
(align/dedup → detect-contradiction → reconcile), each with paper IDs. Then print exactly:

RESEARCH RUN COMPLETE: <report filename>
