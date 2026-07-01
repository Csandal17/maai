"""
intake.py — Maai's intake agent.

Captures a person's symptom description in their own words and wraps it
into a structured record, preserving the verbatim text exactly as given.
This step only listens and records — no editing, no interpretation.
Interpretation happens later, in normalise().
"""

from datetime import datetime, timezone


def intake(description: str, language: str = "en") -> dict:
    """Capture a raw symptom description into a structured intake record.

    Her words are preserved verbatim — never summarised, corrected, or
    'tidied'. The record also carries provenance (language, timestamp)
    so the final advocacy record is honest about where it came from.
    """
    cleaned = description.strip()
    if not cleaned:
        raise ValueError("Empty description — nothing to record.")

    return {
        "verbatim_description": cleaned,
        "language": language,
        "captured_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    test = (
        "I keep waking up at 3am completely drenched in sweat, and I'm so "
        "exhausted during the day I can't focus. My periods have gone all "
        "over the place too."
    )

    record = intake(test)

    print("\nINTAKE RECORD\n")
    for key, value in record.items():
        print(f"  {key}: {value}")
        