<!--
source_urls:
  - https://github.com/modelcontextprotocol/typescript-sdk  (git clone --depth 1; commit ddba550fa91cd5226d994ddf63f1147fb707131d, 2026-07-02)
  - packages/core-internal/src/util/inMemory.ts
  - test/integration/test/server/mcp.test.ts
  - test/integration/test/client/client.test.ts
  - README.md  (Getting Started / Packages)
title: "MCP TypeScript SDK — In-Memory Unit-Testing Recipe (InMemoryTransport.createLinkedPair)"
fetched: 2026-07-05
source_type: git-repository (official TypeScript SDK source + README, extracted via git clone --depth 1)
rights_status: open (Apache-2.0; the MCP project is transitioning MIT -> Apache-2.0 — new code is Apache-2.0, non-specification docs are CC-BY-4.0; legacy code was MIT)
dimension: testing
-->

# MCP TypeScript SDK — In-Memory Unit-Testing Recipe

A runnable, faithful pattern for unit-testing an MCP server against a real MCP `Client`
in the **same process, with no sockets, no subprocess, and no HTTP** — by linking a
`Client` and an `McpServer` over a pair of `InMemoryTransport`s.

## Scope, provenance, and a caveat

This document is extracted from the official `modelcontextprotocol/typescript-sdk`
monorepo at commit `ddba550` (2026-07-02). The SDK now publishes **split packages**
(`@modelcontextprotocol/server`, `@modelcontextprotocol/client`); the in-memory transport
lives in the internal core package and is imported as
`import { InMemoryTransport } from '@modelcontextprotocol/core-internal';` (this is the
exact import the SDK's own test suite uses). In the legacy 1.x single-package SDK the same
class was imported from `@modelcontextprotocol/sdk/inMemory.js`.

**Caveat (substitution note):** the SDK's `README.md` has **no dedicated "testing" or
"in-memory" prose section** — the README covers packages, a minimal stdio "Getting Started"
server, and links to tutorials/examples. The authoritative in-memory *testing* pattern is
therefore drawn from (a) the `InMemoryTransport` source doc-comments and (b) the SDK's own
integration test suite (`test/integration/test/server/mcp.test.ts`,
`test/integration/test/client/client.test.ts`), where `InMemoryTransport.createLinkedPair()`
is used in **~100+ tests**. Every code element below is a verified API call from that repo.

---

## 1. The `InMemoryTransport` API

`packages/core-internal/src/util/inMemory.ts` — doc-comments and signatures (internal
message-queue mechanics elided). This is the entire public surface a test author touches:

```typescript
/**
 * In-memory transport for creating clients and servers that talk to each other
 * within the same process.
 *
 * Intended for testing and development. For production in-process connections, use
 * `StreamableHTTPClientTransport` against a local server URL.
 */
export class InMemoryTransport implements Transport {
    onclose?: () => void;
    onerror?: (error: Error) => void;
    onmessage?: (message: JSONRPCMessage, extra?: { authInfo?: AuthInfo }) => void;
    sessionId?: string;

    /**
     * Creates a pair of linked in-memory transports that can communicate with each
     * other. One should be passed to a Client and one to a Server.
     */
    static createLinkedPair(): [InMemoryTransport, InMemoryTransport];

    async start(): Promise<void>;          // drains any messages queued before start()
    async close(): Promise<void>;          // closes this transport AND its linked peer

    /**
     * Sends a message with optional auth info.
     * This is useful for testing authentication scenarios.
     */
    async send(
        message: JSONRPCMessage,
        options?: { relatedRequestId?: RequestId; authInfo?: AuthInfo },
    ): Promise<void>;
}
```

**Key behaviours that make it test-friendly:**

- `createLinkedPair()` returns a 2-tuple `[clientTransport, serverTransport]`; each
  transport holds a private reference to its peer, so a `send()` on one is delivered
  straight to the other's `onmessage` — no serialization boundary, no network.
- Messages sent **before** the peer has attached an `onmessage` handler are queued and
  flushed on `start()`, so ordering of `connect()` calls is not fragile.
- `close()` on either side tears down **both** ends and fires `onclose`.
- The optional `authInfo` on `send()` exists specifically so tests can exercise
  authenticated / `authInfo`-dependent server handlers in-process.

---

## 2. The canonical wiring pattern

Two lines, verbatim from the SDK test suite, are the whole recipe:

```typescript
const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();

await Promise.all([
    client.connect(clientTransport),
    mcpServer.connect(serverTransport),
]);
```

- `Client.connect(transport)` / `McpServer.connect(transport)` each call
  `transport.start()` and then run the MCP **initialize** handshake (protocol-version
  negotiation + capability exchange). Running both inside `Promise.all` lets the handshake
  complete: the client's `initialize` request is delivered to the server and the response
  comes back, all in-process.
- `McpServer.connect(transport)` is a thin delegate: internally it calls
  `this.server.connect(transport)`. So `mcpServer.connect(serverTransport)` and
  `mcpServer.server.connect(serverTransport)` are equivalent — both appear in the SDK's
  tests. If you build with the **low-level** `Server` class instead of the high-level
  `McpServer`, call `server.connect(serverTransport)` directly.

---

## 3. Walkthrough: linked pair -> connect both -> list / call / read

The following composes the SDK's own test blocks into one coherent example. Every call
(`new McpServer`, `registerTool`, `registerResource`, `createLinkedPair`, `client.connect`,
`client.listTools`, `client.callTool`, `client.readResource`) is a verified API from the
repo.

### 3a. Build a server with a tool and a resource; build a client

```typescript
import { Client } from '@modelcontextprotocol/client';
import { McpServer } from '@modelcontextprotocol/server';
import { InMemoryTransport } from '@modelcontextprotocol/core-internal';
import * as z from 'zod/v4';

// --- Server under test: one tool, one resource ---
const mcpServer = new McpServer({ name: 'test server', version: '1.0' });

mcpServer.registerTool(
    'greet',
    { description: 'Greet someone by name', inputSchema: z.object({ name: z.string() }) },
    async ({ name }) => ({
        content: [{ type: 'text', text: `Hello, ${name}!` }],
    }),
);

mcpServer.registerResource(
    'test',                    // human-readable name
    'test://resource',         // static URI
    {},                        // metadata
    async () => ({
        contents: [{ uri: 'test://resource', text: 'Test content' }],
    }),
);

// --- Client that will drive it ---
const client = new Client({ name: 'test client', version: '1.0' });
```

### 3b. Link the two ends in memory and connect both

```typescript
const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();

await Promise.all([
    client.connect(clientTransport),
    mcpServer.connect(serverTransport),
]);
// After this line the initialize handshake is complete and the client
// knows the server's capabilities.
```

### 3c. Assert list -> call -> read against the live in-process server

```typescript
// LIST tools (this also caches the tool's I/O schemas on the client)
const tools = await client.listTools();
// -> tools.tools contains the 'greet' tool

// CALL the tool and assert the returned content
const callResult = await client.callTool({ name: 'greet', arguments: { name: 'Ada' } });
// -> callResult.content === [{ type: 'text', text: 'Hello, Ada!' }]

// LIST resources
const resources = await client.listResources();
// -> resources.resources[0].name === 'test', .uri === 'test://resource'

// READ a resource by URI
const read = await client.readResource({ uri: 'test://resource' });
// -> read.contents === [{ uri: 'test://resource', text: 'Test content' }]
```

The relevant client methods (all `async`, all verified in
`packages/client/src/client/client.ts`) are:
`listTools()`, `callTool(params)`, `listResources()`, `readResource(params)`,
`listPrompts()`, `getPrompt(params)`. Lower-level, you can also send any request directly
with `client.request({ method: 'tools/call', params: { name: 'greet' } })` — the SDK tests
use both forms.

### 3d. What the SDK's own tests actually assert (verbatim excerpts)

Tool roundtrip, asserting **structured** output
(`test/integration/test/client/client.test.ts`):

```typescript
const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
await Promise.all([client.connect(clientTransport), server.connect(serverTransport)]);

// List tools to cache the schemas
await client.listTools();

// Call the tool - should validate successfully
const result = await client.callTool({ name: 'test-tool' });
expect(result.structuredContent).toEqual({ result: 'success', count: 42 });
```

Resource roundtrip, asserting the listed resource
(`test/integration/test/server/mcp.test.ts`):

```typescript
mcpServer.registerResource('test', 'test://resource', {}, async () => ({
    contents: [{ uri: 'test://resource', text: 'Test content' }],
}));

const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
await Promise.all([client.connect(clientTransport), mcpServer.server.connect(serverTransport)]);

const result = await client.request({ method: 'resources/list' });
expect(result.resources).toHaveLength(1);
expect(result.resources[0]!.name).toBe('test');
expect(result.resources[0]!.uri).toBe('test://resource');
```

---

## 4. Rules of thumb for a testing advisor

- **Prefer `InMemoryTransport.createLinkedPair()` for unit/integration tests of MCP server
  logic.** It exercises the *real* protocol path (initialize handshake, JSON-RPC framing,
  capability negotiation, tool/resource dispatch) without a socket or subprocess, so tests
  are fast and deterministic. Reserve stdio/Streamable-HTTP transports for end-to-end
  transport-level tests.
- **Always `await Promise.all([client.connect(...), server.connect(...)])`.** Connecting
  only one side, or awaiting them sequentially without letting both run, deadlocks the
  handshake.
- **Call `client.listTools()` before `client.callTool(...)`** when the tool has an
  output/structured schema — the client caches schemas at list time and validates the call
  result against them (the SDK's own tests rely on this ordering).
- **`transport.close()` closes both ends** — one `close()` in test teardown is enough; you
  do not need to close each transport separately.
- The runner in this repo is **Vitest** (`test`, `expect`, `vi`, `describe`, `it`). The
  pattern is identical under Jest; only the imported test primitives differ.
- Bring any Standard-Schema library for tool/prompt input schemas (the SDK examples use
  **Zod v4**: `import * as z from 'zod/v4'`).
