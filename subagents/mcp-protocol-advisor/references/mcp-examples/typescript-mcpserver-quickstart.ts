// =============================================================================
// CANONICAL MCP REFERENCE EXAMPLE (read-only; do not edit)
// Demonstrates: the *shape* of a minimal MCP server with the high-level
//   McpServer API -- a TOOL (server.registerTool, with a Zod input/output
//   schema), a templated RESOURCE (server.registerResource + ResourceTemplate),
//   and TRANSPORT setup (Streamable HTTP via Express). The parallel PROMPT API
//   is server.registerPrompt(...) (see the two Python examples in this folder
//   for a prompt end-to-end). Capabilities are declared by the register* calls.
// SDK: @modelcontextprotocol/sdk (TypeScript) v1.22.0 -- stable v1.x line.
// Source: https://github.com/modelcontextprotocol/typescript-sdk/blob/1.22.0/README.md#quick-start
//   (verbatim "Quick Start" code block; raw README:
//    https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/1.22.0/README.md )
// Tag 1.22.0 dated 2025-11-13 (commit 324d4711). Retrieved 2026-07-05.
// NOTE: SDK `main` has moved to v2-beta (split packages
//   `@modelcontextprotocol/server` / `/client`); v1.x remains the stable API.
// =============================================================================

import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { z } from 'zod';

// Create an MCP server
const server = new McpServer({
    name: 'demo-server',
    version: '1.0.0'
});

// Add an addition tool
server.registerTool(
    'add',
    {
        title: 'Addition Tool',
        description: 'Add two numbers',
        inputSchema: { a: z.number(), b: z.number() },
        outputSchema: { result: z.number() }
    },
    async ({ a, b }) => {
        const output = { result: a + b };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);

// Add a dynamic greeting resource
server.registerResource(
    'greeting',
    new ResourceTemplate('greeting://{name}', { list: undefined }),
    {
        title: 'Greeting Resource', // Display name for UI
        description: 'Dynamic greeting generator'
    },
    async (uri, { name }) => ({
        contents: [
            {
                uri: uri.href,
                text: `Hello, ${name}!`
            }
        ]
    })
);

// Set up Express and HTTP transport
const app = express();
app.use(express.json());

app.post('/mcp', async (req, res) => {
    // Create a new transport for each request to prevent request ID collisions
    const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
        enableJsonResponse: true
    });

    res.on('close', () => {
        transport.close();
    });

    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
});

const port = parseInt(process.env.PORT || '3000');
app.listen(port, () => {
    console.log(`Demo MCP Server running on http://localhost:${port}/mcp`);
}).on('error', error => {
    console.error('Server error:', error);
    process.exit(1);
});
