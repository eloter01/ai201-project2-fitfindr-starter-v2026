# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

act as an expert Python developer who writes clean, readable, and production-ready code. When writing Python code for me, you must strictly follow these software engineering principles:
1. Code Readability & Style
	* Follow PEP 8 guidelines strictly (naming conventions, spacing, line lengths).
	* Use descriptive, intention-revealing variable and function names.
	* Keep functions small, focused, and limited to a single responsibility.
2. Defensive Programming & Error Handling
	* Use specific exception handling (e.g., except ValueError, except FileNotFoundError) instead of a catch-all 'except Exception:'.
	* Use the "Look Before You Leap" (LBYL) or "Easier to Ask for Forgiveness than Permission" (EAFP) paradigms appropriately based on the context.
	* Implement explicit validation for function arguments (e.g., checking for None, empty bounds, or invalid types) before processing.
	* Use type hinting for function signatures to improve clarity.
3. Minimal & Meaningful Documentation
	* Do NOT write obvious comments that repeat what the code does (e.g., avoid # increment x by 1).
	* Only use comments to explain the "Why", not the "What" (e.g., complex algorithms, business logic rules, or non-obvious workarounds).
	* Include concise docstrings for functions detailing their purpose, parameters, and return values.
4. Modern Pythonic Practices
	* Use contextual managers (with statements) for resource management (files, network connections).
	* Leverage modern features like f-strings, list comprehensions (where readable), and the pathlib module where appropriate.
5. Incremental & Committable Deliveries
	* Do not implement the entire feature or fix all issues at once. Break the task down into small, independent, logical steps.
	* Present exactly ONE committable change at a time. A change is "committable" if it leaves the codebase in a working state with its own specific focus (e.g., adding a validation layer, implementing a single helper function, refactoring one block).
	* Provide the code for this step, along with a suggested Git commit message following Conventional Commits (e.g., "feat: add input validation for user email").
	* Pause and wait for my approval or feedback before providing the next step.
6. Scope Discipline
* Build only what the current spec section asks for. Later sections often change earlier assumptions, so code written ahead of the spec usually ends up being undone.
* Don't add features, parameters, config options, or abstractions the current section doesn't need, even if they look like obvious next steps. Sections 1 to 4 govern how you write what's in scope, not whether to expand it.
* The current spec is docs/SPEC_phase_2.md (Unit 4). docs/SPEC.md is the Unit 3 spec and still applies, since Unit 4 builds on the same repo. Use them so your design choices don't conflict with later sections, but don't write code that only a later section needs.
* If something in the current section is ambiguous, ask before implementing. For small gaps the spec doesn't cover, choose the simplest option and list it under "Assumptions" in your response.
* If something outside the current scope seems worth adding, suggest it in one line at the end instead of implementing it.
7. Prose writing
* any written prose must be written in simple language, equivalent to how the average college student would write. stay to the point, avoid overly verbose writing.

---

## About this repo

FitFindr is a CodePath AI201 course project. A user asks for a thrifted item in
plain language ("vintage graphic tee under $30, size M"). The agent searches 40
mock listings, suggests outfits using the user's wardrobe, and writes a short
caption to post (a "fit card"). The project spans Unit 3 (build the tools and
the loop) and Unit 4 (MCP, tracing, evaluation). `serve.py` is for Unit 9.

The model is Google Gemini through `google-genai`, not Claude. The key is
`GEMINI_API_KEY` in `.env`. `AI201_MODEL` overrides the model name.

**The student builds:** `tools.py`, `agent.py` (`parse_query`, `run_agent`),
`mcp_server.py` and `scenarios.py` (Unit 4), `criteria.md`, and `README.md`
(the graded submission). The Unit 3 parts are done.

**Given by the starter, leave alone unless asked:** `generate.py`, `trace.py`,
`mcp_client.py`, `app.py`, `run_eval.py`, `serve.py`, `test.py`,
`utils/data_loader.py`, `RUNNING.md`.

## Commands

Python 3.11 to 3.13 only (not 3.14). Activate the venv first:
`.venv\Scripts\Activate.ps1` (PowerShell) or `source .venv/bin/activate`.

```
python test.py                               # environment check, makes one real model call
python app.py fields                         # fields on a listing and a wardrobe item
python app.py listings --full -n 6           # read whole listings
python app.py ask 'vintage graphic tee under $30'   # run the agent once
python app.py ask '...' --trace              # print trace.step() output
python app.py ask '...' --empty-wardrobe     # run with an empty wardrobe
python agent.py                              # runs one matching and one impossible query
python mcp_server.py                         # Unit 4: start the MCP server (it just waits)
python mcp_client.py                         # Unit 4: list the tools the server offers
python run_eval.py --label before            # Unit 4: 5 tries per scenario, cache off
python run_eval.py --label after             # Unit 4: same run after the one improvement
python run_eval.py --tries 10                # more tries per scenario
python serve.py                              # Unit 9: Flask on $PORT, default 5000
```

There is no pytest suite and no linter config. Each tool is tested on its own
with a one-line command (these come from the `tools.py` docstrings):

```
python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
```

Always put queries in **single quotes**. In PowerShell, `"under $30"` in double
quotes silently becomes `"under "`, so the search runs with no price limit and
no error.

## Architecture

Flow: `app.py ask`, `serve.py` (`POST /ask`), and `run_eval.py` all call
`agent.run_agent(query, wardrobe)`. That calls the tools in `tools.py`. Tools
read data through `utils/data_loader.py` and call the model through
`generate.generate()`.

- **Loop order** in `run_agent`: `parse_query`, search, the branch,
  `select_item` (always `results[0]`), `suggest_outfit`, `create_fit_card`.
  Each step calls `trace.check_iterations(steps)` first (the stop condition,
  `config.MAX_ITERATIONS`) and `trace.step(...)` after.
- **Session dict** (`agent.new_session`) is the single source of truth for a
  run. Write each tool's result into the session, then read the next tool's
  input back out of it. Don't pass return values straight from one call to the
  next, because the state criterion checks the session. Callers check
  `session["error"]` first. When it is set, the later fields stay `None`.
- **`parse_query`** uses regex, not the model, on purpose: it's free, gives
  the same answer every time (the state criterion depends on that), and its
  mistakes are easy to read. It finds prices like `under $30` or `$30`, and
  sizes `XXS` to `XXL`, `US 8.5` or `W30` after the word "size", or a bare
  size after a final comma (`..., M`). Phrasing it doesn't know, like
  "nothing over thirty dollars", gives no price, and the run ignores the
  ceiling with no error. The README lists this as a limit.
- **The branch** is the graded part of Unit 3. If the search returns `[]`,
  `_nothing_found_message` puts a message in `session["error"]` that names
  only the filters the user actually set and what to change ("No results" is
  not enough). Then `run_agent` returns without calling `suggest_outfit`.
- **Tool contracts** (from the `tools.py` docstrings):
  - `search_listings(description, size, max_price) -> list[dict]`: best match
    first, at most `config.SEARCH_RESULT_LIMIT`. Returns `[]` on no match,
    never `None` and never an exception. It scores by how many query words
    appear in a listing's title, description, category, style_tags and
    colors. Stopwords and one-letter words are skipped, score 0 is dropped,
    and ties keep the file order.
  - `suggest_outfit(new_item, wardrobe) -> str`: never empty. An empty or
    missing wardrobe gets general styling advice.
  - `create_fit_card(outfit, new_item) -> str`: a 2 to 4 sentence caption
    that names the item, price and platform once each. An empty or
    whitespace `outfit` returns a message instead of raising.
  - Both model tools raise `ValueError` if `new_item` isn't a non-empty dict,
    and return a fixed fallback message if the model sends back nothing.
- **`generate.py`** is the only module that calls the model. It paces to 15
  requests a minute, retries on 429s, caches answers in `.cache/` (keyed on
  model, system prompt, prompt and temperature), and raises `QuotaGuard` after
  300 calls in one process. Bad keys and network failures raise
  `ModelUnavailable` with a readable message. `run_agent` catches it, keeps
  the search results, and sets an error telling the user to check
  `GEMINI_API_KEY`. A query that's already cached never calls the model, so
  testing a bad key needs a new query or `AI201_CACHE=0`.
- **`config.py`** must be imported by every entry point. It loads `.env` and
  switches the Windows console to UTF-8, since fit cards often contain emoji.
  If fit cards come out word-for-word the same, check `CACHE_ENABLED` (turn it
  off with `AI201_CACHE=0`) and `TEMPERATURE` (0.9). `run_eval.py` turns the
  cache off by itself.
- **MCP (Unit 4)**: only `search_listings` moves to MCP. `mcp_server.py`
  imports the real function as `_search_listings_impl` so the registered
  `search_listings` tool doesn't call itself. FastMCP builds the input schema
  from the type hints. The client side is already wired: `agent._search()`
  calls `mcp_client.call_tool("search_listings", {...})`, which starts the
  server over stdio on every call and unwraps the result back into a list of
  dicts. The return value must be the same as the direct call.
- **Silent MCP fallback**: if `call_tool` raises anything, `_search()` falls
  back to calling `search_listings` directly, with no message. The trace step
  is still named `search_listings (via MCP)` either way, so the trace alone
  doesn't prove MCP ran. While the tool block in `mcp_server.py` is still
  commented out, every run uses the fallback. Check with
  `python mcp_client.py` that the tool is listed.
- **Trace (Unit 4)**: `run_agent` already has one `trace.step(name,
  inputs=..., returned=..., note=...)` per loop step. `app.py --trace` and
  `run_eval.py` call `start_trace()` and `get_trace()` themselves.
- **`run_eval.py`** runs every entry in `scenarios.SCENARIOS` with the cache
  off and writes `results/run_<date>_<time>_<label>.md`. It doesn't score
  anything: the Try and Verdict columns come out blank for the student to
  fill in. Each scenario's `"criterion"` must match a number in
  `criteria.md` (`None` marks a diagnostic row), and `"wardrobe"` must be
  `"example"` or `"empty"`. `scenarios.validate()` checks this before a run.
- **`serve.py` (Unit 9)**: the same `run_agent` behind Flask, one request at a
  time under a lock. It must run as `gunicorn serve:app` with the default sync
  worker. `mcp_client` uses `asyncio.run()`, which breaks under
  gevent, eventlet or uvicorn workers.

## Data gotchas

- Load data with `load_listings()`, `get_example_wardrobe()` and
  `get_empty_wardrobe()` instead of reading `data/` directly. The loader drops
  the `_`-prefixed note keys from wardrobes.
- Listing fields: `id`, `title`, `description`, `category`, `style_tags`
  (list), `size`, `condition`, `price` (float), `colors` (list), `brand`
  (str or `None`, only 8 of 40 have one), `platform` (depop, thredUp,
  poshmark). Don't build prompts that assume `brand` is set. The current
  prompts leave it out.
- Sizes come in mixed formats: `S/M`, `M/L`, `XL (oversized)`,
  `One Size / Oversized`, `US 8.5`, `W30 L30`. A plain substring check gives
  wrong matches (`"s" in "us 9"`, `"l" in "xl"`). The chosen rule is in
  `tools._size_matches` and written up under "How sizes match" in the README
  Tool Inventory, so change both together. One Size passes any filter.
  Otherwise parentheses are dropped, the size is split on `/`, and one shared
  option is a match, so `M` matches `S/M` but `L` doesn't match `XL`, `US 8`
  doesn't match `US 8.5`, and `W30` doesn't match `W30 L30`.
- In `app.py`'s `EXAMPLE_QUERIES`, every query matches some listing except
  `designer ballgown size XXS under $5`, which tests the empty-search branch.

## Course rules that affect the work

- `docs/SPEC_phase_2.md` is the Unit 4 brief and the current one.
  `docs/SPEC.md` is the Unit 3 brief. Unit 4 adds to the same repo, so both
  still apply. `SPEC.md` points to `docs/acceptance_criteria.md`, which
  doesn't exist. That guidance is at the bottom of `SPEC.md` instead.
- Unit 4 allows only two changes to the agent: the MCP move and one
  improvement. Everything else stays the same, so the before and after runs
  can be compared.
- `criteria.md`: the student writes criteria 3 to 5 and the reasons for all
  five. The brief says a model must not write them, so only critique them when
  asked. In Unit 4, never edit or delete an original criterion. Add any
  revision underneath it.
- `README.md` is graded. Sample Run, Run Log and Loop Trace must be real
  output pasted as text, so never make up output. The Planning Loop section
  must name a real `file::function` (`agent.py::run_agent`).
- The commit history is graded (at least 4 new commits per unit) and shows the
  criteria came before the results. Don't rewrite or squash history, force
  push, or recreate the repo. `results/` is committed on purpose.
- `requirements.txt` pins upper bounds on purpose. Don't upgrade packages.
- A few starter files use `except Exception:  # noqa: BLE001` on purpose, so
  students see a message instead of a traceback. Leave those alone. Rule 2
  above applies to new code.
