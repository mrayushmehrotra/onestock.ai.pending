import httpx
from bs4 import BeautifulSoup
from utils.logger import logger

class NewsCollector:
    @staticmethod
    async def fetch_et_headlines(symbol: str) -> list[str]:
        url = f"https://economictimes.indiatimes.com/topic/{symbol}"
        logger.info(f"Scraping ET headlines for {symbol} from {url}")
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                logger.error(f"Failed to fetch ET news: {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.text, "html.parser")
            headlines = [h.get_text(strip=True) for h in soup.select("h3.clr a")]
            return headlines[:15]

if __name__ == "__main__":
    import asyncio
    headlines = asyncio.run(NewsCollector.fetch_et_headlines("RELIANCE"))
    print(headlines)
