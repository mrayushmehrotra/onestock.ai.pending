import yfinance as yf
import pandas as pd
from agents.base_agent import BaseAgent
from utils.logger import logger

class DataFetcherAgent(BaseAgent):
    name = "DataFetcherAgent"

    async def run(self, symbols: list[str]) -> dict[str, pd.DataFrame]:
        results = {}
        for symbol in symbols:
            try:
                # Try NSE first
                ticker = yf.Ticker(f"{symbol}.NS")
                df = ticker.history(period="2y")
                if df.empty:
                    # Try BSE
                    ticker = yf.Ticker(f"{symbol}.BO")
                    df = ticker.history(period="2y")
                
                if not df.empty:
                    df.dropna(inplace=True)
                    results[symbol] = df
                    logger.info(f"Successfully fetched data for {symbol}")
                else:
                    logger.warning(f"No data found for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching {symbol}: {e}")
        
        return results
