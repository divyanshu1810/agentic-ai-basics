import asyncio
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_cohere import ChatCohere
from langchain_ollama.chat_models import ChatOllama
from mcp_use import MCPAgent, MCPClient
from mcp.client.session import ClientSession
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    ErrorData,
    TextContent
)

import os
import warnings

warnings.filterwarnings("ignore", category=Warning)
os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"

load_dotenv()
def llmCohere():
    return ChatCohere(
        id='command-a-03-2025',
        temperature=0.9
    )

def llmOllama():
    return ChatOllama(
        model = "qwen2.5:1.5b",
        temperature = 1.0,
        num_predict = 1024,
    )

async def sampling_callback(
        context: ClientSession,
        params: CreateMessageRequestParams
) -> CreateMessageResult | ErrorData:
    """
    Sampling callback implementation.
    This function receives a prompt and returns an LLM response.
    """
    prompt = params.messages[-1].content.text
    hints = params.modelPreferences.hints
    reqmodels = []

    for h in hints:
        reqmodels.append(h.name)
    
    model_used = "Default"

    if "qwen" in reqmodels:
        llm2 = llmOllama()
        model_used = "Qwen2.5:1.5b"
        response = llm2.invoke(prompt).content
    else:
        response = llmCohere().invoke(prompt).content

    return CreateMessageResult(
        content=TextContent(text=response.split('\n')[-1], type="text"),
        model=model_used,
        role="assistant"
    )

async def run():
    config_file = "config.json"

    client = MCPClient.from_config_file(
        file_path=config_file, 
        sampling_callback=sampling_callback
    )

    agent = MCPAgent(
        llm=llmCohere(),
        client=client,
        max_steps=15,
        additional_instructions = "You are a helpful assistant. response with tool output",
        memory_enabled=True,
        use_server_manager=True
    )

    server_names = client.get_server_names()
    await client.create_all_sessions()

    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", ""]:
                print("Ending conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                continue
            print("\nAssistant: ", end="", flush=True)
            try:
                response = await agent.run(user_input)
            except Exception as e:
                print(f"\nError: {e}")
    finally:
        await agent.close()            

def main():
    asyncio.run(run())
if __name__ == "__main__":
    main()
