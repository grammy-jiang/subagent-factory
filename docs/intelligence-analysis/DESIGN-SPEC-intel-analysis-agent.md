# Design-spec — Intelligence-Analysis AI Agent (companion to BLUEPRINT-…md)

> The *how* extracted from the blueprint so the blueprint stays implementation-neutral. Derived from four
> domain-advisor reviews (agent-skills, mcp-quality, mcp-security, ai-agent-engineering; full transcripts
> in this session's task outputs). This document is design-spec, not blueprint — it realizes the
> blueprint's decisions. Do not treat any item here as settled scope; each phase's build reads its
> section here and validates against the blueprint's decisions + success criteria.

## Layer 1 — SKILLS (4)
1. `structured-analytic-techniques` — ONE skill, internally re-layered: `SKILL.md` body = master loop +
   stage router (frame → hypotheses → ACH → key-assumptions check → judgment → pre-mortem); push each
   technique's mechanics to `references/{ach,key-assumptions-check,premortem}.md` (loaded on demand).
   Description enumerates technique names/synonyms AND natural triggers ("intelligence assessment",
   "competing hypotheses", "likelihood/estimate") — analysts don't speak jargon. Absorbs confirmation-bias
   / mirror-imaging checks at the hypothesis-gen + key-assumptions steps.
2. `calibrated-forecasting` — probabilistic judgment, Fermi decomposition, updating; absorbs the
   anchoring/availability/overconfidence checklist as a pre-commit self-check; bundle a small
   deterministic script for compound-probability arithmetic (don't do that math via token generation).
   Brier/persistence lives in the calibration-tracker MCP, not the skill.
3. `osint-investigation` — WHEN/WHY/HOW to search+verify; must NOT restate osint-toolkit mechanics in
   prose; routes grading through `source-evaluation` at the archiving step; delegates large verification
   fan-outs to a forked context/subagent (only the verified conclusion re-enters main context).
4. `source-evaluation` — reliability (A–F) + credibility (1–6) grading for ANY sourced item (HUMINT or
   OSINT). Grading (skill) stays separate from persistence (evidence-ledger MCP).
Governance: `allowed-tools` per skill (web fetch/search for osint-investigation; likely none for
calibrated-forecasting/source-evaluation). `osint-investigation` = explicit-invocation only + a
deterministic (hook/permission) block for high-risk taskings (searching a named private individual) —
prose reminder is not sufficient. No sensitive data in skill definitions.

## Layer 2 — SUBAGENTS (2)
1. `analytic-tradecraft-reviewer` (Heuer/Kahneman/SAT/Jervis) — devil's advocate. Receives RAW case state
   (evidence rows, ACH matrix, source grades) enforced read-only at the MCP-permission layer, NOT the
   agent's narrative. On re-review, re-feed prior review notes (subagents cold-start).
2. `deception-detection-reviewer` (Masterman/Jervis D&D) — deferred (needs a real evidence chain).

## Layer 3 — MCP servers
Shared contract: analyst/skill supplies the JUDGMENT value (grade/rating/probability) as a REQUIRED
INPUT; the tool validates-against-scale, computes the derived result, persists. Append-only + hash-chained
records; corrections = superseding entries. Shared `case_id` (+ `analyst_id`, `forecast_id`,
`evidence_id`). Structured `is_error=True` results, never silent empty/wrong. Read-back (`list_*`,`get_*`)
ops are required. Verify per-tool: calibration/ach = deterministic code tests vs hand-computed fixtures
FIRST; osint connectors = against REAL services, not mocks. Cross-server: an evidence grade revision marks
dependent ACH cells stale and forces re-score before the matrix reads.
- **calibration-tracker** — build FIRST (impossible without persistent state). Ops: `log_forecast`,
  `resolve_forecast`, `get_calibration_report`, `list_forecasts`. Entity-keyed by `forecast_id`/
  `analyst_id`/`case_id` (a forecast resolves months later → not session-scoped). Lock probability+question
  at commit; only outcome appended. Access = analyst + authorized reviewers (personal performance record).
  Schedule periodic reflection over history + a whole-agent calibration eval (Tetlock questions).
- **evidence-ledger** — per `evidence_id` ↔ `case_id`; append-only grade history. Ops: `add_evidence`,
  `update_grade`, `get_evidence`, `list_evidence`. Carries a PII/classification/redaction field
  (source-identity compromise = life-safety). Collection stores raw (hash+timestamp, no trust judgment);
  grade is analyst-confirmed before ach-engine trusts it.
- **ach-engine** — build LAST (most ambiguous boundary). Per `case_id`, incremental. Cell consistency
  ratings ELICITED from model/analyst (inputs); tool = score, rank by least-total-inconsistency, flag
  diagnostic evidence. Ops: `update_matrix`, `score_matrix`, `get_matrix`.

## Layer 4 — OSINT (security-gated before any live connector)
`osint-toolkit` = PRIMITIVES ONLY: `search(query, connector)` (one tool, connector param — NOT one per
source), `extract_exif`, `compute_hash`, candidate-only `reverse_image_search`/`get_map_tile`. Archive
output writes a provenance field INTO evidence-ledger (no second custody store). Geolocation *verification*
is a workflow → the `osint-investigation` skill, not the tool.
Vision/coordinate contract: explicit semantic-role/modality/coordinate-reference-frame fields on every
geo/image output; EXIF DMS→decimal conversion + any resizing INSIDE the tool contract (no out-of-band
scripts); runtime validators that let the caller halt/replan on misaligned data.
Security controls (all ship together): (a) osint-toolkit = SOLE internet egress; ledger/ach/calibration
have none by default; (b) allowlist outbound destinations; (c) SSRF defenses on every resolved URL (block
private/reserved/link-local/metadata IPs, HTTPS-only, re-validate post-DNS-resolution); (d) every return
(text AND image metadata) is inert data, never instruction; osint-toolkit's writes to the ledger are
untrusted PROPOSALS gated by analyst confirmation, never a trusted internal RPC. Resource quotas +
circuit-breakers on metered calls. Deployment surface must support live network.

## Test techniques
Deterministic-fixture tests (hand-computed Brier scores, ACH rankings) gate trust before any LLM-judge.
evidence-ledger verifies via schema/enum conformance. osint connectors evaluate against real services
(rate limits, dead links, schema drift are the authentic failure modes). Whole-agent eval per phase gate.
