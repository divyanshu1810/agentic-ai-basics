from mcp_use.server import Context, MCPServer

server = MCPServer(
	name="File Server", 
	host="127.0.0.1", 
	port=8028
)

@server.tool()
async def get_workspace_info(ctx: Context) -> str:
	"""Get information about the client's available workspaces."""
	roots = await ctx.list_roots()
	if not roots:
    	return "No roots available from client"
	lines = [f"Available workspaces ({len(roots)}):"]
	for root in roots:
    	name = root.name or "(unnamed)"
    	lines.append(f"  - {name}: {root.uri}")
	return "\n".join(lines)
