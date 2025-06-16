"""Extract text, split pages, and merge PDFs."""
from __future__ import annotations

from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter

REPORT_PDF = Path("report.pdf")
APPENDIX_PDF = Path("appendix.pdf")


def extract_text(report: Path = REPORT_PDF) -> Path:
    reader = PdfReader(report)
    text_path = report.with_suffix(".txt")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text_path.write_text(text, encoding="utf-8")
    return text_path


def split_pages(report: Path = REPORT_PDF) -> None:
    reader = PdfReader(report)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        with open(f"page_{i}.pdf", "wb") as f:
            writer.write(f)


def merge_appendix(report: Path = REPORT_PDF, appendix: Path = APPENDIX_PDF) -> Path:
    report_reader = PdfReader(report)
    appendix_reader = PdfReader(appendix)
    writer = PdfWriter()
    for p in report_reader.pages:
        writer.add_page(p)
    for p in appendix_reader.pages:
        writer.add_page(p)
    out_path = Path("combined.pdf")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_path


def main() -> None:
    extract_text()
    split_pages()
    merge_appendix()


if __name__ == "__main__":
    main()
