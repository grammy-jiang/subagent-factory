# evidence_ledger MCP server — r3 review

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/mcp_servers/evidence_ledger/` (`server.py`, `store.py`, `models.py`; imported `common.py`, `staleness.py`)
**Date:** 2026-07-11
**Reviewers:** mcp-protocol-advisor · mcp-security-advisor · mcp-quality-advisor · python-reviewer (parallel, review-only)

## Test gate

```
cd /home/grammy-jiang/projects/intelligence-analysis-agent && python -m pytest tests/ -q
→ 99 passed
```
0 test failures → no test-driven must-fix.

## Overall

Small, well-scoped 8-tool append-only ledger. Strong write-path discipline: hash-chained rows + fsync'd external manifest cross-check, fail-loud pydantic `Literal` validation, redaction-by-default, `mask_error_details=True`, stderr-only prints (stdio JSON-RPC stream clean), parameterized SQL throughout (only f-string SQL is table-name interpolation off an internal whitelist tuple, correctly `noqa`'d). No egress. No hardcoded secrets. The judgment-input-vs-computed boundary is *modeled* correctly (server computes `analyst_id`/`graded_at`/`superseded`/`row_hash`/`last_change_direction`; caller supplies `judgment_source`/`reliability`/`credibility`/`pii`) — but see MF-1: it is not *enforced* in code.

---

## MUST-FIX

### MF-1 — Judgment boundary enforced only in docstrings; untrusted caller can inject `analyst_confirmed`
`server.py:120,128-134,155-159` · `store.py:220-276` (`_insert_grade`/`grade_evidence`/`update_grade`)
`judgment_source` is a plain caller-supplied enum. `_insert_grade` never reads the evidence row's `source_channel` before accepting `analyst_confirmed`. Any caller (incl. prompt-injected/compromised agent) can `add_evidence(source_channel="ingested", ...)` then immediately `grade_evidence(..., judgment_source="analyst_confirmed")`, defeating the collect-then-grade gate ach-engine relies on. Exactly the "can an untrusted caller inject a graded verdict?" risk — yes, trivially.
*Fix:* enforce in `store.py`: when the evidence row's `source_channel == "ingested"`, reject `analyst_confirmed` on the first grade (force `model_draft`, then require a distinct out-of-band-confirmed `update_grade` to promote) — or gate `analyst_confirmed` behind a host-controlled flag/elicitation (analogous to `EVIDENCE_ALLOW_UNREDACT`) rather than trusting a same-call string arg.
*(security#1)*

### MF-2 — `EVIDENCE_ALLOW_UNREDACT` gate checks presence, not truthiness (life-safety)
`server.py:71` — `not redact_pii and not os.environ.get("EVIDENCE_ALLOW_UNREDACT")`
`os.environ.get` returns a string; `EVIDENCE_ALLOW_UNREDACT=false` / `=0` (reasonable operator intent to *disable*) is a non-empty → truthy string, so unredaction is granted anyway. File's own framing is "source identity is life-safety" — highest-impact correctness bug.
*Fix:* explicit allow-list, e.g. `os.environ.get("EVIDENCE_ALLOW_UNREDACT", "").strip().lower() in ("1","true","yes")`.
*(python#1 rated must-fix; security#2 rated should-fix — consolidated to must-fix on life-safety impact)*

---

## SHOULD-FIX

### SF-1 — Read-path IDs bypass the stated `_MAX_ID` size cap
`server.py:170,182,194` — `get_evidence(evidence_id)`, `list_evidence(case_id)`, `get_source_history(source_id)` take plain `str`, unlike write tools which apply `Annotated[str, Field(max_length=_MAX_ID)]`. Contradicts server's own S7 input-hardening rationale; unbounded string reaches SQLite before any cap. *Fix:* annotate the three read-tool id params with the same `_MAX_ID` cap.
*(all four reviewers: protocol#3, security#4, quality#3, python#2)*

### SF-2 — `expected_observables` values unbounded (only entry count capped)
`server.py:86,104-105` · `store.py:161-183` — `_MAX_OBSERVABLES=256` caps key count but no `_MAX_TEXT` on key/value length, unlike every other free-text field on the same tool. An `ingested` caller smuggles an unbounded payload into the append-only (no-delete) DB, bloating it and slowing `verify_chain` scans — breaks stated S7 anti-bloat intent. *Fix:* validate each key/value length (`≤ _MAX_ID` / `≤ _MAX_TEXT`) in `add_evidence`. (Protocol also notes the 256 cap isn't schema-visible — add `maxProperties`.)
*(security#3, quality#2, python-nit, protocol#7)*

### SF-3 — `add_evidence` return omits tamper-evident read-back (`row_hash`)
`models.py:18-24` (`EvidenceRef`), `server.py:78-111` — `EvidenceRef` returns only `evidence_id`/`case_id`/`pii`; grading tools return full `EvidenceRecord` incl. `row_hash` (`store.py:294-299`). Agent that added evidence can't verify what persisted without a second round-trip, and `get_evidence` only echoes (possibly redacted) content, never a write-scoped fingerprint. *Fix:* add `row_hash: str` to `EvidenceRef`, populate from the row's `rh` (`store.py:172,183`). Not content → doesn't reopen redaction concern.
*(protocol#1)*

### SF-4 — No per-parameter JSON Schema `description`
`server.py:80-86,116-121,143-149` (all tools) — FastMCP's `ParsedFunction.from_function` reads only the tool-level docstring, not the `- \`param\`:` bullets, into the schema; no `Annotated` field passes `description=`. Load-bearing prose ("IMMUTABLE once stored", "NEVER set analyst_confirmed unless...") is invisible to any client/LLM inspecting `inputSchema.properties`. *Fix:* add `Field(description=...)` per param, especially safety-critical `pii`/`judgment_source`.
*(protocol#2, quality-nit)*

### SF-5 — `verify_chain` / `verify_signals_chain` collide with 3 sibling servers
`server.py:207,215` — bare `verify_chain` reused verbatim in `ach_engine`, `osint_toolkit`, `calibration_tracker`. If the client flattens tools without server-scoped prefix, agent sees 4 identical names, can't disambiguate. *Fix:* rename `evidence_verify_chain` / `evidence_verify_signals_chain`, or confirm the deployment always namespaces by server.
*(quality#1)*

### SF-6 — `verify_chain` holds global write lock for unbounded full-table scan
`store.py:361-390` — unauthenticated tool any caller can invoke; holds `_write_lock` across the whole scan of both tables. As ledger grows, repeated/concurrent calls serialize behind long scans and stall `add_evidence`/`grade_evidence` — self-inflicted availability issue reachable from the tool surface. *Fix:* take a read-only snapshot outside the write lock, re-check heads under the lock only briefly; or rate-limit at host.
*(security#5)*

### SF-7 — Read paths use shared cross-thread connection without the lock the store's own comment demands
`store.py:278,301,323` vs `361` — `verify_chain` explicitly holds `_write_lock` because a read interleaved with an in-flight write can see a committed-but-not-yet-manifest-attested row, and `_conn` is shared (`check_same_thread=False`). But `get_evidence`/`list_evidence`/`get_source_history` read the same connection unguarded → the exact race the comment warns about applies. *Fix:* take `_write_lock` (or a read-lock) around these reads, or narrow the `check_same_thread=False` comment to state (and justify) that reads are exempt.
*(python#4)*

### SF-8 — `EvidenceStore.__init__` leaks flock/connection on failure path
`store.py:48-58` — `_acquire_process_lock` then unguarded `sqlite3.connect` + WAL check; if `connect()` raises or the WAL check `raise EvidenceError` fires, the acquired flock (`self._lock_fh`) and any open connection never release. A caller that catches and retries construction in-process sees a spurious "already open by another process". *Fix:* wrap the post-lock body in `try/except` → `self.close()` before re-raise.
*(python#3)*

### SF-9 — `staleness.py` bare `assert` for a check `store.py` deliberately stopped relying on
`staleness.py:55` — `assert table in _TABLES`. `store.py:99-101` replaced the equivalent assert with an explicit `raise ValueError` precisely because assert is stripped under `python -O` (comment N4). `staleness.py` reintroduces the same `-O`-stripped risk. *Fix:* mirror `store.py`'s explicit `if table not in _TABLES: raise ValueError(...)`.
*(python#5)*

### SF-10 — `list_evidence.limit` has no schema-level bound
`server.py:182` — `limit: int = 100`, no `ge`/`le`; `limit=-5` / `999999` pass validation and only fail deep in `store.py:306-307` as `EvidenceError` (wasted round-trip; under-documents the enforced `[1,1000]`). *Fix:* `Annotated[int, Field(ge=1, le=1000)]`.
*(protocol#4)*

### SF-11 — Required id/content fields have no `min_length`
`server.py:80-86,116,143` · `models.py` — `case_id`/`item`/`source_id`/`evidence_id` accept `""` at the schema layer. `item` is IMMUTABLE with no edit tool → an empty-string mis-entry can only be "corrected" by a new row, permanently retaining the empty one. *Fix:* add `min_length=1`.
*(protocol#5)*

---

## NIT

- **N1** `server.py:64/104` — same `expected_observables` value-length gap (subsumed by SF-2). *(python-nit, quality-nit)*
- **N2** `store.py:120-136,182,250-251,392-438` — manifest append not atomic with DB commit: crash between commit and manifest-append leaves a row unattested → next `verify_chain` fails-closed (false-positive tamper alarm after ordinary crash). Safe (fails closed); consider startup self-heal to distinguish crash-gap from real tamper. *(security#6)*
- **N3** `store.py:52-58` — `PRAGMA synchronous` left at WAL default (NORMAL); can lose last committed txn (not corrupt) on power loss. `synchronous=FULL` is stronger for a tamper-evidence ledger. *(security#7)*
- **N4** No `ToolAnnotations` (`readOnlyHint=True`) on the 5 read-only tools (`server.py:169-219`) — informational-only, improves host consent UX. *(protocol#6)*
- **N5** `server.py:142-149` `update_grade` — `reason` vs `rationale` are near-synonym free-text params, easy to transpose if client shows name+type only. Rename `supersede_reason`/`grade_rationale` or push disambiguation into `Field(description=...)`. *(quality-nit)*
- **N6** `server.py:130,156` — docstring says "Default to `model_draft`" but `judgment_source` is required with no schema default → "default" wording could mislead an agent into thinking it's optional. Reword. *(quality-nit)*
- **N7** `models.py:10` `Credibility = Literal["1".."6"]` — quoted-string digits; a model emitting int `3` fails non-coercing Literal validation. Document "pass quoted string" or add a coercing validator. *(quality-nit)*
- **N8** `server.py:141` — naming drift: `*_evidence` object noun everywhere except `update_grade`; consider `update_evidence_grade`. *(quality-nit)*
- **N9** `server.py:182`,`store.py:320` — `cursor` is a stringified internal `seq`; add "treat as opaque, echo `next_cursor` unmodified" to docstring. *(quality-nit)*
- **N10** `store.py:220-223,256-257,266-267` — `_insert_grade`/`grade_evidence`/`update_grade` params untyped while rest of file/`server.py` fully annotated. Add hints. *(python-nit)*
- **N11** `server.py:184-185` — `list_evidence` docstring thinner than siblings (omits default/bound/opaque-cursor note); align once SF-4 adds per-param descriptions. *(protocol#8)*

---

## Non-findings (checked clean)

SQL injection (all values parameterized; f-string SQL only interpolates whitelisted table names) · path traversal / unsafe deserialization (no caller-controlled paths; `json.loads` only reads back the server's own writes; no pickle/eval) · hash-chain correctness (prev-hash linkage verified DB-internal + fsync'd external manifest cross-check catches truncation/reset; single lock across head-read→insert→commit→manifest, no TOCTOU) · no-egress (no network imports; `show_banner=False` suppresses FastMCP version-check HTTP) · secrets (env-config only, no embedded creds; `mask_error_details=True`) · stdio hygiene (all `print()` → stderr) · error handling (`EvidenceError → ToolError`, never bare exception; `mask_error_details` unaffected by ToolError) · enum/type validation (all pydantic `Literal`) · judgment-input-vs-computed boundary *modeled* correctly (computed fields never writable) — but not enforced, see MF-1.

MUST_FIX_COUNT: 2
