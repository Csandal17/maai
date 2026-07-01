"""
chain.py — Maai's pipeline.

Wires intake() -> normalise() into one advocacy record:
  raw description  ->  captured verbatim  ->  clinical mapping
The output is a single dict, ready for the PDF generator (step 4).
No interpretation beyond language mapping — Maai helps her be heard.
"""

from intake import intake
from normalise import normalise


def build_record(description: str, language: str = "en") -> dict:
    """Run a symptom description through the full Maai pipeline.

    Returns one structured advocacy record combining:
      - her captured verbatim + provenance (from intake)
      - the detected language and verbatim->clinical mappings (from normalise)
    """
    captured = intake(description, language=language)
    mapped = normalise(captured["verbatim_description"])

    return {
        "verbatim_description": captured["verbatim_description"],
        "language_supplied": captured["language"],
        "language_detected": mapped["detected_language"],
        "captured_at": captured["captured_at"],
        "items": mapped["items"],
    }


if __name__ == "__main__":
    test = (
        "I keep waking up at 3am completely drenched in sweat, and I'm so "
        "exhausted during the day I can't focus. My periods have gone all "
        "over the place too."
    )

    record = build_record(test)

    print(f"\nCaptured at: {record['captured_at']}")
    print(f"Language (supplied / detected): {record['language_supplied']} / {record['language_detected']}\n")
    print("ADVOCACY RECORD\n")
    for item in record["items"]:
        print(f'  "{item["verbatim"]}"')
        print(f'   → {item["clinical"]}\n')
        