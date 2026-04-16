import nsepython
from typing import Dict, Any, List
import pandas as pd

class NSEProvider:
    """
    Provides stock and market data using NSE APIs.
    """
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Fetch real-time quote for a given symbol."""
        try:
            # Note: nsepython uses NSE's live website which can be flaky
            quote = nsepython.nse_quote_meta(symbol)
            return quote
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return {}

    def get_market_status(self) -> str:
        """Check if the market is open."""
        try:
            return nsepython.nse_marketStatus()
        except:
            return "CLOSE"

    def get_top_gainers(self) -> List[Dict[str, Any]]:
        """Fetch top gainers of the day."""
        try:
            gainers = nsepython.nse_get_top_gainers()
            return gainers.to_dict('records') if isinstance(gainers, pd.DataFrame) else gainers
        except:
            return []

if __name__ == "__main__":
    provider = NSEProvider()
    print(f"Market Status: {provider.get_market_status()}")
    # Small test
    # print(provider.get_stock_quote("RELIANCE"))
