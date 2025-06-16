# Automated Data Entry

**Objective:**  
Automate filling a web form at `http://example.com/form` with Selenium:
- Read entries from `input.csv`
- For each row, navigate to the form, fill fields `name`, `email`, `age`, and submit
- Log successes and failures

**Codex Prompt:**  
“Generate a Python script using `selenium.webdriver.Chrome` that reads `input.csv`, iterates rows, opens `http://example.com/form`, fills `name`, `email`, `age`, clicks submit, and logs status.”
