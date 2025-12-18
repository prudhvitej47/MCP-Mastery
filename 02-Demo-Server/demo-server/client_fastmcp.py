import asyncio
from fastmcp import Client

async def main():
    url = "http://127.0.0.1:8000/mcp"
    async with Client(url) as client:
        if client.is_connected:
            print("Connected to the MCP server")

        tools = await client.list_tools()
        print("\n--- Available tools ---")
        for t in tools:
            print(f"{t.name}: {t.description}")

        response = await client.call_tool("add", {"a": 21, "b": 24})
        print("\n--- Tool Response ---")
        print(response)

if __name__ == "__main__":
    asyncio.run(main())