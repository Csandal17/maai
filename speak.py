"""
speak.py — Maai's accessibility read-back.

Takes a finished advocacy record and reads it aloud, so a woman can
hear her record and confirm it captures her before handing it over.
Two-step pattern proven in Serenum: Claude condenses the record into
natural spoken sentences, then ElevenLabs synthesises the audio.
Additive only — the record and PDF are untouched.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic
from elevenlabs.client import ElevenLabs

load_dotenv()
claude = Anthropic()
eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

VOICE_ID = "E4IXevHtHpKGh0bvrPPr"  # Emilia — calm, warm; matches Serenum

CONDENSE_PROMPT = """You turn a symptom advocacy record into short, natural spoken
sentences for the woman who made it, so she can hear her record read back.

Rules:
- Speak TO her ("You described...", "In your words...")
- Include every item: her phrase, then the clinical term
- If an item has no clinical equivalent, say her words were kept exactly
  as she said them
- No diagnosis, no conclusions, no advice — you only read back the record
- End with: "This record draws no conclusions. Your clinician interprets it."
- Respond in the same language as her verbatim phrases, so she hears her
  record in her own language
- Plain sentences only, no headers or lists — this will be spoken aloud"""

def speak_record(record: dict, output_path: str = "maai_readback.mp3") -> str:
    """Condense an advocacy record to spoken text, synthesise it, return the mp3 path."""
    # Step 1: Claude condenses the record into natural speech
    record_text = "\n".join(
        f'She said: "{item["verbatim"]}" — clinical term: {item["clinical"]}'
        for item in record["items"]
    )
    message = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=CONDENSE_PROMPT,
        messages=[{"role": "user", "content": record_text}],
    )
    spoken_text = message.content[0].text.strip()

    # Step 2: ElevenLabs synthesises the speech
    audio = eleven.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=spoken_text,
        model_id="eleven_multilingual_v2",
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path


if __name__ == "__main__":
    from chain import build_record

    test = (
        "For the past three weeks I've been absolutely wiped out by the middle of "
        "the day, even when I've slept. I get out of breath just going up the "
        "stairs, which never used to happen."
    )

    path = speak_record(build_record(test))
    print(f"\nAudio written: {path}")
