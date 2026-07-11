# Review — osint_toolkit FastMCP server (r3)

**Target:** `mcp_servers/osint_toolkit/` (intelligence-analysis-agent)
**Mode:** READ-ONLY, single pass. 4 parallel lenses (mcp-protocol / mcp-security / mcp-quality / python) + test gate.
**Files (actual):** `server.py`, `models.py`, `artifacts.py`, `audit.py`, `egress.py`, `exif.py`, shared `mcp_servers/common.py`.
**Note:** requested `store.py` / `staleness.py` do **not** exist in this package — `artifacts.py` (file-backed) + `audit.py` (sqlite hash-chain) fill the store role. (`mcp_servers/staleness.py` is a *sibling* package's file, cited only as a 0600-hardening precedent.)

## Test gate
`cd intelligence-analysis-agent && python -m pytest tests/ -q` → **122 passed, 0 failed.** No test-derived must-fix.

---

## MUST-FIX

### MF1 — Blocked exfiltration attempt leaves NO audit row (breaks documented control #10)
`server.py:109-110` (`search`), `server.py:134` (`fetch`) — verified in source.
`_screen(query)` / `_screen(url)` runs **before** the first `audit.record(...)`. When `_screen` raises `ToolError` (a case-identifier exfil hit — exactly the event most worth logging), the function returns before any audit row is written. The file's own invariants (control #10 "every outbound call audited"; MF2 "a real fetch that dies must still leave a log row") are violated on the one path that matters most.
**Fix direction:** record an `attempt`/`blocked (screen)` audit row before/around `_screen`, mirroring the pre-egress `audit.record(... "attempt")` already used at `:144`/`:152`.
Reported by: python-reviewer. **CONFIRMED** in code.

### MF2 — `res.data.evidence_id` deref crashes on shape-drift; guard covers only the `None` case
`server.py:309-311` — verified. Guard at `:309` handles `res.data is None`, but `:311` then does attribute access `res.data.evidence_id`. If fastmcp `Client.call_tool` returns `.data` as a plain `dict` (common when the caller holds no client-side pydantic model for the callee output schema) or a shape-drifted object, `.evidence_id` raises `AttributeError` — masked to an opaque error instead of the intended clear `ToolError` (the S2 comment states that exact intent but under-implements it).
**Failure:** evidence-ledger returns a well-formed structured result as a dict → every (or most) ledger writes surface as a generic masked error; write path looks broken.
**Fix direction:** normalize `res.data` (dict-or-model) before deref, or `getattr`/`.get` with an explicit `ToolError` on missing `evidence_id`.
Reported by: mcp-protocol + python. **CONFIRMED** the guard is incomplete; the "every successful write" magnitude is fastmcp-version-dependent (PLAUSIBLE).

### MF3 — `verify_chain()` cannot detect tail-truncation → "append-only / un-forkable" claim not met
`audit.py` `verify_chain` (re-derives `row_hash` forward from `GENESIS`, checks `prev_hash` linkage only); relied on at startup `server.py:337-341`.
No externally persisted checkpoint (expected head hash / row count) exists, and the chain hash is **unkeyed/public**. An operator or local attacker with write access to `audit.db` can delete the last N rows (e.g. an `attempt`→`ok` egress pair) — the remainder stays self-consistent and `verify_chain()` still returns `ok=True`, silently erasing an egress event from the control-#10 trail. A full rewrite recomputes cleanly for the same reason.
**Fix direction:** anchor the head (persist expected head hash + count out-of-band, or HMAC-key the chain) so truncation/rewrite is detectable.
Reported by: mcp-security. **CONFIRMED** structurally (forward-only re-derivation, no anchor).

---

## SHOULD-FIX

### SF1 — Security-critical `confirmed`/`pii` booleans are self-asserted by the calling agent (collect-vs-judgment boundary)
`server.py:119-125` (`fetch`), `:210-217` (`reverse_image_search`), `:239-246` (`get_map_tile`), `:265-271` (`propose_to_ledger.pii`).
Each gates real-world consent (unconfirmed fetch / subject-image upload / coordinate disclosure / life-safety PII redaction) behind a plain client bool the docstring says the "host MUST bind to real human approval." **By design** the binding is delegated upstream — so this is the documented judgment-input boundary, not a package bug. But: (a) nothing in the JSON schema signals these are approval-bound controls vs ordinary optional flags, and (b) `pii` **defaults to `False`** on a life-safety redaction decision. A prompt-injected/compromised agent sets `confirmed=True` / `pii=False` with zero friction.
**Fix direction:** make `pii` non-defaulting (force an explicit assertion); mark these fields in schema/annotations as host-bound approval gates so the boundary is discoverable, not prose-only.
Reported by: quality (#1,#2) + security (#1). Deliberate boundary — hardening, not correctness.

### SF2 — Startup fail-closed gates live only in `main()`; bypassable by an alternate entrypoint
`server.py:337-361` (audit-chain-integrity refusal + loopback-only `EVIDENCE_LEDGER_URL` check). Both run only inside `main()` (guarded by `__main__`). `fastmcp run server.py:mcp`, a test harness, or a different supervisor that imports the module-level `mcp` and calls `.run()` skips both — a broken chain (MF3) still serves, and a hostile `EVIDENCE_LEDGER_URL` silently receives unscreened `case_id`/`source_id`/`note` (routed WITHOUT `_screen`/`validate_url`/audit per `:320-334`).
**Fix direction:** move both gates to import time or into the guarded tool bodies (fail-closed regardless of entrypoint). Supported path runs `main()`, so should-fix not must.
Reported by: mcp-security (#4).

### SF3 — Unaudited exception types escape `fetch`/`audit.record`, breaking the "every call audited" invariant inconsistently
`server.py:153-166` catches only `EgressError`/`OSError`/`ssl.SSLError`/`http.client.HTTPException`; any other error from `fetch_pinned`/`_resolve_redirect` propagates uncaught → no audit row. Separately, every `audit.record(...)` call is itself unwrapped: a transient `sqlite3.OperationalError` (DB locked/disk full) propagates as an opaque masked error instead of the file's deliberate `ToolError` taxonomy.
Reported by: python (#2) + mcp-protocol (#2).

### SF4 — Store files created without restrictive permissions (0600)
`audit.py:22-38` (`audit.db` + `-wal`/`-shm`) and `artifacts.py:33-43` (fetched images/docs w/ possible subject location/likeness) rely on umask only, unlike the sibling `StalenessStore` 0600 pattern. Another local account can read resolved-internal-IP recon data / sensitive artifacts, bypassing the MCP boundary.
Reported by: security (#3,#5).

### SF5 — `_session_urls` global: unbounded, unlocked, and not session-partitioned
`server.py:67,169`. Module-level `set`, no TTL/cap/eviction (unbounded memory in a long session), mutated with no lock (other shared state uses `self._lock`), and single process-wide — under a future multi-session transport (Streamable HTTP) one client's fetched-URL provenance would satisfy another client's `confirmed=False` gate at `:132` (cross-session leak). Safe only under today's 1:1 stdio.
Reported by: python (#4) + protocol (#5) + security (#8).

### SF6 — Exfiltration screen is a coarse, defeatable substring check
`server.py:84-97` (`_norm_screen`/`_screen`) casefold + strip-non-alnum only. Identifier interleaved with an extra char (`CASE1X234`) or Base64/hex/URL-encoded passes; it is the sole content-level control on the egress surface.
Reported by: security (#7).

### SF7 — Stub tools always fail, but schemas advertise full success types; failure caveat buried
`server.py:100-113` (`search`), `:206-230` (`reverse_image_search`), `:233-256` (`get_map_tile`) unconditionally `raise ToolError` (no live connector) yet register rich output schemas (`SearchResult`/`CandidateMatches`/`MapTile`). Worse, `fetch`'s docstring teaches a `search → fetch` provenance flow that **cannot succeed** (stub `search` never populates `_session_urls`), so an agent burns turns retrying a by-design-non-functional path.
**Fix direction:** surface "not configured in this deployment" structurally (or gate registration on `OSINT_LIVE`); correct `fetch`'s docstring to state the flow is inert here.
Reported by: quality (#4,#6).

### SF8 — Missing per-field schema descriptions / caps on `artifact_ref` (schema-vs-doc drift)
`server.py:176` (`compute_hash`), `:185` (`extract_exif`), `:208` (`reverse_image_search`) declare `artifact_ref: str` with **no** `Field(max_length=...)` — contradicting the file's own "every free-text field is capped" invariant (`propose_to_ledger.artifact_ref` at `:262` *is* capped). Nothing in the schema says `artifact_ref` is an opaque store token (not a URL/filename), so an agent may pass `compute_hash(artifact_ref="https://…/photo.jpg")`.
Reported by: protocol (#3) + quality (#5).

---

## NITS
- **`CONNECTOR_HOSTS` (models.py:13-17) is dead code** — defined, imported nowhere; `fetch` explicitly uses SSRF blocklist with no per-connector allowlist. Landmine for future real connectors if wired carelessly. (python #6, security #6)
- **`connector` enum shared across 3 tools** with only one sensible value each and no per-tool restriction → schema-valid nonsense calls e.g. `search(connector="image")`. (quality #3)
- **No MCP tool annotations** (`readOnlyHint`/`destructiveHint`/`openWorldHint`) on any tool, losing a client-side trust signal. (protocol #4)
- **`EgressAudit.close()` never called** (server.py:61); sqlite conn closed only at process exit — dead lifecycle API. (python #7)
- **`egress.py:119 assert pinned is not None`** in the SSRF chokepoint is stripped under `python -O`; prefer explicit `raise`. (python #8)
- **`fetch` name collision** with generic "fetch URL text" pattern — returns an opaque `artifact_ref`, not page text; agents may expect content back. (quality #8)
- **`verify_chain()` docstring** gives no trigger condition / how to react to `ok=False`. (quality #9)
- **`note` cap (500) silently truncates**; framing ("never scored") may mislead an agent into writing analysis there. (quality #7)
- **IPv6 zone-id literals** (`[::1%eth0]`) not explicitly handled in `_parse_ip_literal` (egress.py:43-58) — likely fails safe; add a regression test. (security #9)
- **Guard ordering** in `fetch` (provenance check before `_screen`) differs from other tools — align for predictable error precedence. (protocol #6)

MUST_FIX_COUNT: 3
