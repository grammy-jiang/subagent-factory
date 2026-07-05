---
name: mcp-protocol-compliance-checklist
kind: reference
status: ready
provenance:
  principles:
  - P088
  - P105
  - P114
  - P057
  - P085
  - P103
  - P193
  - P194
  - P195
  - P196
  - P172
  - P116
  - P135
  - P012
  - P200
  - P123
  - P124
  - P115
  - P125
  - P065
  - P097
  - P086
  - P091
  - P100
  - P134
  - P006
  - P007
  - P053
  - P056
  claims:
  - C01420
  - C01421
  - C01429
  - C01437
  - C01441
  - C01442
  - C01445
  - C01446
  - C00523
  - C00524
  - C00557
  - C00561
  - C00530
  - C00531
  - C00535
  - C00558
  - C00560
  - C01346
  evidence:
  - E00808
  - E00809
  - E00816
  - E00819
  - E00820
  - E00821
  - E00822
  - E00823
  - E00313
  - E00314
  - E00343
  - E00347
  - E00320
  - E00321
  - E00325
  source_anchors:
  - 74c00514b52f-c0000
  - 22497acd1d63-c0001
  - 22497acd1d63-c0002
  - 1974633645bd-c0000
  authored_from_digest: 9dd41bd670cabc02a22340908a24059b4613fcb57f37bf65109284050d97900c
---

# MCP Protocol Compliance & Security Review Checklist

A review checklist for MCP server/client protocol correctness, transport hygiene, error handling, and security. Work checks in validator dependency order; a missing prerequisite is a failure, never a SKIP [P105], [P153].

## Initialization & capabilities

- Initialize handshake completes and the negotiated protocol version matches before any request is handled [P088], [P114], [P167].
- Every capability the peer will use is declared at initialize; no capability-negotiation gaps [P103], [P193].
- Read-only connection facts (server_info, capabilities) are populated on entering the client session [P164].

## JSON-RPC & transport

- Only valid JSON-RPC 2.0 is emitted on the stdio channel; diagnostics go elsewhere, never on the message stream [P006], [P194].
- Transport is chosen explicitly with its endpoint and auth; absolute paths in config/.env/executable [P065], [P102].
- Request/response and session identifiers are preserved across exchange, tool calls, and resource access [P086].

## Errors & results

- Tool/server failures are structured JSON-RPC error objects mapped to the correct code [P057].
- A failing tool returns is_error=True with the message in content, not a protocol-layer throw [P085].
- CallToolResult is read as content / structured_content / is_error, consumed separately [P091].
- Emitted content conforms to the declared schema; out-of-band handling is brought inside declared contracts [P196], [P134].

## Behavioural fault detection

- Faults are detected behaviourally: a well-formed JSON-RPC response with wrong content is still a fault [P056], [P007].
- Runtime conformance is verified against a live session, not inferred from a clean build [P053].
- Checks share one slug across SUCCESS/FAILURE outcomes; reports are structured and timestamped per server [P152], [P123], [P124].

## Security & session review

- MCP tools are treated as untrusted; each threat vector is mapped to a defense [P012].
- mcp-scan security analysis is on by default; authentication (Authorization header, token validity) is checked [P135], [P116].
- Server-level configuration is actually enforced; session lifecycle is validated [P115], [P200].
- Review effort is prioritized by repository frequency plus practitioner-confirmed severity [P125].

## Grounding

Principles: P088, P105, P114, P057, P085, P103, P193, P194, P195, P196, P172, P116, P135, P012, P200, P123, P124, P115, P125, P065, P097, P086, P091, P100, P134, P006, P007, P053, P056. Sources are distillation-only; no verbatim source quotation.
