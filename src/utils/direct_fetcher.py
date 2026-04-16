import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict

class DirectFetcher:
    """
    Directly fetches website content using requests and BeautifulSoup.
    Optimized for feeding clean text to the AI reasoning engine.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        }

    def get_clean_text(self, url: str) -> Optional[str]:
        try:
            print(f"Directly fetching: {url}...")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Remove noise
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()
            
            # Get main text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Basic cleaning: remove empty lines and limit length for AI context
            lines = [line for line in text.split('\n') if len(line) > 20]
            clean_text = '\n'.join(lines[:100]) # Limit to first 100 relevant blocks
            
            return clean_text
            
        except Exception as e:
            print(f"Direct fetch failed for {url}: {e}")
            return None

if __name__ == "__main__":
    fetcher = DirectFetcher()
    # Test with a live URL
    content = fetcher.get_clean_text("https://economictimes.indiatimes.com/markets/stocks/news")
    if content:
        print(f"Extracted {len(content)} characters.")
        print("Sample content for AI:")
        print(content[:500] + "...")
