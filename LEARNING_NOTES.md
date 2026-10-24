# Python Project Learning Notes

These notes summarize the project-structure and local-LLM concepts applied in
this project.

## 1. `uv init` and `main.py`

- Python does not require a file named `main.py`. That name is a convention,
  not a language rule.
- `uv init` behavior depends on the kind of project being initialized and the
  uv version/options. A script project can be initialized with
  `uv init --script main.py`.
- A package project commonly uses a `src/` layout instead of a root-level
  `main.py`. This project is a package project, with importable code in
  `src/simple_llm_call/`.
- For a tiny standalone script, a root-level `main.py` is reasonable. For a
  package with multiple modules and a configured command, the package layout
  used here is appropriate.

## 2. Package modules and imports

The package currently has this structure:

```text
src/simple_llm_call/
├── __init__.py
├── app.py
├── llm_client.py
└── temperature_demo.py
```

- `__init__.py` marks `simple_llm_call` as a package. It can be empty; it does
  not have to contain the application entry point or import every module.
- `app.py` coordinates the application.
- `llm_client.py` contains the shared function that configures the model and
  sends a prompt.
- `temperature_demo.py` contains the temperature comparison function.
- Modules in the same package can use relative imports, for example:
  `from .llm_client import ask_question`.
- Prefer putting executable work inside functions. Top-level code runs when a
  module is imported, which can otherwise trigger unintended API calls.

## 3. The `main()` function and the console command

`main()` is an ordinary function name, not a special Python keyword. The
project's `pyproject.toml` connects the terminal command to that function:

```toml
[project.scripts]
simple-llm-call = "simple_llm_call.app:main"
```

When you run `uv run simple-llm-call`, uv invokes
`simple_llm_call.app:main`. The function can be renamed, but the part after the
colon in `pyproject.toml` must be changed to match.

The annotation `-> None` means the function is not intended to return a value.
It can still print output and call other functions.

## 4. The root `.env` file

A common convention is to keep local environment configuration in `.env` at
the project root, alongside `pyproject.toml`, rather than inside the importable
package:

```text
simple-llm-call/
├── .env
├── pyproject.toml
└── src/
```

This project resolves the root from `app.py` and loads `.env` explicitly, so
running the command does not depend on which directory happens to be the
current working directory.

The configuration uses:

```dotenv
GEMINI_API_URL=http://<local-server-host>:8081/v1beta/models
GEMINI_MODEL=<model-name-supported-by-your-server>
```

Replace the placeholders with the local server address and a model name that
the server actually supports. Keep machine-specific `.env` files out of Git;
`.gitignore` ignores `.env` files.

## 5. Local Gemini-compatible API configuration

`llm_client.py` uses LangChain's `ChatGoogleGenerativeAI` client with the
configured local endpoint. The code expects `GEMINI_API_URL` to end in
`/v1beta/models`, removes that API path to provide the server base URL, and
lets the client construct its request URL.

The installed LangChain/Google client requires a non-empty API key value even
when a custom local endpoint is configured. The code passes `"local"` as a
placeholder; it is not a real credential and no API key is stored in `.env`.
The local server must accept that authentication behavior (for example, ignore
the placeholder key).

An error such as `Unknown model: gemini-2.5-flash` means the server does not
recognize the requested model name. Use the name shown by/configured for your
local server. The temperature demo now uses `GEMINI_MODEL` rather than
hard-coding a separate model.

## 6. Temperature comparison

`run_temperature_demo()` sends the same coffee-shop tagline prompt twice,
setting `temperature` to `0` and `1`. Temperature is a model-generation
parameter; it does not change the prompt or the API endpoint. A lower
temperature generally makes output more predictable, while a higher one can
make it more varied. Results still depend on the model and server.

Run the full application from the project root with:

```powershell
uv run simple-llm-call
```

This makes real requests to the configured local model server.
