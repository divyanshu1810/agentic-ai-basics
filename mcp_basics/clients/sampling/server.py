from mcp.server.fastmcp import FastMCP, Context
from mcp.types import ModelPreferences, SamplingMessage, TextContent
import pandas as pd
from pathlib import Path

server_dir = Path(__file__).parent.resolve()

mcp = FastMCP(
    name="sampling_server",  
    port=8005, 
    stateless_http=False, 
    streamable_http_path="/samplingserver", 
    host="127.0.0.1"
)

@mcp.tool(
    name="get_product",
    title="Get Product of a Category",
)
async def get_product(query: str, ctx: Context) -> str | list[dict]:
    """
    Identifies a product category from a user query using an LLM and retrieves 
    matching product records from the local database.
    This tool performs a two-step process:
    1. It samples an LLM to classify the natural language 'query' into one of the predefined categories found in the 'product.csv' dataset.
    2. It filters the dataset for the identified category and returns the corresponding product list.
    Args:
        query (str): The user's natural language input or question (e.g., "I need new running shoes").
        ctx (Context): The MCP context object used to manage the session and trigger 
        LLM sampling for category classification.
    Returns:
        str | list[dict]: Returns a list of dictionaries representing product records if a valid category is identified and matches exist. 
            Returns "No Data Found!" if the LLM prediction does not match existing categories or no products are available.
    """
    df = pd.read_csv(f"{server_dir}/csvs/product.csv")
    categories = str(set(df['Category']))
    prompt = f"""Identify the product category of the following query as {categories}.
    Just output a single word - {categories}.
    Query to analyze: {query}"""

    sampling_response = await ctx.session.create_message(
        messages=[SamplingMessage(
            role="user",
            content=TextContent(
                type="text",
                text=prompt)
            )
        ],
        temperature=0.7,
        max_tokens=100,
        model_preferences=ModelPreferences(
            hints=[
                {"name":"llama"},
                {"name":"gpt"},
                {"name":"gemini"}
            ],
            costPriority=0.3,
            speedPriority=0.8,
            intelligencePriority=0.7
        )
    )

    if sampling_response.content.type=="text":
        category = sampling_response.content.text
    if category in categories:
        response = df[df['Category'] == category].to_dict(orient='records')
    else:
        response = "No Data Found!"

    return response

def main():
    """Entry point for the direct execution server."""
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
