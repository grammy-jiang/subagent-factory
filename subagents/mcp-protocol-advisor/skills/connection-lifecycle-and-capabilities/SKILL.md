---
name: connection-lifecycle-and-capabilities
kind: skill
status: ready
provenance:
  principles:
  - P009
  - P011
  - P017
  - P031
  - P067
  - P070
  - P102
  - P124
  - P125
  - P126
  - P197
  claims:
  - C00135
  - C00136
  - C00121
  - C00122
  - C00114
  - C00115
  - C00128
  - C00132
  - C00111
  - C00112
  - C00142
  - C00143
  - C00129
  - C00130
  - C00119
  - C00120
  - C00147
  - C00148
  - C00145
  - C00146
  - C00127
  evidence:
  - E00134
  - E00135
  - E00120
  - E00121
  - E00113
  - E00114
  - E00127
  - E00131
  - E00110
  - E00111
  - E00141
  - E00142
  - E00128
  - E00129
  - E00118
  - E00119
  - E00146
  - E00147
  - E00144
  - E00145
  - E00126
  source_anchors:
  - 884720004be3-c0000
  authored_from_digest: c8ab60c92326be3e38fadf378813e039c613babe73cc937ecaefba450e6c75e1
---

# Connection Lifecycle And Capabilities

Drive the three-phase lifecycle and negotiate capabilities before any feature is used. This skill
packages 11 grounded principles the mcp-protocol-advisor applies when this layer of the Model
Context Protocol is in scope. Each finding names the rule, the protocol revision it belongs to, the
failure or interoperability break it prevents, the conforming behaviour, and the trade-off or
residual risk.

## When this applies

- Terminating an MCP connection.
- A client and server may support different protocol versions.
- Implementing or reviewing MCP connection setup.
- Exchanging messages during the operation phase.
- Establishing or reviewing an MCP client-server connection.
- Sending any MCP request that expects a response.
- Building or validating the capability object exchanged at initialization.
- A request is about to be sent before the handshake completes.
- Implementing error handling for MCP connection setup.
- A long-running request emits progress notifications.
- The transport is HTTP.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P009 (high confidence).** Shut down through the transport rather than protocol messages: MCP defines no shutdown message. For stdio, the client closes the server's input stream, then escalates to SIGTERM and finally SIGKILL if the server does not exit in a reasonable time (the server may instead close its output and exit); for HTTP, close the…
2. **P011 (high confidence).** Negotiate the protocol version explicitly: the client proposes the latest version it supports, the server echoes that version if supported or otherwise offers the latest version it supports, and the client disconnects if it cannot support the server's chosen version.
3. **P017 (high confidence).** Drive initialization as a client-initiated handshake: client sends an initialize request carrying its protocol version, capabilities, and implementation info; the server replies with its own capabilities and info; then the client sends an initialized notification before normal operation.
4. **P031 (high confidence).** Confine operation-phase behaviour to the negotiated envelope: use only the protocol version and the capabilities that were successfully negotiated, and never invoke a feature the peer did not advertise.
5. **P067 (high confidence).** Treat the MCP connection as a strict three-phase lifecycle (initialization, then operation, then shutdown) and make initialization the very first interaction before any other traffic.
6. **P070 (high confidence).** Set a timeout on every sent request (configurable per request) and, when it elapses without a success or error response, issue a cancellation notification and stop waiting, to prevent hung connections and resource exhaustion.
7. **P124 (high confidence).** Restrict traffic during the handshake window: the client sends nothing but pings until the initialize response arrives, and the server sends nothing but pings and logging until the initialized notification arrives.
8. **P125 (high confidence).** Handle the expected lifecycle failure modes explicitly: protocol-version mismatch, failure to negotiate required capabilities, and request timeouts; report an unsupported protocol version with JSON-RPC error code -32602 and data listing supported and requested versions.
9. **P126 (high confidence).** You may reset a request's timeout clock on receiving a progress notification for it, but always enforce a hard maximum timeout regardless of progress, to bound the impact of a misbehaving peer.
10. **P197 (high confidence).** On HTTP transports, send the negotiated version in an MCP-Protocol-Version header on every request after initialization.
11. **P102 (medium confidence).** Advertise and interpret capabilities against the defined catalog (client: roots, sampling, elicitation, tasks, experimental; server: prompts, resources, tools, logging, completions, tasks, experimental) and honour sub-capabilities such as listChanged (prompts/resources/tools) and subscribe (resources only).

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P009, P011, P017, P031, P067, P070, P102, P124, P125, P126, P197. Every cited claim,
evidence record, and source anchor resolves in this package's distilled spine
(`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context
Protocol specification is distillation-only here: paraphrased, never quoted.

