import asyncio
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from mcp_use import MCPAgent, MCPClient

load_dotenv()

async def run():
    client = MCPClient.from_config_file("config/tool_server.json")

    agent = MCPAgent(
        llm=ChatCohere(),
        client=client
    )

    await client.create_all_sessions()

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = await agent.run(user_input)
        print("\nAssistant:", response)

    await agent.close()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()