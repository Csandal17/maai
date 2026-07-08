"""
make_pdf.py — Maai's advocacy record generator.

Turns a build_record() output into a clinician-ready PDF:
her verbatim words, the clinical mappings beside them, and a visible
statement that this record contains no diagnosis or conclusions.
Reuses the fpdf2 patterns proven in Lagomy.
"""

from pathlib import Path
from fpdf import FPDF

# Noto Sans SC — free pan-Unicode font bundled in the repo, so PDFs
# render her words in ANY language, on any machine (incl. HF Spaces).
FONT_PATH = str(Path(__file__).parent / "fonts" / "NotoSansSC.ttf")


def make_pdf(record: dict, annotated: dict = None, output_path: str = "maai_record.pdf") -> str:
    """Render an advocacy record dict into a PDF. Returns the file path."""
    if not Path(FONT_PATH).exists():
        raise FileNotFoundError(
            f"Unicode font not found at {FONT_PATH} — tell Claude, we'll pick another font."
        )

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Unicode", "", FONT_PATH)
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- Header ---
    pdf.set_font("Unicode", size=22)
    pdf.cell(w=0, h=12, text="Maai", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Unicode", size=11)
    pdf.cell(w=0, h=8, text="Symptom advocacy record — prepared from the patient's own words",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # --- Provenance ---
    pdf.set_font("Unicode", size=9)
    pdf.cell(w=0, h=6, text=f"Captured: {record['captured_at'][:10]}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f"Language detected: {record['language_detected']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Her full description, verbatim ---
    pdf.set_font("Unicode", size=12)
    pdf.cell(w=0, h=8, text="In her own words", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Unicode", size=10)
    pdf.multi_cell(w=0, h=6, text=record["verbatim_description"], new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Mapped items ---
    pdf.set_font("Unicode", size=12)
    pdf.cell(w=0, h=8, text="What she described, in clinical terms", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    for item in record["items"]:
        pdf.set_font("Unicode", size=10)
        pdf.multi_cell(w=0, h=6, text=f'"{item["verbatim"]}"', new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(w=0, h=6, text=f'    -  {item["clinical"]}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # --- SOCRATES gap-map (optional) ---
    if annotated and annotated.get("not_yet_described"):
        pdf.ln(2)
        pdf.set_font("Unicode", size=12)
        pdf.cell(w=0, h=8, text="Not yet described — the clinician may wish to ask about",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Unicode", size=10)
        for dim in annotated["not_yet_described"]:
            pdf.multi_cell(w=0, h=6, text=f"   -  {dim}", new_x="LMARGIN", new_y="NEXT")
            
    # --- Visible guardrail ---
    pdf.ln(4)
    pdf.set_font("Unicode", size=9)
    pdf.multi_cell(
        w=0, h=5,
        text=(
            "This record maps the patient's own words to clinical vocabulary. "
            "It contains no diagnosis, assessment, or conclusion. "
            "All interpretation rests with the clinician."
        ),
        new_x="LMARGIN", new_y="NEXT",
    )

    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    from chain import build_record

    test = (
        "I keep waking up at 3am completely drenched in sweat, and I'm so "
        "exhausted during the day I can't focus. My periods have gone all "
        "over the place too."
    )

    path = make_pdf(build_record(test))
    print(f"\nPDF written: {path}")
