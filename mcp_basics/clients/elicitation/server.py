from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
import pandas as pd
from typing import Optional
from pathlib import Path

server_dir = Path(__file__).parent.resolve()

mcp = FastMCP(
    name="elicitation_server",  
    port=8006, 
    stateless_http=False, 
    streamable_http_path="/elicitationserver", 
    host="127.0.0.1"
)

class ElicitationResponse(BaseModel):
    user_name: str = Field(
        default=None, 
        description="user name", 
        min_length=3, 
        max_length=50
    )

@mcp.tool()
async def collect_username(ctx: Context) -> str:
    """Collect user name with a simple text request.
    Prompts the user to provide their name via an interactive text request.
    This tool initiates a structured elicitation process.
    Returns:
        str: A status message confirming the captured name, or an informative 
            string explaining why the name was not collected (e.g., declined 
            or cancelled).
    """
    
    result = await ctx.elicit(
        message="Please provide your name", 
        schema=ElicitationResponse
    )
    
    if result.action == "accept" and result.data:
        if result.data.user_name:
            return f"Thank you for your time, provided User Name is: {result.data.user_name}"
        else:
            return "No user name provided"
    elif result.action == "decline":
        return "Elicitation declined by user"

    return "Elicitation Cancelled by User"

class searchResponse(BaseModel):
    quantity: Optional[int] = Field(
        default=10, 
        description="Number of items in stock", 
        min=0, 
        max=100
    )
    category: str = Field(
        default=None, 
        description="Category of the product", 
        examples=['Sports & Outdoors', 'Electronics', 'Groceries', 'Home Goods']
    )
    unit_price: Optional[float] = Field(
        default=10, 
        description="Price of the Product", 
        min=0, 
        max=100
    )

def fetch_product(dataframe, category=None, quantity=None, unit_price=None):
    """
    Fetches Products from the DataFrame based on Category, and quantity, and/or unit_price.
    """
    query_conditions = pd.Series([True] * len(dataframe))
    if category:
        query_conditions = query_conditions & (dataframe['Category'].str.lower() == category.lower())
    if quantity:
        query_conditions = query_conditions & (dataframe['Stock_Quantity']>= float(quantity))
    if unit_price:
        query_conditions = query_conditions & (dataframe['Price']<= float(unit_price))
    return dataframe[query_conditions].to_dict(orient='records')

@mcp.tool(
    name="search_products",
    title="Perform Product Search",
)
async def search_products(ctx: Context) -> list[dict] | str:
    """
    Searches the product database based on user-defined filters including category, 
    minimum stock quantity, and maximum unit price.
    This tool triggers an interactive flow elicitations that prompts the user for search criteria 
    via the context object. It then filters the product dataset to find matching items.
    Args:
        ctx (Context): The runtime context used to interact with the user (via elicit) 
             and manage the tool's execution lifecycle.
    Returns:
        list[dict]: A list of product dictionaries matching the search criteria if 
            the user provides data and matches are found.
        str: A status message if the search is declined ("Search declined by user") 
             or cancelled ("Search Cancelled by User").
    Yields:
        An interaction schema (searchResponse) to the user to collect:
            - category (str): The type or classification of the product.
            - quantity (int): The minimum quantity available in stock.
            - unit_price (float): The maximum price per individual unit.
    """
    df = pd.read_csv(f"{server_dir}/csvs/product.csv")
    result = await ctx.elicit(
        message="Please provide search attributes", schema=searchResponse
    )

    if result.action == "accept" and result.data:
        data = result.data
        result = fetch_product(
            dataframe=df, 
            category=data.category, 
            quantity=data.quantity, 
            unit_price=data.unit_price
        )
        return result
    elif result.action == "decline":
        return "Search declined by user"
    return "Search Cancelled by User"

def main():
    """Entry point for the direct execution server."""
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
