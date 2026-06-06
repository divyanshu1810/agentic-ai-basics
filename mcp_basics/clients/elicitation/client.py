import asyncio
from langchain_cohere import ChatCohere
from rich.pretty import pprint
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient
from mcp.shared.context import RequestContext
from mcp.types import ElicitRequestParams, ElicitResult
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

async def elicitation_callback(
    context: RequestContext,
    params: ElicitRequestParams
) -> ElicitResult:
    """
    Elicitation callback implementation.
    This function receives a request for user inputs and returns the user's response.
    Example showing how to use all parameters."""

    if hasattr(params, 'requestedSchema') and params.requestedSchema:
        schema = getattr(params, 'requestedSchema', None)
        schema_type = schema.get('type')
        if schema_type == 'object':
            properties = schema.get('properties', {})
            user_data = {}
            required_fields = []
            for field_name, field_def in properties.items():
                mandatory_field, field_type = 'Optional', 'Undefined'
                if 'type' in field_def.keys():
                    field_type = field_def.get('type', 'string')
                    mandatory_field= ' *(Mandatory Field)'
                    required_fields.append(field_name)
                else:
                    if 'anyOf' in field_def.keys():
                        field_type = field_def.get('anyOf')[0]['type']
                field_description = field_def.get('description', '')
                prompt = f"{field_name} ({field_type} - {field_description} - {mandatory_field}):"
                value = input(prompt)
                if field_type == 'string':
                    value = value.lower().strip() if value else None
                elif field_type == 'number':
                    value = float(value) if value else None
                elif field_type == 'integer':
                    value = int(value) if value else None
                elif field_type == 'boolean':
                    value = value.lower() in ('true', '1', 'yes') if value else None
                
                user_data[field_name] = value
            
            missing_fields = [
                field for field in required_fields 
                if field not in user_data or not user_data[field]
            ]

            if missing_fields:
                return ElicitResult(action="cancel")
            
            return ElicitResult(action="accept", content=user_data)
    
async def run():
    config_file = "config.json"
    client = MCPClient.from_config_file(
        file_path=config_file, 
        elicitation_callback=elicitation_callback
    )    

    agent = MCPAgent(
        llm=llmCohere(),
        client=client,
        max_steps=15,
        additional_instructions = "You are a helpful assistant. response with tool output",
        memory_enabled=True,
        use_server_manager=True
    )

    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", ""]:
                print("Ending conversation...")
                break
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
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
