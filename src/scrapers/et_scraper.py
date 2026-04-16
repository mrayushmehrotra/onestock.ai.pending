from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime

class ETScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://economictimes.indiatimes.com"
        self.markets_url = f"{self.base_url}/markets"

    def scrape(self) -> List[Dict[str, Any]]:
        html = self.fetch_page(self.markets_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        news_items = []
        
        # Consistent selector found by subagent
        links = soup.select('a.font_faus')
        
        for link in links:
            title = link.get('title', '').replace('Link for ', '').strip()
            href = link.get('href', '')
            
            if not title and link.find('span'):
                title = link.find('span').get_text(strip=True)
            elif not title:
                title = link.get_text(strip=True)

            if title and href:
                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                news_items.append({
                    "title": title,
                    "url": full_url,
                    "source": "Economic Times",
                    "scraped_at": datetime.now().isoformat()
                })
        
        # Deduplicate
        unique_news = {item['url']: item for item in news_items}.values()
        return list(unique_news)

if __name__ == "__main__":
    scraper = ETScraper()
    results = scraper.scrape()
    for item in results[:5]:
        print(f"Title: {item['title']}\nURL: {item['url']}\n")
