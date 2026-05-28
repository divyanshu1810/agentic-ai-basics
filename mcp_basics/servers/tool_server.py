from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="tool_server",  
    port=8001,
    stateless_http=False, 
    streamable_http_path="/toolserver", 
    host="127.0.0.1", 
    warn_on_duplicate_tools=True
)

@mcp.tool(
    name = "add",
    title = "add",
    description = "Add two numbers",
    annotations={
        'readOnlyHint': True,
        'destructiveHint': False,
        'idempotentHint': False,
        'openWorldHint': False
    }
)
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool(
    name = "subtract",
    title = "subtract",
    description = "Subtract two numbers",
    annotations={
        'readOnlyHint': True,
        'destructiveHint': False,
        'idempotentHint': False,
        'openWorldHint': False
    }
)
async def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool(
    name = "multiply",
    title = "multiply",
    description = "Multiply two numbers",
    annotations={
        'readOnlyHint': True,
        'destructiveHint': False,
        'idempotentHint': False,
        'openWorldHint': False
    }
)
async def multiply(a: int, b: int) -> int:
    """multiply two numbers"""
    return a * b

@mcp.tool(
    name = "divide",
    title = "divide",
    description = "Divide two numbers",
    annotations={
        'readOnlyHint': True,
        'destructiveHint': False,
        'idempotentHint': False,
        'openWorldHint': False
    }
)
async def divide(a: int, b: int) -> int:
    """divide two numbers"""
    if b == 0:
        b = 1
    return a / b

@mcp.tool(
    name = "power",
    title = "power",
    description = "raising to the power",
    annotations={
        'readOnlyHint': True,
        'destructiveHint': False,
        'idempotentHint': False,
        'openWorldHint': False
    }
)
async def power(a: int, b: int) -> int:
    """raising to the power"""
    return a ** b

def main():
    """Entry point for the direct execution server."""
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
