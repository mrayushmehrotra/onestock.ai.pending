from typing import List, Dict, Any
import asyncio
from .et_scraper import ETScraper
from .mint_scraper import MintScraper
from .mc_scraper import MoneyControlScraper
from .bs_scraper import BSScraper
from src.utils.ticker_extractor import extract_tickers

class ScraperManager:
    def __init__(self):
        self.scrapers = [
            ETScraper(),
            MintScraper(),
            MoneyControlScraper(),
            BSScraper()
        ]

    async def run_all(self) -> List[Dict[str, Any]]:
        all_news = []
        for scraper in self.scrapers:
            print(f"Running scraper for {scraper.__class__.__name__}...")
            try:
                news = scraper.scrape()
                for item in news:
                    # Enrich with tickers
                    text_to_scan = f"{item['title']} {item.get('summary', '')}"
                    item['tickers'] = list(extract_tickers(text_to_scan))
                
                all_news.extend(news)
                print(f"Scraped {len(news)} items from {scraper.__class__.__name__}")
            except Exception as e:
                print(f"Error in {scraper.__class__.__name__}: {e}")
        
        # Deduplicate results based on URL
        unique_news = {item['url']: item for item in all_news}.values()
        return list(unique_news)

if __name__ == "__main__":
    manager = ScraperManager()
    async def test():
        news = await manager.run_all()
        print(f"\nTotal unique news items: {len(news)}")
        for item in news[:10]:
            print(f"[{item['source']}] {item['title']} - {item['url']}")

    asyncio.run(test())
