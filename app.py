"""
app.py — Maai's interface.

A minimal Gradio skin over the proven pipeline:
paste a symptom description in any language -> see the advocacy
record -> download the clinician-ready PDF.
Function today; theming (palette, Fraunces/Inter) is weekend work.
"""

import gradio as gr
from chain import build_record
from make_pdf import make_pdf
from speak import speak_record


def run_maai(description: str):
    """Full pipeline: description -> record -> PDF. Returns display text + PDF path."""
    if not description or not description.strip():
        return "Please describe what you've been experiencing.", None, None

    record = build_record(description)

    lines = [
        f"Language detected: {record['language_detected']}",
        "",
        "HER WORDS  →  CLINICAL TERMS",
        "",
    ]
    for item in record["items"]:
        lines.append(f'"{item["verbatim"]}"')
        lines.append(f"    →  {item['clinical']}")
        lines.append("")

    pdf_path = make_pdf(record)
    return "\n".join(lines), pdf_path, record

css = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&display=swap');

.gradio-container {
    background-color: #F7F4EF !important;
    max-width: 780px !important;
    margin: 0 auto !important;
}

#header { text-align: center; }
#header h1 {
    font-family: 'Fraunces', serif !important;
    font-size: 3.2em !important;
    font-weight: 600 !important;
    color: #2B2A26 !important;
    margin-bottom: 0.1em !important;
}

.block, .form, textarea, input {
    border-radius: 12px !important;
    border-color: #DCCFBC !important;
}

button.primary {
    font-family: 'Fraunces', serif !important;
    font-size: 1.1em !important;
}
"""

theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#F7F4EF", c100="#EFE9DF", c200="#DCCFBC", c300="#C6B29A",
        c400="#A98F73", c500="#8C7355", c600="#7A6349", c700="#65523C",
        c800="#514230", c900="#3D3124", c950="#2B2A26",
    ),
    neutral_hue="stone",
    font=gr.themes.GoogleFont("Inter"),
    font_mono=gr.themes.GoogleFont("Inter"),
)

with gr.Blocks(title="Maai", theme=theme, css=css) as demo:
    gr.Markdown(
        "# Maai\n"
        "*See what time reveals.*\n\n"
        "**The AI health advocate for women's cardiovascular health**",
        elem_id="header",
    )
    gr.Markdown(
        "Maai means the meaningful interval between things — the space where "
        "health patterns emerge.\n\n"
        "Women's heart symptoms are dismissed every day. Women are 50% more "
        "likely than men to be misdiagnosed after a heart attack, and the "
        "symptoms often don't look like the ones on the poster: exhaustion, "
        "breathlessness, nausea, jaw or back pain. For women facing language "
        "or cultural barriers, being heard is harder still.\n\n"
        "Maai helps you be harder to dismiss. Describe what you've been "
        "experiencing over recent days or weeks, in your own words, in any "
        "language. Maai maps your words to clinical terms a doctor recognises — "
        "never replacing them, never drawing conclusions. The clinician "
        "interprets. Maai helps you be heard.\n\n"
        "**Maai is for patterns over time, not symptoms happening right now. "
        "If you have chest pain, breathlessness, or other symptoms now, call 999.**"
    )

    description = gr.Textbox(
        label="In your own words",
        placeholder="e.g. For the past few weeks I've been exhausted by lunchtime, breathless going up the stairs, and there's an ache in my jaw that comes and goes...",
        lines=5,
    )
    submit = gr.Button("Prepare my record")

    record_display = gr.Textbox(label="Your advocacy record", lines=14)
    pdf_file = gr.File(label="Download for your appointment")

    record_state = gr.State()
    listen = gr.Button("Hear my record read aloud")
    audio_out = gr.Audio(label="Your record, read back", type="filepath")

    submit.click(fn=run_maai, inputs=description,
                 outputs=[record_display, pdf_file, record_state])

    def read_aloud(record):
        if not record:
            raise gr.Error("Prepare a record first, then listen.")
        return speak_record(record)

    listen.click(fn=read_aloud, inputs=record_state, outputs=audio_out)

if __name__ == "__main__":
    demo.launch()
