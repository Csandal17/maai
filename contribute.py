"""
contribute.py — Maai's citizen-science contribution layer.

Turns a personal advocacy record into an anonymised pattern for the
shared dataset. Privacy by design: no verbatim text, no name, no exact
age, no location — only symptom categories, language, and month.
Contribution is always opt-in, and always AFTER she has her record.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

DATASET_PATH = Path(__file__).parent / "contributions.jsonl"


def make_contribution(record: dict, age_band: str = "not_given") -> dict:
    """Filter a full record down to the anonymised, shareable schema.

    Deliberately excludes: verbatim text, full description, exact
    timestamp (month only), and anything identifying.
    """
    return {
        "clinical_categories": [item["clinical"] for item in record["items"]],
        "n_symptoms": len(record["items"]),
        "language_of_entry": record["language_detected"],
        "age_band": age_band,
        "timestamp_month": datetime.now(timezone.utc).strftime("%Y-%m"),
    }


def save_contribution(contribution: dict) -> int:
    """Append a contribution to the dataset. Returns the new total count."""
    with open(DATASET_PATH, "a") as f:
        f.write(json.dumps(contribution) + "\n")
    with open(DATASET_PATH) as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    from chain import build_record

    test = (
        "For the past three weeks I've been absolutely wiped out by the middle of "
        "the day, and I get out of breath just going up the stairs."
    )

    record = build_record(test)
    contribution = make_contribution(record, age_band="45-54")

    print("\nFULL RECORD KEEPS (private):", list(record.keys()))
    print("\nCONTRIBUTION SHARES (anonymous):")
    print(json.dumps(contribution, indent=2))

    total = save_contribution(contribution)
    print(f"\nSaved. Dataset now holds {total} contribution(s).")
    