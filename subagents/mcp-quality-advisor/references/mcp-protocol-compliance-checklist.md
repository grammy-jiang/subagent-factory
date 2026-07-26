---
name: mcp-protocol-compliance-checklist
kind: reference
status: ready
provenance:
  principles:
  - P016
  - P018
  - P073
  - P077
  - P093
  - P094
  - P096
  - P098
  - P104
  - P105
  - P114
  - P116
  - P127
  - P128
  - P129
  - P134
  - P164
  - P166
  - P179
  - P184
  authored_from_digest: 2cef0963d3f61638bd3e316e4f5aa0f523b94c6e8af318a5a135411489983a16
---

# Reference: MCP protocol-compliance checklist

A runtime-level conformance checklist. A server can compile and match its spec yet still violate
coordination, so verify behaviourally. Validate the whole surface and never let an un-run check count
as passing [P096], [P164].

## Handshake and capabilities

- Complete the initialize handshake before processing any request; gate request handling on it [P127].
- Declare every capability you will use at initialize; advertise tools/prompts/resources accurately [P114].
- `protocol` is the foundation validator; respect validator dependency order [P116].

## Transport and message stream

- On stdio, emit only valid JSON-RPC 2.0 on the message stream; route logs off the protocol channel [P016].
- Select the client transport by its argument type (in-process / Streamable HTTP / stdio) [P105].
- For HTTP, supply endpoint and OAuth; with offline_access, include refresh_token in grant_types [P077], [P104].
- Validate request headers: reject a request whose Mcp-Method/Mcp-Name header disagrees with the body [P166].

## Errors, results, and identifiers

- Represent failures as structured JSON-RPC error objects mapped to the correct code; never a success
  carrying an error [P073].
- Treat a failing tool as an ordinary result with `is_error=True` (message in `content`); check it [P093].
- Read a `CallToolResult` as separate fields — `content`, `structured_content`, `is_error` [P098].
- Preserve request/response and session identifiers consistently across the exchange [P094].

## Listing, review, and reporting

- Page every list call with a cursor loop until no next cursor [P018].
- On review, check that server-level configuration is actually enforced, not silently ignored [P128].
- Check authentication: Authorization header present, token well-formed, unexpired, correct audience [P129].
- Rely on automatic protocol-version negotiation (client sends LATEST, server returns highest mutual) [P179].
- Check tool identification: tools declared in capabilities with valid input/output schemas [P184].
- Emit a structured, timestamped aggregated report per server plus an aggregate [P134].

## Principles applied

- **[P016]** Keep diagnostic and other non-protocol output off the JSON-RPC message stream; on the stdio transport, emitting anything other than valid JSON-RPC on standard output corrupts the stream and breaks client parsing.
- **[P018]** Page every MCP list call with a cursor loop, collecting results until the response has no next cursor rather than assuming the first page is complete.
- **[P073]** Represent tool and server failures as structured JSON-RPC error objects mapped to the correct error code; never return a success response that carries hidden failure information, and never surface application failures as bare HTTP status codes.
- **[P077]** Choose the transport explicitly and supply its required endpoint and authentication: stdio is the default; HTTP needs --endpoint plus OAuth 2.0 (automatic Dynamic Client Registration, pre-registered credentials, or a personal access token); SSE needs --endpoint plus a Bearer token.
- **[P093]** Treat a failing tool as an ordinary result with `is_error=True` (the exception message is placed in `content` for the model), always check `is_error` before trusting `structured_content` (which is `None` on failure), and remember a Client method raises `MCPError` only when the server returns a JSON-RPC error rather than a result.
- **[P094]** Preserve request-response and session identifiers consistently across message exchange, tool invocation, and result propagation, so requests, results, and related streaming events stay correlated.
- **[P096]** Validate the full MCP compliance surface — the initialize handshake, JSON-RPC 2.0 conformance, advertised capabilities (tools/prompts/resources), security, and registry/OSS conformance — rather than checking connectivity alone.
- **[P098]** Read a `CallToolResult` as three separately-consumed fields — `content` for the model, `structured_content` (JSON matching the tool's output_schema) for application code, and `is_error` for success — and do not conflate the model-facing and code-facing halves.
- **[P104]** OAuth client scopes and registration: with offline_access in the AS scopes_supported a client SHOULD include refresh_token in grant_types (and MAY include offline_access in the request scope); when the server lacks DCR it MUST use pre-registered credentials via context; it should follow the WWW-Authenticate scope from the 401; and it validates the iss parameter when the server advertises it.
- **[P105]** Select the Client transport by the type of its single positional argument: an MCPServer/Server instance for in-process, a URL string for Streamable HTTP, or a transport object (usable as `async with ... as (read, write)`) for anything else.
- **[P114]** Declare every capability you will use at initialize (client capabilities in the Client constructor; server capabilities inferred by McpServer from registered handlers, or declared on the low-level Server) — the SDK throws when code uses an undeclared capability.
- **[P116]** Treat `protocol` as the mandatory foundation validator and respect validator dependency order (capabilities, ping, errors, security all depend on it); extend validation through the plugin model instead of ad-hoc checks.
- **[P127]** Gate request handling on completion of the initialization handshake so no request is processed before the session is fully initialized; because initialization instability spans several startup steps, expect to harden the whole startup sequence rather than a single step.
- **[P128]** When reviewing MCP state and configuration, check that server-level configuration parameters are actually enforced rather than accepted and silently ignored, that session identifiers are neither stale, reused, absent, nor stripped by middleware, and that server-managed resource state is persisted and kept fresh across operations.
- **[P129]** When reviewing MCP security, check authentication (Authorization header present, token well-formed and unexpired), token validation (token audience and other claims verified on receipt, tokens not forwarded upstream unverified), and authorization (access-control checks enforced after authentication before executing capabilities or tool invocations).
- **[P134]** Emit a structured, timestamped aggregated report: one JSON report per server (named <server>.json under output/), an aggregate servers_validation.json, and a Markdown summary table of per-server status/errors/warnings — recording Name, Command, Status, counts, and report file, and adding an Error_Message on failures.
- **[P164]** Never report a missing prerequisite as SKIPPED: because SKIPPED counts as green in pass counts, exit codes, and baselines, a check that cannot be exercised (missing fixture, rejected probe, undeclared feature) must FAIL via notTestable()/untestableCheck() naming the missing prerequisite; reserve SKIPPED for genuinely inapplicable checks.
- **[P166]** MCP request-header validation (server, SEP-2243): reject a request whose Mcp-Method or Mcp-Name header disagrees with the body (or is missing for a name-carrying body) with HTTP 400 and JSON-RPC -32020 (HeaderMismatch); treat header names case-insensitively but values case-sensitively, accept optional whitespace around Mcp-Name per RFC 9110 section 5.5, and reject a request where a custom header is omitted while its value is present in the body.
- **[P179]** Rely on the SDK's automatic protocol-version negotiation (client sends LATEST_PROTOCOL_VERSION, server returns the highest mutually supported version from SUPPORTED_PROTOCOL_VERSIONS) but handle the error the client throws when the server's version is unsupported.
- **[P184]** When reviewing MCP tool handling, check tool identification (tools declared in the capabilities object with valid input/output schemas so they are discoverable and callable), tool execution (input types validated, execution terminates, runtime errors surfaced as error objects), and tool result propagation (result payload present, correctly structured, no success response masking a tool failure, no result-visibility races).

Sources are distillation-only: this reference paraphrases and restructures; no verbatim quotation.

