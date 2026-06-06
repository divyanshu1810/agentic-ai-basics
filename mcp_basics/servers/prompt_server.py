from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent
from pydantic import Field, Annotated
from pathlib import Path

mcp = FastMCP(
    name="prompt_server", 
    port=8004, 
    stateless_http=False, 
    streamable_http_path="/promptserver", 
    host="127.0.0.1",
    warn_on_duplicate_prompts=True
)

@mcp.prompt(
    name="explain-topic",
    title="Prompt Template for explanation",
    description="Generates a user message asking for an explanation of a topic."
)
def explain_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic. 
    This docstring is ignored when description is provided."""
    return f"Can you please explain the concept of '{topic}'?"

@mcp.prompt(
    name="summarize_prompt",
    description="Creates a request to summarize a content with specific parameters",
)
def summarize_prompt(
    content_uri: str = Field(description="The URI of the resource containing the content."),
    summary_type: str = Field(default="short", description="Type of summary.")
) -> str:
    """This docstring is ignored when description is provided."""
    return f"Please perform a '{summary_type}' summary on the text found at {content_uri}."

@mcp.prompt()
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """"
    Generates a structured user message requesting a code implementation.
    This prompt template assists in creating consistent code generation requests 
    for an LLM, specifying both the target language and the functional requirements.
    Args:
        language (str): The programming language in which the function should be written 
            (e.g., 'Python', 'TypeScript', 'Rust').
        task_description (str): A detailed description of the logic or behavior the 
            generated function must implement.
    Returns:
        PromptMessage: A formatted message object containing the role 'user' and the 
            templated request text.
    """
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))

@mcp.prompt()
def roleplay_scenario(character: str, situation: str) -> list[PromptMessage]:
    """
    Initializes a structured roleplaying environment by defining the model's persona 
    and the surrounding context.
    This prompt template streamlines the setup for interactive storytelling or 
    simulation by establishing a consistent starting point for the LLM.
    Args:
        character (str): The specific persona, profession, or fictional identity 
            the AI should adopt (e.g., "a medieval blacksmith" or "a seasoned detective").
        situation (str): The immediate context or conflict the character is facing 
            to start the interaction (e.g., "standing in a crowded market during a rainstorm").
    Returns:
        list[PromptMessage]: A list of structured message objects that prime the model 
            with the user's roleplay instructions and an initial assistant acknowledgment.
    """
    return [
        PromptMessage(f"Let's roleplay. You are {character}. The situation is: {situation}"),
        PromptMessage("Okay, I understand. I am ready. What happens next?", role="assistant")
    ]

@mcp.prompt()
def log_analysis_prompt(
    data_uri: str,                        
    analysis_type: str = "short",      
    include_charts: bool = False
) -> str:
    """
    Creates a robust prompt to analyze log data with specific parameters.
    Args:
        data_uri (str): The location/identifier of the log data to be processed.
        analysis_type (str, optional): The depth of the investigation. 
            Options typically include "short", "detailed", or "comprehensive". 
            Defaults to "short".
        include_charts (bool, optional): Whether to request visual representations 
            of the data trends. Defaults to False.
    Returns:
        str: A formatted instruction string for the LLM.
    """
    prompt = f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
    if include_charts:
        prompt += " Include relevant charts and visualizations."
    return prompt

@mcp.prompt()
def data_analysis_prompt(
    n_rows: Annotated[int, Field(description="Number of Records or Rows in the Dataset")], 
    columns: Annotated[str | list[str], Field(description="Column Names of the Dataset")],   
    domain: Annotated[str,Field(descrption="Domain of Expertise")],     
    data_desciption: Annotated[str,Field(description="A representative Title for the data to analyze")] 
) -> str:
    """
    Generates a structured, high-context prompt for an LLM to perform professional data analysis.
    This tool constructs a persona-driven instruction set focusing on data cleaning, 
    exploratory analysis, and business intelligence reporting based on specific 
    metadata provided about a dataset.
    Args:
        n_rows (int): The total count of records in the dataset. Used to help the 
            model understand the scale and statistical significance of the data.
        columns (str or list[str]): A list of strings representing the headers or features 
            available in the dataset.
        domain (str): The specific field of expertise the analyst persona 
            should adopt (e.g., "Healthcare", "E-commerce"). 
        data_description (str): A brief title or summary of what the 
            dataset represents to provide context for trend identification. 
    Returns:
        str: A formatted multi-line string containing the role, context, task 
            instructions, and output constraints.
    """
    prompt = f"""
Role: Act as an expert Data Analyst in Python with 10 years of experience in {domain}.
Context: I am providing a dataset containing {n_rows} rows with the following columns: 
{columns}. 
This data represents {data_desciption}.
#Task - Generate code for:
1. Cleaning the data by identifying missing values and suggesting handling methods.
2. Performing exploratory data analysis to find the top 3 trends in Sales and Revenue.
3. Identifying any significant anomalies or outliers.
Output: Generate code snippets to highlight findings in a structured report with a summary table and a list of 3 actionable business recommendations based on these insights.
Constraint: Do not make assumptions beyond what is explicitly shown in the provided data.
    """
    return prompt

def main():
    """Entry point for the direct execution server."""
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
