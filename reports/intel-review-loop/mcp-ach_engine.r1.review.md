# ACH-engine MCP server — Review r1

Target: `intelligence-analysis-agent/mcp_servers/ach_engine/{server,store,models}.py`
(+ shared `mcp_servers/common.py`, `mcp_servers/staleness.py`).
Reviewers: mcp-protocol-advisor, mcp-security-advisor, mcp-quality-advisor, python-reviewer.
Mode: READ ONLY (no edits).

## Test gate

`cd intelligence-analysis-agent && python -m pytest tests/ -q` → **99 passed, 0 failed.** No test must-fix.

---

## MUST-FIX (dedup, ranked)

### M1 — `rated_ts` excluded from hashed payload → staleness gate silently tamperable
`store.py:165-179` (rate_cell hash payload) + `store.py:303-307` (`_payload_for`). `rated_ts` is
stored and drives `_cell_stale` (`store.py:197-199`) and the `score_matrix` staleness blocker
(`store.py:229-230`), but is never in the hashed dict. A raw `UPDATE cells SET rated_ts=...` changes
business-logic behaviour with **zero hash recomputation** — `verify_chain` still returns `ok=True`.
→ Add `rated_ts` (and every DB column that feeds logic) to the hash payload in `rate_cell` AND
`_payload_for`. (security)

### M2 — `verify_chain` ignores the manifest → trailing-row truncation undetected
`store.py:269-293`. `verify_chain` recomputes the chain purely from rows currently in the tables; it
never reads `manifest_path` (written on every insert, `store.py:83-87`). Deleting the last N rows
leaves a self-consistent shorter chain → `verify_chain` reports `ok=True` with a lower
`rows_verified`, silently. Manifest is dead code from the verifier's view.
→ In `verify_chain`, reconcile computed head/row-count per table against the last manifest entry.
(security)

### M3 — Manifest written before DB commit + no rollback → manifest records uncommitted rows
`store.py:97-125` (`create_matrix`/`_insert_hypothesis`/`add_hypothesis`) call `_append_manifest`
right after `execute()`, then `commit()` later — opposite of `rate_cell` (commit at :180 then
manifest at :181). A crash/failure between manifest write and final commit records a `row_hash` for a
row never durably committed; no `rollback()` exists anywhere. Breaks the exact integrity guarantee the
store exists for.
→ Move every `_append_manifest(...)` to after its `commit()` (mirror `rate_cell`); wrap each
multi-statement write in `with self._conn:` / try-except + `rollback()`. (python)

### M4 — `judgment_source` is a self-attested tool param → bypasses the `model_draft` scoring gate
`server.py:47-62`, `store.py:151-186,231-232`. `rate_cell` takes `judgment_source` verbatim from the
caller. Nothing separates "a human confirmed this" from "the agent that computed the rating typed the
label." An agent can pass `judgment_source="analyst_confirmed"` for its own draft and sail through the
`model_draft` blocker. The collect-then-grade cross-check (`staleness.latest_grade_source`) protects
only the *evidence grade*, not the *cell rating's own* source — real hole in the judgment vs
collect-then-grade boundary the docstrings sell as a guarantee.
→ Don't trust a plain param for confirmation; require an out-of-band signal (distinct human-only
confirm tool, or a `grade_signals`-style cross-store signal) before a cell may carry
`analyst_confirmed`. (security; quality #3/#4 corroborate the boundary is under-specified)

### M5 — `rate_cell` returns hardcoded `superseded=False` even on a correction
`store.py:160,182-186`. `prior = self._effective_cell(...)` is computed to gate the `reason`
requirement, but the returned `CellRecord` hardcodes `superseded=False` regardless. This
engine-computed field always lies → the agent can never trust the read-back to tell a correction from
a new rating; corrupts the judgment/computed boundary the schema exists to keep clear.
→ `superseded = prior is not None`. (protocol + quality, both must-fix)

### M6 — `ACHStore` sqlite connection missing `check_same_thread=False`
`store.py:50` vs sibling `staleness.py:28-32`, which sets it explicitly with a comment warning FastMCP
may dispatch a tool body on a worker thread (default `True` → `sqlite3.ProgrammingError`). `ACHStore`
missed the same fix → exposed to the exact failure the sibling was hardened against; surfaces as an
unhandled internal exception to the model. (Tests pass because they call on one thread.)
→ `sqlite3.connect(db_path, check_same_thread=False)`; keep single-writer discipline / add a write
lock. (protocol + security + python, 3-way consensus)

---

## SHOULD-FIX

- **S1 — `list_matrices` cursor unguarded + tool not wrapped.** `store.py:259` `int(cursor)` raises an
  uncaught `ValueError` on a malformed cursor; `server.py:86-89` (`list_matrices`) and
  `verify_chain` are the only tools with no `try/except ACHError → ToolError` wrapper, so raw
  exceptions leak to the client. → Guard the parse (`raise ACHError("invalid cursor")`) and wrap both
  tools like their siblings. (protocol/security/python, consensus)
- **S2 — `assert table in _TABLES` is the only SQL-identifier guard.** `store.py:77,275`. Assertions
  are stripped under `python -O`, re-opening f-string interpolation of `table`. → Replace with an
  explicit `if table not in _TABLES: raise ValueError(...)`. (python)
- **S3 — No length bounds / non-empty checks on caller free-text & IDs.** `case_id`, `hypothesis`
  text, `reason`, `evidence_id`, `hypothesis_id` (`server.py:29,39,48-55`; `models.py`). Append-only,
  never pruned → unbounded chain growth (resource exhaustion); empty/whitespace hypothesis text
  (`store.py:107-125`) and blank `evidence_id` (`store.py:151-162`) are silently accepted. → Add
  `Field(max_length=...)` + `min_length=1`/`.strip()` checks; mirror `create_matrix`'s fail-fast.
  (security + quality)
- **S4 — `evidence_id` origin/validity undocumented and unvalidated at write time.** `evidence_id`
  is minted by the separate evidence-ledger server (`staleness.py:100-107`), but `rate_cell` neither
  says so nor checks existence — deferred to a later opaque `score_matrix` blocker. The blocker
  message (`store.py:224-228`) is identical for "never registered (typo)" vs "registered but
  ungraded," so a typo is told to "grade it" (wrong remediation). → Document that `evidence_id` must
  reference an evidence-ledger item; validate at rate-time; distinguish the two failure modes in the
  message. (quality)
- **S5 — Judgment-input enum semantics not on the tool surface.** `rate_cell` docstring never defines
  `Consistency` (`C`/`I`/`N/A`) or `Strength` (`strong`/`weak`) (`models.py:9-10`), and never warns
  that `judgment_source="model_draft"` will later block `score_matrix`. Agent must guess ACH
  semantics / discovers the constraint after the fact. → Spell out enum meanings + the model_draft
  consequence via docstring `Args:` / `Field(description=...)`. (quality + protocol #5)

---

## NICE

- N1 — Tool docstrings are prose, not `Args:` sections → no per-param `description` in `inputSchema`
  (`server.py:28-95`). Add `Args:` / Pydantic `Field(description=...)`. (protocol/quality)
- N2 — `RankItem` (`models.py:56-59`) carries only `hypothesis_id`; agent must cross-call
  `get_matrix` to resolve text before presenting a ranking. Add `text`. (quality)
- N3 — No batch `rate_cells`; n×m round trips for a full matrix. Consider a batch variant. (quality)
- N4 — `verify_chain` docstring doesn't tell the agent to stop/escalate on `ok=False`. Add guidance.
  (quality)
- N5 — `close()` defined but never called; register `atexit`/`finally` around `mcp.run()`.
  (python)
- N6 — `rate_cell` (`store.py:151-153`) missing param type hints, inconsistent with the rest of the
  file. Annotate. (python)
- N7 — `analyst_id` is one static `ACH_ANALYST_ID` env value, not per-caller → weak audit trail if
  the process serves multiple analysts. (security)

---

## Confirmed clean (no finding)

- **SQL injection:** all queries parameterized; the only interpolated identifier (`table`) is drawn
  from the fixed `_TABLES` tuple (guarded — see S2). (security + python)
- **No-egress:** no `requests`/`httpx`/`urllib`/`socket` import in any reviewed file; no network path
  (no OSINT path present in this server). (security)
- **Secrets:** none embedded; `DB_PATH`/`STALENESS_DB`/`ACH_ANALYST_ID` are env with local-path
  defaults. (security)
- **stdio hygiene:** `main()` (`server.py:98-104`) sends startup + chain-failure diagnostics to
  `sys.stderr` only; nothing pollutes the stdout JSON-RPC stream. (protocol)
- **Genesis / canonicalization:** `_head` returns `GENESIS = "0"*64` for empty tables (matches
  verifier start `prev`); `canon()` uses `sort_keys=True` + fixed separators. (security)
- **Structured output:** all tools declare explicit Pydantic return types (well-formed output
  schemas); score is engine-computed with no caller-injectable `Ranking`. (protocol + security)

## Residual risk (accept or mitigate, not a discrete bug)

Even after M1/M2, this is a local, unsigned, unanchored hash chain: an attacker with direct write
access to both the sqlite file and the manifest can forge a fully self-consistent alternate chain
from genesis. Internal consistency ≠ authenticity vs a privileged attacker. Mitigate only with an
external anchor (signed checkpoint / remote WORM log).

MUST_FIX_COUNT: 6
