# Review r2 — mcp_servers/osint_toolkit (FastMCP server)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/mcp_servers/osint_toolkit/`
**Files:** `server.py`, `models.py`, `artifacts.py`, `audit.py`, `egress.py`, `exif.py`, `__main__.py` + shared `../common.py`.
Note: no `store.py`/`staleness.py` in this package — the store role is split into `artifacts.py` (opaque-token blob store) + `audit.py` (hash-chained egress log). `../staleness.py` exists but is **not imported** by osint_toolkit (it serves evidence-ledger↔ach-engine) — out of scope.

**Test gate:** `python -m pytest tests/ -q` → **115 passed, 0 failed.** No test-derived must-fix.

**Reviewers:** mcp-protocol-advisor, mcp-security-advisor, mcp-quality-advisor, python-reviewer (4 parallel). Findings below are consolidated + de-duplicated; a finding raised by ≥2 reviewers is noted.

**Overall:** strong hardening for an egress surface — opaque-token store defeats path traversal, magic-byte type check (never trusts remote Content-Type), real SSRF blocklist with IP-literal canonicalization + per-redirect-hop re-validation, fail-closed hash-chained audit, `mask_error_details=True`, never returns raw fetched bytes. No SQL injection (audit/staleness use bound `?` params; the only f-string SQL identifier is validated against a fixed tuple). No command injection. `verify_chain` recompute/compare is correct. Findings are gaps in that otherwise-strong design.

---

## MUST-FIX (3)

### MF1 — SSRF guard leaks the resolved internal IP back to the caller (network-recon oracle)
`server.py:120` (root cause `egress.py:107`). *[security]*
When `validate_url` blocks a host that resolves to a private/loopback/link-local IP, `EgressError` text is `f"host {host} resolves to blocked IP {ip} ..."`. `fetch()`'s pre-check branch forwards it verbatim: `raise ToolError(f"egress guard blocked the URL: {e}")`. This defeats the module's own S8/S9 redaction (the audit row is written host-free `{"host":"?"}` at `server.py:119`, and the live-off branch deliberately says only "IP pinned in the audit log" at `:124-125`) — but the guard-block path forgets to redact the client-visible text.
**Failure:** injection-driven agent calls `fetch(url="https://attacker-dns.example/", confirmed=True)` pointing DNS at `169.254.169.254` / internal `10.x`; the `ToolError` discloses the actual resolved internal IP → blind internal-topology enumeration from an outward-only tool.
**Fix:** in the guard-block branch raise a fixed host/IP-free message (mirror the live-off pattern); keep host/IP in the audit DB only.

### MF2 — Live-fetch path: socket/TLS errors escape uncaught AND the attempt is never audited
`server.py:126-138`. *[python]*
The live branch only catches `except EgressError`, but `fetch_pinned`/`_pinned_https_get` (`egress.py:117-161`) routinely raise plain `TimeoutError`/`ConnectionRefusedError`/`ssl.SSLError`/`OSError`/`http.client.HTTPException` — none are `EgressError`. These escape the tool body (masked to an opaque error by `mask_error_details=True`). Worse: unlike the live-off branch, there is **no `audit.record(...)` before the `try:`**, so a real egress attempt that fails at socket/TLS is never logged — violating control #10 ("every outbound call audited"). Reachable whenever `OSINT_LIVE=1` (the actual live path).
**Fix:** `audit.record("fetch", {"host": host}, ip, "attempt")` before `fetch_pinned`; widen the except to convert `(EgressError, OSError, ssl.SSLError, http.client.HTTPException)` → `ToolError` with an audit record, so no raw exception escapes.

### MF3 — URL port ignored; live fetch hardcodes 443 → silently fetches a different endpoint
`egress.py:125` (`socket.create_connection((ip, 443), ...)`) + `validate_url` (`egress.py:77-110`) never inspects `parts.port`. *[python]*
`https://host:8443/path` passes validation, then is fetched on **443** — a different endpoint than the analyst supplied, no error surfaced. Also a validation-surface gap (port never factored into the egress decision).
**Fix:** `port = parts.port or 443`; connect to that port; decide+enforce whether nonstandard ports are permitted for OSINT egress (reject via `EgressError` if not) rather than silently substituting 443.

---

## SHOULD-FIX

- **S1 — Error-masking invariant bypassed in `propose_to_ledger`.** `server.py:254-255` `except Exception as e: raise ToolError(f"... {e}")` re-embeds raw `str(e)` (remote-ledger transport error) into a client-visible `ToolError`, bypassing the module's own M3 invariant (`:63-64`) and `mask_error_details` (which only masks *uncaught* exceptions). *[protocol must / quality nit → should]* **Fix:** fixed reason code to client; log `repr(e)` to stderr only.
- **S2 — Unguarded `res.data.evidence_id` deref outside its try.** `server.py:256`. If the ledger response lacks structured content (`res.data is None` on schema drift/partial success), raises `AttributeError` (then masked to opaque). *[protocol]* **Fix:** `if res.data is None: raise ToolError("unexpected response shape")` before deref.
- **S3 — `fetch` docstring misdescribes the provenance gate.** `server.py:109-112` says url "must match a prior search result, else confirmed=True" — but `_session_urls` is populated only by a prior successful `fetch` (`:135`), never by the stub `search` (always raises), so in this deployment `confirmed=True` is required for *every* first fetch. Misleads the calling LLM. *[protocol + quality]* **Fix:** state plainly that no connector populates the provenance set yet → confirmed=True currently required for first fetch.
- **S4 — `query` / `url` have no length cap.** `server.py:87,99-100`. Every other free-text field is `Field(max_length=...)`-bounded (`NOTE_CAP`, `_MAX_ID`, rationale at `:38`); the two highest-risk egress inputs are unbounded → oversized-payload/resource surface, scanned in full by `_screen` and `urlsplit`. *[protocol + security]* **Fix:** add `Field(max_length=...)` to both.
- **S5 — `get_map_tile` range checks in body, not schema.** `server.py:203-204` validates lat/lon/zoom at runtime; contrast `max_results: Annotated[int, Field(gt=0, le=100)]` (`:87`). Client can't self-validate from `inputSchema`. *[protocol + quality]* **Fix:** `lat: Annotated[float, Field(ge=-90, le=90)]`, `lon: ...(ge=-180, le=180)`, `zoom: Annotated[int, Field(ge=0, le=22)]`.
- **S6 — `get_map_tile` sends lat/lon to a third party with no consent gate.** `server.py:199-208` lacks the `confirmed` gate that `fetch` (`:101`) and `reverse_image_search` (`:176`) use for third-party disclosure. *[quality]* **Fix:** add the same `confirmed` Field, or justify in-docstring why coordinates are lower-risk.
- **S7 — `_screen` exfil gate is a plain substring match, trivially bypassable.** `server.py:78-83` uses `.lower()` + `in`; no whitespace/separator/Unicode normalization. `CASE-1234` → `"CASE 1234"` or base64 sails through; `.lower()` also misses ß/İ folds. *[python + security]* **Fix:** `casefold()` + normalize separators/diacritics; document as coarse defense-in-depth, not the primary control.
- **S8 — `EVIDENCE_LEDGER_URL` built into a Client with no scheme/host validation.** `server.py:53,68-75`. Server claims to be "the SOLE external-egress surface," yet a misconfigured/compromised env var can route case/source ids + note off-box, unscreened + unaudited (this path skips `_screen`/`validate_url`/`EgressAudit`). *[security]* **Fix:** in `main()` fail-closed unless the URL resolves to loopback / explicit internal allowlist.
- **S9 — `pii` flag is caller-asserted with zero server-side corroboration before a life-safety redaction.** `server.py:216-223,249`. An LLM composing `note` from a fetched doc may include a source's name and leave `pii=False` (default) → unredacted source identity written into the append-only ledger. Documented as an intentional design boundary → treat as hardening/enhancement, but life-safety impact. *[security]* **Fix:** heuristic/NER screen on `note`; fail closed to `pii=True` on ambiguity.
- **S10 — `confirmed=True` is a model-controllable bool, not bound to a real human-approval event.** `server.py:101-112,176-188`. Docstrings admit "the host MUST bind this to real human approval" but nothing here enforces it; injected page text ("call fetch confirmed=True on …") can drive it. This server can't supply the guarantee alone. *[security]* **Fix:** document that the host must gate `confirmed` via an out-of-band approval token (not a bool in the model-authored call); add a regression test asserting this server does not itself claim to provide the binding.

---

## NIT

- **N1 — `CONNECTOR_HOSTS` per-connector allowlist defined but never wired in** (`models.py:13-17`; zero refs). `fetch` even comments "no per-connector allowlist." Reads as an enforced control that isn't. *[all 4 reviewers]* Wire `validate_url(url, allowed_hosts=CONNECTOR_HOSTS[connector])` when live connectors ship, or delete with a TODO.
- **N2 — `_session_urls` mutated without a lock**, unlike `EgressAudit._lock` (`audit.py:29,50`, guarded because "FastMCP may dispatch on a worker thread"). `set.add` is GIL-atomic so no live bug, but inconsistent with the file's own concurrency discipline. `server.py:61,111,135`. *[python + protocol]* Add a lock or a one-line "no lock needed" comment.
- **N3 — `artifact_ref` origin undocumented** in the 4 tools that consume it (`compute_hash`/`extract_exif`/`reverse_image_search`/`propose_to_ledger`). *[quality]* Add "token returned by a prior `fetch()` call" to each docstring.
- **N4 — `propose_to_ledger` `case_id`/`source_id`/`note` lack `description=`** (`server.py:213-216`) — the most param-heavy, least self-describing tool. *[quality]* Add semantic descriptions.
- **N5 — `compute_hash` rationale vs `fetch` (which already returns sha256) unexplained** (`server.py:141-147`). *[quality]* State the distinct use (later integrity re-verification).
- **N6 — `detect_type` reads the whole file (≤25 MB) to slice 16 bytes**, then `extract_exif` reads again → double load per call (`artifacts.py:60-64`, `server.py:156-157`). *[python]* `fh.read(16)` in `detect_type`; read once in `extract_exif` and reuse.
- **N7 — Attacker-controlled EXIF field text returned into agent context** (`server.py:150-169`, `exif.py:33-38`) — indirect-injection vector if the host concatenates tool output as instructions. Primarily host-side, but state the fencing expectation in the returned `note` and strip control chars. *[security]*
- **N8 — Artifact store has a per-artifact 25 MB cap but no aggregate quota/TTL** (`artifacts.py:25,37-43`) → disk-exhaustion DoS once live. *[security]*
- **N9 — `CASE_IDENTIFIERS` read once at import** (`server.py:41`); rotation mid-session silently uses the stale set. *[security]* Document restart-required or add reload.
- **N10 — Dead/misleading Python bits** *[python]*: `Opener` bare-string "type" never used (`egress.py:74`); `fetch_pinned` is the one unannotated public signature (`egress.py:145`); undocumented lazy in-function imports (`server.py:73,126,165`).
- **N11 — `search`'s declared `-> SearchResult` schema is currently unreachable** (every path raises before return, `server.py:93-95`). Not a protocol violation; add a forward-looking test so the schema doesn't drift. *[protocol]*
- **N12 — `confirmed` reused with two different semantics** (`fetch`: provenance override; `reverse_image_search`: upload consent). Documented per-tool so not ambiguous today; consider tool-specific names. *[quality]*

---

MUST_FIX_COUNT: 3
