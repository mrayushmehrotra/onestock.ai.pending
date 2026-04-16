from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime

class BSScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.business-standard.com"
        self.markets_url = f"{self.base_url}/markets"

    def scrape(self) -> List[Dict[str, Any]]:
        html = self.fetch_page(self.markets_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        news_items = []
        
        # Selectors identified: a.smallcard-title and a p
        # We will try both
        
        # Strategy 1: smallcard-title
        small_cards = soup.select('a.smallcard-title')
        for link in small_cards:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            if title and href:
                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                news_items.append({
                    "title": title,
                    "url": full_url,
                    "source": "Business Standard",
                    "scraped_at": datetime.now().isoformat()
                })

        # Strategy 2: a p (often in main grid)
        p_links = soup.select('a p')
        for p in p_links:
            a_tag = p.find_parent('a')
            if not a_tag:
                continue
            title = p.get_text(strip=True)
            href = a_tag.get('href', '')
            if title and href and len(title) > 20: # Filter for likely headlines
                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                news_items.append({
                    "title": title,
                    "url": full_url,
                    "source": "Business Standard",
                    "scraped_at": datetime.now().isoformat()
                })
        
        # Deduplicate
        unique_news = {item['url']: item for item in news_items}.values()
        return list(unique_news)

if __name__ == "__main__":
    scraper = BSScraper()
    results = scraper.scrape()
    for item in results[:5]:
        print(f"Title: {item['title']}\nURL: {item['url']}\n")
