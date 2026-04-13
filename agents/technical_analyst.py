import pandas as pd
import pandas_ta as ta
from agents.base_agent import BaseAgent
from utils.logger import logger

class TechnicalAnalystAgent(BaseAgent):
    name = "TechnicalAnalystAgent"

    async def run(self, market_data: dict[str, pd.DataFrame]) -> dict[str, dict]:
        results = {}
        for symbol, df in market_data.items():
            if df.empty or len(df) < 200:
                logger.warning(f"Insufficient data for tech analysis of {symbol}")
                continue
            
            # Compute technical indicators
            df.ta.rsi(length=14, append=True)
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            df.ta.bbands(length=20, std=2, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.ema(length=200, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.obv(append=True)
            df.ta.adx(length=14, append=True)
            df.ta.stoch(k=14, d=3, append=True)

            latest = df.iloc[-1]
            results[symbol] = {
                "rsi": latest.get("RSI_14"),
                "macd_hist": latest.get("MACDh_12_26_9"),
                "bb_upper": latest.get("BBU_20_2.0"),
                "bb_lower": latest.get("BBL_20_2.0"),
                "ema_20": latest.get("EMA_20"),
                "ema_50": latest.get("EMA_50"),
                "ema_200": latest.get("EMA_200"),
                "atr": latest.get("ATRr_14"),
                "obv": latest.get("OBV"),
                "adx": latest.get("ADX_14"),
                "stoch_k": latest.get("STOCHk_14_3_3"),
                # Signals
                "golden_cross": bool(latest.get("EMA_50", 0) > latest.get("EMA_200", 0)),
                "price_above_ema20": bool(latest["Close"] > latest.get("EMA_20", 0)),
                "volume_spike": bool(latest["Volume"] > df["Volume"].rolling(20).mean().iloc[-1] * 1.5)
            }
        
        return results
