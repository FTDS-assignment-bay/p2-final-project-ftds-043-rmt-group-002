# description_scraper.py for Female Daily

"""
Product Description Scraper for FemaleDaily URLs

This script reads a CSV file containing product URLs, visits each page using Selenium,
and extracts the product description. The results are saved to a new CSV file.

- Input:  CSV file with URLs (first column)
- Output: CSV file with columns: url, product_desc
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Define Variables
INPUT_CSV = "femaledaily-2025-07-12.csv"
OUTPUT_CSV = "product_descriptions.csv"
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

def get_product_description(driver, url, wait_timeout=ELEMENT_WAIT_TIMEOUT):
    """
    Visit the given URL and extract the product description text.
    Returns the description string, or None if not found.
    """
    driver.get(url)

    # Try to expand the description if a button exists
    try:
        desc_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "id_button_description"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", desc_button)
        driver.execute_script("arguments[0].click();", desc_button)
        time.sleep(0.5)
    except Exception:
        pass  # Button not found or not clickable

    # Wait for the description element and return its text
    try:
        desc_elem = WebDriverWait(driver, wait_timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-desc"))
        )
        return desc_elem.text
    except Exception:
        return None

# Run the script

urls = load_urls(INPUT_CSV)
print(f"Processing {len(urls)} URLs from {INPUT_CSV}")

driver = setup_driver(headless=False)
results = []

for idx, url in enumerate(urls, 1):
    print(f"Scraping {idx}/{len(urls)}: {url}")
    desc = get_product_description(driver, url)
    if desc is None:
        print(f"  Description not found for {url}")
    results.append({"url": url, "product_desc": desc})

# Save results to CSV
desc_df = pd.DataFrame(results)
desc_df.to_csv(OUTPUT_CSV, index=False)
print(f"Data saved to {OUTPUT_CSV} ({len(results)} rows).")

driver.quit()
print("Script finished.")