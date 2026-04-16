import json
import random
from typing import List, Dict, Any

class ReasoningDatasetBuilder:
    """
    Generates a Chain-of-Thought (CoT) dataset for Indian stock market reasoning.
    """
    
    def generate_sample(self, news_title: str, tickers: List[str], season: str, weather_temp: float) -> Dict[str, str]:
        # Simple logical templates for reasoning
        thought_process = []
        
        # Step 1: Analyze News
        thought_process.append(f"Analyzing news: '{news_title}'.")
        if tickers:
            thought_process.append(f"Identified key tickers: {', '.join(tickers)}.")
        
        # Step 2: Consider Seasonality
        thought_process.append(f"Current season is {season} with a temperature of {weather_temp}°C.")
        
        # Step 3: Combine logic
        potential_impact = "Neutral"
        if "RELIANCE" in tickers or "TCS" in tickers:
            potential_impact = "Significant for Nifty50"
        
        if season == "SUMMER" and weather_temp > 35:
            thought_process.append("High temperature in summer significantly boosts demand for Solar and Cooling sectors.")
            potential_impact = "Bullish for Power/Appliances"
        elif season == "WINTER" and weather_temp < 15:
            thought_process.append("Cold winter increases demand for thermal wear and power-intensive heating.")
            potential_impact = "Bullish for Textiles/Power"

        thought = " ".join(thought_process)
        
        return {
            "prompt": f"News: {news_title}\nTickers: {', '.join(tickers)}\nSeason: {season}\nTemp: {weather_temp}°C",
            "reasoning": thought,
            "prediction": f"Market Direction: {potential_impact}"
        }

    def build_synthetic_set(self, count: int = 100) -> List[Dict[str, str]]:
        dataset = []
        seasons = ["SUMMER", "WINTER", "MONSOON", "AUTUMN"]
        sample_news = [
            "RBI keeps repo rate unchanged",
            "FIIs turn net buyers in Indian equities",
            "Crude oil prices spike amid Middle East tensions",
            "Monsoon progress remains on track across India",
            "Corporate earnings for Q4 show resilience"
        ]
        
        for _ in range(count):
            dataset.append(self.generate_sample(
                news_title=random.choice(sample_news),
                tickers=random.sample(["RELIANCE", "TCS", "HDFCBANK", "SBIN", "WIPRO"], k=random.randint(1, 3)),
                season=random.choice(seasons),
                weather_temp=random.randint(10, 45)
            ))
            
        return dataset

if __name__ == "__main__":
    builder = ReasoningDatasetBuilder()
    data = builder.build_synthetic_set(10)
    with open("data/reasoning_dataset_v1.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Generated 10 reasoning samples.")
