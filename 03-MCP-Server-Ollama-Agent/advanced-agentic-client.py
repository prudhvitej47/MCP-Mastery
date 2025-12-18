import asyncio
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")

async def main():
    client = MCPClient.from_config_file(os.path.join(os.path.dirname(__file__), "mcp.json"))

    # Better model for understanding multiple mcp servers and tools
    # ollama pull gpt-oss:120b-cloud
    llm = ChatOllama(
        model="gpt-oss:120b-cloud",
        base_url="https://ollama.com",
        client_kwargs={
            "headers": {
                "Authorization": f"Bearer {api_key}"
            }
        }
        #model="gpt-oss:20b",
        #num_gpu=99, # Given my Mac has only 16GB unified memory & gpt-oss needs 16GB+ to run, I am forcing Ollama to offload to GPU layer as much as possible
        #num_ctx=1024 # Limits the context window to 1024 token (vs. default 2048-4096 tokens). Reduces memory footprint dramatically.
    )

    agent = MCPAgent(llm=llm, client=client, max_steps=30, use_server_manager=True)

    result = await agent.run(
        "What's the weather in New York and the 3-day forecast? Also what's 18 multiplied by 90 and then divided by 3?"
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())