# FitFindr capstone implementation plan

Implement [Shape B from the brainstorm](capstone_plan.md) in the existing CLI. When outfit generation fails, show the selected listing and explain the failure. When only fit-card generation fails, show the listing and the outfit. Keep the shared agent loop and session dictionary. Search ranking, wardrobe validation, and Flask deployment are outside this phase.

## How we will commit

Work on one step at a time. At the end of each step, I’ll show you the changed files, what I verified, any open issues, and the proposed Conventional Commit message. **I’ll ask for your explicit approval and wait before committing.** Approval applies only to that step. After the approved commit, I’ll move to the next step. Existing work and the brainstorm stay outside these commits unless you explicitly include them.

Follow `AGENTS.md` for Python style, dependency bounds, tool contracts, and course evidence. Keep provider calls in `generate.py`, state transitions in `agent.py`, and CLI output in `app.py`. Keep tests focused on behavior the existing smoke checks miss.

## 1. Define the scope and evaluation targets

- Add a capstone **The Shape** section to `README.md` with the objective and scope. Add your five criteria and reasons under a new capstone heading in `criteria.md`, preserving the earlier criteria.
- Use the brainstorm’s five scenarios as starting points: a stalled outfit request, a recoverable `429`, persistent `429`s, blank outfit text, and failure after the outfit succeeds. Decide the timeout budget and where the clock starts. Count the initial call toward the attempt limit. Set the targets before collecting scored results.
- **Verify** that each criterion has a trigger, a measurable target, a reason, and a result that another person can score from the output.

**Proposed commit** `docs: define capstone scope and acceptance criteria`

## 2. Add a repeatable failure harness

- Extend `run_eval.py` and `scenarios.py` with an opt-in capstone mode that runs the real agent and captures the existing CLI output. A proposed invocation is `python run_eval.py --capstone --tries 3 --label capstone_before`. Preserve the current Unit 4 evaluation command. Script responses at the Gemini client or transport boundary so `generate.py` still handles retries and response parsing.
- Use `vintage graphic tee under $30`, the example wardrobe, and a fresh response script per trial. Disable caching, track provider attempts per stage, and capture elapsed time and stdout. Use direct local search in the capstone harness to isolate the model cases. Record that choice and check the normal CLI search path separately.
- **Verify** all five triggers can run without credentials, with a harness-level cutoff so the existing code cannot stall the evaluation. Use a timeout-aware transport fixture with a controlled delay for timing. An exception raised immediately only exercises error reporting. Check a successful scripted run and confirm the legacy eval command still parses.

**Proposed commit** `test: add repeatable capstone failure scenarios`

## 3. Bound the Gemini calls

- In `generate.py` and `config.py`, set a transport timeout and a per-stage deadline using a monotonic clock. Count pacing, retry waits, and every provider attempt against that deadline. Keep one retry policy at the adapter boundary and check how the installed SDK handles its own retries.
- Retry a transient `429` within the agreed attempt limit and remaining budget. Honor usable retry hints and skip the wait when there is no attempt left or the hint exceeds the remaining budget. Surface timeout and exhausted rate-limit outcomes as specific `ModelUnavailable` failures. Preserve the existing auth error, successful-response caching, and usage counts.
- **Verify** a successful request, one `429` followed by success, repeated `429`s, an over-budget retry hint, and a stalled request. Check the actual attempt count and elapsed time. Use scripted checks here and reserve the scored comparison for Step 6.

**Proposed commit** `fix: bound Gemini timeouts and rate-limit retries`

## 4. Preserve and display partial results

- Treat blank provider responses as a model-stage failure. Ignore already-cached blank entries and avoid writing new ones. Make the change in the shared model path and update the tool docstrings and README inventory to describe it. Keep the existing direct fit-card behavior for callers that pass a blank outfit as input.
- In `agent.py`, identify the failed stage and preserve the existing `error` field plus any listing or outfit already stored in the session. Stop before calling the fit-card tool when the outfit fails. In `app.py`, render the fields that exist and include a short message for the missing stage.
- **Verify** that the matching query still shows all three outputs, an impossible query still stops before either model call, and an empty wardrobe still uses general styling. Check that blank outfit output triggers zero fit-card calls and that a fit-card failure shows the exact outfit produced earlier in the run.

**Proposed commit** `fix: show partial results when model stages fail`

Steps 2–4 provide the three focused commits for the spec’s build milestone.

## 5. Add structured run records and document the launch command

- Write one JSON Lines record per submitted CLI query or capstone eval trial, including early exits and caught exceptions. Include UTC timestamp, query, actual output or error summary, run duration, model-stage duration, outcome, failed stage, attempt counts, and whether the provider was live or scripted. Use one record when the eval runs through the CLI path. Keep API keys and raw provider errors out of the logs.
- Document `python app.py ask` in `RUNNING.md`, along with the exact demo command once implemented, the log location, the supported Python environment, tested dependency versions, and the Gemini key requirement. FitFindr uses a hosted model and needs no local model files.
- **Verify** that success, no-match, partial output, and an unexpected exception all produce parseable records. Check the documented launch command from a clean checkout of the approved code before final submission.

**Proposed commit** `feat: record structured FitFindr runs`

## 6. Capture the baseline and diagnose misses

- Run the completed initial extension against the five criteria three times each. Save the real output and structured records in `results/`. In the README, give each criterion a target, three trial cells, a `MET` or `MISSED` verdict, and an example output with the producing file and function.
- Diagnose each miss by naming the stage and the mechanism. Use the evidence to select one improvement. If all five pass, document which target was too easy or what limitation the evidence exposes, then choose one focused improvement before retesting. Keep the original targets for the comparison.
- **Verify** that all 15 scored trials are accounted for and that the README results can be traced to the saved output.

**Proposed commit** `test: record capstone baseline and diagnoses`

## 7. Make one improvement and rerun the comparison

- Implement the improvement selected in Step 6. Rerun the same five scenarios three times with identical fixtures, cache and search settings, and scoring rules. Save the second set of evidence and place the tables side by side in the README.
- **Verify** the affected behavior and the full 15-trial rerun. Describe what improved, what regressed, and any remaining misses based on the captured results.

**Proposed commit** `fix: <name the improvement supported by the baseline>`

## 8. Measure cost and finish the capstone write-up

- Measure ten successful live, uncached runs of the matching query. Use the difference in `generate.token_counts()` across each run and report the mean tokens per query. Multiply the mean by 100 for a day of 100 one-query users. Keep scripted demo runs out of that calculation.
- Finish **Instrumentation** with ten real records plus a failure record, **What It Costs** with the measured method and arithmetic, and **What's Still Broken** with what remains and why work stops there. Add the next priority and a new **How I Used AI** section under `## Capstone`. Keep the earlier course write-up.
- **Verify** the clean-checkout launch command, both demo cases, evidence links, and cost arithmetic. For the demo, show a `429` that recovers and a failed fit card that leaves the outfit on screen.

**Proposed commit** `docs: report capstone costs and remaining limits`

Sources: [Capstone specification](final_SPEC.md), [criteria guidance](acceptance_criteria.md), and [repository conventions](../AGENTS.md).
