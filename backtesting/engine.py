import pandas as pd
from backtesting.metrics import calculate_sharpe_ratio, calculate_max_drawdown
from utils.logger import logger

class BacktestEngine:
    def __init__(self, predictions_df: pd.DataFrame, price_data: pd.DataFrame):
        self.predictions = predictions_df
        self.prices = price_data

    def run(self, forward_days: int = 10):
        logger.info(f"Running backtest for {len(self.predictions)} trades...")
        results = []
        
        for _, row in self.predictions.iterrows():
            symbol = row["symbol"]
            date = row["date"]
            
            # Find entry and exit prices
            symbol_prices = self.prices[self.prices["symbol"] == symbol]
            entry_price_row = symbol_prices[symbol_prices["Date"] == date]
            
            if entry_price_row.empty: continue
            
            entry_price = entry_price_row["Close"].iloc[0]
            
            # Find exit price (n days later)
            future_prices = symbol_prices[symbol_prices["Date"] > date].head(forward_days)
            if future_prices.empty: continue
            
            exit_price = future_prices["Close"].iloc[-1]
            ret = (exit_price - entry_price) / entry_price
            results.append(ret)
            
        returns_series = pd.Series(results)
        return {
            "total_trades": len(results),
            "win_rate": (returns_series > 0).mean() if not returns_series.empty else 0,
            "avg_return": returns_series.mean() if not returns_series.empty else 0,
            "sharpe_ratio": calculate_sharpe_ratio(returns_series),
            "max_drawdown": calculate_max_drawdown(returns_series)
        }
