# PDF Manipulation

## Project Overview
`pdf_tasks.py` demonstrates how to automate common PDF workflows using PyPDF2. It can extract text from a report, split pages into separate files and merge an appendix onto the end.

## Variables
The constants `REPORT_PDF` and `APPENDIX_PDF` point to the PDF files that will be processed. These can be changed to work with different source documents or appendices.

## Instructions
Install PyPDF2 via `pip install PyPDF2` and place the sample PDFs in this directory. Run `python pdf_tasks.py` to create a text file from the report, generate individual page PDFs and output a combined document that includes the appendix.

## Explanation
The script uses `PdfReader` and `PdfWriter` to manipulate pages. `extract_text` saves the report's text for easy searching. `split_pages` writes each page into its own file, while `merge_appendix` builds a new PDF containing both the original report and the appendix pages. The functions can be mixed and matched in other automation workflows.
