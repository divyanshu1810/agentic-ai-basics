##-----------------Imports-----------------
from langchain_aws import ChatBedrockConverse
from langchain_cohere import ChatCohere
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.utilities import SerpAPIWrapper
from langchain_tavily import TavilySearch
from langchain_core.tools import Tool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from rich.pretty import pprint
from typing import AsyncIterable, Any
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    BaseMessage,
)
import uuid
load_dotenv()
 
##-----------------Rest of the Code-----------------

def llmCohere():
    return ChatCohere(
        id='command-a-03-2025',
        temperature=0.9
    )

#-------Websearch Tool using TAVILY------------
websearch_tool_tavily = TavilySearch(
    max_results=5,
    topic="general",
    include_answer=True,
    include_raw_content=True,
    search_depth="basic",
)

# Defining Websearch Agent----------------------------------
class WebsearchAgent:
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
    SYSTEM_INSTRUCTION = (
        """You are a specialized assistant for question-answering tasks which search the web to retrieve relevant information on a given topic from the open internet.
    Your sole purpose is to use the 'perform_websearch' tool to search the web to retrieve the latest relevant information required to answer the given query.
    
    Use the retrieved relevant information to answer the question.
    Summarize the retrieved contents to formulate a comprehensive answer.
    
    Important:
    - Provide well-structured output with section headings.
    - Use lists, tables, and bullet points if required.
    If you don't know the answer, just say that you don't know.
    """
    )
    def __init__(self):
        self.model = llmCohere()
        self.tools = [websearch_tool_tavily]
        self.graph = create_agent(
            self.model,
            tools=self.tools,
            checkpointer=InMemorySaver(),
            system_prompt=self.SYSTEM_INSTRUCTION,
            debug=True
        )
    # ------ Implementation code continues------------------------

    #--- Invoke Method of the Websearch Agent---------------------
    def invoke(self, query, context_id) -> dict[str, Any]:
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': context_id}}
        print(inputs)
        output = self.graph.invoke(inputs,config=config)
        message = output['messages'][-1].content
        return {
                    'is_task_complete': True,
                    'content':message,
                }