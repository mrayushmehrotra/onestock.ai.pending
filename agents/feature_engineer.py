import numpy as np
import pandas as pd
import joblib
from agents.base_agent import BaseAgent
from utils.logger import logger
from config.settings import settings

class FeatureEngineerAgent(BaseAgent):
    name = "FeatureEngineerAgent"

    def __init__(self):
        super().__init__()
        self.scaler = None
        try:
            self.scaler = joblib.load(settings.SCALER_PATH)
        except:
            logger.warning("Scaler not found at startup. Will need to be loaded or created before prediction.")

    async def run(self, market_data, tech_data, fund_data, sentiment_data) -> list[dict]:
        feature_vectors = []
        for symbol in market_data:
            df = market_data[symbol]
            tech = tech_data.get(symbol, {})
            fund = fund_data.get(symbol, {})
            sent = sentiment_data.get(symbol, 0.0)

            if not tech: continue

            close = df["Close"].iloc[-1]
            vol = df["Volume"].iloc[-1]
            
            # Simple feature construction
            raw_features = [
                close / df["Close"].mean(),                              # close_norm
                vol / df["Volume"].mean(),                               # volume_norm
                (close - df["Close"].iloc[-5]) / df["Close"].iloc[-5] if len(df) > 5 else 0, # price_change_5d
                tech.get("rsi", 50) / 100,
                tech.get("macd_hist", 0),
                tech.get("adx", 0) / 100,
                tech.get("stoch_k", 0) / 100,
                float(tech.get("golden_cross", False)),
                float(tech.get("price_above_ema20", False)),
                float(tech.get("volume_spike", False)),
                self._safe_float(fund.get("pe_ratio"), 25) / 100,
                self._safe_float(fund.get("pb_ratio"), 1) / 20,
                self._safe_float(fund.get("roe"), 15) / 100,
                self._safe_float(fund.get("debt_equity"), 0) / 5,
                sent
            ]
            
            feature_vectors.append({
                "symbol": symbol,
                "features": raw_features
            })
        
        return feature_vectors

    def _safe_float(self, val, default):
        try:
            return float(val) if val is not None else default
        except:
            return default
