# Review — ach_engine FastMCP server (r3)

**Target:** `intelligence-analysis-agent/mcp_servers/ach_engine/{server,store,models}.py`
**Scope:** ONE review pass, READ ONLY. 4 parallel reviewers (mcp-protocol, mcp-security, mcp-quality, python) + code verification of every must-fix.
**Test gate:** `python -m pytest tests/ -q` → **110 passed** (no failing tests → no test-derived must-fix).
Note: no `common.py` / `staleness.py` inside `ach_engine/` (grep matched inline text only); shared chain primitives live in `mcp_servers/common.py` + `mcp_servers/staleness.py`, reviewed by security agent.

---

## MUST-FIX

### M1. TOCTOU race: chain-head read OUTSIDE `_write_lock` → can permanently corrupt ledger + raise false tamper alarms
**`store.py:151-152` (create_matrix), `store.py:271-272` (rate_cell); also `store.py:402-451` (verify_chain)**

`prev = self._head(table)` + `rh = row_hash(prev, payload)` computed BEFORE `with self._write_lock:` (line 156 / 273). Only the INSERT is serialized. Store's own comment (`store.py:58-60`) says FastMCP dispatches tool bodies on worker threads → concurrent `rate_cell`/`create_matrix` anticipated. Two concurrent calls read same stale tail hash, then serialize the INSERT: second row's `prev_hash` no longer matches actual head. `verify_chain` then reports `ok=False` (store.py:418) and `main()` refuses to serve (server.py:217-221) — **ordinary non-adversarial concurrency permanently breaks the append-only ledger, indistinguishable from real tamper.**

Verified against code:
- `create_matrix` reads head at line 151, lock at 156. BUG.
- `rate_cell` reads head at line 271, lock at 273. BUG.
- `_insert_hypothesis` reads head INSIDE the lock (store.py:176). Correct — copy this pattern.
- `verify_chain` (store.py:402-451) does its per-table `SELECT`s + separate manifest-file read with NO lock → a concurrent legit write between table-read and manifest-read makes the two views disagree → **spurious** `ChainMismatch` / `ok=False` on untampered data.

**Fix:** move the `_head(...)` + `row_hash(...)` INSIDE `with self._write_lock:` immediately before the INSERT in both `create_matrix` and `rate_cell` (mirror `_insert_hypothesis`); and take the write lock across the whole read pass of `verify_chain` (table reads + manifest read) so it observes a snapshot consistent with single-writer discipline.

### M2. `create_matrix` hypotheses have NO per-string length cap — bypasses the server's own documented DoS/size invariant
**`server.py:104-114`** (vs. `add_hypothesis` at `server.py:125`; store at `store.py:144-183`)

`hypotheses: list[str]` uses `Field(max_length=_MAX_HYPOTHESES)` which caps **item count** (64), NOT per-item string length. `add_hypothesis` — adding one hypothesis to the same matrix — caps its string at `_MAX_TEXT` (10k). `_insert_hypothesis` (store.py:171) only checks non-blank, not length. So the SF3 invariant the file documents as defense ("input-size caps… one oversized call would persist forever and drag verify_chain's full-table scan… cheap DoS", server.py:79-83) is enforced on one entry path and silently bypassable on the other: 64 megabyte-sized hypotheses via `create_matrix`. List also lacks `min_length=1` though store hard-requires non-empty (store.py:147) → declared schema looser than actual contract. Flagged independently by protocol + quality agents.

**Fix:** `hypotheses: Annotated[list[Annotated[str, Field(max_length=_MAX_TEXT)]], Field(min_length=1, max_length=_MAX_HYPOTHESES)]` — schema then agrees with `add_hypothesis`'s per-item bound and the store's non-empty contract.

---

## SHOULD-FIX

### S1. `verify_chain` crashes (masked) on a truncated manifest line instead of returning `ok=False`
**`store.py:121-141`** (`json.loads` at 136; `except FileNotFoundError:` at 139)
Manifest appended with plain `write()` (store.py:117-119); crash/OOM mid-append leaves a truncated last line. `_manifest_state()` catches only `FileNotFoundError` → raises unhandled `json.JSONDecodeError` (`_translate_ach_errors` only catches `ACHError`, server.py:86-99) → masked crash at startup (server.py:217). Defeats `verify_chain`'s documented "always return ChainStatus, flag truncation" contract and the STOP-on-`ok=False` workflow.
**Fix:** catch `(json.JSONDecodeError, KeyError)` per-line; treat malformed trailing line as truncation → `ok=False`, not a raise.

### S2. `analyst_confirmed` grade not bound to the specific cell judgment
**`store.py:242-257`** (tool surface server.py:157-165)
Gate only checks the *evidence item* currently carries an `analyst_confirmed` signal — not that a human reviewed *this* (evidence×hypothesis) rating. Once any evidence item is ever analyst-confirmed, a caller can label a fresh model-generated `rate_cell` as `judgment_source="analyst_confirmed"` and it's scored as human-vetted. Code's M4 comment already flags this as known-open. This is the judgment-input-vs-computed boundary leak.
**Fix:** bind confirmation to the specific rating (a `confirm_cell` step stamping a cell-specific token derived from the cell `row_hash`/nonce that `rate_cell` must match). Until closed, don't treat `analyst_confirmed` cells as a genuine human-in-the-loop guarantee.

### S3. `chmod` failures silently degrade the whole tamper-evidence trust model
**`server.py:36-39`, `store.py:92-97`, `staleness.py:53-59`**
Design states tamper-evidence "rests entirely on OS file-permission isolation" (server.py:67-70), yet all three `chmod` calls swallow `OSError` with bare `pass` + no log. On a filesystem forbidding chmod (the comment's own example) the server prints "chains OK; serving" with zero signal the one load-bearing control failed.
**Fix:** on `OSError`, `print(..., file=sys.stderr)` a clear warning that permissions could not be restricted → tamper-evidence NOT enforced on this filesystem.

### S4. `rate_cell` `strength` mandatory even when semantically meaningless
**`server.py:150-156`**
`strength` has no default → required on every call, but its own description says it's "only read when consistency=='I'; supply 'weak' as a placeholder" for C/N/A. Highest-traffic tool forces agents to fabricate a no-op value on most calls (conditional-requirement not modeled).
**Fix:** default `strength = "weak"`, optional exactly where it's a no-op.

### S5. `get_matrix` returns all `cells` unpaginated (unlike `list_matrices`)
**`server.py:187-192`, `models.py:36-40`**
Up to 64 hypotheses × unbounded evidence; `score_matrix` needs every pair rated → hundreds of cells returned in one payload, no `limit`/`cursor`. Large/unbudgetable context for the caller.
**Fix:** add `limit`/`cursor` or an evidence_id/hypothesis_id filter; document max payload.

### S6. `analyst_id` hash-chained but never surfaced in any read model
**`store.py:78,267` vs `models.py:25-33` (Cell), `models.py:43-53` (CellRecord)**
Per-deployment identity supported via `ACH_ANALYST_ID` (multi-analyst anticipated) yet no read model exposes who rated a cell — only via raw DB.
**Fix:** add `analyst_id: str` to `Cell` + `CellRecord`.

---

## NICE-TO-HAVE (condensed)
- **Unbounded ledger growth:** `add_hypothesis` callable unlimited times → 64-cap trivially bypassed; `rate_cell` has no re-rate/supersede cap → `verify_chain` O(n) scan unbounded (security #4). Add per-matrix hypothesis cap + coarse volume guard.
- **No tool annotations:** add `readOnlyHint` to `get_matrix`/`list_matrices`/`verify_chain` (protocol #2).
- **`add_hypothesis` read-back doesn't name new `hypothesis_id`** — only inferable as last array element (protocol #3). Document or return it top-level.
- **Read paths (`get_matrix`/`list_matrices`/`score_matrix`) unlocked** on shared `check_same_thread=False` connection — relies implicitly on SQLite serialized-mode build; document or lock (protocol #4). (Same root as M1.)
- **Batch `rate_cells` tool** — N×M matrix needs N×M round-trips before `score_matrix` (quality #5). Add atomic batch append.
- **`case_id` unvalidated free text**, no registration/lookup, no cross-check that `evidence_id` belongs to matrix's case (quality #6, security #6). Name source-of-truth in field description.
- **Value-domain literals duplicated** `store.py:36-38` vs `models.py:9-11` (SF7 defense-in-depth is intentional, but hand-copied → drift risk). Derive store tuples via `typing.get_args(Consistency)` etc. (python #4).
- **`consistency` terse codes "C"/"I"/"N/A"** — LLM-recall-error-prone; descriptive tokens if a hash-domain migration is ever on the table (quality #7).
- **Untyped `Callable` decorator** server.py:86 (python #5); **stores never `close()`'d / no `atexit`** → no clean WAL checkpoint on shutdown (python #6); **N+1 in `list_matrices`** store.py:397 (python #3); **dangling docstring** server.py:170 (quality #8).

---

## Solid (no finding — verified)
- **SQL injection:** all values bound as `?`; only interpolated identifiers are table names from hardcoded `_TABLES`, allow-list-guarded in `_head` (store.py:105-106). Clean.
- **Path traversal:** DB/manifest paths resolved once from server env at startup, never from tool params.
- **stdio:** all diagnostics `print(..., file=sys.stderr)`; `show_banner=False` suppresses FastMCP's version-check egress (server.py:223-225 — assumption, pin fastmcp to keep it true).
- **Structured output / read-back:** every tool returns a pydantic model; every mutating tool returns a genuine post-write read-back, not an input echo.
- **Error boundary:** `_translate_ach_errors` + `mask_error_details=True` → no unshaped uncaught exception reaches the client (except S1's manifest edge).
- **Value-domain enforcement** double-checked at store level (store.py:33-38) independent of pydantic; **genesis/tamper + truncation reconciliation** logic sound; **no secrets** anywhere.

---

MUST_FIX_COUNT: 2
