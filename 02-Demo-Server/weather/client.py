import asyncio
from fastmcp import Client

async def main():
    url = "http://127.0.0.1:8000/mcp"
    async with Client(url) as client:
        if client.is_connected:
            print("Connected to the Weather MCP Server")

        tools = await client.list_tools()
        print("\n--- Available tools ---")
        for t in tools:
            print(f"{t.name}: {t.description}")

        print("\n--- Getting current weather in London ---")
        forecast = await client.call_tool("get_weather", {"location": "London"})
        print(forecast)
        print(forecast.data)

        print("\n--- Getting weather forecast for Visakhapatnam ---")
        forecast1 = await client.call_tool("get_forecast", {"location": "Visakhapatnam"})
        print(forecast1)
        print(forecast1.data)

        print("\n--- Getting weather forecast for Bangalore ---")
        forecast2 = await client.call_tool("get_forecast", {"location": "Bangalore"})
        print(forecast2)
        print(forecast2.data)
        print("\n--- The end ---")


if __name__ == "__main__":
    asyncio.run(main())