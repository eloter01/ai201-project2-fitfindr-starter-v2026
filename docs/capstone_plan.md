# FitFindr capstone brainstorm

## Shape B | Harden against failure

**Keep the listing when Gemini fails. Keep the outfit when only the fit card fails.** This gives the demo a clear outcome people can see in the existing CLI. The extension covers the two Gemini stages and what FitFindr displays when either one stops. Search ranking, wardrobe validation, and Flask deployment are out of scope for this proposal.

`generate.py` already retries rate limits, but throws a `RuntimeError` if it runs out of attempts. `agent.py` catches `ModelUnavailable` and retains earlier results in the session, but `app.py` prints only the error on that path. In `tools.py`, blank outfit text becomes a fallback string that the agent can feed to the fit-card generator as if it were a real outfit. The existing invalid-key evaluation is useful as a regression check. A new demo should show temporary failure recovery and usable partial results.

## Five scenarios to consider

Use these prompts to write your own five criteria in a new capstone section of `criteria.md`. Set the targets and their reasons before collecting the scored baseline. Three out of three is a sensible target for each scripted fault because the trigger and expected behavior are deterministic.

| Trigger | What to look for |
| --- | --- |
| Outfit request stalls | The outfit stage returns within the chosen time budget, and the CLI displays the listing and a timeout message. |
| First outfit attempt returns `429`, next attempt succeeds | Exactly one outfit retry appears in the evidence, and the CLI displays a fit card. |
| Outfit requests keep returning `429` | The CLI displays the listing and a rate-limit message after at most three attempts, including the initial attempt. |
| Outfit response contains only whitespace | A message says the outfit is unavailable, and the harness records zero fit-card requests. |
| Outfit succeeds and the fit-card request fails | The CLI displays the listing and the original generated outfit, with a message that the fit card is unavailable. |

For the timeout scenario, define the clock before testing. For example, propose an eight-second model-stage budget from the start of outfit generation until control returns, including pacing and retry waits. Measure that interval with a monotonic clock. If you also score when the message reaches the CLI, time it separately from the same starting point and document the allowed margin for rendering. Keep search and process startup outside the model-stage measurement.

## Small implementation path

1. **Make the failures repeatable.** Add scripted provider responses to the existing evaluation flow. Inject at the model client or transport boundary so the actual adapter's timeout, retry, and blank-response handling runs. Reuse the CLI rendering path so the evidence includes what users see. Use `vintage graphic tee under $30`, the example wardrobe, and a fresh script per trial with caching disabled. Keep the search path identical across the comparisons. If MCP stalls in the test environment, explicitly use direct local search in both sets and check normal MCP separately.
2. **Bound the model calls.** Put the transport timeout and retry limit in `generate.py`. Count the initial call toward the attempt cap. Include local pacing and backoff in the stage budget. If the service asks for a delay longer than the remaining budget, report the rate limit. Avoid a final sleep when there is no attempt left. Keep blank model text out of the cache and handle already-cached blank text at the same boundary.
3. **Show the partial result.** Have `agent.py` record the stage and reason for the stop while preserving the session fields that succeeded. Route blank outfit text into the failure path before caption generation. Have `app.py` display any listing or outfit in the session alongside the stage-specific message. Keep successful queries and the existing no-match branch as regression checks.

For the live demo, show a single `429` that recovers and a failed fit card that leaves the listing and outfit visible. Use a short scripted retry delay. For the timeout evidence, use a controlled slow response at the timeout boundary and time it. An immediately raised timeout exception checks the message path, while a slow response exercises the wait limit. Record the fault mode in the run log so readers can tell which calls were scripted.

## Evaluation and submission

- **Order the work.** Agree on criteria before collecting results. A run against today's code is useful as a starting snapshot. For the required comparison, build the first version of the extension, run all five criteria three times each, and diagnose the misses. Pick one improvement from those results and rerun the identical 15 trials. For example, if an attempt begins just before the stage deadline and runs past it, limit that attempt's transport timeout to the time remaining. Split the initial build into at least three focused commits, as Milestone 2 asks.
- **Record real runs.** Use one JSON Lines record per run with a timestamp, query, output or error, duration, outcome, failed stage, attempt counts, and fault mode. Write a record on early returns and exceptions too. Save the actual CLI output and records in `results/`. In the README, show the before and after tables side by side with three trial columns and a `MET` or `MISSED` verdict for each criterion. Include actual output for each criterion, the producing file and function, and the code stage and mechanism behind each miss.
- **Make it runnable.** Document a single launch command in `RUNNING.md` and verify it from a clean checkout. The likely normal command is `python app.py ask`; document the scripted demo separately. List the Python version used, the tested dependency versions, and the Gemini key requirement. FitFindr uses a hosted model, so it needs no local model files.
- **Measure cost separately.** Run ten live, uncached successful queries and take the mean of the per-run Gemini token counts. Use the difference in `generate.token_counts()` before and after each run. Report the mean and multiply it by 100 for the daily total if 100 people each run one query. Leave scripted provider responses out of the live token measurement.
- **Finish the capstone write-up.** Add **The Shape**, **Instrumentation**, **What It Costs**, **What's Still Broken**, and a new **How I Used AI** under `## Capstone` in `README.md`. Include at least ten actual log entries plus a failure example, the run tables and diagnoses, and what you would tackle next. Preserve the earlier project write-up and criteria.

Source: [Capstone specification](final_SPEC.md) and [acceptance criteria guidance](acceptance_criteria.md).
