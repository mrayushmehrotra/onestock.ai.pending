import yfinance as yf
import pandas as pd
from utils.logger import logger

class BSECollector:
    @staticmethod
    def fetch_historical(symbol: str, period: str = "5y") -> pd.DataFrame:
        ticker_symbol = f"{symbol}.BO"
        logger.info(f"Fetching historical data for {ticker_symbol} from yfinance")
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period)
        return df

if __name__ == "__main__":
    collector = BSECollector()
    data = collector.fetch_historical("500325") # Reliance BSE
    logger.info(f"Fetched {len(data)} rows for BSE symbol")
