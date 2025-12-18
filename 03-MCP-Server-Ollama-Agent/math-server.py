from fastmcp import FastMCP

mcp = FastMCP("Math Server")

@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
async def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
async def divide(a: int, b: int) -> str | float:
    """Divide two numbers"""
    if b == 0:
        return "Error: Division by zero!"
    return a / b


if __name__ == "__main__":
    # mcp.run(transport="stdio")

    # uncomment the above line and comment the below line to run the server using agentic-client.py,
    # which runs the server by itself using stdio

    mcp.run(transport="streamable-http", port=8001)