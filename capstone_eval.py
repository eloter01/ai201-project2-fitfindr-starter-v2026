"""Run a CLI query against scripted Gemini HTTP responses in a subprocess."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch

from scenarios import CAPSTONE_SCENARIOS


TRIAL_TIMEOUT_SECONDS = 45
SLOW_RESPONSE_SECONDS = 9
OUTFIT = "Pair the tee with straight-leg jeans and white sneakers."
FIT_CARD = "Straight-leg jeans and sneakers keep it casual. The tee was $18 on depop."


def run_trial(scenario_id: str) -> dict:
    """Capture CLI output and trial metrics with an independent wall-clock cutoff."""
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [sys.executable, "-u", str(Path(__file__).resolve()), scenario_id],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=TRIAL_TIMEOUT_SECONDS,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "crashed": f"Trial exceeded the {TRIAL_TIMEOUT_SECONDS}-second harness cutoff.",
            "stdout": (exc.stdout or b"").decode("utf-8", errors="replace"),
            "stderr": (exc.stderr or b"").decode("utf-8", errors="replace"),
            "wall_seconds": time.monotonic() - started,
        }

    stdout = completed.stdout
    if completed.returncode:
        record = {"crashed": f"Trial process exited with code {completed.returncode}."}
    else:
        # The worker writes its metadata after the unmodified CLI transcript.
        transcript, _, metadata = stdout.rstrip("\n").rpartition("\n")
        try:
            record = json.loads(metadata)
        except json.JSONDecodeError:
            record = {"crashed": "Trial process did not return valid metadata."}
        else:
            stdout = transcript

    return {
        **record,
        "stdout": stdout,
        "stderr": completed.stderr,
        "wall_seconds": time.monotonic() - started,
    }


def _run_worker(scenario_id: str) -> dict:
    """Install the offline transport, then use the same single-query CLI path."""
    import httpx
    from google import genai
    from google.genai.types import HttpOptions

    import agent
    import app
    import config
    from utils.data_loader import get_example_wardrobe

    config.CACHE_ENABLED = False
    attempts = {"outfit": 0, "fit_card": 0}
    stage_seconds = {}
    stage = ""
    failed_stage = None

    def measure(name, tool):
        def call(*args):
            nonlocal stage, failed_stage
            stage = name
            started = time.monotonic()
            try:
                return tool(*args)
            except Exception:
                failed_stage = name
                raise
            finally:
                stage_seconds[name] = time.monotonic() - started

        return call

    def search_locally(parsed):
        return agent.search_listings(**parsed)

    def respond(request: httpx.Request) -> httpx.Response:
        attempts[stage] += 1
        if stage == "outfit":
            if scenario_id == "outfit-timeout":
                # MockTransport does not enforce socket timeouts itself. Use
                # the read timeout the real SDK passed to the HTTP request.
                read_timeout = request.extensions.get("timeout", {}).get("read")
                if read_timeout is not None and read_timeout < SLOW_RESPONSE_SECONDS:
                    time.sleep(read_timeout)
                    raise httpx.ReadTimeout(
                        "Scripted outfit response stalled.", request=request
                    )
                time.sleep(SLOW_RESPONSE_SECONDS)
            if scenario_id == "rate-limited" or (
                scenario_id == "retry-once" and attempts[stage] == 1
            ):
                return httpx.Response(429, json={"error": {
                    "code": 429, "status": "RESOURCE_EXHAUSTED", "message": "Please retry in 0.1s",
                }})
            text = "   " if scenario_id == "blank-outfit" else OUTFIT
        else:
            if scenario_id == "fit-card-failure":
                return httpx.Response(400, json={"error": {
                    "code": 400, "status": "INVALID_ARGUMENT", "message": "Scripted caption rejection",
                }})
            text = FIT_CARD

        return httpx.Response(200, json={"candidates": [{
            "content": {"role": "model", "parts": [{"text": text}]},
        }]})

    live_client_factory = genai.Client

    def offline_client(*, http_options=None, **kwargs):
        options = HttpOptions.model_validate(http_options or {})
        options = options.model_copy(update={"httpx_client": http_client})
        kwargs.update(http_options=options, vertexai=False)
        return live_client_factory(**kwargs)

    session = None
    crashed = None
    with (
        httpx.Client(transport=httpx.MockTransport(respond), trust_env=False) as http_client,
        patch.dict(os.environ, {"GEMINI_API_KEY": "scripted-capstone-key"}),
        patch.object(genai, "Client", offline_client),
        patch.object(agent, "_search", search_locally),
        patch.object(agent, "suggest_outfit", measure("outfit", agent.suggest_outfit)),
        patch.object(agent, "create_fit_card", measure("fit_card", agent.create_fit_card)),
    ):
        try:
            query = CAPSTONE_SCENARIOS[scenario_id]["query"]
            # The parent records the trial, even if this worker is killed.
            session = app._ask_one(
                query, get_example_wardrobe(), use_trace=True, log_run=False
            )
        except Exception as exc:  # noqa: BLE001 — a crashed trial is evidence
            crashed = f"Unexpected query error ({type(exc).__name__})."

    return {
        "session": session,
        "crashed": crashed,
        "attempts": attempts,
        "stage_seconds": stage_seconds,
        "failed_stage": failed_stage,
    }


if __name__ == "__main__":
    print(json.dumps(_run_worker(sys.argv[1])))
