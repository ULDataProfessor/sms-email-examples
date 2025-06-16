# Automated Data Entry

## Project Overview
This project uses Selenium to submit a web form automatically for each row in a CSV file. It is useful for scenarios where repetitive form filling is required, such as entering test data or migrating legacy records.

## Variables
`FORM_URL` specifies the target form URL and `CSV_PATH` points to the CSV file with fields `name`, `email`, and `age`. Logging is configured in `form_filler.py` so that successes and failures are displayed in the console.

## Instructions
Install the Selenium Python package and ensure you have the appropriate WebDriver installed. Place your `input.csv` in the same directory and run `python form_filler.py`. The script opens the browser, fills in each row and submits the form automatically.

## Explanation
`form_filler.py` reads the CSV using pandas, then iterates through each entry, opening the form with `webdriver.Chrome`. Using element locators it populates the fields and submits the form. Errors are caught so the loop continues even if a particular submission fails.
