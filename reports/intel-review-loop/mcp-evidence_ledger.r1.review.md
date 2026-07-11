# evidence_ledger MCP server — Review r1

**Target:** `~/projects/intelligence-analysis-agent/mcp_servers/evidence_ledger/` (`server.py`, `store.py`, `models.py`, `__main__.py`) + shared imports `mcp_servers/common.py`, `mcp_servers/staleness.py`.
**Mode:** REVIEW ONLY. 4 parallel lenses — mcp-protocol, mcp-security, mcp-quality, python-reviewer.
**Date:** 2026-07-11.

## Test gate

```
cd ~/projects/intelligence-analysis-agent && python -m pytest tests/ -q
→ 88 passed
```

No test failures → **0 test-driven must-fix**.

## Clean bills (verified, not findings)

- **No-egress:** confirmed. No `requests`/`urllib`/`socket`/`httpx`/`aiohttp`/`http.client` anywhere in `evidence_ledger/`.
- **SQL injection:** confirmed clean. Every value query parameterized (`?`). Only f-string SQL interpolates a table name drawn from a hardcoded internal tuple `_TABLES` (`store.py:61,233`, `staleness.py:53,119`), correctly `noqa: S608`.
- **stdio hygiene:** clean. Only `print()` calls go to `sys.stderr` (`server.py:140,142`); nothing pollutes stdout; `mcp.run()` defaults to stdio.
- **Structured output:** all 7 tools return typed Pydantic models, never raw strings.
- **Append-only at app layer:** no `UPDATE`/`DELETE` on `evidence`/`grades`; GENESIS sentinel consistent; supersede-not-edit correct.
- **Read-back:** deterministic — grade/update return `get_evidence` from same in-process connection post-commit.

---

## MUST-FIX (consolidated, deduped)

### MF1 — `judgment_source="analyst_confirmed"` is caller-asserted; no human gate `[security]`
`server.py:60-95`, `models.py:13`, `store.py:114-138`, `staleness.py:84-103`.
Whole collect-then-grade integrity claim ("an ingested, ungraded artifact can never reach scored output") rests on `judgment_source` faithfully recording human confirmation. But it's a plain string param — any MCP caller (incl. an autonomous agent) passes `judgment_source="analyst_confirmed"` and self-certifies. Trivially exploitable; defeats the cross-server gate ach-engine trusts.
**Fix:** don't accept `analyst_confirmed` as an ordinary same-call param. Route it through a host-gated/interactive-confirmation path (separate privileged tool exposed only post-human-confirmation, or a session-bound elicitation result the server validates).

### MF2 — `redact_pii=False` has no server-side authorization `[security]`
`server.py:98-113`.
Docstring calls PII redaction "life-safety" and says unredaction "should" be host-gated — but no gate exists in code. Any caller does `get_evidence(id, redact_pii=False)` → raw source-identifying content, zero check. Comment is aspirational, not enforced.
**Fix:** treat unredaction as privileged — require an explicit host approval signal (not a same-call boolean from the caller asking to see PII), or split into a separate tool the host exposes only post-confirmation.

### MF3 — `verify_chain` blind to tail truncation / whole-chain reset `[security]`
`store.py:227-251` vs `store.py:65-69`.
Chain only proves internal self-consistency of rows that currently exist — no external anchor. An actor with write access to `evidence.db` deletes last N rows; `verify_chain` returns `ok=True` (just smaller `rows_verified`). Code already writes a witness log (`manifest.jsonl`) on every insert but **never reads it back**. Sibling `calibration_tracker/store.py:539-606` already implements exactly the cross-check (`_check_manifest`, self-chained manifest, fail-closed) — known-fixable, not inherent. This undermines the `server.py:137-143` "REFUSING TO SERVE" startup gate.
**Fix:** port `calibration_tracker`'s manifest pattern — self-chain the manifest, and in `verify_chain` compare each table's DB head to the manifest's last head; fail closed on missing/short manifest.

### MF4 — grade insert commits before cross-store staleness signals; non-atomic, no compensation `[python]`
`store.py:114-138` — `_conn.commit()` (L133) then `staleness.mark_stale`/`mark_graded` (L137-138) write a **separate** `staleness.db`, no spanning transaction, no try/except.
Crash / lock / disk-full between L133 and L138 → grade durably exists but `grade_signals` never written → ach-engine's `latest_grade_source` reports "never graded" for graded evidence (or `stale_events` missed → a stale ACH cell never invalidated). Fails silently (tool returns normally). Directly breaks the invariant `staleness.py` claims to guarantee.
**Fix:** wrap the two staleness writes in try/except with a compensating/reconcile path (mark grade unconfirmed on failure, or log+retry), or explicitly document as accepted design-v3 risk if cross-DB atomicity is out of scope.

### MF5 — `verify_chain(case_id)` param dead + misleading scope `[quality, python; also flagged should by protocol, security]`
`server.py:124-127`, `store.py:227-251`.
4/4 lenses flagged. `case_id` only labels output (`scope=case_id or "all"`) — the loop (`SELECT * ... ORDER BY seq ASC`, L233) always walks the full global chain, and `grades` has no `case_id` column to scope by. Caller asking "verify case X" gets `scope="X", ok=True` while the whole ledger was checked. Superset-safe but a misleading audit/tamper-evidence contract.
**Fix:** drop the param and document verification as always-global, or implement real per-case filtering and make `scope` accurate.

### MF6 — `Grade` omits `analyst_id` though server computes + hashes it `[quality]`
`models.py:26-34` vs `store.py:114-138` (`analyst_id` written into every grade row, folded into `row_hash` L120/129).
`Grade` (returned by `get_evidence`/`grade_evidence`/`update_grade`) has no `analyst_id` — the calling agent can never answer "who made this judgment" from any tool response, despite the design's whole analyst-vs-model / life-safety framing.
**Fix:** add `analyst_id: str` to `Grade` and return it. (See also SF7 — that id is a static process-wide env value, weakening its evidentiary value.)

### MF7 — `add_evidence` params undocumented + `item` immutability never stated `[quality]`
`server.py:39-50`.
Docstring documents only `pii` and `expected_observables`. `case_id`/`item`/`source_id`/`evidence_type`/`source_channel` get zero description — `item` especially (raw text? summary? URL?). And there is no `edit_item`/`update_evidence` tool: `item` is permanently fixed once stored, but nothing tells the agent, so a mis-entry has no recovery but a new record.
**Fix:** document each param; explicitly state "item is immutable once stored — no edit tool exists." Also document `EvidenceType` values (esp. `absence` = absence-of-expected-evidence) and `SourceChannel`.

### MF8 — cross-server `analyst_confirmed` gate invisible in grade docstrings `[quality]`
`server.py:59-95` vs `staleness.py:5-7,96-98`.
The rule "ach-engine refuses to SCORE any cell whose evidence's latest grade is not `analyst_confirmed`" lives only in `staleness.py`'s docstring, which the calling agent never sees. An agent grading `judgment_source="model_draft"` gets no local warning; failure surfaces later cross-server with no local clue how to fix.
**Fix:** add one sentence to both `grade_evidence`/`update_grade` docstrings stating the ach-engine gate + the `update_grade(..., analyst_confirmed)` remedy.

---

## SHOULD-FIX

- **SF1 — unwrapped `int(cursor)` in `list_evidence` `[security, python, protocol]`.** `store.py:189`; `list_evidence`/`get_source_history` tools (`server.py:108-121`) skip the `EvidenceError→ToolError` wrap every other tool uses. Bad cursor → raw uncaught `ValueError` at the MCP boundary (possible traceback/path leak), inconsistent contract. **Fix:** guard the parse, raise `EvidenceError("invalid cursor")`, wrap both tools.
- **SF2 — head-read → INSERT race, no lock/transaction `[security, python]`.** `store.py:89-90,123-124`. `_head()` read then INSERT computed from it, no serialization. Concurrent tool calls → two rows same `prev_hash` → next `verify_chain` fails → whole server trips "REFUSING TO SERVE". Sibling `calibration_tracker/store.py:74` explicitly serializes this. **Fix:** wrap head-read+INSERT+manifest in one critical section (lock or `BEGIN IMMEDIATE`).
- **SF3 — single shared `sqlite3.Connection`, default `check_same_thread=True` `[python]`.** `store.py:34`, module-scope `store` at `server.py:34`. If FastMCP dispatches sync tools on a threadpool, 2nd concurrent call from another thread → `sqlite3.ProgrammingError`. **Fix:** verify+document FastMCP's dispatch, or `check_same_thread=False` + `threading.Lock`, or thread-local connections. (Same root as SF2.)
- **SF4 — unkeyed hash chain, forgeable with DB write access `[security]`.** `common.py:18-19`. No HMAC key / external signature; anyone with the (open-source) algo + file write rewrites any row and regenerates a self-consistent chain. Detects accidental corruption, not local compromise. **Fix:** HMAC-SHA256 with a server-held key not co-located with the DB, or periodic external anchoring (aligns with MF3).
- **SF5 — writes not in a transactional context manager `[python]`.** `store.py:91-99,125-134` — manual `execute` + `commit`. Use `with self._conn:` for auto commit/rollback so an error can't leave an implicit open transaction on the WAL connection.
- **SF6 — `pii` is bare self-declared boolean, no detection `[security]`.** `server.py:44`. An `ingested` (untrusted) item under-declaring `pii=False` is never redacted. **Fix:** defense-in-depth PII heuristic on ingested items → flag for analyst review.
- **SF7 — `analyst_id` static process-wide env value `[quality, security]`.** `store.py:32`. Every grade attributed to one string set at startup; no per-caller/session binding. Weakens `get_source_history` provenance and compounds MF1. **Fix:** derive from real per-session identity where the deployment has one.
- **SF8 — `SourceHistory.last_change_direction` typed bare `str`, not `Literal` `[quality]`.** `models.py:59` (only ever `improved|worsened|same|n/a`, `store.py:217,220`). No enum in exposed schema. **Fix:** `Literal[...]`.
- **SF9 — `verify_chain` vs `verify_signals_chain` scope not differentiated `[quality]`.** `server.py:124-134`. Parallel names, disjoint stores; an agent running only `verify_chain` at startup may think integrity is fully checked. **Fix:** cross-reference docstrings; consider `verify_evidence_chain`.
- **SF10 — no server-level `instructions=` / workflow overview `[quality]`.** `server.py:35`. No single place an agent discovers the add→grade→(update)→read lifecycle + the ach-engine gate. **Fix:** pass `instructions=`.

## NICE-TO-HAVE

- **N1 — `EvidenceRef` lacks `row_hash` `[protocol]`.** `models.py:18-24`. Confirming chain position of a just-written row needs a 2nd `get_evidence` round-trip. Add `row_hash` to the ref.
- **N2 — no `Field(description=...)` on any model field `[protocol, quality]`.** `models.py`. Schemas rely entirely on docstrings; e.g. `Grade.reason` vs `rationale`, `item=="REDACTED"` sentinel undocumented in-schema.
- **N3 — `EvidenceRecord.row_hash` scope ambiguous `[quality]`.** `models.py:47` — covers only the `evidence` row, not the separate grade chain; agent may assume it attests the whole record. Document.
- **N4 — table allowlist guarded by `assert` `[python]`.** `store.py:59`, `staleness.py:51` — stripped under `python -O`. Use `if table not in _TABLES: raise ValueError`.
- **N5 — no size/length bounds on free-text inputs `[security]`.** `item`/`case_id`/`source_id`/`expected_observables` — unbounded DB growth + hashing cost. Add `Field(max_length=...)`.
- **N6 — DB + manifest created with default perms `[security]`.** `server.py:29-31`, `store.py:34,68`. DB holds PII. `os.chmod(path, 0o600)`.
- **N7 — truthiness defaulting `x or {}` / `x or env` `[python]`.** `store.py:32,82`. Prefer `is None` to distinguish not-given from explicitly-empty.
- **N8 — duplicated chain-walk/verify logic `[python]`.** `store.py:227-266` ≈ `staleness.py:106-135`. Factor a shared `verify_hash_chain(conn, tables, payload_fn)` into `common.py`.
- **N9 — `os.path`/string concat instead of `pathlib` `[python]`.** `server.py:26`, `store.py:33`.
- **N10 — redundant `int(bool(pii))` `[python]`.** `store.py:96`. bool is already stored as 0/1.
- **N11 — `grade_evidence`/`update_grade` noun flips (evidence vs grade) `[quality]`; `unknown evidence_id` error doesn't teach retry `[quality]`** (`store.py:106`).
- **N12 — startup `SystemExit(1)` before `initialize` handshake `[protocol]`.** `server.py:137-143`. Defensible refuse-to-serve; confirm host treats "subprocess exits pre-initialize + stderr line" as legible, not a hang.

---

## Per-lens must-fix tally (pre-dedup)
protocol 0 · security 3 · quality 4 · python 2 · tests 0. Deduped union = 8 (verify_chain counted once).

MUST_FIX_COUNT: 8
