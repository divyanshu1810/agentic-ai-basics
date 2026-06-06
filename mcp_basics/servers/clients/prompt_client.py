import asyncio
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from mcp_use import MCPAgent, MCPClient
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

async def run():
    config_file = "configs/prompt_server.json"
    client = MCPClient.from_config_file(config_file)

    agent = MCPAgent(
        llm=llmCohere(),
        client=client,
        max_steps=15,
        additional_instructions = "You are a helpful assistant. response using the best available prompts, resource information and tools",
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
                print(response)
            except Exception as e:
                print(f"\nError: {e}")
    finally:
        await agent.close()          

def main():
    asyncio.run(run())
if __name__ == "__main__":
    main()
