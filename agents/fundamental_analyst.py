from agents.base_agent import BaseAgent
from data.collectors.screener_collector import ScreenerCollector
from utils.logger import logger
import asyncio

class FundamentalAnalystAgent(BaseAgent):
    name = "FundamentalAnalystAgent"

    async def run(self, symbols: list[str]) -> dict[str, dict]:
        results = {}
        # Fetch fundamentals in parallel
        tasks = [ScreenerCollector.fetch_fundamentals(symbol) for symbol in symbols]
        fundamental_data_list = await asyncio.gather(*tasks)
        
        for symbol, data in zip(symbols, fundamental_data_list):
            if data:
                results[symbol] = data
                logger.info(f"Fundamental analysis complete for {symbol}")
            else:
                logger.warning(f"No fundamental data for {symbol}")
        
        return results
