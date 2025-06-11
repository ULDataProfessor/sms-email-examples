# Invoice OCR Scanner

This module processes scanned invoice PDFs or JPEGs and extracts
structured data using Tesseract OCR. Parsed results are saved to CSV
and inserted into a SQLite database.

## How OCR Works

OCR (Optical Character Recognition) engines like Tesseract analyze
images of text and convert the shapes of the characters into actual
text data. Tesseract applies image preprocessing and pattern matching
to recognize individual letters. When given a PDF, pages are converted
into images before running OCR. The output is a block of raw text that
represents all text detected on the invoice.

## Parsing Rules

The parser searches the OCR text with simple regular expressions:

- **Invoice number** – the first match of `Invoice` followed by an ID.
- **Date** – a string formatted like `MM/DD/YYYY` or `MM-DD-YYYY`.
- **Vendor** – text following the word `Vendor` on its line.
- **Total** – the amount following the word `Total`, with or without a
  dollar sign.

These rules are intentionally basic and may need to be customized for
different invoice layouts.

## Running the Scanner

1. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Put invoice PDFs or JPEGs in a directory, e.g. `invoices/`.
3. Run the script:
   ```bash
   python main.py invoices/ --csv results.csv --db invoices.db
   ```
4. Inspect `results.csv` for the extracted data. The same rows are also
   appended to the `invoices` table inside `invoices.db`.

You can rerun the script on new invoice batches by pointing to a
different directory or file list. Review the CSV output to verify that
the parsing rules captured the fields correctly.
