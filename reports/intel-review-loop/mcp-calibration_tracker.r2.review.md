# Review — calibration_tracker MCP server (r2)

Target: `intelligence-analysis-agent/mcp_servers/calibration_tracker/{server,store,models}.py`
(no `common.py`/`staleness.py` exist — not imported). Review-only pass, 4 reviewers
(mcp-protocol, mcp-security, mcp-quality, python) + verification of contested findings.

## Test gate

Command as specified — `cd intelligence-analysis-agent && python -m pytest tests/ -q` —
**FAILS**: `Interrupted: 10 errors during collection` / `ModuleNotFoundError: No module named
'mcp_servers'`. Cause: `pyproject.toml [tool.pytest.ini_options]` sets `testpaths` but no
`pythonpath`, so the repo root is not on `sys.path` and every test module's `from mcp_servers...`
import fails at collection. This breaks the documented gate command for the whole repo (all 10
test modules, not just calibration).

With `PYTHONPATH=. python -m pytest tests/ -q` → **83 passed**; calibration subset
(`test_calibration_tracker.py test_calibration_wire.py test_cross_server_staleness.py`) → **26
passed**. So no calibration *code* test fails — the failure is a one-line test-infra config gap.

→ **MUST-FIX (M1):** add `pythonpath = ["."]` to `[tool.pytest.ini_options]` in `pyproject.toml`
so the literal gate command collects. (Repo-infra, not calibration logic, but the gate as written
does not run.)

## Verification of contested findings (rejected / downgraded)

- **python-reviewer "MUST-FIX: guaranteed cross-thread sqlite crash" (`store.py:78`
  `check_same_thread` default True) — REJECTED (CONTRADICTED).** Claim was that FastMCP dispatches
  every sync tool to a worker thread, so the import-time connection would raise
  `sqlite3.ProgrammingError` on every call. Empirically false for the installed `fastmcp>=2.3`:
  probed the in-memory `Client` path — the tool body runs on the **same thread id** that created
  the connection, and `log_forecast` returns a valid id. The wire test `test_calibration_wire.py`
  (in the 83-pass suite) drives the full FastMCP path and passes. Downgraded to **nice-to-have**:
  set `sqlite3.connect(db_path, check_same_thread=False)` as cheap defense in case a future
  fastmcp changes its dispatch model.
- **python-reviewer "MUST-FIX: read paths unlocked → race" — DOWNGRADED** for the same reason:
  serialized single-thread dispatch means reads cannot concurrently interleave writes in-process.
  Real concurrency risk is *cross-process* (see S3), which the lock never addressed. Keep as
  should-fix hardening only.

## Should-fix

- **S1 — No rollback around INSERT+commit** (`store.py:229-239`, `305-311`, `331-336`). Each write
  path does `self._conn.execute(INSERT...)` then `.commit()` with no `try/except`. On a failed
  execute the connection's open transaction is left uncommitted; the next successful write's
  `commit()` can durably persist it — smuggling a partial row into the append-only ledger this
  design exists to protect. Fix: wrap in `with self._conn:` (auto commit/rollback) or
  `try/except: self._conn.rollback(); raise`.

- **S2 — `created_ts` stored but excluded from the row hash** (`store.py:224-235` payload omits it;
  `_payload_for` `store.py:487-494` also omits it). Confirmed: `created_ts` is a real column
  (gates the idempotency window, `store.py:207`) that `verify_chain` never covers, so it can be
  altered in the DB file without detection — a hole in the "tamper-evident" guarantee. Blast radius
  is limited (only idempotency-window timing). Fix: add `created_ts` to both the `log_forecast`
  payload and `_payload_for`'s forecasts branch. Note: breaking hash-format change → needs a
  documented chain re-baseline, not a silent flip.

- **S3 — No cross-process/analyst enforcement of the single-writer + ownership model**
  (`store.py:69-82`, and `resolve_forecast`/`void_forecast`/`get_forecast`/`list_forecasts` never
  compare `row["analyst_id"]` to `self.analyst_id`). Default DB is a single shared file
  (`data/calibration.db`, `server.py:25`), `analyst_id` silently defaults to `"local-analyst"`
  (`store.py:72`), and `threading.RLock` only serializes in-process. So (a) two processes on the
  same DB can fork the chain (caught only fail-closed at *next* startup by `verify_chain`), and
  (b) any instance can resolve/void/read another analyst_id's rows. Design comments scope this to
  single-writer-local, so not must-fix, but the shared default path + silent identity fallback make
  accidental collision easy. Fix: OS-level exclusive `flock` on a sidecar lock at startup (fail
  closed if held); add `if row["analyst_id"] != self.analyst_id: raise ForecastError(...)` in the
  read/mutate paths; fail loud (raise) when no analyst_id/env is set instead of defaulting.

- **S4 — Missing `Field` descriptions/bounds on primary params** (`server.py:78,95,104,114,132`).
  `forecast_id` (bare `str` in resolve/void/get), `reason` (bare in `void_forecast`, vs
  `resolve_forecast`'s `max_length=4000`), `is_correction` (bare bool, but flips semantics), and
  the `case_id` filters in `list_forecasts`/`get_calibration_report` all lack the
  `Annotated[..., Field(description=..., max_length=...)]` that `log_forecast` uses. An agent
  reading only the JSON schema gets no hint that `forecast_id` is the value returned by
  `log_forecast`. Fix: annotate to match `log_forecast`'s standard (e.g.
  `forecast_id: Annotated[str, Field(max_length=200, description="ID returned by log_forecast.")]`).
  (Raised independently by protocol, security, and quality reviewers.)

- **S5 — `log_forecast` read-back is too thin** (`server.py:35-73` returns `ForecastRef` =
  `{forecast_id, case_id, locked_at}`, `models.py:12-17`). The fields locked forever
  (`probability`, `question`, `resolution_criteria`, `horizon`) are not echoed, so the agent cannot
  confirm the immutable write from the call's own response without a second `get_forecast`. Fix:
  return the full `ForecastRecord` (as `resolve_forecast`/`void_forecast` already do).

- **S6 — `judgment_source` input/output type asymmetry & self-asserted "human-confirmed"**
  (`server.py:59-62`, `store.py:174-178`, `models.py:9,30`). Input `Literal["analyst_confirmed"]`
  (one value, also the default) while the read model type is
  `Literal["analyst_confirmed","model_draft"]` — `model_draft` is unreachable through this API, so
  a schema-reading agent is misled. Also the "requires a human-confirmed judgment" promise is only
  a caller-supplied string an autonomous agent satisfies by default (no real enforcement). Fix:
  narrow the read type or document `model_draft` as reserved; reword the guarantee to "caller
  attests; not independently verified" (or move enforcement out of the tool argument). Consider
  dropping the single-value parameter entirely and keeping the check as an internal invariant.

- **S7 — `horizon` never format-validated** (`store.py:181-193` checks only non-empty + length).
  Docstring (`server.py:52-57`) promises "ISO date … or ISO-8601 duration," but garbage
  (`"whenever"`, `"3mo"`) is locked permanently into the immutable chain. Fix: validate against
  `date.fromisoformat` / an ISO-8601 duration pattern before accepting.

- **S8 — Idempotency window undocumented** (`server.py:65-67`, `store.py:195-211`). A retried
  identical `log_forecast` within 5s silently returns the original `forecast_id` instead of a new
  row — changes what a retrying agent should expect, but no tool description mentions it. Fix: state
  it in the docstring.

## Nice-to-have

- N1 — `mask_error_details` left default `False` (`server.py:32`): unexpected (non-`ForecastError`)
  exceptions propagate raw text (DB path, SQL fragments) to the client. Pass
  `mask_error_details=True`; explicit `ToolError` messages are unaffected.
- N2 — Default FastMCP startup banner triggers a "check for newer version" HTTP egress
  (`server.py:157` `mcp.run(transport="stdio")` with `show_banner` default True). Inconsistent with
  this repo's egress discipline. Pass `show_banner=False`.
- N3 — `check_same_thread=False` defensive set (`store.py:78`) — see verification note above; not a
  live bug in the installed fastmcp.
- N4 — `assert table in _TABLES` before f-string table-name interpolation (`store.py:112`,
  `463-465`) is stripped under `python -O`. Use `if table not in _TABLES: raise ValueError(...)`.
  (Not injection: `table` is always one of 3 internal literals.)
- N5 — `locked_at` parse failure silently disables the anti-backdating check (`store.py:286-293`):
  `except ValueError: locked_dt = None` skips the "resolved_at cannot predate locked_at" invariant.
  Prefer log-and-raise.
- N6 — `threading.RLock` where a plain `Lock` suffices (`store.py:77`); no write path re-enters.
- N7 — Module-import DB side effect (`server.py:31` `store = CalibrationStore(DB_PATH)` runs at
  import) hurts testability; consider a lazy singleton / app-factory.
- N8 — `PRAGMA journal_mode=WAL` result unchecked (`store.py:79`); on some filesystems SQLite
  silently falls back, invalidating the concurrency assumptions. Fetch and assert `"wal"`.
- N9 — Doc/enum gaps for agent consumers: `CalibrationReport.note` value set undocumented
  (`models.py:76`), `ChainMismatch.row_id` overloaded (numeric seq vs `<manifest-*>` sentinels,
  `models.py:79-83`), pagination "check next_cursor, not item count" not stated (`server.py:124`),
  generic `"invalid cursor."` message (`store.py:374`).

## Confirmed clean (no finding)

- SQL fully parameterized — every value binds via `?`; only interpolated strings are internal
  table-name constants from the fixed `_TABLES` whitelist (not attacker-controlled).
- Collect-then-grade boundary sound: `forecasts` rows are only `INSERT`ed, never `UPDATE`d;
  re-resolution forces an explicit appended correction; `resolved_at >= locked_at` enforced; void
  blocked once resolved. No backfill of the answer possible.
- `analyst_id` never a tool parameter (all 7 tool signatures checked) — only via constructor / env,
  matching the trust-boundary docstring.
- No network egress imports; no hardcoded/logged secrets; diagnostics go to `stderr` not `stdout`
  (stdio JSON-RPC clean); `main()` verifies the chain and fails closed (`SystemExit(1)`) before
  serving.
- Hash canonicalization correct: `json.dumps(sort_keys=True, ...)` makes payload hashing
  order-independent; `datetime.now(timezone.utc)` used throughout (aware); genesis handled.

MUST_FIX_COUNT: 1
