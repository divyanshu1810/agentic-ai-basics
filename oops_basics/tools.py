from abc import ABC, abstractmethod

# Abstract Tool
class Tool(ABC):
    @abstractmethod
    def execute(self, input_data):
        pass


# Concrete Tools
class WebSearchTool(Tool):
    def execute(self, query):
        return f"Searching web for: {query}"


class CalculatorTool(Tool):
    def execute(self, expression):
        return eval(expression)


# Agent
class Agent:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def run(self, tool_name, input_data):
        if tool_name not in self.tools:
            return "Tool not found"
        return self.tools[tool_name].execute(input_data)


# Usage
agent = Agent()
agent.register_tool("search", WebSearchTool())
agent.register_tool("calc", CalculatorTool())

print(agent.run("search", "AI agents"))
print(agent.run("calc", "2 + 3 * 5"))