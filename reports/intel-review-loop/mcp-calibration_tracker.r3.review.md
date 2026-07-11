# Review — mcp_servers/calibration_tracker (r3)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/mcp_servers/calibration_tracker/` (`server.py`, `store.py`, `models.py`, `__main__.py`).
FastMCP stdio server (design v3, Server 1): append-only, per-table hash-chained SQLite ledger of analytic forecasts + Brier/Murphy calibration report.

**Reviewers (parallel):** mcp-protocol-advisor · mcp-security-advisor · mcp-quality-advisor · python-reviewer.
`common.py` / `staleness.py` exist as siblings but are **not imported** by this server (grep-confirmed by 3 reviewers) — out of scope.

## Test gate

```
cd /home/grammy-jiang/projects/intelligence-analysis-agent && python -m pytest tests/ -q
→ 88 passed
```

**0 test FAILs.** No test-driven must-fix.

## Verified-clean (stated so review is not re-run on these)

- **SQL injection:** all VALUES bound; only internal `_TABLES`-checked table-name literals interpolated (`store.py:141-142,520-524`). Clean.
- **No-egress:** no `requests`/`httpx`/`urllib`/`socket`; `show_banner=False` disables FastMCP's outbound version-check (`server.py:190-192`). Clean.
- **Secrets:** none embedded; only non-secret env config (`CALIBRATION_DB`, `CALIBRATION_ANALYST_ID`).
- **stdio hygiene:** both `print()` → `sys.stderr` (`server.py:187,189`); banner suppressed. Clean.
- **Error surfacing:** `ForecastError`→`ToolError`, and even unexpected exceptions become `CallToolResult(isError=True)` not JSON-RPC errors (traced in installed mcp-SDK) with `mask_error_details=True` masking paths/SQL. Correct protocol/tool-error split.
- **Structured output / read-back:** all tools return Pydantic models (auto `outputSchema`+`structuredContent`); mutations echo full `ForecastRecord`.
- **Cross-analyst isolation:** wrong-analyst rows reported identically to nonexistent ("unknown forecast_id") — no enumeration oracle; all reads filter by `analyst_id`.
- **Judgment-vs-computed boundary:** `probability` (judgment) + `outcome` (ground truth) are the only score-adjacent inputs; `brier`/resolution/reliability exposed only via read-only `get_calibration_report`; `row_hash` self-documents "NOT a judgment or score." Agent cannot hand-write a score.

---

## MUST-FIX (3) — invariant / integrity breaks

### M1 [CRITICAL/correctness] TOCTOU race defeats append-only "single-resolution" invariant — `store.py:302-338, 362-374`
`resolve_forecast` / `void_forecast` run their decision reads (`_forecast_row`, `_is_voided`, `_latest_resolution`, lines 305-316 / 363-370) **before** `with self._write_lock:` (lock opens 339 / 375). Only the head-read+INSERT+manifest is serialized. Two concurrent `resolve_forecast(same id, is_correction=False)` can both read `existing=None`, both pass validation, both serialize through the lock, both INSERT → two un-marked "first" resolutions for one forecast, silently defeating the core no-double-resolve invariant. The store's own `N3` comment (`store.py:84-85`) already flags that FastMCP may dispatch tool bodies on worker threads (and `check_same_thread=False`), so this class of race is a live concern that was handled for the hash-chain read but **not** for the business-rule pre-checks.
**Fix:** move `_forecast_row`/`_is_voided`/`_latest_resolution` inside `self._write_lock` (re-check after acquiring, before INSERT).

### M2 [HIGH/security] Manifest **tail-truncation** bypasses `verify_chain` — `store.py:160-177, 514-544, 562-608`
`verify_chain` checks (a) each table's internal chain and (b) the manifest's own self-chain + that its **final** head equals the DB's **final** head. An attacker with filesystem write can `DELETE FROM resolutions WHERE seq > X` **and** drop the matching trailing manifest lines — both self-chains stay internally consistent and the final heads still agree → `ok=True`, deletion undetected. The fail-closed whole-table check (`store.py:569-577`) only fires when a DB head returns fully to `GENESIS`, not on partial rollback. This is a concrete bypass of the load-bearing tamper-evidence claim (cheaper than the "recompute-forward" residual risk the code already documents).
**Fix:** put a monotonic per-table row-count (or global seq) in each manifest entry; fail `verify_chain` when the current DB row count < last-attested count. (Durable fix = ship heads to an off-host WORM log, as the code comment already recommends.)

### M3 [HIGH/security] Immediate self-grading — `horizon` stored but never enforced — `store.py:302-337`, `server.py:53-59`
Only anti-backdating guard is `resolved_dt < locked_dt`. A forecast can be resolved milliseconds after `log_forecast`, and `horizon` ("Locked forever", the future resolution window) is **never read** in `resolve_forecast`. Combined with `judgment_source='analyst_confirmed'` being a self-attested, unverified caller literal, an adversarially-prompted agent that already knows the answer can log then immediately self-grade with hindsight — defeating the purpose of grading *advance* judgments. (The attestation being unverified is documented-by-design; the enforceable gap is the unused `horizon` / no min-latency.)
**Fix:** when `horizon` is a plain ISO date, reject `resolved_at` earlier than it; and/or enforce a minimum `resolved_at − locked_at` gap. **Confirm intended latency policy with the owner** — may be a deliberate tradeoff.

---

## HIGH (non-blocking design)

### H1 [python] Module-level singleton with import-time side effects — `server.py:30`
`store = CalibrationStore(DB_PATH)` opens the sqlite conn + takes the OS `flock` at **import**. Importing when the lock is held raises `ForecastError` and crashes the importer; tests need `CALIBRATION_DB` env gymnastics + `# noqa: E402`. Global mutable state on import.
**Fix:** lazy `get_store()` / construct inside `main()`; import stays side-effect-free.

---

## MEDIUM

- **[quality] No MCP tool annotations** — `server.py:36-181`. None of the 7 tools declare `readOnlyHint`/`idempotentHint`/`destructiveHint`. 4 reads + 3 append-only writes are indistinguishable except via docstring; clients can't auto-approve safe reads. **Fix:** `ToolAnnotations(readOnlyHint=True)` on reads; `destructiveHint=False` on writes; `idempotentHint=True` on `log_forecast` (5s dedup).
- **[security] `void_forecast` enables selective exclusion (score-gaming)** — `store.py:362-389`. Free-text `reason`, no legitimacy check; caller can void a forecast about to resolve badly → dropped from Brier. **Fix:** surface void `reason`s prominently in the report (not just `n_voided`); consider flag/rate-limit near `horizon`.
- **[security] World-readable ledger files** — `store.py:86,98,173`, `server.py:28`. DB/manifest/lock/data-dir created at process umask; ledger holds possibly-sensitive `question`/`rationale`/`reason` text. **Fix:** `chmod 0600` files, `0700` dir after creation.
- **[quality+protocol] `judgment_source` is inert** — `server.py:60-66`, `models.py:9`. Single-value `Literal["analyst_confirmed"]` **with default = that value** → never a conscious act; `models.py` `JudgmentSource` still carries `"model_draft"` the server can never emit (output-schema drift). **Fix:** drop the param (hardcode server-side) or make it required no-default; narrow `ForecastRecord.judgment_source` to `Literal["analyst_confirmed"]`.
- **[quality] `brier` has no schema description** — `models.py:60-76`. The headline metric lacks a `Field(description=...)` (scale/direction) while the secondary components have one. **Fix:** describe `brier` (0=perfect,1=worst,lower better) + `n`/`n_voided`/`buckets`/`note`.
- **[quality+protocol] `list_forecasts` `resolved` filter applied after pagination** — `store.py:419-448`, `server.py:139-157`. Filter runs in Python on the `limit+1` raw fetch; a page can return `items=[]` with non-null `next_cursor`. An agent treating empty `items` as "done" under-reports. **Fix:** document "page while `next_cursor != null`, even if `items` empty"; or filter before paginating.
- **[python] Flat `ForecastError` conflates business-rule vs infra faults** — `store.py:37-38,91,103-106`. WAL-unavailable / lock-contention raise the same type as bad-probability. **Fix:** split `StoreUnavailableError` from `ForecastError`.

## LOW

- **[python] Resource class has no context-manager** — `store.py:68-114`. Owns conn + flock but no `__enter__`/`__exit__`; every caller hand-writes `close()`. **Fix:** add CM protocol.
- **[python] Re-raises drop `from e`** — `store.py:321-324,327-333,423-426`. Add explicit `from e`.
- **[protocol] Server `version` not set** — `server.py:33`. `serverInfo.version` reports FastMCP's library version, not a calibration-tracker build, in the initialize handshake. **Fix:** pass `version=`.
- **[quality] `resolved=False` silently includes voided forecasts** — `server.py:144-147`. Document the overlap (voided → `outcome=None`).
- **[quality] Idempotency docstring says "byte-identical" but key uses `ROUND(probability,4)`** — `server.py:73-75`, `store.py:230-238`. Reword to "probability equal to 4 dp".
- **[quality] `resolved_at` naive→UTC coercion undocumented** — `server.py:93-95`, `store.py:60-65`. Add "naive values interpreted as UTC".
- **[security] `resolved_at` has no upper bound** — `store.py:319-337`. Accepts year-9999. **Fix:** bound to `<= now + skew`.
- **[security] `CALIBRATION_DB` env used without path containment** — `server.py:25-28`. Not MCP-reachable; defense-in-depth: validate against an allowed base dir.
- **[security] Unbounded ledger growth + full re-walk every startup** — `server.py:185`, `store.py:522-524`. `verify_chain` `fetchall()`s all rows; no row cap. **Fix:** checkpoint/archival + capped growth.
- **[python/quality] Dead `ForecastRef` model with stale docstring** — `models.py:12-17`. Unused; `log_forecast` returns `ForecastRecord`. **Fix:** delete (or wire + fix docstring).
- **[python] N+1 read pattern / bare `list` hint** — `store.py:431,440-446,464-469`. Per-row `get_forecast`/`_latest_resolution`/`_correction_count`; consolidate; type `list[int|str]`.

---

## Consolidation notes

- 26 raw findings across 4 reviewers → deduped. Cross-reviewer overlaps merged: the `resolved`-filter-after-pagination issue (quality + protocol), the inert `judgment_source`/`model_draft` drift (quality + protocol), and dead `ForecastRef` (quality + python).
- No CRITICAL from security/protocol/quality; the sole CRITICAL is python's TOCTOU race (M1), corroborated in spirit by the store's own `N3` concurrency comment.
- Must-fix set = the three findings that break a load-bearing invariant (append-only single-resolution, tamper-evidence, advance-judgment integrity). H1 (import-time singleton) is a real HIGH but no wrong-output/serving failure on the normal path, so it is high-priority-non-blocking, not must-fix. M3 should be confirmed against intended latency policy before enforcing.

MUST_FIX_COUNT: 3
