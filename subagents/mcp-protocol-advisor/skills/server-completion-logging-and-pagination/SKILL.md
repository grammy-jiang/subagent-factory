---
name: server-completion-logging-and-pagination
kind: skill
status: ready
provenance:
  principles:
  - P022
  - P049
  - P050
  - P081
  - P095
  - P099
  - P100
  - P107
  - P108
  - P109
  - P110
  - P147
  - P148
  - P177
  - P178
  - P179
  - P180
  - P181
  - P188
  - P229
  - P232
  - P233
  - P248
  - P251
  - P252
  claims:
  - C00573
  - C00574
  - C00544
  - C00545
  - C00560
  - C00565
  - C00587
  - C00588
  - C00540
  - C00541
  - C00594
  - C00595
  - C00590
  - C00591
  - C00550
  - C00551
  - C00559
  - C00562
  - C00570
  - C00577
  - C00561
  - C00571
  - C00583
  - C00584
  - C00593
  - C00538
  - C00539
  - C00556
  - C00557
  - C00549
  - C00555
  - C00564
  - C00585
  - C00586
  - C00568
  - C00569
  - C00554
  - C00558
  - C00563
  - C00553
  - C00542
  - C00548
  evidence:
  - E00564
  - E00565
  - E00535
  - E00536
  - E00551
  - E00556
  - E00577
  - E00578
  - E00531
  - E00532
  - E00584
  - E00585
  - E00580
  - E00581
  - E00541
  - E00542
  - E00550
  - E00553
  - E00561
  - E00568
  - E00552
  - E00562
  - E00573
  - E00574
  - E00583
  - E00529
  - E00530
  - E00547
  - E00548
  - E00540
  - E00546
  - E00555
  - E00575
  - E00576
  - E00559
  - E00560
  - E00545
  - E00549
  - E00554
  - E00544
  - E00533
  - E00539
  source_anchors:
  - b287e6ef9e11-c0000
  - 88cd5f33cd8f-c0000
  - e59fbe4c002a-c0000
  authored_from_digest: 296c5062d24f1e2e946194766a571ac37d449af0862c0f178dc0aa16411605bb
---

# Server Completion Logging And Pagination

Run completion, logging, and pagination to spec, leaking no secrets. This skill packages 25 grounded
principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol is in
scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- Composing the data payload of any log message.
- Implementing or reviewing a server's completion response.
- A client has configured a minimum log level.
- A client iterates through a paginated MCP result set.
- Designing or reviewing the completion request path of an MCP client or server.
- A client stores or forwards a pagination cursor.
- Implementing the server side of a paginated MCP operation.
- Validating an incoming cursor.
- Building an interactive client that issues completion requests as the user types.
- Designing how a client surfaces logs to users.
- Operating a server or client that produces or stores logs.
- Structuring the content of a log notification.
- Choosing a pagination scheme for an MCP operation.
- Building a client that lists resources, templates, prompts, or tools.
- Reviewing or building an MCP server that provides completion suggestions.
- Completion suggestions could reveal access-controlled or sensitive data.
- Operating a server that exposes the completion endpoint.
- Assigning or interpreting log severities in MCP.
- A client consumes a paginated MCP list response.
- Sizing buffers or loops around page results.
- A logging/setLevel request is invalid or configuration fails.
- Handling any incoming completion request.
- Choosing how to surface completion suggestions in a client.
- Building an MCP server that sends log notifications.
- A completion request cannot be fulfilled.
- The completion target exposes more than one argument.
- Fuzzy matching suits the argument domain being completed.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P022 (high confidence).** Never emit credentials, secrets, PII, or exploitable internal details in logs; strip and monitor for sensitive content before sending.
2. **P049 (high confidence).** Return completion results as a `completion` object whose `values` are relevance-ranked and capped at 100 items per response, and expose the optional `total` count and a `hasMore` boolean when further matches exist beyond those returned.
3. **P050 (high confidence).** Honour the client-configured minimum log level: expose `logging/setLevel`, and once a level is set send only messages at that level and above via `notifications/message`.
4. **P081 (high confidence).** Drive the pagination loop by echoing the previously returned cursor in the follow-up request's params.cursor, and stop when a response omits nextCursor (treat a missing nextCursor as end-of-results).
5. **P095 (high confidence).** Model completion requests as `completion/complete`, identifying the target with a reference that is either `ref/prompt` (prompt by name) or `ref/resource` (resource by URI template), and naming the argument being completed by its `name` and current `value`.
6. **P099 (high confidence).** Treat cursors as fully opaque tokens: do not parse, modify, or make assumptions about their format, and do not persist them across sessions.
7. **P100 (high confidence).** Servers should provide stable cursors, handle invalid cursors gracefully, and return JSON-RPC error code -32602 (Invalid params) when a supplied cursor is invalid.
8. **P147 (high confidence).** Use opaque cursor-based pagination (a server-issued position token), never numbered/offset pages, so the pagination scheme stays server-controlled.
9. **P148 (high confidence).** Clients should support both paginated and non-paginated flows so they interoperate with servers regardless of whether a given response returns a nextCursor.
10. **P177 (high confidence).** An MCP server that offers argument autocompletion MUST advertise the `completions` capability (an empty object) in its capabilities; a server that returns completion suggestions without declaring this capability is non-conformant.
11. **P178 (high confidence).** Control access to sensitive completion suggestions and prevent completion-based information disclosure, so that probing the completion endpoint cannot enumerate or infer restricted values.
12. **P179 (high confidence).** Rate-limit completion handling on the server: appropriate rate limiting is a security requirement, not merely an optimization.
13. **P180 (high confidence).** Use the eight RFC 5424 syslog severity levels (debug→emergency) as the log severity vocabulary, and attach a severity to every notification.
14. **P181 (high confidence).** Let the server determine page size; clients must not assume a fixed page size or hardcode one.
15. **P229 (high confidence).** Validate all completion inputs before processing them.
16. **P232 (high confidence).** Do not assume or hard-require a specific completion user-interaction model; the protocol mandates none, so present suggestions through whatever interface fits the application (e.g. an IDE-style dropdown).
17. **P233 (high confidence).** Declare the `logging` capability before a server emits any log-message notifications.
18. **P107 (medium confidence).** On the client side, debounce rapid successive completion requests, cache results where appropriate, and degrade gracefully when results are missing or partial.
19. **P108 (medium confidence).** Treat the logging presentation layer as implementation-defined: the protocol mandates no UI model, and clients may present, filter, search, visually distinguish, and persist log messages as they choose.
20. **P109 (medium confidence).** Harden log output operationally: rate-limit messages, validate all data fields, and control access to logs.
21. **P110 (medium confidence).** Make log data actionable and correlatable: include relevant context in the data field and use consistent logger names.
22. **P188 (medium confidence).** Return standard JSON-RPC errors for logging failures — `-32602` for an invalid log level and `-32603` for configuration errors.
23. **P248 (medium confidence).** Signal completion failures with the standard JSON-RPC error codes: -32601 when the completions capability is unsupported, -32602 for an invalid prompt name or missing required arguments, and -32603 for internal errors.
24. **P251 (medium confidence).** When completing an argument on a prompt or template that has multiple arguments, include the already-resolved argument values in `context.arguments` so the server can return context-dependent suggestions.
25. **P252 (medium confidence).** Apply fuzzy matching to completion suggestions where appropriate rather than requiring exact prefix matches.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P022, P049, P050, P081, P095, P099, P100, P107, P108, P109, P110, P147, P148, P177,
P178, P179, P180, P181, P188, P229, P232, P233, P248, P251, P252. Every cited claim, evidence
record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`,
`evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context Protocol specification is
distillation-only here: paraphrased, never quoted.

