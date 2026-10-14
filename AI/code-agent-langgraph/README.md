# Code Agent with LangGraph

A LangGraph-based coding agent that generates source code from a task, writes the result to disk, validates it with the appropriate compiler or syntax checker, and retries generation when validation fails.

## Project Flow

```text
START
  |
  v
generator -> writer -> verifier
                         |
                  success / retry
```

The agent is implemented as a state graph:

1. `generator` sends the task to an OpenAI-compatible chat model and stores the generated code.
2. `writer` writes the generated code to the configured output path.
3. `verifier` validates the generated code according to the requested language.
4. The routing function either ends the graph or sends it back to `generator`, up to three iterations.

## Project Structure

```text
code-agent-langgraph/
├── .env                 # Local environment variables; do not commit secrets
├── output/              # Generated files
├── src/
│   ├── __init__.py
│   ├── main.py          # Graph definition and example entry point
│   ├── nodes.py         # Generation, writing, and validation nodes
│   ├── states.py        # AgentState definition
│   └── tools.py         # File-writing helper
└── test/                # Test files
```

## Requirements

- Python 3.10 or newer
- An OpenAI-compatible API endpoint
- The required Python packages installed in the active virtual environment
- Optional validation tools, depending on the target language:
  - .NET SDK for C# or .NET
  - Node.js for JavaScript
  - Go for Go
  - Java JDK for Java
  - Rust compiler for Rust

Install the main packages in the project virtual environment:

```powershell
python -m pip install langgraph langchain-openai langchain-core python-dotenv
```

## Environment Variables

Create a `.env` file in the project directory. Use placeholders for secrets and keep the file out of source control:

```env
OPENAI_API_KEY=your-api-key
ENDPOINT_URL=https://your-openai-compatible-endpoint/v1
DEPLOYMENT_MODEL_NAME=your-model-deployment
```

`ChatOpenAI` uses these values in `src/nodes.py`:

- `ENDPOINT_URL`: OpenAI-compatible API base URL
- `OPENAI_API_KEY`: API credential
- `DEPLOYMENT_MODEL_NAME`: model or deployment name

## Running the Agent

From the project directory:

```powershell
python src/main.py
```

You can also run it as a package from the workspace root:

```powershell
python -m src.main
```

The current example asks the model to generate a .NET minimal API and writes the result to:

```text
output/Program.cs
```

Edit `initial_input` in `src/main.py` to change the task, output path, or target language.

## Supported Validation

The verifier currently supports:

- Python: in-memory compilation with `compile`
- C# and .NET: temporary project creation followed by `dotnet build`
- JavaScript: syntax checking with `node -c`
- Go: `go vet`
- Java: `javac`
- Rust: `rustc`

Unknown languages skip explicit validation with a warning.

## Important Current Limitation

The current verifier returns `error_message`, while the routing function reads `success` and `error`. Because those state fields are not updated from the verifier result, retry and success routing may not behave as intended. The state contract should be aligned before relying on automatic correction loops in production.

## Security Notes

- Never commit `.env` files or API keys.
- Generated code is written to the path supplied in the graph state. Review that path before running the agent.
- Validation executes external compiler commands for some languages. Run the agent in a controlled development environment when processing untrusted prompts or generated code.
