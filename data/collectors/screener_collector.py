import httpx
from utils.logger import logger

class ScreenerCollector:
    @staticmethod
    async def fetch_fundamentals(symbol: str) -> dict:
        url = f"https://www.screener.in/api/company/{symbol}/?format=json"
        logger.info(f"Fetching fundamentals for {symbol} from Screener.in")
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                logger.error(f"Failed to fetch credentials from Screener: {resp.status_code}")
                return {}
            
            data = resp.json()
            return {
                "pe_ratio": data.get("ratios", {}).get("Price to Earning"),
                "pb_ratio": data.get("ratios", {}).get("Price to book value"),
                "eps": data.get("ratios", {}).get("EPS in Rs"),
                "roe": data.get("ratios", {}).get("Return on equity"),
                "debt_equity": data.get("ratios", {}).get("Debt to equity"),
                "promoter_holding": data.get("shareholding", {}).get("promoter"),
                "industry": data.get("industry")
            }

if __name__ == "__main__":
    import asyncio
    fundamental_data = asyncio.run(ScreenerCollector.fetch_fundamentals("RELIANCE"))
    print(fundamental_data)
