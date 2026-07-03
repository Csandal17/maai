"""
normalise.py — Maai's hero agent.

Maps a person's own words describing symptoms to clinical terminology,
keeping BOTH, so nothing they said is erased. Language mapping only —
never a diagnosis. The clinician interprets; Maai helps them be heard.
"""

import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = """You are a clinical language normaliser for Maai, a women's health advocacy tool.

Your only job: map a person's own words describing their symptoms to recognised clinical terminology, so a clinician can understand them more easily.

Hard rules:
- NEVER replace the person's words. Always keep their exact phrase (verbatim) alongside the clinical term.
- NEVER diagnose, name conditions, judge severity, or draw conclusions. You map language only — the clinician interprets.
- If the input is not in English, map to English clinical terms but keep the verbatim phrase exactly as written, in its original language.
- Only map what is actually stated. Never infer symptoms that were not described.
- Represent EVERY part of what she said. Never omit, skip, or silently drop any symptom or expression she describes — even if it is vague, informal, or culturally specific.
- If an expression has no direct clinical equivalent (for example a traditional-medicine or culturally-specific concept), KEEP her exact words verbatim and set the clinical field to "No direct clinical equivalent". Never invent or force a clinical term onto it, and never drop it.
- Detect the language the person wrote in and report it in plain English (e.g. "English", "Spanish", "Chinese (Simplified)").

Return ONLY valid JSON — no preamble, no markdown fences — in exactly this shape:
{
  "detected_language": "the language she wrote in, in English",
  "items": [
    {"verbatim": "their exact words", "clinical": "clinical term(s)"}
  ]
}"""


def normalise(description: str) -> dict:
    """Take a free-text symptom description, return a dict with 'detected_language'
    and 'items' (each mapping verbatim -> clinical)."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": description}],
    )
    raw = message.content[0].text.strip()

    # Safety net: strip markdown fences if the model ever wraps the JSON
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[raw.find("{"):]

    return json.loads(raw)


if __name__ == "__main__":
    test = (
        "I keep waking up at 3am completely drenched in sweat, and I'm so "
        "exhausted during the day I can't focus. My periods have gone all "
        "over the place too."
    )

    result = normalise(test)

    print(f"\nDETECTED LANGUAGE: {result['detected_language']}")
    print("\nHER WORDS  →  CLINICAL TERMS\n")
    for item in result["items"]:
        print(f'  "{item["verbatim"]}"')
        print(f'   → {item["clinical"]}\n')
        