
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]


async def _list_mcp_tools():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_servers.risk_mcp_server"],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description or "",
                }
                for tool in result.tools
            ]


def list_mcp_tools() -> list[dict]:
    """Return tools exposed by the project-risk MCP server."""
    return asyncio.run(_list_mcp_tools())


async def _call_mcp_tool(
    tool_name: str,
    arguments: dict,
) -> dict:
    """Call a tool exposed by the project-risk MCP server."""

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_servers.risk_mcp_server"],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            available_tools = await session.list_tools()
            allowed_tools = {
                tool.name for tool in available_tools.tools
            }

            if tool_name not in allowed_tools:
                raise ValueError(
                    "Requested MCP tool is not available."
                )

            result = await session.call_tool(
                tool_name,
                arguments=arguments,
            )

            if result.isError:
                raise RuntimeError("MCP tool call failed.")

            output = []

            for item in result.content:
                if hasattr(item, "text"):
                    try:
                        output.append(json.loads(item.text))
                    except json.JSONDecodeError:
                        output.append(item.text)

            return {
                "tool_name": tool_name,
                "content": output,
            }


def call_mcp_tool(
    tool_name: str,
    arguments: dict,
) -> dict:
    """Synchronously call an approved project-risk MCP tool."""
    return asyncio.run(
        _call_mcp_tool(tool_name, arguments)
    )