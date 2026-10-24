# Simple LLM Call

A small Python project that sends prompts to a locally hosted, Gemini-compatible
model API using LangChain.

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- A running local model server that supports the Gemini `v1beta` API

## Configuration

Create a `.env` file in the project root, next to `pyproject.toml`:

```dotenv
GEMINI_API_URL=http://<local-server-host>:8081/v1beta/models
GEMINI_MODEL=<model-name-supported-by-your-server>
```

Replace the host and model name with values for your local server. The URL
should end in `/v1beta/models`. The `.env` file is ignored by Git.

## Run

From the project root, install the project dependencies and run the app:

```powershell
uv sync
uv run simple-llm-call
```

The app asks the model how many moons Jupiter has, repeats the question with a
short-answer system prompt, then compares a coffee-shop tagline at temperatures
`0` and `1`. Both demos use the model configured by `GEMINI_MODEL`; ensure the
model name is supported by your local server.

## Project layout

```text
src/simple_llm_call/
├── app.py              # Application entry point
├── llm_client.py       # Shared LangChain client and prompt invocation
└── temperature_demo.py # Temperature comparison
```

The `simple-llm-call` command is configured in `pyproject.toml` to run
`simple_llm_call.app:main`.