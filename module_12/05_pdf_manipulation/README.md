# PDF Manipulation

**Objective:**  
Automate PDF tasks:
- Extract all text from `report.pdf`
- Split each page into a separate PDF (`page_1.pdf`, etc.)
- Merge `appendix.pdf` at the end

**Codex Prompt:**  
“Write a Python script using PyPDF2 that reads `report.pdf`, extracts its text to `report.txt`, splits each page into `page_#.pdf`, then appends all pages of `appendix.pdf` to the end of a new `combined.pdf`.”
