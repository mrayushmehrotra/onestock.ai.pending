from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime

class MoneyControlScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.moneycontrol.com"
        self.markets_url = f"{self.base_url}/news/business/markets/"

    def scrape(self) -> List[Dict[str, Any]]:
        html = self.fetch_page(self.markets_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        news_items = []
        
        # Selector identified: li.clearfix
        items = soup.select('li.clearfix')
        
        for li in items:
            a_tag = li.find('a')
            h2_tag = li.find('h2')
            
            if not a_tag:
                continue
                
            title = a_tag.get('title') or (h2_tag.get_text(strip=True) if h2_tag else a_tag.get_text(strip=True))
            href = a_tag.get('href')
            
            if title and href and '/news/' in href:
                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                
                # Try to get summary if available in 'p' tag
                p_tag = li.find('p')
                summary = p_tag.get_text(strip=True) if p_tag else ""

                news_items.append({
                    "title": title,
                    "summary": summary,
                    "url": full_url,
                    "source": "MoneyControl",
                    "scraped_at": datetime.now().isoformat()
                })
        
        # Deduplicate
        unique_news = {item['url']: item for item in news_items}.values()
        return list(unique_news)

if __name__ == "__main__":
    scraper = MoneyControlScraper()
    results = scraper.scrape()
    for item in results[:5]:
        print(f"Title: {item['title']}\nSummary: {item['summary']}\nURL: {item['url']}\n")
