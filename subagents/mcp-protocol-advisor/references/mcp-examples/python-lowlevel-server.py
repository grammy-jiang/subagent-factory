# =============================================================================
# CANONICAL MCP REFERENCE EXAMPLE (read-only; do not edit)
# Demonstrates: the low-level `Server` API that FastMCP wraps -- explicit
#   PROMPT handlers (@server.list_prompts / @server.get_prompt), explicit
#   CAPABILITY NEGOTIATION (server.get_capabilities(...) fed into
#   InitializationOptions), and stdio TRANSPORT. This is the spec-faithful
#   layer beneath FastMCP's sugar; TOOL and RESOURCE handlers follow the same
#   pattern (@server.list_tools()/@server.call_tool(),
#   @server.list_resources()/@server.read_resource()).
# SDK: mcp (Python) v1.28.1 -- stable v1.x line (production-recommended).
# Source (raw): https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v1.28.1/examples/snippets/servers/lowlevel/basic.py
# Source (blob): https://github.com/modelcontextprotocol/python-sdk/blob/v1.28.1/examples/snippets/servers/lowlevel/basic.py
# Upstream file last changed 2025-07-16 (commit 0b4ce00b). Retrieved 2026-07-05.
# =============================================================================

"""
Run from the repository root:
uv run examples/snippets/servers/lowlevel/basic.py
"""

import asyncio

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Create a server instance
server = Server("example-server")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="example-prompt",
            description="An example prompt template",
            arguments=[
                types.PromptArgument(name="arg1", description="Example argument", required=True)
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Get a specific prompt by name."""
    if name != "example-prompt":
        raise ValueError(f"Unknown prompt: {name}")

    arg1_value = (arguments or {}).get("arg1", "default")

    return types.GetPromptResult(
        description="Example prompt",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text", text=f"Example prompt text with argument: {arg1_value}"
                ),
            )
        ],
    )


async def run():
    """Run the basic low-level server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
