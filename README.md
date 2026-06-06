# 🤖 Agentic AI Basics

A hands-on learning repository covering the core building blocks of modern Agentic AI systems — from Python OOP fundamentals to production-grade A2A (Agent-to-Agent) protocols. Each module is self-contained and progressively builds toward real-world agentic architectures.

---

## 📁 Repository Structure

```
agentic-ai-basics/
├── oops_basics/          # Python OOP fundamentals for AI engineering
├── langchain_basics/     # LangChain & RAG with Jupyter notebooks
├── langgraph_basics/     # LangGraph stateful agent graphs
├── fastapi_basics/       # FastAPI microservices — Event Service + Assistant Service
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

### 2. `fastapi_basics/` — FastAPI Microservices

Two independent FastAPI services demonstrating REST API design, SQLAlchemy ORM, Pydantic v2 validation, and inter-service communication.

#### Architecture

```
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│   Assistant Service              │◄──────►│   Event Service                  │
│   assistant_service/app.py       │  HTTP  │   event_service/app.py           │
│   port 8000 (default)            │        │   port 8001 (default)            │
│   Natural-language query layer   │        │   CRUD + SQLite via SQLAlchemy   │
└──────────────────────────────────┘        └──────────────────────────────────┘
```

#### Event Service (`event_service/`)

A full CRUD REST API backed by **SQLite** via **SQLAlchemy**, with **Pydantic v2** request/response schemas.

| File | Role |
|------|------|
| `app.py` | FastAPI app — all route handlers |
| `models.py` | SQLAlchemy `Event` ORM model (`events` table) |
| `schemas.py` | Pydantic `EventCreate`, `EventUpdate`, `EventOut` schemas with validators |
| `config.py` | SQLAlchemy engine + session factory + `get_db` dependency |

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/events/` | Create a new event |
| `GET` | `/events/` | List all events (ordered by date) |
| `GET` | `/events/{id}` | Fetch a single event |
| `PUT` | `/events/change/{id}` | Update an event |
| `DELETE` | `/events/cancel/{id}` | Delete an event |
| `GET` | `/events/upcoming/` | All future events |
| `GET` | `/events/next/` | The single next upcoming event |
| `GET` | `/events/today/` | Events happening today |

**Event model fields:** `id`, `title`, `city`, `date`, `organizer`, `organizer_email`

#### Assistant Service (`assistant_service/`)

A lightweight natural-language query layer that calls the Event Service and returns plain-English answers.

| File | Role |
|------|------|
| `app.py` | FastAPI app — health check + `/assistant` GET & POST endpoints |

**Supported query patterns** (via `?q=` parameter):

| Query | Response |
|-------|----------|
| `"next event"` / `"first upcoming"` | Returns the single next upcoming event |
| `"upcoming"` / `"future events"` | Returns all future events |
| `"events in <city>"` | Filters events by city name |
| `"events on YYYY-MM-DD"` | Filters events by exact date |
| `"how many"` / `"count"` | Returns total event count |

**Environment variable:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `EVENT_SERVICE_URL` | `http://localhost:8001` | Base URL of the Event Service |

#### Setup & Run

```bash
cd fastapi_basics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies for each service
pip install -r event_service/requirement.txt
pip install -r assistant_service/requirement.txt

# 1. Start the Event Service (terminal 1)
uvicorn event_service.app:app --port 8001 --reload

# 2. Start the Assistant Service (terminal 2)
EVENT_SERVICE_URL=http://localhost:8001 uvicorn assistant_service.app:app --port 8000 --reload
```

**Interactive docs** are auto-generated at `http://localhost:8000/docs` and `http://localhost:8001/docs`.

**Dependencies:** `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic[email]`, `requests`

---

### 3. `langchain_basics/` — LangChain & RAG

Jupyter notebooks exploring LangChain's core abstractions.

| File | Content |
|------|---------|
| `main.ipynb` | LangChain chains, prompts, and LLM wrappers |
| `session.ipynb` | Retrieval-Augmented Generation (RAG) pipeline — embeddings, vector store, retrieval chain |

PDF assets (`emendo.pdf`, `resume.pdf`) are used as document sources for RAG experimentation.

---

### 4. `langgraph_basics/` — LangGraph Stateful Agents

Jupyter notebooks for building stateful, graph-based agent workflows with LangGraph.

| File | Content |
|------|---------|
| `rag.ipynb` | LangGraph RAG agent — nodes, edges, conditional routing, and `InMemorySaver` checkpointing |

---

### 5. `mcp_basics/` — Model Context Protocol (MCP)

A comprehensive MCP implementation covering all MCP primitives — **Tools**, **Resources**, **Prompts**, **Sampling**, **Elicitation**, and **Roots** — across independent FastMCP servers and feature-focused client demos.

#### Architecture

```
                        ┌─────────────────────────────────────────────────────┐
                        │                servers/                             │
                        │  tool_server.py      port 8001  /toolserver        │
                        │  resource_server.py  port 8003  /resourceserver    │
                        │  prompt_server.py    port 8004  /promptserver      │
                        └───────────────────┬─────────────────────────────────┘
                                            │  streamable-http (MCPAgent + Cohere)
          ┌─────────────────────────────────▼─────────────────────────────────┐
          │  servers/clients/                                                 │
          │  tool_client.py     ←→  tool_server.json     (port 8001)         │
          │  resource_client.py ←→  resource_server.json (port 8003)         │
          │  prompt_client.py   ←→  prompt_server.json   (port 8004)         │
          └───────────────────────────────────────────────────────────────────┘

Advanced MCP Features  (clients/ — each subfolder is self-contained)

  clients/sampling/     server.py  ←→  client.py      (port 8005)  LLM Sampling
  clients/elicitation/  server.py  ←→  client.py      (port 8006)  Elicitation
  clients/root/         root_server.py ←→ root_client.py (port 8028) Roots
```

#### File Structure

```
mcp_basics/
├── servers/
│   ├── tool_server.py         # FastMCP arithmetic tools       (port 8001)
│   ├── resource_server.py     # FastMCP resources              (port 8003)
│   ├── prompt_server.py       # FastMCP prompts                (port 8004)
│   └── clients/
│       ├── tool_client.py         # Client → tool_server
│       ├── resource_client.py     # Client → resource_server
│       └── prompt_client.py       # Client → prompt_server
├── clients/
│   ├── sampling/
│   │   ├── server.py          # FastMCP sampling server        (port 8005)
│   │   ├── client.py          # Client with sampling_callback
│   │   └── config.json
│   ├── elicitation/
│   │   ├── server.py          # FastMCP elicitation server     (port 8006)
│   │   ├── client.py          # Client with elicitation_callback
│   │   └── config.py          # (JSON config)
│   └── root/
│       ├── root_server.py     # MCPServer with Roots support   (port 8028)
│       ├── root_client.py     # Client with list_roots_callback
│       └── config.json
├── config/
│   ├── tool_server.json       # MCP config → port 8001
│   ├── resource_server.json   # MCP config → port 8003
│   └── prompt_server.json     # MCP config → port 8004
├── pyproject.toml
└── main.py
```

---

#### 🔧 Tool Server (`servers/tool_server.py`) — port 8001

Built with **FastMCP** over `streamable-http`. Exposes 5 arithmetic tools with MCP annotations (`readOnlyHint`, `idempotentHint`, etc.):

| Tool | Description |
|------|-------------|
| `add(a, b)` | Returns `a + b` |
| `subtract(a, b)` | Returns `a - b` |
| `multiply(a, b)` | Returns `a * b` |
| `divide(a, b)` | Returns `a / b` (division-by-zero guard) |
| `power(a, b)` | Returns `a ** b` |

Client: `servers/clients/tool_client.py` — interactive REPL with `ToolError` handling, conversation memory, and `clear` command.

---

#### 📦 Resource Server (`servers/resource_server.py`) — port 8003

Demonstrates all FastMCP resource types — static text, file-backed, JSON config, directory listing:

| Resource URI | Type | Description |
|---|---|---|
| `resource://greeting` | `@mcp.resource` (text) | Simple greeting string |
| `resource://notice` | `TextResource` | System maintenance notice |
| `file://app/logs/application.log` | `@mcp.resource` (async file read) | Application log file |
| `data://config` | `@mcp.resource` (JSON) | App configuration from `data/config.json` |
| `file://<readme_path>` | `FileResource` | Project README file |
| `resource://data-files` | `DirectoryResource` | Recursive listing of the `data/` directory |

Client: `servers/clients/resource_client.py` — interactive REPL that answers questions using resource content.

---

#### 💬 Prompt Server (`servers/prompt_server.py`) — port 8004

Demonstrates all FastMCP prompt return types — plain strings, `PromptMessage`, and `list[PromptMessage]`:

| Prompt | Returns | Description |
|--------|---------|-------------|
| `explain-topic(topic)` | `str` | Generates an explanation request for any topic |
| `summarize_prompt(content_uri, summary_type)` | `str` | Creates a summarization request for a resource URI |
| `generate_code_request(language, task_description)` | `PromptMessage` | Structures a code generation request |
| `roleplay_scenario(character, situation)` | `list[PromptMessage]` | Sets up a multi-turn roleplay conversation |
| `log_analysis_prompt(data_uri, analysis_type, include_charts)` | `str` | Constructs a log analysis instruction |
| `data_analysis_prompt(n_rows, columns, domain, data_description)` | `str` | Generates a professional data analysis prompt with persona, tasks, and constraints |

Client: `servers/clients/prompt_client.py` — interactive REPL that leverages prompts, resources, and tools together.

---

#### 🔁 Sampling (`clients/sampling/`) — port 8005

Demonstrates the **MCP Sampling** primitive — a server can request the client's LLM to generate a response mid-tool-execution.

**Server** (`server.py`): Exposes a `get_product` tool that uses `ctx.session.create_message()` to ask the client's LLM to classify a user query into a product category, then filters a local `product.csv` and returns matching records.

**Client** (`client.py`): Registers a `sampling_callback` that receives `CreateMessageRequestParams` from the server. It inspects model preference `hints` and routes to the appropriate LLM:

| Hint | LLM used |
|------|----------|
| `"llama"` / `"qwen"` | Ollama (`qwen2.5:1.5b`) |
| default | Cohere (`command-a-03-2025`) |

---

#### 🙋 Elicitation (`clients/elicitation/`) — port 8006

Demonstrates the **MCP Elicitation** primitive — a server can pause tool execution and request structured input from the client's user at runtime.

**Server** (`server.py`): Two tools that use `ctx.elicit()` with Pydantic schemas:

| Tool | Schema | Description |
|------|--------|-------------|
| `collect_username` | `user_name (str)` | Interactively collects the user's name |
| `search_products` | `category`, `quantity`, `unit_price` | Collects search filters, queries `product.csv` |

**Client** (`client.py`): Registers an `elicitation_callback` that introspects the JSON schema (`properties`, `anyOf`, `type`), prompts the user field-by-field with type coercion (`str`/`int`/`float`/`bool`), and returns an `ElicitResult`.

---

#### 🌳 Roots (`clients/root/`) — port 8028

Demonstrates the **MCP Roots** primitive — clients advertise accessible filesystem roots to the server, enabling context-aware tool behaviour.

**Server** (`root_server.py`): An `MCPServer` exposing a `get_workspace_info` tool that calls `ctx.list_roots()` to discover and list all workspaces declared by the client.

**Client** (`root_client.py`): Registers a `list_roots_callback` that returns a `ListRootsResult` with dynamically determined `Root` objects (URI + name).

---

#### Setup & Run

```bash
cd mcp_basics

# Install dependencies
uv sync

# ── Servers (servers/) ──────────────────────────────────────────────
uv run python servers/tool_server.py       # Terminal 1 — port 8001
uv run python servers/resource_server.py  # Terminal 2 — port 8003
uv run python servers/prompt_server.py    # Terminal 3 — port 8004

# ── Matching clients ────────────────────────────────────────────────
uv run python servers/clients/tool_client.py
uv run python servers/clients/resource_client.py
uv run python servers/clients/prompt_client.py

# ── Advanced features (clients/) — start server first, then client ──
cd clients/sampling    && uv run python server.py   # port 8005
                       && uv run python client.py

cd clients/elicitation && uv run python server.py   # port 8006
                       && uv run python client.py

cd clients/root        && uv run python root_server.py  # port 8028
                       && uv run python root_client.py
```

**Dependencies:** `fastmcp`, `mcp-use`, `langchain-cohere`, `langchain-ollama`, `aiofiles`, `pandas`, `python-dotenv`

---

### 6. `a2a_basics/` — Agent-to-Agent (A2A) Protocol

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
| `fastapi_basics` | `EVENT_SERVICE_URL` | Base URL of the Event Service (default: `http://localhost:8001`) |
| `a2a_basics` | `COHERE_API_KEY` | Cohere LLM (`command-a-03-2025`) |
| `a2a_basics` | `TAVILY_API_KEY` | Tavily web search tool |
| `mcp_basics` | `COHERE_API_KEY` | Cohere LLM for MCP agent |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Package Manager | [uv](https://github.com/astral-sh/uv) (modules 1–2, 5–6), pip/venv (fastapi_basics) |
| LLM | Cohere `command-a-03-2025` |
| Agent Framework | LangGraph (ReAct), LangChain |
| Web Search | Tavily Search API |
| REST API | FastAPI, Uvicorn |
| ORM | SQLAlchemy + SQLite |
| Validation | Pydantic v2 |
| MCP | FastMCP, mcp-use |
| A2A Protocol | a2a-sdk (Google) |

---

## 🚀 Learning Path

```
oops_basics  ──►  langchain_basics  ──►  langgraph_basics  ──►  fastapi_basics  ──►  mcp_basics  ──►  a2a_basics
   OOP               LangChain              LangGraph              FastAPI REST        MCP tools        A2A Protocol
fundamentals         & RAG basics          stateful graphs        microservices        & clients        production agent
```

---

## 📄 License

This repository is intended for educational and learning purposes.
