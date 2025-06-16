"""Automatically submit web forms from CSV data."""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

FORM_URL = "http://example.com/form"
CSV_PATH = "input.csv"

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


def submit_entry(driver: webdriver.Chrome, entry: pd.Series) -> None:
    """Fill the form with a row of data."""
    driver.get(FORM_URL)
    driver.find_element(By.NAME, "name").send_keys(str(entry["name"]))
    driver.find_element(By.NAME, "email").send_keys(str(entry["email"]))
    driver.find_element(By.NAME, "age").send_keys(str(entry["age"]))
    driver.find_element(By.CSS_SELECTOR, "form").submit()


def main(csv_file: Path = Path(CSV_PATH)) -> None:
    data = pd.read_csv(csv_file)
    driver = webdriver.Chrome()
    for _, row in data.iterrows():
        try:
            submit_entry(driver, row)
            logging.info("Submitted %s", row.get("email"))
        except Exception as exc:
            logging.error("Failed to submit %s: %s", row.get("email"), exc)
    driver.quit()


if __name__ == "__main__":
    main()
