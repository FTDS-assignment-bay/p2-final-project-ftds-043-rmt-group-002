# review_scraper.py for Female Daily

"""
Product Review Scraper for FemaleDaily URLs

This script reads a CSV file containing product URLs, visits each page using Selenium,
and extracts product brand, price, shade, and all review on 1st page. The results are saved to a new CSV file.

- Input:  CSV file with URLs (first column)
- Output: CSV file with columns: url, product_brand, product_price, product_shade, product_review
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define Variables
INPUT_CSV = "femaledaily-2025-07-12.csv"
OUTPUT_CSV = "product_review.csv"
ELEMENT_WAIT_TIMEOUT = 10  # Seconds

def load_urls(input_csv, start_row=0):
    """
    Load URLs from a CSV file, starting from a specific row.
    Returns a pandas Series of URLs.
    """
    df = pd.read_csv(input_csv)
    return df.iloc[start_row:1, 0]

def setup_driver(headless=False):
    """
    Initialize and return a Selenium Chrome WebDriver.
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def get_product_info_and_reviews(driver, url, wait_timeout=ELEMENT_WAIT_TIMEOUT):
    """
    Visit the given URL and extract product brand, price, shade, and all reviews.
    Returns a dictionary with the extracted data.
    """
    driver.get(url)
    data = {
        "url": url,
        "product_brand": None,
        "product_price": None,
        "product_shade": None,
    }
    try:
        brand_elem = WebDriverWait(driver, wait_timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-brand"))
        )
        data["product_brand"] = brand_elem.text.strip()
    except Exception:
        pass

    try:
        price_elem = WebDriverWait(driver, wait_timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-price"))
        )
        data["product_price"] = price_elem.text.strip()
    except Exception:
        pass

    try:
        shade_elem = WebDriverWait(driver, wait_timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-shade"))
        )
        data["product_shade"] = shade_elem.text.strip()
    except Exception:
        pass

    review_texts = []
    try:
        review_elems = WebDriverWait(driver, wait_timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".text-content"))
        )
        for elem in review_elems:
            text = elem.text.strip()
            if text:
                review_texts.append(text)
    except Exception:
        pass

    for i, review in enumerate(review_texts, 1):
        data[f"product_review_{i}"] = review

    return data

# Run the script

urls = load_urls(INPUT_CSV)
print(f"Processing {len(urls)} URLs from {INPUT_CSV}")

driver = setup_driver(headless=False)
results = []

for idx, url in enumerate(urls, 1):
    print(f"Scraping {idx}/{len(urls)}: {url}")
    data = get_product_info_and_reviews(driver, url)
    results.append(data)

# Find the maximum number of reviews for any product
max_reviews = 0
for row in results:
    review_cols = [k for k in row.keys() if k.startswith("product_review_")]
    max_reviews = max(max_reviews, len(review_cols))

# Ensure all rows have the same review columns
for row in results:
    for i in range(1, max_reviews + 1):
        col = f"product_review_{i}"
        if col not in row:
            row[col] = None

columns = (
    ["url", "product_brand", "product_price", "product_shade"] +
    [f"product_review_{i}" for i in range(1, max_reviews + 1)]
)
review_df = pd.DataFrame(results, columns=columns)
review_df.to_csv(OUTPUT_CSV, index=False)
print(f"Data saved to {OUTPUT_CSV} ({len(results)} rows).")

driver.quit()
print("Script finished.")
