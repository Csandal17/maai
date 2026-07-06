---
title: Maai
emoji: ♾️
colorFrom: gray
colorTo: green
sdk: gradio
app_file: app.py
---

# Maai

**The AI health advocate for women's cardiovascular health.**
*See what time reveals.*

Maai means the meaningful interval between things — the space where health
patterns emerge. Women are 50% more likely than men to be misdiagnosed
after a heart attack, and their symptoms often don't look like the ones on
the poster. Maai helps a woman be harder to dismiss: she describes what
she's been experiencing in her own words, in any language, and Maai maps
her words to clinical terms a doctor recognises — never replacing them,
never drawing conclusions. The clinician interprets. Maai helps her be heard.

**Live demo:** https://huggingface.co/spaces/Csandal17/maai

## What it does

- **Advocacy record** — maps her exact words to clinical vocabulary,
  keeping both. Untranslatable expressions (e.g. Traditional Chinese
  Medicine terms) are preserved verbatim and honestly flagged, never
  dropped or forced into a mapping.
- **Clinician-ready PDF** — a printable record with her words and the
  clinical terms side by side, with full Unicode/CJK support.
- **Read-back (accessibility)** — opt-in audio of her record, in her own
  language, so she can confirm it captures her before handing it over.
- **Citizen science layer** — after she has her record, she can optionally
  contribute an anonymised pattern (categories, age band, language, month —
  never her words) to a shared dataset. The aggregate view is seeded with
  clearly-labelled synthetic data and is descriptive only.

## The guardrails

Maai never diagnoses, scores, concludes, or predicts. Every record and
the interface itself state this. It is for patterns over time, not
symptoms happening right now — anyone with symptoms now is directed
to call 999. Nothing a woman says is ever silently dropped.

## Architecture

Plain Claude API pipeline — deliberately no agent framework, because the
agents are pure transformations with no tool-use or looping:
intake.py  →  normalise.py  →  chain.py  →  make_pdf.py
↘  speak.py (ElevenLabs read-back)
↘  contribute.py / aggregate.py

- **Stack:** Python 3.12, uv, Anthropic API, Gradio, fpdf2, ElevenLabs
- **Fonts:** Noto Sans SC bundled (via Git LFS) for CJK PDF rendering
- **Proven in:** English, Spanish, and Chinese (Simplified), end to end
  on the live deployment

## Running locally

```bash
git clone https://github.com/Csandal17/maai.git
cd maai
uv sync
cp .env.example .env   # add ANTHROPIC_API_KEY and ELEVENLABS_API_KEY
uv run python app.py
```

## Roadmap

- **SOCRATES annotation** (working prototype on the `socrates-experiment`
  branch) — tags each record item with the clinical dimensions her words
  address, and gap-maps what's not yet described for the clinician to ask into
- Advocacy coaching — her rights and how to ask, never test recommendations
- Native-speaker verification of multilingual read-back
- Voice input

## Evidence base

The problem is documented, not asserted — see [SOURCES.md](SOURCES.md)
(BHF *Bias and Biology*, 2019, and supporting literature).

MIT License