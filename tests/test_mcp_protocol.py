
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check_mcp_connection():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_servers.risk_mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tool_result = await session.list_tools()
            tool_names = {tool.name for tool in tool_result.tools}

            print("Discovered MCP tools:", sorted(tool_names))

            assert "get_project_risks" in tool_names
            assert "search_project_knowledge" in tool_names

            result = await session.call_tool(
                "get_project_risks",
                arguments={"project_id": "PRJ-001"},
            )

            assert not result.isError, (
                f"MCP tool call failed: {result.content}"
            )

            print("MCP tool call completed successfully.")
            print("MCP protocol connection verified.")


def test_mcp_protocol_connection():
    asyncio.run(check_mcp_connection())