import asyncio
from mcp.types import Root, ListRootsResult
from mcp_use.client import MCPClient

async def custom_roots_callback(context):
    """Dynamically determine roots based on context."""
    return ListRootsResult(
        roots=[
            Root(
                uri="file:///dynamic/path", 
                name="Dynamic Root"
            ),   
        ]
    )

async def main():
    client = MCPClient(
        config="config.json", 
        list_roots_callback=custom_roots_callback
    )

if __name__ == "__main__":
    asyncio.run(main())



		

