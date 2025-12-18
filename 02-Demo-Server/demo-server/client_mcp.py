import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    url = "http://127.0.0.1:8000/mcp"
    async with streamable_http_client(url) as (read, write, get_session_id):
        async with ClientSession(read, write) as session:
            print("Session ID before initialization:", get_session_id())

            await session.initialize()
            print("Session ID after initialization:", get_session_id())

            result = await session.call_tool("add", {"a": 21, "b": 24})
            print("Result from the server:", result)

if __name__ == "__main__":
    asyncio.run(main())