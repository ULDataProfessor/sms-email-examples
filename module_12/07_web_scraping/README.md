# Web Scraping for Data Collection

## Project Overview
`scrape_products.py` retrieves product details from an example e-commerce page and saves them to a CSV file. It demonstrates the basics of making HTTP requests and parsing HTML content.

## Variables
`URL` defines the page to scrape while `OUTPUT` is the filename of the generated CSV. You can edit these constants to target other sites or output locations.

## Instructions
Install the requirements with `pip install requests beautifulsoup4`. Run `python scrape_products.py` to download the page and create `products.csv` containing the scraped `name`, `price` and link for each product item.

## Explanation
The script makes a GET request then uses BeautifulSoup to search for elements marked with `.product` CSS classes. Each item is stored as a dictionary and finally written using `csv.DictWriter`. This approach is easily extendable to more complex scraping tasks.
