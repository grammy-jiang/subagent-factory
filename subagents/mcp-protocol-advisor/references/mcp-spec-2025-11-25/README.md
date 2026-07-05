# MCP spec 2025-11-25 — bundled reference index

Authoritative Model Context Protocol specification, version **2025-11-25**, fetched from
modelcontextprotocol.io. Bundled read-on-demand so the `mcp-advisor` can answer precise protocol
questions from the **original text** — Read the matching section below, then answer verbatim-grounded
with a citation. This is a point-in-time copy; check modelcontextprotocol.io for a newer spec version.

Rights: Apache-2.0 (spec/code) / CC-BY-4.0 (docs) — see `NOTICE.md`.

## "Read this section when you need…"

### Base protocol
| file | read it for |
|---|---|
| `mcp-spec-overview.md` | spec intro, JSON-RPC 2.0 basis, MUST/SHOULD (RFC 2119) conventions |
| `mcp-spec-architecture.md` | hosts / clients / servers roles, design principles, trust boundaries |
| `mcp-spec-basic-overview.md` | message types (request/response/notification), IDs, error objects, general rules |
| `mcp-spec-basic-lifecycle.md` | `initialize`/`initialized` handshake, **capability negotiation**, version, shutdown |
| `mcp-spec-basic-transports.md` | **stdio** + **Streamable HTTP** transports, framing, SSE, session management |
| `mcp-spec-basic-authorization.md` | **OAuth 2.1** auth, tokens, auth-server metadata, protected-resource metadata |
| `mcp-spec-basic-security-best-practices.md` | token passthrough, confused-deputy, session hijacking, threat mitigations |

### Server features (what a server exposes)
| file | read it for |
|---|---|
| `mcp-spec-server-overview.md` | server capability declaration |
| `mcp-spec-server-tools.md` | `tools/list`, `tools/call`, input/output schema, **annotations**, result content, tool errors |
| `mcp-spec-server-resources.md` | `resources/list`, `resources/read`, **templates**, subscriptions, resource content types |
| `mcp-spec-server-prompts.md` | `prompts/list`, `prompts/get`, prompt arguments, prompt message shape |
| `mcp-spec-server-util-completion.md` | argument autocompletion (`completion/complete`) |
| `mcp-spec-server-util-logging.md` | server log messages, log levels (`logging/setLevel`) |
| `mcp-spec-server-util-pagination.md` | cursor-based pagination for list operations |

### Client features (what a client offers back)
| file | read it for |
|---|---|
| `mcp-spec-client-sampling.md` | `sampling/createMessage`, model preferences, human-in-the-loop |
| `mcp-spec-client-roots.md` | exposing filesystem roots to servers |
| `mcp-spec-client-elicitation.md` | a server requesting **structured input from the user** mid-task |

### Cross-cutting utilities
| file | read it for |
|---|---|
| `mcp-spec-util-cancellation.md` | cancelling in-flight requests |
| `mcp-spec-util-ping.md` | liveness / keepalive |
| `mcp-spec-util-progress.md` | progress notifications for long operations |
| `mcp-spec-util-tasks.md` | long-running **task** management |

### Exact types
| file | read it for |
|---|---|
| `mcp-spec-schema.md` | the **full JSON-RPC type schema** — read for the exact field names, types, and message shapes (large; grep it for a specific type) |
