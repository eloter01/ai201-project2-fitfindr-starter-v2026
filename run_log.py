"""Structured records for local CLI queries and capstone trials."""

from datetime import datetime
import json
import os
from pathlib import Path
import sys


def write_run(
    path: Path,
    *,
    timestamp: datetime,
    query: str,
    provider: str,
    duration_seconds: float,
    session: dict | None,
    attempts: dict[str, int] | None,
    stage_seconds: dict[str, float],
    failed_stage: str | None = None,
    failure: str | None = None,
    scenario: str | None = None,
) -> None:
    """Append one record while keeping a log write failure out of the query."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    def redact(text: str | None) -> str | None:
        return text.replace(api_key, "[redacted]") if text and api_key else text

    output = None
    error = failure
    outcome = "error" if failure else "completed"
    if session is not None:
        item = session.get("selected_item")
        listing = None
        if item:
            listing = {
                "title": redact(item.get("title")),
                "price": item.get("price"),
                "platform": redact(item.get("platform")),
            }
        output = {
            "listing": listing,
            "outfit": redact(session.get("outfit_suggestion")),
            "fit_card": redact(session.get("fit_card")),
        }
        failed_stage = session.get("failed_stage") or failed_stage
        if not failure and session.get("error"):
            error = session["error"]
            outcome = "partial" if item else "no_match"

    record = {
        "timestamp": timestamp.isoformat(),
        "input": {"query": redact(query)},
        "output": output,
        "error": redact(error),
        "duration_seconds": duration_seconds,
        "stage_seconds": stage_seconds,
        "outcome": outcome,
        "failed_stage": failed_stage,
        "attempts": attempts,
        "provider": provider,
        "scenario": scenario,
    }

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as log:
            log.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        print(f"Could not write the run log at {path}.", file=sys.stderr)
