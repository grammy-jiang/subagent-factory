# osint_toolkit MCP server — Review R1

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/mcp_servers/osint_toolkit/`
**Files read:** `server.py`, `models.py`, `audit.py`, `artifacts.py`, `egress.py`, `exif.py`, `__main__.py` + imported `mcp_servers/{common,staleness}.py`, `mcp_servers/evidence_ledger/{store,server}.py`. (No `store.py` in this package — evidence writes go through `evidence_ledger.store.EvidenceStore`.)
**Reviewers:** mcp-protocol-advisor, mcp-security-advisor, mcp-quality-advisor, python-reviewer.
**Test gate:** `python -m pytest tests/ -q` → **110 passed, 0 failed.** No test failures → no test-derived must-fix.

Findings deduped across reviewers. `[P]`=protocol `[S]`=security `[Q]`=quality `[Py]`=python.

---

## MUST-FIX

### M1. evidence.db double-writer → crash at import time `[P·S]`
`server.py:51` opens `EvidenceStore(_EVIDENCE_DB, _staleness)` on the **same** default file (`data/evidence.db`) that `evidence_ledger/server.py:36` also opens. `EvidenceStore.__init__` takes an OS-exclusive `fcntl.flock(LOCK_EX|LOCK_NB)` for the process lifetime (`evidence_ledger/store.py:79-90`, "refusing to open a second writer") **at module import**, before `mcp.run()`. Both servers must run concurrently (osint proposes → analyst grades via evidence_ledger → ach scores); whichever starts second raises uncaught `EvidenceError` before completing the MCP `initialize` handshake. Breaks the default multi-server topology + the collect-then-grade pipeline.
**Fix:** route `propose_to_ledger` through evidence_ledger over the MCP/RPC boundary (not a second in-process writer), or make the lock write-scoped rather than lifetime-held.

### M2. `propose_to_ledger` bypasses evidence_ledger's input-size caps `[S·P·Q]`
`server.py:165` — `case_id`/`source_id` (and `note`) have no length constraint; call goes straight to `EvidenceStore.add_evidence()`. The S7 caps (`_MAX_ID=512`, `_MAX_ITEM=100_000`) live only on evidence_ledger's **own** FastMCP tool schema (`evidence_ledger/server.py:61-64,80-82`), enforced by Pydantic on that tool — a direct Python call bypasses them entirely. A compromised/confused caller writes unbounded-length fields into the shared **append-only hash-chained** ledger.
**Fix:** add `Annotated[str, Field(max_length=...)]` matching `_MAX_ID` to `propose_to_ledger`, **or** (better, un-bypassable) move size-cap enforcement into `EvidenceStore.add_evidence()` itself.

### M3. `mask_error_details=True` missing `[P]`
`server.py:54` — `FastMCP("osint-toolkit")` omits `mask_error_details=True`. All three sibling servers set it (`ach_engine/server.py:77`, `calibration_tracker/server.py:33`, `evidence_ledger/server.py:53-57`). Without it, any non-`ToolError` (sqlite error, disk-full, internal bug) leaks raw `str(e)` — DB paths, SQL fragments — to the client. osint_toolkit is self-documented as "the SOLE external-egress surface" processing untrusted fetched bytes (EXIF, artifact I/O) — highest-risk server, only one unmasked.
**Fix:** add `mask_error_details=True` to the constructor.

### M4. Socket fd leak on TLS handshake failure → DoS `[Py]`
`egress.py:121-132` (`_pinned_https_get`) — `raw_sock = socket.create_connection(...)` and `tls = ctx.wrap_socket(raw_sock, ...)` both run **before** the `try/finally`. If `wrap_socket` raises (bad cert / handshake timeout — routine for an SSRF-hardened fetcher probing hostile hosts), `tls` never binds, `finally: tls.close()` never runs, `raw_sock` never closes. Each failed handshake leaks one fd → fd exhaustion (process DoS).
**Fix:**
```python
raw_sock = socket.create_connection((ip, 443), timeout=15)
try:
    tls = ctx.wrap_socket(raw_sock, server_hostname=host)
except Exception:
    raw_sock.close()
    raise
```

---

## SHOULD-FIX

### Provenance gate / `_session_urls`
- **S5. `_session_urls` never populated by `search`/`reverse_image_search` `[Q·Py·P·S]`** — `server.py:52` comment says the set holds "URLs returned by prior search," but only `fetch` inserts (line 100). When live connectors ship, the "must come from a prior search result" gate (line 80) becomes permanently unsatisfiable via the intended path — only `confirmed=True` works, defeating the two-tier design. **Becomes MUST-FIX the moment a live connector is wired.** Today: fix the comment or add candidate URLs to the set before returning.
- **S6. `_session_urls` is an unscoped, unlocked, unbounded process-global `[S·Py]`** — `server.py:52,80,100`. Named "session" but shared across every case/client/connection with no lock, no eviction/TTL. One client's confirmed fetch satisfies the bypass for an unrelated case (isolation break); unbounded memory growth (DoS). **Fix:** scope by case_id/session, cap size + evict, add a lock.

### `confirmed` flag
- **S7. `confirmed: bool` is a plain caller-supplied arg, not a verified human signal `[S·Q]`** — `server.py:77` (fetch), `:138` (reverse_image_search). Nothing stops the calling model from setting `confirmed=True` itself; server can't tell human approval from LLM self-approval. If the host doesn't hard-wire UI approval to this exact flag, control #7c is self-satisfied. **Fix:** use a FastMCP elicitation call, or document that the host MUST gate this param.

### Egress / info disclosure
- **S8. DNS-resolution oracle in tool-error text `[P]`** — `server.py:90` returns the resolved `ip` in the client-facing `ToolError` for any valid non-blocked host, usable without `OSINT_LIVE` (via `confirmed=True`). IP already in the audit record (line 89). **Fix:** generic client message; keep IP audit-only.
- **S9. Audit `outcome` column bypasses the field allowlist `[S]`** — `audit.py:40-54` filters `fields` through `LOGGABLE_FIELDS` (because query/url carry case identifiers) but stores `outcome` verbatim; `server.py:86,96` interpolate raw `EgressError` text (`f"blocked: {e}"`) which can include `host`. Defeats the fail-closed "never log an unlisted field" guarantee for the one free-text column. **Fix:** map EgressErrors to a fixed set of reason codes.
- **S10. `_default_resolver` catches only `socket.gaierror` `[Py]`** — `egress.py:61-65`. Other resolution failures (`UnicodeError` from IDNA-invalid host, `OSError`) escape unwrapped, bypassing the `EgressError` taxonomy that `fetch` converts to `ToolError`. **Fix:** catch `(socket.gaierror, UnicodeError, OSError)` or re-raise as `EgressError`.

### Missing controls (flag before `OSINT_LIVE`)
- **S11. Exfil screen silently no-ops when unconfigured `[S]`** — `server.py:39,57-62`: `CASE_IDENTIFIERS` defaults empty → `_screen()` blocks nothing, no startup warning. Operator can believe control #7a is active when inert. **Fix:** loud startup warning, or refuse `OSINT_LIVE` with empty identifier set.
- **S12. Startup verifies only the egress-audit chain `[S]`** — `main()` `server.py:184-191` calls `audit.verify_chain()` fail-closed, but `_evidence`/`_staleness` are written (`propose_to_ledger`) with no chain check. Tampered/forked ledger not detected before appending. **Fix:** also `verify_chain()` those, refuse to serve on failure.
- **S13. Design controls #7b (block collection targeting a named private individual, fail-closed) and #8 (per-connector rate-limit/budget/circuit-breaker) unimplemented `[S]`** — per `docs/design/phase4-osint-design.md` §65 these are "load-bearing, ship together"; grep finds no impl. Only #7a + SSRF guard present. Flag before enabling live connectors.

### Concurrency / lifecycle (`[Py]`)
- **S14. `audit.py:22` `sqlite3.connect()` omits `check_same_thread=False`** — every sibling store sets it (FastMCP may dispatch a tool body on a worker thread). If that happens, the audit trail gating `main()`'s fail-closed check raises `sqlite3.ProgrammingError` while others keep working.
- **S15. `EgressAudit.record()` has no lock (TOCTOU hash-chain fork) `[Py]`** — `audit.py:36-54`: read-head → hash → INSERT unguarded. `EvidenceStore` guards this exact sequence with `_write_lock` (SF2/SF3/M1). Two concurrent calls read the same `prev_hash` and both insert → forked chain that `verify_chain()` depends on. **Fix:** wrap head-read+insert+commit in a `threading.Lock`, mirroring `EvidenceStore`.
- **S16. `EvidenceStore.__init__` not exception-safe `[Py]`** — `evidence_ledger/store.py:34-58`: `flock` taken before `sqlite3.connect`; if the WAL-mode check raises `EvidenceError`, `_lock_fh` never releases and `_conn` never closes. In-process retry then gets a misleading "already open by another process" from its own leaked lock. **Fix:** try/except around connect/WAL that releases lock + closes conn before re-raising. (Cross-package; flag to evidence_ledger owner.)

### Schema / tool quality (`[Q]`)
- **S17. No `Field(max_length=...)` on any string param `[P·Q]`** — `server.py:66,77,165` (`query`,`url`,`case_id`,`source_id`,`note`,`artifact_ref`). Overlaps M2. Also add per-param bounds so oversized input is rejected at JSON-Schema validation, matching `evidence_ledger/server.py:80-149`.
- **S18. `note` silently truncated `[Q·P]`** — `server.py:173` `note[:NOTE_CAP]` (500); `ProposalRef` returns no truncation flag/length, caller can't tell judgment content was dropped. **Fix:** reject over-length with `ToolError`, or surface truncation in the return model.
- **S19. Stub tools always raise `ToolError`, undocumented `[Q·P]`** — `search`/`reverse_image_search`/`get_map_tile` (`server.py:66-73,137-161`) unconditionally raise "no live connector," but docstrings don't disclose it; an agent may select/retry them. Their outputSchemas (`SearchResult`/`CandidateMatches`/`MapTile`) are advertised but currently unreachable. **Fix:** state stub status in docstrings, or don't register while no connector configured.
- **S20. `CONNECTOR_HOSTS` imported but never enforced `[Py·P·S]`** — `server.py:24` imports it; `validate_url()` (`:84`) never gets `allowed_hosts`. Per-connector allowlist (design control #2) is dead code. **Fix:** thread `CONNECTOR_HOSTS[connector]` into the guard when connectors go live; drop the import until then.
- **S21. Computed provenance flattened into an opaque string `[Q]`** — `server.py:173` packs `artifact_ref`+`sha` (computed) and `note` (judgment) into one string; `ProposalRef` (`models.py:68-72`) carries no `sha256` structurally → consumers must string-parse. **Fix:** keep computed fields and note separate, structurally, in the write and in `ProposalRef`.
- **S22. `ExifData.fields` mixes raw tags with computed GPS `[Q]`** — `exif.py:38-42`, `models.py:41-47`: raw EXIF strings alongside synthesized `gps_lat`/`gps_lon` (decimal-degree conversions), no schema distinction; agent can't tell computed from passthrough. **Fix:** split raw `fields` + a typed `gps: {lat: float, lon: float} | None`.
- **S23. `pii: bool` on `propose_to_ledger` undocumented `[Q]`** — `server.py:165`, passed straight to `add_evidence` as an unvalidated judgment. Document the semantics/downstream consequence.
- **S24. Shared `Connector` Literal across three single-connector tools `[Q]`** — `models.py:9`, used by `search`/`reverse_image_search`/`get_map_tile`; schema permits `get_map_tile(connector="web")`. **Fix:** per-tool restricted Literal, or drop the param for single-connector tools.
- **S25. `max_results` unbounded `[Q]`** — `server.py:66`, while `get_map_tile` range-checks lat/lon/zoom (`:156`). Inconsistent. **Fix:** `Field(gt=0, le=100)`.
- **S26. No per-parameter `Field(description=...)` on safety-critical params `[Q]`** — clients that surface only the JSON schema get zero call-fill guidance for `confirmed`/`pii`. Add at minimum for those two.

---

## NIT
- **N1. F-string with no interpolation `[Py·P]`** — `server.py:62` `f"pre-egress gate: ...blocked"` (ruff F541). Drop `f`.
- **N2. `compute_hash` redundant round-trip `[Q]`** — `server.py:106-112`: only route to an `artifact_ref` is `fetch`, which already returns `sha256`; `extract_exif` re-hashes inline (`:121-122`). Document the distinct use, or fold hash+type-detect into one `inspect_artifact`.
- **N3. Decompression-bomb guard soft in 1×–2× `[S]`** — `exif.py:11` `MAX_IMAGE_PIXELS=64M`; Pillow only errors above 2×, warns (non-fatal) 1×–2× → ~128M-px images pass despite "resource-limited" claim.
- **N4. `MAX_IMAGE_PIXELS` is a process-wide global mutation `[S]`** — `exif.py:11` mutates PIL class attr at import, affecting all Pillow usage in-process.
- **N5. Duplicated 25 MiB caps `[S]`** — `artifacts.py:25` vs `egress.py:68`, independently defined, can drift. Single source of truth.
- **N6. `confirmed` name overloaded `[Q]`** — provenance override (fetch) vs upload consent (reverse_image_search). Rename per-tool.
- **N7. Duplicate models `[Q]`** — `SearchResult` ≡ `CandidateMatches` (`models.py:26-30`,`54-58`); share one.
- **N8. `ExifData.candidate`/`MapTile.candidate` always `True` `[Q]`** — `models.py`; carries no info, reads as a computed per-call signal. Drop or actually compute.
- **N9. Generic tool name `search` `[Q]`** — unnamespaced across a multi-server repo; consider `osint_search`.
- **N10. `_mark_staleness_signals` retry duplicates `stale_events` `[Py]`** — `evidence_ledger/store.py:196-219`: 2-attempt retry re-runs both `mark_stale`+`mark_graded` even if only the second failed → duplicate row. Isolate retry per-call.
- **N11. `Opener` fake type alias `[Py]`** — `egress.py:71` assigns a plain `str`, never referenced. Make a real `TypeAlias` and use it, or drop.
- **N12. Missing annotations `[Py]`** — `egress.py:135` `fetch_pinned` fully unannotated; `exif.py:14` `dms` param unannotated. Inconsistent with the rest of the module.
- **N13. Local mid-function `from .egress import fetch_pinned` `[Py]`** — `server.py:91`: module already loaded, buys nothing; move to top-level. (The `.exif` local import `:130` is justified — defers PIL.)
- **N14. `MapTile.artifact_ref` undocumented `[Q]`** — `models.py:60-64`; explain what artifact a map tile maps to.

---

## Verified correct (no finding)
- Artifact tokens: regex-validated server-issued UUIDs before path join (`artifacts.py:14,45-47`) — no traversal.
- SQL fully parameterized; only f-string SQL is internal literal table names guarded against a fixed `_TABLES` tuple (`staleness.py`, `evidence_ledger/store.py`).
- No shell-out/command execution anywhere.
- SSRF guard (`egress.py`): canonicalizes IP literals, blocks private/loopback/link-local/reserved/multicast/0.0.0.0/8/100.64/10, resolves once + pins socket to that IP (anti-rebinding), re-validates every redirect hop. Solid.
- Magic-byte type detection (`artifacts.py:60-65`) instead of trusting remote `Content-Type`.
- `exif.py` broad `except Exception: pass` is deliberate + documented ("never raises on adversarial input") — justified.

MUST_FIX_COUNT: 4
