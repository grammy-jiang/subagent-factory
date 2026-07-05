---
name: verifying-mcp-protocol-compliance
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P006
  - P007
  - P012
  - P015
  - P041
  - P053
  - P056
  - P057
  - P063
  - P064
  - P065
  - P085
  - P086
  - P088
  - P091
  - P097
  - P098
  - P099
  - P101
  - P102
  - P103
  - P104
  - P105
  - P114
  - P115
  - P116
  - P117
  - P123
  - P124
  - P125
  - P135
  - P149
  - P150
  - P151
  - P152
  - P153
  - P154
  - P155
  - P156
  - P157
  - P158
  - P159
  - P160
  - P161
  - P162
  - P163
  - P164
  - P165
  - P166
  - P167
  - P168
  - P172
  - P185
  - P192
  - P193
  - P194
  - P195
  - P196
  claims:
  - C00031
  - C00530
  - C00536
  - C00539
  - C00559
  - C00521
  - C00563
  - C01284
  - C01285
  - C01360
  - C01361
  - C01379
  - C01380
  - C00581
  - C00596
  - C00597
  - C00598
  - C00599
  evidence:
  - E00001
  - E00320
  - E00326
  - E00327
  - E00345
  - E00311
  - E00349
  - E00745
  - E00746
  - E00782
  - E00783
  - E00792
  - E00793
  - E00364
  - E00377
  source_anchors:
  - 46bbfd26b8df-c0001
  - 22497acd1d63-c0001
  - 22497acd1d63-c0002
  - 9a2be171fb4e-c0000
  - 1974633645bd-c0000
  - c3e4e099b722-c0000
  authored_from_digest: 4f805a8e408d4f235e5d4abbbc1474ff214f3ca15326736e34456fee8c3f31da
---

# Skill: verifying-mcp-protocol-compliance

## Purpose

Verify that an MCP server is protocol-compliant, secure, and debuggable at the runtime level, not only that it builds. Cover the initialize handshake, JSON-RPC 2.0 conformance, transport binding, capability negotiation, structured errors, and the SDK-test / Inspector / validator tooling that exercises them [P088], [P053], [P105].

## When to use

- You are reviewing, testing, or debugging an MCP server or client for protocol correctness.
- A connection fails, a capability misbehaves, or a fault returns well-formed but wrong output.
- You are building conformance tests or wiring SDK in-memory tests for a server.

## Procedure

1. **Validate the full compliance surface in dependency order.** Check the initialize handshake, JSON-RPC 2.0 conformance, advertised capabilities, and each declared primitive; treat protocol as the mandatory foundation validator and respect validator dependency order (capabilities, primitives) [P088], [P105]. Gate request handling on completion of the initialization handshake so nothing is processed before the session is ready [P114], [P103].
2. **Verify at runtime, not only at build time.** A server can compile and still be non-conformant at the protocol runtime level — verify behaviour against a live session [P053]. Detect faults behaviourally: many return a well-formed JSON-RPC response with wrong content rather than crashing or erroring [P056], [P007].
3. **Represent failures as structured JSON-RPC errors.** Map tool and server failures to the correct JSON-RPC error code as structured error objects; for a failing tool, return it as an ordinary result with is_error=True and the message in content rather than throwing at the protocol layer [P057], [P085]. Read a CallToolResult as three separately-consumed fields — content, structured_content, is_error [P091].
4. **Keep the transport channel clean and explicit.** On stdio, emit only valid JSON-RPC on stdout — never diagnostic output on the message stream, which corrupts the transport; route logs elsewhere [P006], [P194]. Choose the transport explicitly and supply its endpoint and auth (stdio default; HTTP needs its endpoint) and use absolute paths in config/.env/executable [P065], [P102].
5. **Preserve identifiers and negotiate the version.** Preserve request-response and session identifiers consistently across message exchange, tool invocation, and resource access [P086]. Rely on the SDK's automatic protocol-version negotiation (client sends LATEST, server returns its supported version) and declare every capability you will use at initialize [P167], [P103].
6. **Drive SDK clients and in-memory tests correctly.** Drive an MCP Client through `async with Client(...)`, which connects, negotiates, and reads the read-only connection facts (server_info, capabilities) on entry [P160], [P164]. Use InMemoryTransport / a linked pair only for in-process unit and integration testing, establishing the connection by running client and server connect concurrently, with an anyio asyncio backend fixture [P104], [P168], [P163].
7. **Reach for the Inspector first when debugging.** Use the MCP Inspector as the transport-agnostic way to invoke a server's tools, resources, and prompts; launch it via npx matched to how the server is distributed, exercise each capability tab, and mind its Bearer-token auth and timeout settings [P157], [P154], [P155], [P158], [P159]. Work a connection failure as an ordered checklist [P162].
8. **Never let a missing prerequisite read as green.** Give a check one slug shared by its SUCCESS and FAILURE outcomes, and never report a missing prerequisite as SKIPPED — SKIPPED counts as green in pass counts and exit codes and hides a real gap [P152], [P153]. Emit a structured, timestamped report per server and configure validation reproducibly via named profiles or a config file [P123], [P125].
9. **Review security and session state.** Treat MCP tools as untrusted and map each threat vector to its defense; keep mcp-scan security analysis enabled by default and check authentication, session lifecycle, and that server-level config is actually enforced [P012], [P135], [P116], [P115], [P193]. Prioritise review effort by repository frequency plus practitioner-confirmed severity [P015].

## Pitfalls / anti-patterns

- Trusting a clean build as evidence of conformance — compile success is not runtime compliance [P053].
- Reporting a missing prerequisite as SKIPPED, which silently counts as a pass [P153].
- Writing logs to stdout on the stdio transport, corrupting the JSON-RPC stream [P006].

## Grounding

Principles: P005, P006, P007, P012, P015, P041, P053, P056, P057, P063, P064, P065, P085, P086, P088, P091, P097, P098, P099, P101, P102, P103, P104, P105, P114, P115, P116, P117, P123, P124, P125, P135, P149, P150, P151, P152, P153, P154, P155, P156, P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168, P172, P185, P192, P193, P194, P195, P196. Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.
