# 🤖 Agentic AI Basics

A hands-on learning repository covering the core building blocks of modern Agentic AI systems — from Python OOP fundamentals to production-grade A2A (Agent-to-Agent) protocols. Each module is self-contained and progressively builds toward real-world agentic architectures.

---

## 📁 Repository Structure

```
agentic-ai-basics/
├── oops_basics/          # Python OOP fundamentals for AI engineering
├── langchain_basics/     # LangChain & RAG with Jupyter notebooks
├── langgraph_basics/     # LangGraph stateful agent graphs
├── mcp_basics/           # Model Context Protocol (MCP) server + client
└── a2a_basics/           # Agent-to-Agent (A2A) protocol implementation
```

---

## 🧩 Modules

### 1. `oops_basics/` — Python OOP for AI Engineering

Core Python object-oriented patterns as they apply to AI agent design.

| File | Concept |
|------|---------|
| `oop.py` | Encapsulation, Inheritance, Polymorphism (Animal → Dog/Cat) |
| `basics.py` | Class methods vs. static methods on a `User` class |
| `circle.py` | Input validation, geometry calculations with `Circle` |
| `data.py` | `__repr__` and Python `@dataclass` for clean data models |
| `tools.py` | Abstract base classes (`ABC`) modelling an Agent with pluggable tools (`WebSearchTool`, `CalculatorTool`) |
| `stream.py` | FastAPI `StreamingResponse` for simulating LLM token streaming |
| `sort.py` | Sorting algorithms as utility primitives |

**Key takeaway:** `tools.py` directly mirrors how real LangChain / LangGraph tool registries work under the hood — abstract `Tool` class + concrete implementations + a dispatcher `Agent`.

---

### 2. `langchain_basics/` — LangChain & RAG

Jupyter notebooks exploring LangChain's core abstractions.

| File | Content |
|------|---------|
| `main.ipynb` | LangChain chains, prompts, and LLM wrappers |
| `session.ipynb` | Retrieval-Augmented Generation (RAG) pipeline — embeddings, vector store, retrieval chain |

PDF assets (`emendo.pdf`, `resume.pdf`) are used as document sources for RAG experimentation.

---

### 3. `langgraph_basics/` — LangGraph Stateful Agents

Jupyter notebooks for building stateful, graph-based agent workflows with LangGraph.

| File | Content |
|------|---------|
| `rag.ipynb` | LangGraph RAG agent — nodes, edges, conditional routing, and `InMemorySaver` checkpointing |

---

### 4. `mcp_basics/` — Model Context Protocol (MCP)

A minimal but complete MCP implementation: a **FastMCP tool server** and an **LLM-powered client** that connects to it.

#### Architecture

```
┌─────────────────────────────┐        ┌──────────────────────────────────┐
│   MCP Client (client.py)    │◄──────►│  FastMCP Tool Server             │
│   MCPAgent + ChatCohere     │  HTTP  │  tools/tool_server.py            │
│   (mcp-use)                 │        │  http://127.0.0.1:8001/toolserver│
└─────────────────────────────┘        └──────────────────────────────────┘
```

#### Tool Server (`tools/tool_server.py`)

Built with **FastMCP** over `streamable-http` transport. Exposes 5 arithmetic tools:

| Tool | Description |
|------|-------------|
| `add(a, b)` | Returns `a + b` |
| `subtract(a, b)` | Returns `a - b` |
| `multiply(a, b)` | Returns `a * b` |
| `divide(a, b)` | Returns `a / b` (guards against division by zero) |
| `power(a, b)` | Returns `a ** b` |

#### MCP Client (`client.py`)

An interactive REPL powered by `mcp-use`'s `MCPAgent` and **Cohere** (`ChatCohere`). The agent reads the server config from `config/tool_server.json` and can call any registered tool based on natural language input.

#### Server Config (`config/tool_server.json`)

```json
{
  "mcpServers": {
    "tool_server": {
      "transport": "streamable-http",
      "url": "http://127.0.0.1:8001/toolserver"
    }
  }
}
```

#### Setup & Run

```bash
cd mcp_basics

# Install dependencies
uv sync

# 1. Start the MCP Tool Server (terminal 1)
uv run python tools/tool_server.py

# 2. Start the MCP Client (terminal 2)
uv run python client.py
```

**Dependencies:** `fastmcp`, `mcp-use`, `langchain-cohere`

---

### 5. `a2a_basics/` — Agent-to-Agent (A2A) Protocol

A production-style implementation of Google's **A2A (Agent-to-Agent) protocol** — an open standard for agents to discover, communicate with, and delegate tasks to other agents over HTTP.

#### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    A2A Server  (port 8024)                       │
│                                                                  │
│  ┌───────────────┐   ┌──────────────────────┐   ┌──────────────┐ │
│  │  Agent Card   │   │  DefaultRequest      │   │  InMemory    │ │
│  │  (/.well-known│   │  Handler             │   │  Task Store  │ │
│  │  /agent.json) │   │                      │   │              │ │
│  └───────────────┘   └──────────┬───────────┘   └──────────────┘ │
│                                 │                                │
│                     ┌───────────▼───────────┐                    │
│                     │ WebSearchAgentExecutor│                    │
│                     │  (agent_executor.py)  │                    │
│                     └───────────┬───────────┘                    │
│                                 │                                │
│                     ┌───────────▼──────────┐                     │
│                     │   WebsearchAgent     │                     │
│                     │  (WebSearchAgent.py) │                     │
│                     │  LangGraph ReAct +   │                     │
│                     │  Cohere command-a    │                     │
│                     │  TavilySearch tool   │                     │
│                     └──────────────────────┘                     │
└──────────────────────────────────────────────────────────────────┘
```

#### Key Components

| File | Role |
|------|------|
| `main.py` | Bootstraps the A2A server — registers `AgentCard`, `AgentSkill`, push notifications, and starts Uvicorn |
| `WebSearchAgent.py` | Core LangGraph ReAct agent with Tavily web search tool and Cohere LLM (`command-a-03-2025`) |
| `agent_executor.py` | `AgentExecutor` subclass — bridges A2A protocol events (`TaskUpdater`, `EventQueue`) to the LangGraph agent |

#### Agent Card

The server automatically exposes an Agent Card at `/.well-known/agent.json`:

```json
{
  "name": "Websearch Agent",
  "description": "Helps with searching and retrieving real-time information on any topic from the open internet using google search",
  "version": "1.0.0",
  "skills": [
    {
      "id": "web_search",
      "name": "Perform Web search",
      "tags": ["search", "web"]
    }
  ]
}
```

#### Setup & Run

```bash
cd a2a_basics

# Install dependencies
uv sync

# Set required environment variables
cp .env.example .env
# Add: COHERE_API_KEY, TAVILY_API_KEY

# Start the A2A server
uv run python main.py --host 127.0.0.1 --port 8024
```

The agent is then discoverable and callable by any A2A-compliant client or orchestrator.

**Dependencies:** `a2a-sdk`, `langgraph`, `langchain-cohere`, `langchain-tavily`, `uvicorn`

---

## 🔑 Environment Variables

| Module | Variable | Purpose |
|--------|----------|---------|
| `a2a_basics` | `COHERE_API_KEY` | Cohere LLM (`command-a-03-2025`) |
| `a2a_basics` | `TAVILY_API_KEY` | Tavily web search tool |
| `mcp_basics` | `COHERE_API_KEY` | Cohere LLM for MCP agent |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Package Manager | [uv](https://github.com/astral-sh/uv) |
| LLM | Cohere `command-a-03-2025` |
| Agent Framework | LangGraph (ReAct), LangChain |
| Web Search | Tavily Search API |
| MCP | FastMCP, mcp-use |
| A2A Protocol | a2a-sdk (Google) |
| API Server | Uvicorn / Starlette, FastAPI |

---

## 🚀 Learning Path

```
oops_basics  ──►  langchain_basics  ──►  langgraph_basics  ──►  mcp_basics  ──►  a2a_basics
   OOP               LangChain              LangGraph             MCP tools        A2A Protocol
fundamentals         & RAG basics          stateful graphs        & clients        production agent
```

---

## 📄 License

This repository is intended for educational and learning purposes.
