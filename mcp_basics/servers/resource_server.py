import json
import pandas as pd
from mcp.server.fastmcp import FastMCP
from pathlib import Path
from mcp.server.fastmcp.resources import TextResource,FileResource, BinaryResource, DirectoryResource
import aiofiles
import asyncio 

server_dir = Path(__file__).parent.resolve()

mcp = FastMCP(
    name="ResourceServer",  
    port=8003, 
    stateless_http=False, 
    streamable_http_path="/resourceserver", 
    host="127.0.0.1",
    warn_on_duplicate_resources=True
)

@mcp.resource(
    uri="resource://greeting",
    name="get_greeting",
    title="Get Greeting message",
    description="Get Simple Greeting message",
    mime_type="text/plain"
)
async def get_greeting() -> str:
    """Provides a simple greeting message."""
    return "Hello from FastMCP Resources!"

notice_resource = TextResource(
    uri="resource://notice",
    title="Application Notice",
    name="Important Notice",
    text='''System maintenance scheduled for Sunday 10th August, 2025, from 10:00 Hrs to 17:00 hrs." \
    During this period, the application will be unavailable. We apologize for any inconvenience this may cause and appreciate your patience as we work to improve our services.'''
)
mcp.add_resource(notice_resource)


log_file_path = Path(f"{server_dir}/app/logs/application.log")
@mcp.resource(
    uri="file://app/logs/application.log",
    name="read_application_log",
    title="Read Application Logs",
    description="Read Inventory Management System Log file",
    mime_type="text/plain"
)
async def read_application_log() -> str:
    """Reads content from a specific log file asynchronously."""
    try:
        async with aiofiles.open(log_file_path, mode="r") as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        return "Log file not found."

## Helper Function
def read_json_file(file_path):
    """
    Reads a JSON file, parses it, and returns the data as a Python dictionary.
    Args:
        file_path (str): The path to the JSON file.
    Returns:
        dict or None: The parsed JSON data if successful, otherwise None.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception as e:
        return None

@mcp.resource(
    uri="data://config",
    name="get_config",
    title="Get Application Configuration",
    description="Get Inventory Management System Configuration in JSON format",
    mime_type="application/json"
)
async def get_config() -> dict:
    """Reads application configuration as JSON."""
    json_file_path = Path(f"{server_dir}/data/config.json")
    json_data = read_json_file(json_file_path)
    return json_data

readme_path = Path(f"{server_dir}/data/README.txt")
if readme_path.exists():
    readme_resource = FileResource(
        uri=f"file://{readme_path.as_posix()}",
        path=readme_path,
        name="Project README File",
        description="MC-Hilton Inventory Management System README File.",
        mime_type="text/markdown"
    )
    mcp.add_resource(readme_resource)

data_dir_path = Path(f"{server_dir}/data/")
if data_dir_path.is_dir():
    data_listing_resource = DirectoryResource(
        uri="resource://data-files",
        path=data_dir_path,
        name="Resource Server Directory Listing",
        description="Lists files available in the Server directory.",
        recursive=True
    )
    mcp.add_resource(data_listing_resource)

def main():
    """Entry point for the direct execution server."""
    mcp.run(transport="streamable-http")
    
if __name__ == "__main__":
    main()
