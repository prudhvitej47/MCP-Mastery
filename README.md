To get the MCP Server up and running:
```shell
uv add fastmcp mcp h2
uv add langchain mcp-use langchain-ollama "mcp-use[search]"
```

To display the project package dependencies:
```shell
uv tree
```

To run the MCP Server:
```shell
uv run demo-server/server.py/
```

MCP Server starts running on: http://127.0.0.1:8000/mcp


#### How does MCP work when running a weather MCP server and LLM on Ollama locally?

Here is the breakdown of what each component does in your `agentic-client.py` example:

### 1. The Host (MCP Server)
In your code, the **Host** is the `weather-server.py` process.
*   **Purpose:** It acts as the "provider" of capabilities. It contains the actual logic for interacting with the outside world (in this case, fetching weather data from `wttr.in`).
*   **Role:** It exposes "tools" (like `get_weather` and `get_forecast`) to the client. It doesn't know *why* it's being called; it just waits for a command, executes the tool, and returns the data.
*   **Lifecycle:** It is spawned by the client (via the `uv run` command in your config) and communicates over `stdio`.

### 2. The Client (`MCPClient`)
The **Client** is the bridge or the "orchestrator" of connections.
*   **Purpose:** It manages the connection to one or more MCP Servers. It handles the low-level communication (sending JSON-RPC requests over standard input/output).
*   **Role:** It discovers what tools are available on the servers and makes them accessible to the Agent. Think of it as the "USB Hub" that connects various peripherals (servers) to the computer (the agent).

### 3. The LLM (`ChatOllama`)
The **LLM** is the "brain" or the "reasoning engine."
*   **Purpose:** It understands natural language and decides *how* to solve a problem. 
*   **Role:** When you ask "What's the weather in Bangalore?", the LLM realizes it doesn't know the answer but sees that a `get_weather` tool is available. It generates a "tool call"—essentially saying, "I want to run `get_weather` with the argument `Bangalore`."
*   **Note:** In your case, it’s running locally via Ollama.

### 4. The Agent (`MCPAgent`)
The **Agent** is the "operator" that closes the loop.
*   **Purpose:** It manages the conversation flow between the User, the LLM, and the Client.
*   **Role:** 
    1.  It sends your prompt to the LLM.
    2.  It takes the LLM's request to use a tool.
    3.  It asks the **Client** to execute that tool on the **Host**.
    4.  It takes the result from the Host and feeds it back to the LLM.
    5.  It repeats this until the LLM has enough info to give you a final answer.

---

### What if the LLM is running on a remote server?

If you decide to move your LLM (Ollama or a provider like OpenAI/Claude) to a remote server, here is what changes:

1.  **Network Communication:** Instead of your agent talking to `localhost:11434`, it will send HTTP requests over the internet to the remote IP or domain.
2.  **Latency:** You will experience a slight delay (network round-trip time) for every "thought" the LLM has, as the prompt must travel to the server and the response must travel back.
3.  **Security:** You would likely need an API Key or an SSH tunnel to securely communicate with that remote instance.
4.  **The Local Advantage Stays:** Even if the **LLM** is remote, your **MCP Client and Host** usually stay local. This is the "magic" of MCP: A remote "brain" (LLM) can use its reasoning to control tools that are running locally on *your* machine (like reading your local files or checking your local weather).

**In Summary:**
*   **LLM:** Thinks and decides.
*   **Agent:** Coordinates the thinking and doing.
*   **Client:** Connects the Agent to the Tools.
*   **Host (Server):** Actually performs the work.