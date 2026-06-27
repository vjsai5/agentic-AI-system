
import os
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

def create_pdf(text, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=48,
        bottomMargin=48,
    )
    styles = getSampleStyleSheet()
    story = []

    for block in text.splitlines():
        cleaned = block.strip()
        if not cleaned:
            story.append(Spacer(1, 8))
            continue
        story.append(Paragraph(escape(cleaned), styles["BodyText"]))
        story.append(Spacer(1, 6))

    doc.build(story or [Paragraph("No report content generated.", styles["BodyText"])])
    return path
