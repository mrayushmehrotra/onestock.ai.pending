import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, headers: Dict[str, str] = None):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_page(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        pass
