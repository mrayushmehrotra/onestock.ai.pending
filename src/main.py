from fastapi import FastAPI, BackgroundTasks
from src.agents.reasoning_agent import ReasoningAgent
from src.scrapers.manager import ScraperManager
from src.utils.scheduler import NewsScheduler
import uvicorn

app = FastAPI(title="OneStock AI")
agent = ReasoningAgent()
scraper_manager = ScraperManager()

# Initialize scheduler on startup
@app.on_event("startup")
async def startup_event():
    scheduler = NewsScheduler()
    scheduler.start()

@app.get("/")
async def root():
    return {"message": "OneStock AI Backend Active", "reasoning_engine": "SmolLM-135M"}

@app.post("/predict")
async def predict_stock(news_title: str):
    """
    Manually trigger prediction for a specific news headline.
    """
    # Simple mock item for reasoning
    item = {
        "title": news_title,
        "tickers": ["UNKNOWN"], # Ticker extractor would be used here normally
        "summary": "Manual analysis requested."
    }
    result = await agent.reason_on_news(item)
    return result

@app.get("/daily-analysis")
async def daily_analysis():
    """
    Returns reasoning for the top 5 latest news items.
    """
    # In a real setup, this would fetch from the database
    news = await scraper_manager.run_all()
    analysis = []
    for item in news[:5]:
        res = await agent.reason_on_news(item)
        analysis.append(res)
    
    return {"analysis": analysis}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
