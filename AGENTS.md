# FitFindr repository guide

FitFindr is a CodePath AI201 Python project. It searches 40 local mock thrift
listings, uses Google Gemini to suggest an outfit around the best match, and
writes a short caption called a fit card. The build and evaluation write-ups
are in `README.md`. See `RUNNING.md` for setup and troubleshooting. Some of its
starter notes predate the implemented tools and MCP registration.

## Architecture and contracts

- `app.py` (CLI), `serve.py` (Flask), and `run_eval.py` (evaluation) all call
  `agent.run_agent(query, wardrobe)`. Keep the agent loop shared across entry
  points.
- `agent.py` parses the query with regex, searches, selects `results[0]`,
  suggests an outfit, and generates a fit card. Parsing recognizes dollar-sign
  prices and the documented size formats. Unsupported phrases such as `under
  thirty dollars` leave the corresponding filter unset.
- The session dict is the source of truth. Write each stage's output into it
  and use that stored output for the next stage. Callers check `session["error"]`.
  An empty search sets an actionable message based on the supplied filters and
  stops before either model tool runs. The agent catches `ModelUnavailable`
  and retains search results and any other work already in the session.
- `tools.py` holds the tool implementations. Search is deterministic and local.
  It applies optional size and inclusive price filters, ranks by shared
  keywords with stable ties, and returns up to `config.SEARCH_RESULT_LIMIT`
  listing dicts. No matches return `[]`. Size matching uses whole options
  separated by `/`, strips parentheticals, and lets One Size pass any filter.
- `suggest_outfit` uses the wardrobe when it has items and asks for general
  styling advice when it is empty. `create_fit_card` uses the outfit and the
  same listing. Both tools reject a missing or empty listing dict and return
  fallback strings when Gemini sends blank text. The fit-card tool skips its
  model call when given blank outfit input.
- `utils/data_loader.py` is the shared access point for `data/listings.json`
  and `data/wardrobe_schema.json`. Use its wardrobe helpers to strip note
  keys and get the common `{"items": [...]}` shape. Listing `brand` and
  wardrobe item `notes` can be `None`.
- `mcp_server.py` registers only `search_listings` with FastMCP and delegates
  to `tools.search_listings`. Keep its typed schema and results aligned with
  the direct tool. `mcp_client.py` starts a stdio subprocess per call and
  unwraps the result. `agent._search()` silently falls back to the direct tool
  on MCP exceptions. The trace labels either path `search_listings (via MCP)`,
  so use the MCP client command to check registration separately.
- `generate.py` is the shared Gemini adapter for the application. It paces
  requests, retries rate limits, caches responses in `.cache/`, and records
  process-level call and token counts. Each model stage has a time budget and
  a cap on attempts. Timeouts and rate limits raise `ModelUnavailable`
  subclasses the agent can catch.
  `config.py` loads `.env`, configures Windows console UTF-8, and holds model,
  cache, pacing, and iteration settings. `AI201_MODEL` overrides the configured
  model and `AI201_CACHE=0` bypasses the cache.
- `trace.py` records the loop steps and enforces the iteration cap. It uses
  process-level state and prints steps to the console. The CLI's `--trace`
  path and the evaluation harness reset the trace before a run.
- `serve.py` exposes `GET /health` and `POST /ask`. The latter accepts JSON
  with a `query` and an optional `wardrobe` dict, and returns the session.
  The server serializes agent runs within a process. Use the default sync
  Gunicorn worker for hosted runs (`gunicorn serve:app`). The MCP client uses
  `asyncio.run()` and needs a synchronous entry point.

## Development conventions

- Follow PEP 8. Prefer small functions, descriptive names, typed signatures,
  and short docstrings for public contracts. Use comments to explain why a
  rule exists. Prefer explicit input checks, specific exceptions, and context
  managers for resources. Preserve intentional exception boundaries when
  editing existing code.
- Keep changes focused and independently reviewable. Use Conventional Commits
  when asked to commit. Treat course scaffolding as shared infrastructure and
  edit it when the task calls for it. Keep the README's tool inventory aligned
  with changes to tool contracts.
- Use Python 3.11–3.13 and install the version ranges in `requirements.txt`
  without loosening their bounds. Store `GEMINI_API_KEY` in the ignored `.env`
  created from `.env.example`. Keep keys out of code, logs, and commits.
- `criteria.md`, `README.md`, and `results/` hold course evidence. Preserve
  existing criteria and record revisions below the original with a reason.
  Use real text output from runs for evidence. Keep `results/` tracked and
  preserve commit history. `.github/MAINTAINERS.md` covers the upstream
  starter's grading hash baseline.

## Commands and verification

Run from the repository root. Create a virtual environment with
`python -m venv .venv` using a supported interpreter. Activate it with
`.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate`
on macOS/Linux, then run `python -m pip install -r requirements.txt`.
Use single quotes around queries so the shell preserves dollar signs.

| Command | Purpose |
| --- | --- |
| `python app.py fields` | Inspect the listing and wardrobe fields locally. |
| `python app.py listings --full -n 6` | Browse full mock listings. |
| `python app.py examples` | List sample queries. |
| `python mcp_client.py` | Start the local MCP subprocess and list its tools. `python mcp_server.py` starts the stdio server and waits for a client. |
| `python app.py ask 'designer ballgown size XXS under $5' --trace` | Check the empty-search branch without Gemini. |
| `python app.py ask 'vintage graphic tee under $30' --trace` | Exercise the full loop. Add `--empty-wardrobe` to exercise general styling advice. |
| `python agent.py` | Run the matching and impossible examples directly. |
| `python test.py` | Check the environment, dependencies, fixtures, and one live Gemini call. |
| `python run_eval.py --label before` | Run the evaluation scenarios and write a timestamped Markdown report in `results/`. Use `--tries N` to override the default of five. |
| `python serve.py` | Start Flask locally on `PORT`, default `5000`. |

There is no configured pytest suite or linter. The tool docstrings include
standalone smoke commands. `run_eval.py` disables the cache, captures sessions,
traces, and crashes, and leaves scoring to the reviewer. In `scenarios.py`, use
`example` or `empty` for `wardrobe` and match `criterion` to `criteria.md`.
Use `None` for a diagnostic scenario. `--label` names the report and does not
change which scenarios run or inject failures. Matching eval scenarios make
live Gemini calls.
