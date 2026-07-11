# Review — calibration_tracker MCP server (r1)

**Target:** `intelligence-analysis-agent/mcp_servers/calibration_tracker/{server,store,models}.py`
**Type:** FastMCP (2.13.1) stdio server — append-only hash-chained calibration/forecast ledger.
**Reviewers:** mcp-protocol-advisor · mcp-security-advisor · mcp-quality-advisor · python-reviewer (+ orchestrator verification).
**Scope:** REVIEW ONLY — no edits made. `common.py`/`staleness.py` not imported by this server (only `models`/`store`), so not in scope.

## Test gate

```
cd intelligence-analysis-agent && python -m pytest tests/ -q
74 passed in 0.80s
```

No test FAILs → no test-driven must-fix.

## Orchestrator verifications (disputes resolved)

- **Cross-thread sqlite crash (protocol-advisor MUST-FIX) → DOWNGRADED to should-fix.** The advisor claimed FastMCP defaults to `run_in_thread=True` and offloads sync tools to a threadpool, so the module-level `check_same_thread=True` connection would raise `sqlite3.ProgrammingError` on every stdio call. Verified against the installed FastMCP **2.13.1**: `grep` for `run_in_thread`/`to_thread`/`threadpool`/`check_same_thread` across the package = **none**; `FunctionTool.run` invokes the sync fn directly in the event-loop thread (only `await`s if awaitable). Empirical: in-memory client ran the tool on the **main thread** (`tool thread == main? True`). So no cross-thread ProgrammingError in this version. Real residual risk (multi-process / future async dispatch / chain-fork) is kept as **S1**.
- **Manifest whole-chain-deletion gap (python + security MUST-FIX) → CONFIRMED.** Independently reproduced: `_check_manifest` returns `(True, None)` when `os.path.exists(manifest_path)` is False, and only iterates tables present in the surviving manifest lines. Deleting the manifest file (or a table's lines) alongside the DB rows passes `verify_chain` silently — defeating the store docstring's stated "whole-chain-deletion detection." This is **M1**.

---

## MUST-FIX (1)

### M1 — Manifest is not tamper-evident; whole-chain-deletion detection is defeated
`store.py:97-101` (`_append_manifest`), `store.py:386-402` (`_check_manifest`)
The external manifest exists specifically to catch chain truncation/whole-chain deletion, but:
- **(a) Vacuous pass on missing file/table.** `if not self.manifest_path or not os.path.exists(...): return True, None`, and the check only loops over tables that still appear in the manifest. Deleting the manifest file — or all lines for one table — while deleting the matching DB rows passes `verify_chain(ok=True)`. A table whose rows are gone reads `heads[table]==GENESIS` and is never checked.
- **(b) Same trust domain, not self-chained.** `manifest.jsonl` is a plain appendable file with no per-entry hash-chaining and no separate trust boundary from the SQLite DB. Anyone with the filesystem write access needed to truncate the DB (the exact threat) can rewrite the manifest tail in lockstep.

**Fix:** require every table with `heads[table] != GENESIS` to have a matching manifest entry; treat a missing manifest file/table as `ok=False`, not vacuously `True`. Hash-chain manifest entries (include prev-manifest-hash per line) and/or write the manifest to a separate trust domain (remote append-only log / WORM / syslog); document residual risk if only self-chaining is added.

---

## SHOULD-FIX

- **S1 — Non-atomic head-read→INSERT + single shared connection (chain-fork risk).** `store.py:58`, `151-163`, `212-219`, `235-241`; `server.py:32`. `_head()` (SELECT) and the following INSERT are separate statements; a second writer on the same `db_path` (another process, or any future concurrent/async path) can commit between them, so two rows reference the same stale `prev_hash` → permanent chain fork that trips `main()`'s refuse-to-serve gate. Connection is a module-level singleton with `check_same_thread=True` and no lock. *(Not the runtime crash the protocol advisor claimed for 2.13.1 — see verifications — but the concurrency hazard is real.)* **Fix:** wrap head-read + insert in `BEGIN IMMEDIATE … COMMIT`, or serialize all writes behind a `threading.Lock` (+ `check_same_thread=False` if off-thread dispatch is ever enabled).
- **S2 — `list_forecasts` cursor is unguarded and unwrapped.** `store.py:267` (`after = int(cursor)`), `server.py:87-92`. Malformed cursor → uncaught `ValueError` that FastMCP surfaces verbatim (`mask_error_details=False` default), also leaking that the "opaque" cursor is a raw row `seq`. This tool (also `get_calibration_report`, `verify_chain`) lacks the `try/except ForecastError` the other 4 tools have. **Fix:** validate/parse the cursor in the store, raise `ForecastError`, and add the try/except wrapper for consistency (N10).
- **S3 — `model_draft` enum advertised but always rejected (schema lies).** `server.py:43`, `models.py:9`, `store.py:114-118`. The `JudgmentSource` Literal offers `model_draft`, but `log_forecast` unconditionally rejects anything ≠ `analyst_confirmed` → wasted round-trip, no schema-level hint. **Fix:** narrow the tool signature to `Literal["analyst_confirmed"]` (or drop the param and default it).
- **S4 — `resolved_at` unvalidated; no chronology check.** `server.py:59`, `store.py:187-219`. Arbitrary free string, no ISO-8601 parse, no `resolved_at >= locked_at` requirement → outcome can be backdated to any timestamp, corrupting the audit trail (Brier unaffected). **Fix:** parse as ISO-8601 and reject values earlier than the forecast's `locked_at`.
- **S5 — No length limits on free-text fields (DoS / unbounded ledger).** `server.py:38-44`; store. `case_id`, `question`, `resolution_criteria`, `horizon`, `rationale`, `reason` have no `max_length` (schema or store) and are all appended into the hash-chained ledger. **Fix:** add `Field(max_length=…)` mirroring the existing `probability` `Field` pattern.
- **S6 — `question` (and other required strings) not checked non-empty.** `store.py:119-122`. Only `resolution_criteria` is `.strip()`-checked; `question` can be `""`/whitespace, silently corrupting the record the score is computed against. **Fix:** apply the non-empty check to all required string fields.
- **S7 — `limit` silently clamped; bound not in schema.** `store.py:266` (`max(1, min(limit,1000))`), `server.py:89`. Out-of-range `limit` is silently altered and the published `inputSchema` never advertises the `[1,1000]` bound. **Fix:** add `Annotated[int, Field(ge=1, le=1000)]` and reject/echo instead of silently clamping.
- **S8 — `verify_chain(case_id)` is a no-op that reports a false scope.** `store.py:342-369`, `models.py:67`. The SQL walks all rows in all three tables regardless of `case_id`, yet `scope = case_id or "all"` implies a scoped check ran (chain integrity is table-wide by construction and can't be scoped). **Fix:** drop the param, or honor it, and make the response never claim a narrower scope than what ran + fix the docstring.
- **S9 — Manifest append has no flush/fsync.** `store.py:97-101`. `open("a")` → write → close with no `flush()`/`os.fsync()`; on power loss the manifest line can be lost while the DB WAL commit landed → false tamper signal / weakened crash-safety (the whole point of the file). **Fix:** `fh.flush(); os.fsync(fh.fileno())` after the write.
- **S10 — `created_ts` excluded from the hashed payload.** `store.py:139-150` vs `372-378`. `created_ts` (used for the idempotency window) is stored but not in the canonical payload, so a DB-write attacker can alter it undetected and defeat idempotency dedup. **Fix:** include `created_ts` (and ideally `seq`) in the hashed payload, or explicitly document it as out-of-scope for integrity.
- **S11 — Idempotency dedup key is incomplete → silent content loss.** `store.py:124-135`. Key is only `(case_id, question, analyst_id, round(probability,4))`; a retry within 5 s that differs in `resolution_criteria`/`horizon`/`rationale` is treated as a duplicate and the new content is dropped with no error. **Fix:** include the remaining logical fields (or hash the full canonical payload) and raise `ForecastError` on a near-duplicate whose non-key fields differ.
- **S12 — Corrections are unlimited and invisible to graders.** `store.py:187-219`, `models.py:20-34`. `resolve_forecast(is_correction=True)` is uncapped, and `ForecastRecord` / `get_calibration_report` surface only the latest resolution with no `was_corrected`/`correction_count`, so a retroactive outcome flip is invisible without a full `verify_chain` row audit. **Fix:** surface a correction indicator/count on the record and in the report.

### Schema-documentation gaps (should-fix — affect agent correctness, not code correctness)

- **Q1 — `probability`/`outcome` directional semantics undocumented.** `server.py:40,46,59`. Nothing states `probability` = "P(question resolves YES, i.e. outcome=True)"; the Brier `(p-o)²` depends on both pointing the same way, so an agent can silently invert every score. **Fix:** document the direction on both fields.
- **Q2 — Murphy component polarity lives only in a `#` comment.** `models.py:53-54`. "higher = better discrimination" / "lower = better calibrated" never reach the JSON schema the agent sees. **Fix:** move both into `Field(description=…)`.
- **Q3 — `horizon` format undocumented yet locked-forever.** `server.py:42`. Required, immutable, no edit tool; wrong value is unrecoverable short of void+relog. **Fix:** state a format contract (ISO date or `P30D`-style duration) with an example.
- **Q4 — Bare tool schema.** `server.py` signatures / `models.py` fields: only `probability` carries a `Field` constraint; add `Field(description=…)` for non-obvious params/returns (units, ranges, formats).
- **Q5 — `list_forecasts` docstring explains none of its 4 params/pagination.** `server.py:91`. **Fix:** document `resolved=None/True/False` selection + a one-line cursor example.

---

## NICE-TO-HAVE

- **N1** `store.py:57`, `server.py:27,30` — use `pathlib.Path` over `os.path` string concat (`with_suffix`, `mkdir(parents=True, exist_ok=True)`).
- **N2** `store.py:190,222` — `_forecast_row` uses `SELECT *` purely for an existence check; use `SELECT 1 … LIMIT 1` like `_is_voided`.
- **N3** `store.py:263-284` — `list_forecasts` post-filters only the first fetched batch, so a `resolved`-filtered page can return far fewer than `limit`; loop until `limit` accepted or source exhausted.
- **N4** `models.py:12-17` — `ForecastRef` omits `question`/`probability`; returning `ForecastRecord` from `log_forecast` would let the agent confirm committed values without a second `get_forecast` (read-back goal).
- **N5** `server.py` — no `annotations` (`readOnlyHint`/`idempotentHint`) on the 4 pure-read tools + idempotent `log_forecast` (hints only, not a security boundary).
- **N6** `server.py:114` — `mcp.run()` relies on the default transport; pass `transport="stdio"` explicitly given the docstring's stdio-cleanliness promise.
- **N7** `store.py:338` — `CalibrationReport.note` returns bare `"n<10"`; a natural-language caveat is easier for an agent to relay.
- **N8** `models.py:34` — `ForecastRecord.row_hash` returned with no explanation it's an internal integrity value, not a judgment/score.
- **N9** `server.py:27-30` — `CALIBRATION_DB` env path used unvalidated in `os.path.join`/`makedirs` (launch-time config, low risk; defense-in-depth).
- **N10** `server.py:95-105` — `get_calibration_report`/`verify_chain` lack the `try/except ForecastError` wrapper the other tools use (consistency; folds into S2).

---

## Confirmed clean (no action)

- **SQL parameterization:** all VALUES use bound params; only interpolated strings are table-name literals from the fixed `_TABLES` tuple, guarded by `assert table in _TABLES` — no injection surface.
- **In-place mutation / reorder:** correctly detected — `prev_hash` binds each row to the prior row's hash, so an edit or swap breaks the recomputed chain from that point (this is what the manifest gap M1 does *not* cover: whole-chain/tail deletion).
- **Judgment / collect-then-grade boundary:** `log_forecast` hard-rejects `judgment_source != "analyst_confirmed"`; outcomes are only appended (never `UPDATE`d); `void` blocked once resolved; asserted fields live in `ForecastRecord`/`ForecastRef`, computed fields only in `CalibrationReport` (docstrings say "COMPUTE"/"no judgment invented"). Core design sound (modulo S12 visibility).
- **No-egress:** no network/subprocess/external I/O anywhere — only `sqlite3`/`hashlib`/`json`/`os`/`time`/`uuid`/`datetime`.
- **Secrets / stdout hygiene:** no hardcoded secrets; only two `print(..., file=sys.stderr)` calls, nothing on stdout; startup chain-verify failure exits via stderr + `SystemExit(1)` before JSON-RPC starts. Every tool returns a typed pydantic model → structured output + read-back path.
- **Brier / Murphy math:** correct; no float/off-by-one bug found (p==1.0 top-bucket edge handled).

MUST_FIX_COUNT: 1
