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


def run_maai(description: str):
    """Full pipeline: description -> record -> PDF. Returns display text + PDF path."""
    if not description or not description.strip():
        return "Please describe what you've been experiencing.", None

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
    return "\n".join(lines), pdf_path


with gr.Blocks(title="Maai") as demo:
    gr.Markdown("# Maai")
    gr.Markdown(
        "**The AI health advocate for women's cardiovascular health**\n\n"
        "*See what time reveals.* Maai means the meaningful interval between "
        "things — the space where health patterns emerge.\n\n"
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

    submit.click(fn=run_maai, inputs=description, outputs=[record_display, pdf_file])

if __name__ == "__main__":
    demo.launch()
