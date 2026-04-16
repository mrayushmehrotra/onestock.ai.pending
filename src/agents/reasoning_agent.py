from src.models.reasoning_engine import ReasoningModel
from src.utils.seasonal_engine import SeasonalEngine
from src.utils.weather_fetcher import WeatherFetcher
from src.utils.direct_fetcher import DirectFetcher
import asyncio

class ReasoningAgent:
    def __init__(self):
        self.model = ReasoningModel()
        self.seasonal = SeasonalEngine()
        self.weather = WeatherFetcher()
        self.fetcher = DirectFetcher()

    async def reason_on_news(self, news_item: dict, fetch_content: bool = False):
        """
        Main logic: News + Context -> Reasoning -> Prediction
        """
        title = news_item.get('title', '')
        summary = news_item.get('summary', '')
        url = news_item.get('url', '')
        tickers = news_item.get('tickers', [])
        
        # Optionally fetch full article content for deeper AI reasoning
        article_text = ""
        if fetch_content and url:
            article_text = self.fetcher.get_clean_text(url) or ""
            summary = (summary + "\n" + article_text)[:2000] # Limit for AI context
        
        # 1. Get Context
        seasonal_context = self.seasonal.get_current_seasonal_context()
        weather_data = await self.weather.get_weather_metric("Delhi") # Default to Delhi
        
        # 2. Build Prompt for CoT
        prompt = (
            f"SYSTEM: You are an Indian Stock Market Analyst. Always perform reasoning first.\n"
            f"CONTEXT:\n"
            f"- Season: {seasonal_context['season']} ({seasonal_context['reasoning_hint']})\n"
            f"- Temperature: {weather_data['temp']}°C\n"
            f"NEWS: {title}\n"
            f"SUMMARY: {summary}\n"
            f"TICKERS: {', '.join(tickers)}\n"
            f"TASK: Reason about how the news and season impact these stocks and provide a prediction."
        )
        
        # 3. Generate Reasoning
        # Note: In real setup, self.model.load() should be called once
        result = self.model.generate_reasoning(prompt)
        
        return {
            "news": title,
            "tickers": tickers,
            "reasoning": result,
            "season": seasonal_context['season'],
            "weather": weather_data
        }

if __name__ == "__main__":
    agent = ReasoningAgent()
    async def test():
        res = await agent.reason_on_news({
            "title": "SpiceJet shares soar 18%",
            "tickers": ["SPICEJET"],
            "summary": "Increased demand for travel noted."
        })
        print(res)
    
    asyncio.run(test())
