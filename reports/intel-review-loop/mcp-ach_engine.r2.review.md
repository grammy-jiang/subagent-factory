# Review — ach-engine MCP server (r2)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/mcp_servers/ach_engine/` (`server.py`, `store.py`, `models.py`, `__main__.py`) + used deps `mcp_servers/common.py`, `mcp_servers/staleness.py`.
**Mode:** review only, no edits.
**Reviewers (parallel):** mcp-protocol-advisor, mcp-security-advisor, mcp-quality-advisor, python-reviewer.
**Test gate:** `python -m pytest tests/ -q` → **104 passed, 0 failed** (no test-derived must-fix).

Consolidated + deduped. Cross-reviewer agreement noted per item.

---

## MUST-FIX

### MF1 — `score_matrix`: an unrated hypothesis silently wins the ranking
`store.py:287-334` (esp. 315-333). `blockers` is built only from cells that exist in `_effective_cells`. A hypothesis with **zero rated cells** — e.g. one just added via `add_hypothesis` before existing evidence is re-rated against it — never appears in `blockers`, yet is still in `hyps`/`ordered` with `strong=0, weak=0`. Sort key `(strong_inconsistencies, weak_inconsistencies)` then ranks the untested hypothesis first (0/0 beats any evaluated hypothesis). This is the exact ACH failure the design exists to prevent.
**Fix:** in `score_matrix`, block/flag any hypothesis lacking full evidence coverage (add a coverage blocker per (hypothesis × evidence) gap), or refuse to rank incompletely-rated hypotheses. Also correct `add_hypothesis` docstring (`server.py:38-40`) — new hypothesis has **absent**, not merely unrated, cells.
*(mcp-quality M1; unique — a real correctness bug, highest severity.)*

### MF2 — `mask_error_details` not set → raw internals leak to the client
`server.py:25` `mcp = FastMCP("ach-engine")`. Verified against installed fastmcp (`tools/tool_manager.py:167-172`): any non-`ToolError` (e.g. `sqlite3.OperationalError`, disk-full, latent bug) is re-raised as `ToolError(f"Error calling tool ...: {e}")` with raw `{e}` — can carry `DB_PATH` fragments / SQL text. Both sibling servers set `mask_error_details=True` with a comment naming this exact risk (`evidence_ledger/server.py:53-57`, `calibration_tracker/server.py:31-33`); ach-engine is the outlier.
**Fix:** `FastMCP("ach-engine", mask_error_details=True)`.
*(mcp-protocol M1 + mcp-quality S6 — agree.)*

### MF3 — `staleness.py:55` guards f-string SQL with `assert` (stripped under `python -O`)
`_head()` does `assert table in _TABLES` then builds `f"SELECT row_hash FROM {table} ..."` (`staleness.py:57`). Under `-O`/`PYTHONOPTIMIZE` the assert vanishes, re-opening SQL-identifier interpolation. `store.py:82-89` already fixed the **identical** hazard with an explicit `if table not in _TABLES: raise ValueError(...)` and a comment saying why; staleness.py never got the twin fix. Currently unreachable (callers pass literals) but a latent injection landmine and an in-repo inconsistency.
**Fix:** mirror store.py — replace the `assert` with an explicit raise. (Both `verify_chain` f-string loops iterate the hardcoded `_TABLES` tuple, so guarding `_head` closes the gap.)
*(python-reviewer M1; python-reviewer S2 = same f-string-SQL pattern, general form.)*

### MF4 — `verify_chain(case_id=...)` advertises a scope filter that does nothing
`server.py:107`, `store.py:351-397`. `case_id` is only echoed into `scope` (`store.py:366,387,396`); the method always walks **every** row in every table. A caller reading `scope: X, ok: True` reasonably believes case X's chain is clean when the whole DB was checked. Safe direction (over-verifies) but a broken tool contract — **both** siblings deliberately **removed** this param for this reason (`evidence_ledger/server.py:206`, `calibration_tracker/server.py:174-177`). ach-engine is the lone server exposing the dead affordance.
**Fix:** drop `case_id`, or implement real per-case scoping. Trivial; 3/4 reviewers flagged.
*(mcp-quality M2, mcp-security S3, mcp-protocol S1 — full agreement.)*

### MF5 — Hash chain is unkeyed SHA-256; FS-write access forges history undetected
`common.py:18-19` `row_hash = sha256(prev_hash + canon(payload))` — no HMAC/secret/external anchor. `verify_chain` (`store.py:351-397`, `staleness.py:115-139`) only catches tampering that doesn't recompute the trailing chain; a rewrite that recomputes hashes verifies `ok=True`. `grade_signals` (the collect-then-grade oracle, read at `store.py:295`/`216-224`) lives in the same unkeyed store — an actor with write access to `ACH_DB`/`STALENESS_DB` (**including the constrained agent itself if it also holds a filesystem/bash tool**) can insert a forged `analyst_confirmed` row, recompute forward, and pass verification. This is the core judgment-integrity guarantee the server exists to enforce.
**Fix (decision required):** either (a) explicitly document this as a residual risk resting entirely on OS file-permission isolation between agent and DB files (and enforce that isolation — process/user separation so the agent has no direct path to the DBs, restrictive `0600`/`0700` perms per N-list below), or (b) harden with an HMAC-keyed chain / external append-only anchor held outside the writer's reach. Do not leave the guarantee implicit.
*(mcp-security M1 — sole reviewer; flagged must-fix given it undermines the server's stated purpose.)*

---

## SHOULD-FIX

**Schema / self-description**
- **SF1 — No server `instructions=` string.** `server.py:25`. Sibling `evidence_ledger/server.py:38-57` ships `_INSTRUCTIONS` (lifecycle + trust model + cross-server grade gate). ach-engine's lifecycle (`create_matrix→add_hypothesis→rate_cell→score_matrix`) and its hard evidence-ledger dependency surface only reactively in `score_matrix` blocker text. *(quality S3)*
- **SF2 — No per-parameter `Field(description=...)`; docstring Args never reach the JSON Schema.** `server.py:29,39,48-55,98`. Confirmed via `fastmcp/tools/tool.py:445-449`: inputSchema comes from the bare signature; docstring `Args:` are **not** parsed into property descriptions. So `rate_cell`'s detailed C/I/N/A + strong/weak + `judgment_source` trust rules never attach to the schema. Siblings use `Annotated[X, Field(description=...)]` throughout. *(protocol S3 + quality S4 — agree.)*
- **SF3 — No input-size caps.** `case_id`, `hypothesis`, `hypotheses` list, `evidence_id`, `reason` all unbounded (`server.py:29,39,48-56`). Sibling defines `_MAX_ID/_MAX_TEXT/_MAX_ITEM` (`evidence_ledger/server.py:61-64`). Append-only tables with no reclamation → unbounded growth degrades `verify_chain` full-table scans + DoS from one call. *(protocol S2 + security S6 + quality S5 — agree.)*
- **SF4 — Output-model fields undescribed in outputSchema.** `models.py:25-33,43-53,62-66` — `row_hash`, `superseded`, `stale`/`stale_reason`, `leading`. `calibration_tracker/models.py:44-46` Field-describes its `row_hash` ("Internal chain-integrity hash… NOT a judgment or score."); a client can't tell from schema alone that `row_hash` isn't a score, or that `leading: null` = empty/no-leader. *(protocol S5; overlaps quality 12.)*
- **SF5 — `list_matrices` `limit` silently clamped, not schema-constrained.** `store.py:337` does `max(1, min(limit,1000))`; `server.py:98` has no `ge/le` and no doc of the clamp. `calibration_tracker/server.py:148` uses `Field(ge=1, le=1000)` to reject out-of-range up front — this repo's own fail-loud pattern. *(protocol S4 + quality S10 — agree.)*

**Correctness / robustness**
- **SF6 — Non-atomic manifest write → permanent refuse-to-serve after a benign crash.** `store.py:139-141,164,251` append to the manifest **after** the SQLite commit, outside the txn. A crash in that window leaves the manifest behind the tables; `verify_chain`'s reconciliation (`store.py:378-394`) then reports `ok=False (manifest)` indistinguishably from tampering, and `__main__` startup (`server.py:116-120`) hard-exits with no recovery path. Availability DoS. *(security S1)*
- **SF7 — Store trusts the pydantic Literal as the only validation for `consistency`/`strength`/`judgment_source`.** `models.py:9-11` enforce at the tool boundary, but `ACHStore.rate_cell` (`store.py:191-199`) types them `str` with no allow-list. Any direct store caller (tests, scripts, other transport) can write out-of-domain values into the hash-chained payload. Add an explicit check in the store. *(security S2)*
- **SF8 — Concurrent reads unsynchronized on the shared connection.** `store.py:51-53` serializes **writes** via `_write_lock`; reads (`_matrix_row`, `_hypotheses`, `_effective_cell`, staleness `latest_grade_source`) run unlocked. `check_same_thread=False` disables sqlite3's thread-affinity guard but does not make concurrent statement execution on one connection object safe. Plausible correctness/availability bug under concurrent tool dispatch. *(security S7)*
- **SF9 — `create_matrix` accepts degenerate inputs.** `store.py:120-122` checks `hypotheses` non-empty but not (a) `len>=2` — a 1-hypothesis matrix trivially "leads" with 0 inconsistencies; nor (b) `case_id` non-empty/whitespace (unlike the S3-style checks on hypothesis text `store.py:145-146` and evidence_id `store.py:201-202`) — a blank `case_id` groups matrices outside any real case and weakens `list_matrices` read-back. *(quality S9 + security S8)*
- **SF10 — `strength` required even when semantically inert.** `rate_cell` requires it always (`server.py:48-55`) but `store.py:321-325` reads it only when `consistency=="I"`; for `C`/`N/A` it's accepted and discarded. Schema/docstring don't say it's a no-op → agent must supply an arbitrary placeholder for most cells. Consider optional-conditional or document the no-op. *(quality S7)*

**Trust / audit**
- **SF11 — No caller/session identity; static `analyst_id` for the whole process.** `store.py:49` reads `ACH_ANALYST_ID` once; every row stamped with it (`store.py:247`). Multiple sessions sharing one process are indistinguishable in the tamper-evident trail — weakens the accountability the chain provides. *(security S4)*
- **SF12 — Rejected policy-violation attempts not persisted.** `store.py:216-224` blocks a self-attested `analyst_confirmed` and raises `ACHError` → surfaced only to the same caller. An agent trying to forge a confirmed judgment is a real security signal with no durable trace. *(security S5)*

**Python / structure**
- **SF13 — DRY: `except ACHError as e: raise ToolError(str(e)) from e` duplicated verbatim in all 7 tools.** `server.py:32-113`. Extract a `@translate_ach_errors` decorator applied above each `@mcp.tool`. *(python-reviewer 3)*
- **SF14 — Module-level DB/dir side effects at import.** `server.py:16-25` opens real SQLite connections and runs `os.makedirs` purely on `import server`; couples load to `ACH_DB`/`STALENESS_DB` env + filesystem, blocks side-effect-free import for tests. FastMCP needs only `mcp` at module scope — defer store/staleness construction into `main()` or a lazy singleton. *(python-reviewer 4)*
- **SF15 — `main()` uses bare `mcp.run()`.** `server.py:116-122` vs siblings' `mcp.run(transport="stdio", show_banner=False)` (`evidence_ledger:230`, `calibration_tracker:192`) citing the no-egress invariant. Verified: in this fastmcp the banner goes to stderr (`utilities/cli.py:272`), so not a live stdout-corruption/egress bug today — but an unexplained deviation losing the siblings' defense-in-depth. *(protocol S6)*
- **SF16 — Path handling: raw concat + unnormalized `..` + discarded `abspath`.** `server.py:16-21` builds `_DATA` with `../../data` never normalized; `os.makedirs(os.path.dirname(os.path.abspath(p)))` computes then discards the abs path while `DB_PATH` keeps the relative form (fragile vs any `os.chdir`). Also `store.py:50` `db_path + ".manifest.jsonl"`. Prefer one `pathlib.Path(...).resolve()` reused for makedirs + connect. *(python-reviewer 6)*

---

## NITS
- **N1 — Cell/granularity + `row_hash` token overhead.** `rate_cell` is one cell/call; a 10×5 matrix = 50 sequential calls, each returning a `CellRecord` with a 64-char `row_hash` of no analytic value to the agent. Consider a batch `rate_cells` tool and/or omitting `row_hash` from the agent-facing payload. *(quality 8/12)*
- **N2 — `Consistency` literal `"N/A"` contains `/`.** Valid enum, atypical for an LLM-facing literal; `"NA"` more conventional. `models.py:9`. *(quality 11)*
- **N3 — `_effective_cells` ordering comment overstates guarantee.** `store.py:259-266`: value is latest-wins, but dict keeps first-insertion position, so `list(eff.values())` is ordered by first occurrence, not winning-row seq. Harmless today; fix comment or sort by seq if consumers rely on recency order. *(python-reviewer 5)*
- **N4 — Dead defensive `.get(key, 0)`.** `store.py:323,325`: `strong`/`weak` pre-seeded for every hypothesis_id (`:316-317`) and `rate_cell` validates membership → simplify to `strong[...] += 1`. *(python-reviewer 7)*
- **N5 — `except (TypeError, ValueError)` around `int(cursor)`** where `cursor: str | None` — `TypeError` branch likely unreachable if FastMCP/pydantic validate args first. `store.py:338-341`. Comment which case it defends or drop. *(python-reviewer 8)*
- **N6 — `_payload_for` bare `dict` return annotation.** `store.py:399`; prefer `dict[str, str | float]`. *(python-reviewer 9)*
- **N7 — No tool `annotations` (readOnlyHint).** `server.py` — read-only tools (`get_matrix`, `list_matrices`, `score_matrix`, `verify_chain`) indistinguishable from mutating ones at the hint level. Advisory-only. *(protocol N1)*
- **N8 — No restrictive DB/manifest file perms.** `server.py:19-21`, `store.py:94` rely on umask; for intel case data prefer explicit `0700`/`0600`. *(security N2)*
- **N9 — TOCTOU in `analyst_confirmed` check.** `store.py:216-224` reads grade source before the write lock; a concurrent downgrade could pass — but `score_matrix` re-checks live grade at scoring (`store.py:295`), so scored output can't be corrupted. Low. *(security N1)*

---

## Verified clean (no finding)
- **SQL injection:** all data-bearing queries parameterized (`?`); only interpolated identifiers are table names from the hardcoded `_TABLES` allow-list (never caller input) — genuinely safe (modulo MF3's `-O` gap).
- **No-egress:** no `requests`/`httpx`/`urllib`/socket anywhere under `ach_engine/`; SQLite + local JSONL manifest only. (osint carve-out N/A here.)
- **Secrets:** none embedded; only non-secret `ACH_ANALYST_ID` + paths from env.
- **Judgment vs collect-then-grade boundary (logic, apart from MF5 forgery risk):** correctly enforced — `rate_cell` refuses self-attested `analyst_confirmed` unless the cross-store signal already says so (`store.py:216-224`); `score_matrix` independently re-verifies grade source + staleness + `model_draft` at scoring time (`store.py:291-313`), the right place.
- **stdio hygiene:** only `print(..., file=sys.stderr)` (`server.py:119,121`); nothing on stdout outside the protocol stream.
- **Structured output:** every tool returns a named Pydantic model (never a bare array); `list_matrices` returns `MatrixList{items, next_cursor}` with correct over-fetch-by-one cursor pagination and `ACHError` on a bad cursor.

MUST_FIX_COUNT: 5
