# document-automator/create_sample_pdfs.py
"""Helper script: creates the sample input PDFs (input_article.pdf, dummy_doc1.pdf, dummy_doc2.pdf)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
os.makedirs(DOCS, exist_ok=True)


def write_page(c, title, lines):
    width, height = A4
    y = height - 72
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, y, title)
    y -= 32
    c.setFont("Helvetica", 12)
    for line in lines:
        if line.startswith("#"):
            y -= 8
            c.setFont("Helvetica-Bold", 14)
            c.drawString(72, y, line[1:].strip())
            c.setFont("Helvetica", 12)
            y -= 24
        else:
            c.drawString(72, y, line)
            y -= 18
    c.showPage()


# input_article.pdf (2 pages)
c = canvas.Canvas(os.path.join(DOCS, "input_article.pdf"), pagesize=A4)
write_page(c, "Introduction to Automation", [
    "Automation is the creation and application of technology to produce and",
    "deliver goods and services with minimal human intervention. The",
    "implementation of automation technologies, techniques, and processes",
    "improves the efficiency, reliability, and speed of many tasks that were",
    "previously performed manually.",
    "",
    "This leads to increased productivity, reduced costs, and improved quality.",
])
write_page(c, "Benefits of Automation", [
    "1. Increased Efficiency: Tasks are completed faster and with higher throughput.",
    "2. Cost Reduction: Lower labor costs and reduced waste.",
    "3. Improved Accuracy: Minimizes human error.",
    "4. Enhanced Safety: Dangerous tasks can be automated.",
    "5. Greater Consistency: Uniform quality in output.",
    "# Conclusion",
    "Automation is transforming industries globally. Embracing these",
    "technologies is crucial for future competitiveness.",
])
c.save()

# dummy_doc1.pdf / dummy_doc2.pdf (one line each)
for i, text in [(1, "This is Dummy Document 1 - the first page of the merged PDF."),
                (2, "This is Dummy Document 2 - the second page of the merged PDF.")]:
    c = canvas.Canvas(os.path.join(DOCS, f"dummy_doc{i}.pdf"), pagesize=A4)
    write_page(c, f"Dummy Document {i}", [text])
    c.save()

print("Sample PDFs created in", DOCS)
