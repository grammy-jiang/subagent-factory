# =============================================================================
# CANONICAL MCP REFERENCE EXAMPLE (read-only; do not edit)
# Demonstrates: the *shape* of a minimal MCP server with the high-level FastMCP
#   API -- a TOOL (@mcp.tool), a templated RESOURCE (@mcp.resource), a PROMPT
#   (@mcp.prompt), and TRANSPORT setup (Streamable HTTP). Capabilities
#   (tools/resources/prompts) are declared implicitly by the decorators.
# SDK: mcp (Python) v1.28.1 -- stable v1.x line (production-recommended).
# Source (raw): https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v1.28.1/examples/snippets/servers/fastmcp_quickstart.py
# Source (blob): https://github.com/modelcontextprotocol/python-sdk/blob/v1.28.1/examples/snippets/servers/fastmcp_quickstart.py
# Upstream file last changed 2025-11-20 (commit fcffa14b). Retrieved 2026-07-05.
# NOTE: SDK `main` has moved to v2-beta, where FastMCP is renamed `MCPServer`
#   (`from mcp.server.mcpserver import MCPServer`); v1.x remains the stable API.
# =============================================================================

"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
