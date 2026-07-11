# evidence-ledger MCP server — review pass (r2)

Target: `/home/grammy-jiang/projects/intelligence-analysis-agent/mcp_servers/evidence_ledger/`
Files: `server.py`, `store.py`, `models.py` (+ imported `../common.py`, `../staleness.py`).
Reviewers: mcp-protocol-advisor, mcp-security-advisor, mcp-quality-advisor, python-reviewer.
Consolidated + deduped; test FAILs treated as must-fix.

## Test gate

```
cd /home/grammy-jiang/projects/intelligence-analysis-agent && python -m pytest tests/ -q
→ 96 passed
```

0 test failures → 0 must-fix from the gate.

---

## MUST-FIX

### M1. `grade_evidence` uniqueness check is outside the write lock (TOCTOU) — `store.py:246-253`
`self._effective_grade(evidence_id) is not None` is checked BEFORE `self._write_lock` (lock is acquired only later inside `_insert_grade`, `store.py:229`). Two concurrent `grade_evidence` calls for the same `evidence_id` can both observe "no grade yet", both pass, and both insert as first grades — violating the single-first-grade / supersede-via-`update_grade` invariant the design rests on. The `__init__` docstring explicitly anticipates concurrent worker-thread dispatch, so this is reachable.
Fix: perform the existence check inside the same `with self._write_lock:` block that does the insert (check-then-act atomic under the lock).
(python-reviewer)

### M2. `verify_chain` reads DB + manifest without the write lock — `store.py:339-370`
Every writer holds `self._write_lock` across the commit→manifest-append sequence; `verify_chain` takes no lock. A verify interleaved with an in-flight write can read a row already committed but not yet manifest-attested → spurious `ok=False` tamper failure on a healthy ledger (and `main()` `server.py:197` gates serving on `verify_chain`, so a concurrent start could false-refuse). `seed_manifest_baseline` already locks correctly — mirror it.
Fix: acquire `self._write_lock` for the duration of `verify_chain`.
(python-reviewer)

### M3. `mask_error_details=True` not set on FastMCP — `server.py:51`
Framework default is `mask_error_details=False` (verified in installed fastmcp `settings.py`). Any non-`ToolError` exception (e.g. `sqlite3.OperationalError`, disk-full, a bug in `_mark_staleness_signals`) is surfaced to the client with raw exception text — potentially leaking `DB_PATH`, SQL/schema fragments, internals. This is the trio's life-safety server; sibling `mcp_servers/calibration_tracker/server.py:33` already sets `mask_error_details=True`.
Fix: `mcp = FastMCP("evidence-ledger", instructions=_INSTRUCTIONS, mask_error_details=True)`.
(mcp-protocol-advisor)

### M4. Ingested item can be graded `analyst_confirmed` on the first call — `server.py:96-116`, `store.py:246-253`
`source_channel="ingested"` is stored but never read by `grade_evidence`/`update_grade`. Any caller can grade an untrusted, pipeline-supplied item `judgment_source="analyst_confirmed"` on the very first grade — no `model_draft` step, no proof of human review — making it immediately scoreable by ach-engine. The collect-then-grade gate becomes a no-op against a misbehaving/compromised agent.
> DESIGN TENSION — the `_INSTRUCTIONS` docstring (`server.py:40-43`) states the load-bearing human gate lives in the calling workflow, not this server ("only records it faithfully"). So this is arguably intentional. But the server owns the `ingested` vs `analyst_typed` distinction and currently derives zero enforcement from it. Needs a user/design decision: enforce server-side or ratify the external-gate trust model.
Fix (if enforcing): when the evidence row's `source_channel == "ingested"`, reject a first-time `analyst_confirmed` (require passing through `model_draft`), or require a host-verifiable out-of-band confirmation token rather than trusting the caller literal.
(mcp-security-advisor)

**MUST-FIX carries a design-decision dependency on M4 — if the user ratifies the external-gate trust model, must-fix drops to 3.**

---

## SHOULD-FIX

### S1. Grade write commits to `evidence.db` before the cross-store signal write — `store.py:196-244`
`_insert_grade` commits the grade, THEN calls `_mark_staleness_signals` (separate `staleness.db`, no cross-DB txn). On a downgrade (`update_grade` moving `analyst_confirmed → model_draft`) that commits but whose retried signal write ultimately fails, `grade_signals` keeps the stale `analyst_confirmed` while the ledger's true latest is `model_draft` → ach-engine can keep scoring no-longer-confirmed evidence (unsafe direction). Also: on a partial failure the retry (`store.py:202`) re-runs BOTH `mark_stale` and `mark_graded`, duplicating a `stale_events` row (non-idempotent).
Fix: write/invalidate the signal before or atomically with the grade commit, or have ach-engine treat any drift between grade history and `grade_signals` as fail-closed.
(mcp-security-advisor; python-reviewer overlap on manifest-ordering variant below)

### S2. `StalenessStore` connection omits `check_same_thread=False` — `staleness.py:28` (own finding)
`EvidenceStore` opens with `check_same_thread=False` specifically because "a future FastMCP dispatch model may run tool bodies on a worker thread" (`store.py:50-52`). `StalenessStore` opens `sqlite3.connect(db_path)` with the default `check_same_thread=True`. `grade_evidence` → `_mark_staleness_signals` → `staleness._conn.execute` runs on the SAME dispatch thread; if FastMCP ever dispatches on a worker thread, the staleness insert raises `ProgrammingError: SQLite objects created in a thread can only be used in that same thread` — the exact scenario `EvidenceStore` guards against, unguarded here. Inconsistent hardening between two structurally identical stores. (No reviewer caught this.)
Fix: open the staleness connection with `check_same_thread=False` to match, and confirm its writes are serialized (they are, via `EvidenceStore._write_lock` for the ledger's writes; `StalenessStore` has no lock of its own — see S6).

### S3. Manifest append happens after the DB commit with no compensation — `store.py:170-183`, `229-244`
If `_append_manifest` raises (fsync/IO failure) AFTER the SQLite commit succeeds, the row is persisted but never attested → every later `verify_chain` fails-closed forever from a transient IO blip, not real tampering.
Fix: manifest-first ordering (write+fsync manifest entry before the SQLite commit), or catch the append failure and trigger an explicit reconciliation path (as `_mark_staleness_signals` already does).
(python-reviewer)

### S4. `list_evidence` silently clamps `limit` instead of raising — `store.py:294`
`limit = max(1, min(limit, 1000))` silently accepts `0`/negative/`>1000`, contradicting the fail-loud convention the same function applies to `cursor` three lines later ("SF1: must be a business-rule error, not silent"). `limit=0` returns 1 item with no error, hiding a caller bug.
Fix: raise `EvidenceError` for `limit` outside `[1,1000]` (or declare `minimum`/`maximum` so it's rejected before the body).
(python-reviewer + mcp-protocol-advisor — deduped)

### S5. Field semantics live only in `#` comments / server-wide instructions, not in the generated JSON schema — `models.py:26-63`, `server.py:65-177`
The input/computed boundary — `analyst_id` "trusted local binding, folded into row hash", `superseded`, `diagnosticity` "does NOT feed score_matrix", `item` redaction, `grade_sequence` ordering, `row_hash` = evidence-row-only — is written as Python `#` comments; tool per-argument guidance (`pii` required, `evidence_type` enum, `expected_observables` mapping, `cursor` opaque/`limit` clamped) lives only in docstring prose or the server-wide `_INSTRUCTIONS`. FastMCP builds `inputSchema`/`outputSchema` from bare annotations (no Args-block parser, verified in fastmcp source), so none of this reaches the calling agent at call time. Central to the judgment-input-vs-computed boundary the review targets.
Fix: move field semantics to `Field(description=...)` + class docstrings on `Grade`/`EvidenceRecord`/`EvidenceList`/`SourceHistory` (as `EvidenceRef` already does), and per-parameter guidance to `Annotated[T, Field(description=...)]`.
(mcp-quality-advisor #1/#3/#5/#6/#7 + mcp-protocol-advisor #2 — deduped)

### S6. `judgment_source` self-assertion has no per-tool guard-rail in the schema — `server.py:97-140`
Even without server-side enforcement (M4), an autonomous agent sees only a bare `Literal["analyst_confirmed","model_draft"]`; the "asserts a human confirmed it" warning is buried in `_INSTRUCTIONS`, which some clients surface less reliably than per-tool descriptions.
Fix: repeat an explicit imperative in both `grade_evidence`/`update_grade` docstrings/field descriptions, e.g. "Never set `analyst_confirmed` unless a human literally confirmed this grade in this call — default to `model_draft`." Distinguish `rationale` (why this grade) vs `reason` (why it supersedes the prior) at field level.
(mcp-quality-advisor #2/#5)

### S7. No length/size bounds on any free-text or dict field — `models.py`, `server.py:65-93`
No `Field(max_length=...)` on `item`, `case_id`, `source_id`, `diagnosticity`, `rationale`, `reason`, or entry/size cap on `expected_observables`. Store is append-only with no edit/delete, so an ingested pipeline can persist arbitrarily large payloads with no reclamation, degrading `verify_chain`'s full-table scans and DB size (resource-exhaustion).
Fix: add `Field(max_length=...)` caps and a max-entry/value cap on `expected_observables`, validated before persistence.
(mcp-security-advisor)

---

## NITS

- **N1.** `StalenessStore._head` uses `assert table in _TABLES` (stripped under `python -O`) while `EvidenceStore._head` deliberately uses `if ... raise ValueError` for the same f-string SQL — inconsistent hardening. Not attacker-reachable (fixed literal), but mirror the explicit raise. `staleness.py:51` (mcp-security #5 + python-reviewer #5 — deduped).
- **N2.** Store-layer grade methods (`_insert_grade`, `grade_evidence`, `update_grade`) carry no type annotations, unlike the fully-typed `server.py` tool signatures — weakens mypy over the store layer. `store.py:220-256` (python-reviewer).
- **N3.** `verify_chain`/`verify_signals_chain` tools lack the `try/except EvidenceError` wrap every other tool has; harmless today, but leave a comment that the asymmetry is deliberate once M3 sets `mask_error_details=True`. `server.py:180-193` (mcp-protocol-advisor).
- **N4.** No `ToolAnnotations` (`readOnlyHint`/`destructiveHint`) — host can't cheaply separate the 5 read/verify tools from the 3 mutating ones. Advisory-only per spec; cosmetic. `server.py:65-193` (mcp-protocol-advisor).
- **N5.** `_DATA` path never normalized — literal `..` segments leak into `DB_PATH`/`.lock`/`.manifest.jsonl` sidecar paths in logs. `server.py:26` (python-reviewer).
- **N6.** `EvidenceStore.close()` (releases sqlite conn + flock) is never called — module-scope `store`/`staleness` have no `atexit`/finally shutdown. `server.py:33-34` (python-reviewer).
- **N7.** `get_source_history(redact_pii=...)` is gated by `_require_unredact_permitted` and passed to the store, but `SourceHistory` carries no item content, so the param is effectively dead/misleading. `server.py:167-177`, `store.py:310` (own finding).
- **N8.** Consider a `verify_all` convenience tool or leading both verify docstrings with "a full check requires calling both stores" — an agent calling only `verify_chain` may believe the whole ledger is verified. `server.py:180-193` (mcp-quality-advisor #8).
- **N9.** Documented residual (restated, not a new bug): manifest shares the DB's filesystem/trust domain, so an attacker with write to both `evidence.db` and `evidence.db.manifest.jsonl` can forge a self-consistent chain + manifest and `verify_chain` returns `ok=True` (code flags this as SF4). Durable tamper-evidence needs heads shipped to an external WORM/append-only log. Note also `StalenessStore` has NO manifest anchoring at all — tail-truncation of `staleness.db` is undetected by its `verify_chain` (fail-closed for the score gate on the missing-grade direction, but asymmetric vs `evidence.db`). `store.py:120-136`, `staleness.py:111` (mcp-security #4 + own note).

---

## Verified clean (no action)

- SQL parameterization: all user-data queries use `?` placeholders; the only f-string-interpolated identifiers are table names from a fixed internal allowlist — no injection path.
- Append-only: no `UPDATE`/`DELETE` on `evidence`/`grades`; corrections go via superseding `update_grade`.
- `verify_chain` correctly detects single-row tampering, reordering, and mid-chain deletion (chained `prev_hash`/`row_hash` recompute over `seq ASC`).
- stdio hygiene: `main()` writes only to stderr, gates serving on both chain verifications, `show_banner=False` suppresses the version-check egress. No network calls in server/store — no-egress honored.
- Structured output: all tools return typed Pydantic models → real `outputSchema` + populated `structuredContent`. `EvidenceError → ToolError` is the correct isError mapping.
- Redaction gate: `_require_unredact_permitted` host-gated on `EVIDENCE_ALLOW_UNREDACT`; `EvidenceRef` never carries `item`.
- No mutable-default-arg bugs (`expected_observables=None` handled). No secrets in code (all host-set env vars).

MUST_FIX_COUNT: 4
