import asyncio

from langchain_ollama import ChatOllama
from mcp_use import MCPClient, MCPAgent

async def main():
    # Create configuration dict
    config = {
        "mcpServers": {
            "weather": {
                "command": "uv",
                "args": [
                    "run",
                    "--directory",
                    "/Users/prudhvitej/development/Udemy/MCP Mastery/03-MCP-Server-Ollama-Agent",
                    "weather-server.py"
                ]
            },
            "math_server": {
                "command": "uv",
                "args": [
                    "run",
                    "--directory",
                    "/Users/prudhvitej/development/Udemy/MCP Mastery/03-MCP-Server-Ollama-Agent",
                    "math-server.py"
                ]
            }
        }
    }

    # Create MCP client from configuration dict
    client = MCPClient.from_dict(config)

    # Create LLM
    # To pull a model - ollama pull deepseek-r1:8b
    # To pull a model - ollama pull qwen3:8b
    # Ollama models - ollama list
    # Ollama port - lsof -i -P | grep LISTEN | grep ollama
    llm = ChatOllama(base_url="http://localhost:11434", model="qwen3:8b")

    # Create an agent with the client
    # agent = MCPAgent(llm=llm, client=client, max_steps=30) # for a single mcp server
    agent = MCPAgent(llm=llm, client=client, max_steps=30, use_server_manager=True)  # use_server_manager - dynamically manages multiple mcp servers

    result = await agent.run(
        "What's the weather in Bangalore and the 3-day forecast?"
    )
    print(f"Weather Forecast: {result}")

    result = await agent.run(
        "What's sum of 24 and 21 and the result divided by 3?"
    )
    print(f"Calculation Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())