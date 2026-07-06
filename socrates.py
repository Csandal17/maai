"""
socrates.py — Maai's SOCRATES annotation layer (experimental).

Takes a FINISHED advocacy record and adds a clinical-framework layer:
tags each item with the SOCRATES dimension(s) it clearly addresses, and
lists dimensions not yet described — a gap-map for the clinician to ask
into. Annotation only: normalise() is untouched, her words are untouched,
and nothing is ever inferred to fill a gap.
"""

import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

DIMENSIONS = [
    "Site", "Onset", "Character", "Radiation", "Associations",
    "Time course", "Exacerbating / relieving factors", "Severity",
]

SYSTEM_PROMPT = f"""You annotate a symptom advocacy record with the SOCRATES
clinical framework, for Maai, a women's health advocacy tool.

The SOCRATES dimensions: {", ".join(DIMENSIONS)}.

Your only job: for each record item, tag which dimension(s) her words
CLEARLY address — then list the dimensions her record does not yet touch.

Hard rules:
- Tag ONLY what her words explicitly establish. "For three weeks" clearly
  addresses Time course. "Ache in my jaw" clearly addresses Site.
- NEVER infer, guess, or stretch to fill a dimension. An untagged
  dimension is a finding, not a failure.
- NEVER add severity judgements, diagnoses, or conclusions of any kind.
- Every item gets a "dimensions" list — it may be empty.
- "not_yet_described" lists every dimension no item addressed.

Return ONLY valid JSON — no preamble, no markdown fences:
{{
  "items": [
    {{"verbatim": "...", "clinical": "...", "dimensions": ["..."]}}
  ],
  "not_yet_described": ["..."]
}}"""


def annotate_socrates(record: dict) -> dict:
    """Annotate a finished record with SOCRATES dimension tags and gaps."""
    items_text = json.dumps(record["items"], ensure_ascii=False)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": items_text}],
    )
    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.find("{"):]
    return json.loads(raw)


if __name__ == "__main__":
    from chain import build_record

    test = (
        "For the past three weeks I've been absolutely wiped out by the middle of "
        "the day, even when I've slept. I get out of breath just going up the "
        "stairs, which never used to happen. There's a dull ache in my jaw and "
        "across my upper back that comes and goes, and some days I feel sick for "
        "no reason."
    )

    result = annotate_socrates(build_record(test))

    print("\nSOCRATES ANNOTATION\n")
    for item in result["items"]:
        dims = ", ".join(item["dimensions"]) if item["dimensions"] else "—"
        print(f'  "{item["verbatim"]}"')
        print(f"     [{dims}]\n")
    print("Not yet described — the clinician may wish to ask about:")
    for dim in result["not_yet_described"]:
        print(f"  · {dim}")
        