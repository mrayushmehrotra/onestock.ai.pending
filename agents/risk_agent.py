from agents.base_agent import BaseAgent
from utils.logger import logger

class RiskAgent(BaseAgent):
    name = "RiskAgent"

    async def run(self, predictions: list[dict], market_data: dict) -> list[dict]:
        final_picks = []
        for pred in predictions:
            symbol = pred["symbol"]
            df = market_data.get(symbol)
            
            if df is None or df.empty:
                continue

            # Basic risk checks
            close = df["Close"].iloc[-1]
            prev_close = df["Close"].iloc[-2]
            day_change = abs(close - prev_close) / prev_close
            avg_vol = df["Volume"].rolling(20).mean().iloc[-1]

            # 1. Liquidity check
            if avg_vol < 100_000:
                pred["risk_flag"] = "low_liquidity"
                pred["cleared"] = False
            # 2. Circuit breaker check (10% limit)
            elif day_change > 0.09:
                pred["risk_flag"] = "near_circuit_breaker"
                pred["cleared"] = False
            else:
                pred["risk_flag"] = None
                pred["cleared"] = True
            
            final_picks.append(pred)
            
        return [p for p in final_picks if p["cleared"]]
