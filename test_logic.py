import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

from src.utils.seasonal_engine import SeasonalEngine
from src.utils.ticker_extractor import extract_tickers
from src.scrapers.manager import ScraperManager

async def run_check():
    print("--- 1. Testing Seasonal Engine ---")
    seasonal = SeasonalEngine()
    context = seasonal.get_current_seasonal_context()
    print(f"Current Context: {context}")

    print("\n--- 2. Testing Ticker Extractor ---")
    sample_text = "Reliance and HDFC Bank are leading the Nifty today while Solar stocks like Adani Green gain in summer."
    tickers = extract_tickers(sample_text)
    print(f"Sample: {sample_text}")
    print(f"Extracted Tickers: {tickers}")

    print("\n--- 3. Testing Scraper Manager (Fast Check) ---")
    manager = ScraperManager()
    # We'll just run one scraper to verify connectivity if possible
    # but run_all is fine for a full check
    try:
        news = await manager.run_all()
        print(f"Successfully scraped {len(news)} items from 4 sources.")
        if news:
            print(f"Sample news: {news[0]['title']} ({news[0]['source']})")
            print(f"Tickers found in sample: {news[0].get('tickers')}")
    except Exception as e:
        print(f"Scraping error (Expected if network blocked): {e}")

if __name__ == "__main__":
    asyncio.run(run_check())
