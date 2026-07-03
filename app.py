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
        "Describe what you've been experiencing, in your own words, in any language. "
        "Maai prepares a record that helps you be heard — it maps your words to "
        "clinical terms without ever replacing them, and draws no conclusions. "
        "The clinician interprets; Maai helps you be heard."
    )

    description = gr.Textbox(
        label="In your own words",
        placeholder="e.g. I keep waking at 3am drenched in sweat...",
        lines=5,
    )
    submit = gr.Button("Prepare my record")

    record_display = gr.Textbox(label="Your advocacy record", lines=14)
    pdf_file = gr.File(label="Download for your appointment")

    submit.click(fn=run_maai, inputs=description, outputs=[record_display, pdf_file])

if __name__ == "__main__":
    demo.launch()
    