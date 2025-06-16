"""Scrape product information and save to CSV."""
from __future__ import annotations

import csv
import requests
from bs4 import BeautifulSoup

URL = "https://example.com/products"
OUTPUT = "products.csv"


def scrape(url: str = URL) -> list[dict[str, str]]:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    products = []
    for item in soup.select(".product"):
        name = item.select_one(".name").get_text(strip=True)
        price = item.select_one(".price").get_text(strip=True)
        link = item.select_one("a")['href']
        products.append({"name": name, "price": price, "url": link})
    return products


def save_csv(records: list[dict[str, str]], path: str = OUTPUT) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "url"])
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    data = scrape()
    save_csv(data)


if __name__ == "__main__":
    main()
