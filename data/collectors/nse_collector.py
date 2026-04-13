import yfinance as yf
import pandas as pd
from utils.logger import logger
import os

class NSECollector:
    @staticmethod
    def fetch_historical(symbol: str, period: str = "5y") -> pd.DataFrame:
        ticker_symbol = f"{symbol}.NS"
        logger.info(f"Fetching historical data for {ticker_symbol} from yfinance")
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period)
        return df

    @staticmethod
    def save_to_csv(df: pd.DataFrame, symbol: str):
        path = f"data/raw/{symbol}_historical.csv"
        df.to_csv(path)
        logger.info(f"Saved {symbol} data to {path}")

if __name__ == "__main__":
    # Example usage
    collector = NSECollector()
    data = collector.fetch_historical("RELIANCE")
    collector.save_to_csv(data, "RELIANCE")
