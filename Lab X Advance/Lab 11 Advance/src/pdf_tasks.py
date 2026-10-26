# src/pdf_tasks.py
import io
import os

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:  # pypdf is the maintained successor of PyPDF2 (same API)
    from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


class PDFTasks:
    """PDF operations: merging and watermarking."""

    def merge_pdfs(self, input_files, output_file):
        """Merges several PDFs (in order) into one file. Returns the number of pages written."""
        writer = PdfWriter()
        for path in input_files:
            if not os.path.exists(path):
                logger.warning(f"Skipping missing PDF: {path}")
                continue
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
            logger.info(f"Added {len(reader.pages)} page(s) from '{os.path.basename(path)}'.")
        if len(writer.pages) == 0:
            raise ValueError("No pages to merge - none of the input PDFs were found.")
        ensure_directory_exists(os.path.dirname(output_file))
        with open(output_file, "wb") as f:
            writer.write(f)
        logger.info(f"Merged PDF saved: {output_file} ({len(writer.pages)} pages)")
        return len(writer.pages)

    @staticmethod
    def _make_watermark_page(width, height, text, opacity, font_size, angle):
        """Creates a one-page PDF (in memory) with diagonal semi-transparent text."""
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(width, height))
        c.setFillColor(Color(0.85, 0.1, 0.1, alpha=opacity))
        c.setFont("Helvetica-Bold", font_size)
        c.translate(width / 2, height / 2)
        c.rotate(angle)
        c.drawCentredString(0, -font_size / 3, text)
        c.save()
        buf.seek(0)
        return PdfReader(buf).pages[0]

    def add_watermark(self, input_file, output_file, text, opacity=0.25, font_size=72, angle=45):
        """Stamps the watermark text on every page of input_file. Returns the number of pages."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"PDF to watermark not found: {input_file}")
        reader = PdfReader(input_file)
        writer = PdfWriter()
        for page in reader.pages:
            w, h = float(page.mediabox.width), float(page.mediabox.height)
            page.merge_page(self._make_watermark_page(w, h, text, opacity, font_size, angle))
            writer.add_page(page)
        ensure_directory_exists(os.path.dirname(output_file))
        with open(output_file, "wb") as f:
            writer.write(f)
        logger.info(f"Watermarked PDF saved: {output_file} ({len(reader.pages)} pages, text='{text}')")
        return len(reader.pages)
