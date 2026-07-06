"""
aggregate.py — Maai's "What women are revealing" view.

Reads the contribution dataset and computes the collective picture:
which symptoms actually appear in women's patterns, across ages and
languages. Descriptive only, never predictive — show, count, reveal;
never conclude. Same restraint as the personal record.
"""

import json
from collections import Counter
from pathlib import Path

DATASET_PATH = Path(__file__).parent / "contributions.jsonl"

# Map varied clinical phrasings onto display buckets for counting
BUCKETS = {
    "fatigue": ["fatigue", "exhaustion", "malaise", "lethargy", "energy"],
    "breathlessness": ["dyspnoea", "breathless", "shortness of breath"],
    "chest pain (classic)": ["chest pain", "chest tightness", "chest pressure", "angina"],
    "nausea": ["nausea"],
    "jaw / back pain": ["jaw", "mandibular", "back", "dorsal", "interscapular"],
    "sleep disturbance": ["sleep", "insomnia"],
    "dizziness": ["dizz", "light-headed", "lightheaded", "presyncope"],
    "palpitations": ["palpitation"],
    "cold sweats": ["diaphoresis", "sweat"],
}


def load_contributions() -> list[dict]:
    if not DATASET_PATH.exists():
        return []
    with open(DATASET_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def aggregate() -> dict:
    """Compute the collective picture. Descriptive counts only."""
    entries = load_contributions()
    n = len(entries)
    if n == 0:
        return {"total": 0}

    bucket_counts = Counter()
    for e in entries:
        text = " ".join(e["clinical_categories"]).lower()
        for bucket, keywords in BUCKETS.items():
            if any(k in text for k in keywords):
                bucket_counts[bucket] += 1

    return {
        "total": n,
        "symptom_prevalence": {
            b: round(100 * c / n) for b, c in bucket_counts.most_common()
        },
        "age_bands": dict(Counter(e["age_band"] for e in entries).most_common()),
        "languages": dict(Counter(e["language_of_entry"] for e in entries).most_common()),
    }


if __name__ == "__main__":
    view = aggregate()
    print(f"\nWHAT WOMEN ARE REVEALING — {view['total']} contributed patterns\n")
    print("Symptom appears in:")
    for symptom, pct in view["symptom_prevalence"].items():
        print(f"  {pct:3d}%  {symptom}")
    print("\nAge bands:", view["age_bands"])
    print("Languages:", view["languages"])
    