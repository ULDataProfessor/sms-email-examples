import argparse
import os
import re
import sqlite3

import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import pandas as pd


INVOICE_NO_RE = re.compile(r"Invoice\s*#?:?\s*(?P<number>\S+)", re.IGNORECASE)
DATE_RE = re.compile(r"Date\s*:?\s*(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", re.IGNORECASE)
VENDOR_RE = re.compile(r"Vendor\s*:?\s*(?P<vendor>.+)", re.IGNORECASE)
TOTAL_RE = re.compile(r"Total\s*:?\s*\$?(?P<total>[0-9,\.]+)", re.IGNORECASE)


def extract_text(file_path: str) -> str:
    """Extract text from an image or PDF using Tesseract."""
    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        text_parts = [pytesseract.image_to_string(img) for img in images]
        return "\n".join(text_parts)
    else:
        with Image.open(file_path) as img:
            return pytesseract.image_to_string(img)


def parse_invoice(text: str) -> dict:
    """Parse invoice fields using simple regular expressions."""
    invoice = {
        "invoice_number": None,
        "date": None,
        "vendor": None,
        "total": None,
    }

    if m := INVOICE_NO_RE.search(text):
        invoice["invoice_number"] = m.group("number")
    if m := DATE_RE.search(text):
        invoice["date"] = m.group("date")
    if m := VENDOR_RE.search(text):
        invoice["vendor"] = m.group("vendor").strip()
    if m := TOTAL_RE.search(text):
        invoice["total"] = m.group("total")

    return invoice


def process_directory(input_dir: str) -> pd.DataFrame:
    """Scan a directory for invoices and return a DataFrame."""
    records = []
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith((".pdf", ".jpg", ".jpeg")):
            continue
        path = os.path.join(input_dir, fname)
        text = extract_text(path)
        data = parse_invoice(text)
        data["filename"] = fname
        records.append(data)
    return pd.DataFrame(records)


def export_results(df: pd.DataFrame, csv_path: str, db_path: str) -> None:
    df.to_csv(csv_path, index=False)
    conn = sqlite3.connect(db_path)
    df.to_sql("invoices", conn, if_exists="append", index=False)
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoice OCR scanner")
    parser.add_argument("input_dir", help="Directory containing invoice PDFs or images")
    parser.add_argument("--csv", default="invoices.csv", help="Output CSV file")
    parser.add_argument("--db", default="invoices.db", help="SQLite database file")
    args = parser.parse_args()

    df = process_directory(args.input_dir)
    export_results(df, args.csv, args.db)
    print(f"Processed {len(df)} invoices. Results saved to {args.csv} and {args.db}.")


if __name__ == "__main__":
    main()
