import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import random


# Removed def scrape_page(url): - Timed out added a 15 second time out in case the website is slow 

def scrape_page(url, max_retries=3, timeout=15):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    
    if not table:
        print(f"No table found on {url}")
        return pd.DataFrame()
    
    headers = [th.text.strip() for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.text.strip() for td in tr.find_all("td")]
        if cells:
            rows.append(cells)
    return pd.DataFrame(rows, columns=headers)

#change max_pages to match the max pages of the page you are scraping (must match page count in scrape_loop.ipynb)

def scrape_all_pages(base_url, max_pages=135, delay=1.0):
    all_dfs = []
    last_df = None

    for pages in range(1, max_pages + 1):
        url = re.sub(r'([?&])page=\d+', f'\\1page={pages}', base_url)
        print(f"Scraping page {pages}: {url}")

        df = scrape_page(url)
        if df.empty:
            print("No more results - stopping.")
            break

        if last_df is not None and df.equals(last_df):
            print("Repeated page found - stopping.")
            break

        all_dfs.append(df)
        last_df = df
        time.sleep(random.uniform(2,5))

    if not all_dfs:
        return pd.DataFrame()
    
    combined = pd.concat(all_dfs, ignore_index=True)
    combined = combined.drop_duplicates(subset=["Mark", "Competitor", "Date", "Venue"], keep="first")
    return combined




