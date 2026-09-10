# AI Learning Projects

This folder contains practical Python experiments for building applications with LLMs, LangGraph, vector databases, graph databases, retrieval-augmented generation, and voice interfaces.

The projects are intentionally separated by topic. Each project may have its own `.env` file and runtime dependencies.

## Projects

### `Day1`

Introductory API examples:

- `01_encoding.py`: encoding-related learning example
- `open_ai_client/azureopenai.py`: OpenAI-compatible Azure endpoint usage
- `open_ai_client/gemini_api.py`: Gemini API usage
- `open_ai_client/gemini_api_using_openai_sdk.py`: Gemini through the OpenAI SDK interface
- `open_ai_client/weather_openapi.py`: weather tool or OpenAPI experiment
- `open_ai_client/main.py`: client example entry point

Run an individual example from the `AI` directory, for example:

```powershell
python .\Day1\open_ai_client\azureopenai.py
```

### `FastAPI`

A small FastAPI server example.

```powershell
python .\FastAPI\server.py
```

### `langgraph`

LangGraph conversation examples:

- `chat.py` and `chat1.py`: basic state-graph examples
- `chat_checkpoint.py`: conversational state persistence using the remote Neo4j database
- `docker-compose.yml`: local Neo4j configuration for development, if needed

The checkpoint example reads `NEO4J_URI` or `NEO4J_URL`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD`. It currently loads the shared values from `memory_agent/.env` when a local LangGraph `.env` is not present.

Run it from the `AI` directory:

```powershell
python .\langgraph\chat_checkpoint.py
```

### `memory_agent`

A conversational memory application using:

- Mem0 for memory management
- An OpenAI-compatible LLM and embedding endpoint
- Qdrant for vector storage
- Neo4j for graph storage in `memory-graph-db.py`

The Docker Compose file starts a local Qdrant service:

```powershell
docker compose -f .\memory_agent\docker-compose.yml up -d
```

Run the graph-memory example with:

```powershell
python .\memory_agent\memory-graph-db.py
```

### `rag`

A retrieval-augmented generation indexing experiment. `index.py` loads a PDF, splits it into overlapping chunks, creates embeddings, and stores them in a Qdrant collection named `Learning_rag`.

The script expects a PDF named `gsp.pdf` in the `rag` directory and a running Qdrant instance:

```powershell
docker compose -f .\rag\docker-compose.yml up -d
python .\rag\index.py
```

### `voice_agent`

A microphone-based voice assistant that:

1. Captures audio from the default microphone.
2. Converts speech to text with Google speech recognition.
3. Sends the transcript to an OpenAI-compatible chat endpoint.
4. Reads the response aloud with `pyttsx3`.

Run it with:

```powershell
python .\voice_agent\main.py
```

A working microphone, audio drivers, and speech-recognition dependencies are required.

### `code-agent-langgraph`

A LangGraph coding agent that generates source code, writes it to `output/`, and validates it with language-specific tools.

See the dedicated [code-agent-langgraph README](code-agent-langgraph/README.md) for its workflow, supported validators, setup, and current limitations.

## Shared Configuration

Most projects use an OpenAI-compatible endpoint and load configuration through `python-dotenv`:

```env
OPENAI_API_KEY=your-api-key
ENDPOINT_URL=https://your-openai-compatible-endpoint/v1
DEPLOYMENT_MODEL_NAME=your-model-deployment
```

Additional variables used by specific projects include:

```env
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=your-username
NEO4J_PASSWORD=your-password
QDRANT_URL=http://localhost:6333
```

Create the required `.env` file in the project directory that loads it. Do not commit API keys, database passwords, or other secrets.

## Environment Setup

From the repository root, create or activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the packages required by the examples. The repository contains requirement files at the workspace and `AI` levels, but some projects also need their integration packages installed separately as their experiments evolve.

```powershell
python -m pip install -r .\AI\requirement.txt
```

Common additional packages used by these projects include:

```powershell
python -m pip install python-dotenv openai langgraph langchain-openai langchain-core neo4j langgraph-checkpoint-neo4j qdrant-client langchain-qdrant langchain-community langchain-text-splitters mem0ai SpeechRecognition pyttsx3 fastapi uvicorn
```

Install only the packages needed for the example you are running when possible.

## Services

Some examples require external services:

- Qdrant: used by `memory_agent` and `rag`; Docker Compose files are provided.
- Neo4j: used by the LangGraph checkpoint example and the Mem0 graph store. The LangGraph checkpoint example is configured for the remote Neo4j instance specified by environment variables.
- Microphone and audio support: required by `voice_agent`.

## Security and Operational Notes

- Never commit `.env` files or expose their contents in logs.
- Rotate any credentials that have been accidentally shared or committed.
- Review generated code before executing it.
- Generated code and uploaded documents may contain sensitive information; use appropriate local storage and access controls.
- Stop Docker services when they are no longer needed:

```powershell
docker compose -f .\memory_agent\docker-compose.yml down
docker compose -f .\rag\docker-compose.yml down
```
