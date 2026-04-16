from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime

class MintScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.livemint.com"
        self.markets_url = f"{self.base_url}/markets"

    def scrape(self) -> List[Dict[str, Any]]:
        html = self.fetch_page(self.markets_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        news_items = []
        
        # Selectors identified: h2.headline a or Listing story containers
        # Trying a few variations based on observation
        links = soup.select('h2.headline a') or soup.select('.listing-story h2 a')
        
        for link in links:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            if title and href and len(title) > 10:
                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                news_items.append({
                    "title": title,
                    "url": full_url,
                    "source": "LiveMint",
                    "scraped_at": datetime.now().isoformat()
                })
        
        # Deduplicate
        unique_news = {item['url']: item for item in news_items}.values()
        return list(unique_news)

if __name__ == "__main__":
    scraper = MintScraper()
    results = scraper.scrape()
    for item in results[:5]:
        print(f"Title: {item['title']}\nURL: {item['url']}\n")
