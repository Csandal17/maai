"""
seed_data.py — generates the synthetic contribution dataset.

Creates ~80 clinically-plausible SYNTHETIC contributions so the
aggregate view can demonstrate what the citizen-science layer reveals
at scale. Honestly labelled: this is representative synthetic data,
generated from the BHF/atypical-presentation literature — never
presented as real user data.
"""

import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

DATASET_PATH = Path(__file__).parent / "contributions.jsonl"

PROMPT = """Generate exactly 80 synthetic entries for a women's cardiovascular
symptom dataset, as a JSON array. Each entry has this shape:
{"clinical_categories": [...], "n_symptoms": N, "language_of_entry": "...",
 "age_band": "...", "timestamp_month": "..."}

Ground the distribution in the documented reality of women's cardiac
presentations (BHF/atypical-presentation literature):
- Fatigue/exhaustion appears in roughly 65-70% of entries
- Dyspnoea/breathlessness in roughly 50%
- Classic chest pain in only roughly 30%
- Nausea, jaw pain, back pain, sleep disturbance, dizziness, palpitations,
  and cold sweats appear at realistic intermediate rates
- 1-5 categories per entry, clinical-register names (e.g. "atypical fatigue",
  "exertional dyspnoea", "mandibular radiation of pain")
- age_band drawn from: 25-34, 35-44, 45-54, 55-64, 65-74 (weighted to 45-64)
- language_of_entry: mostly "English", with realistic minority of "Spanish",
  "Chinese (Simplified)", "Polish", "Urdu", "Bengali"
- timestamp_month between "2026-01" and "2026-07"

Return ONLY the JSON array — no preamble, no markdown fences."""


def seed() -> int:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        messages=[{"role": "user", "content": PROMPT}],
    )
    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.find("["):]

    entries = json.loads(raw)

    # Overwrite: seed data replaces anything previous
    with open(DATASET_PATH, "w") as f:
        for entry in entries:
            entry["synthetic"] = True  # honesty flag travels with every entry
            f.write(json.dumps(entry) + "\n")

    return len(entries)


if __name__ == "__main__":
    n = seed()
    print(f"\nSeeded {n} synthetic contributions into {DATASET_PATH.name}")
    