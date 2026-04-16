import asyncio
import sys
import os
sys.path.append(os.path.abspath("src"))

from src.scrapers.manager import ScraperManager
from src.utils.ticker_extractor import extract_tickers
from src.utils.seasonal_engine import SeasonalEngine

async def get_pick():
    manager = ScraperManager()
    seasonal = SeasonalEngine()
    
    news = await manager.run_all()
    context = seasonal.get_current_seasonal_context()
    
    print(f"DEBUG: Current Season: {context['season']}")
    
    picks = []
    for item in news:
        tickers = extract_tickers(item['title'])
        if not tickers:
            continue
            
        # Strategy 1: News Sentiment/Impact
        sentiment = "Neutral"
        if any(word in item['title'].upper() for word in ["SURGE", "RISE", "JUMP", "UP", "BUY", "PROFIT", "BEAT"]):
            sentiment = "Bullish"
        
        # Strategy 2: Seasonal Alignment
        seasonal_match = any(t in context['target_sectors'] for t in tickers)
        
        for t in tickers:
            picks.append({
                "ticker": t,
                "news": item['title'],
                "sentiment": sentiment,
                "seasonal_match": seasonal_match
            })
            
    # Filter for Bullish + Seasonal Match if possible
    final_picks = [p for p in picks if p['sentiment'] == "Bullish"]
    
    if final_picks:
        best = final_picks[0]
        print(f"\n--- TODAY'S TOP PICK (ALIGNED WITH LOGIC) ---")
        print(f"STOCK: {best['ticker']}")
        print(f"REASON: {best['news']}")
    else:
        # Fallback to the first bullish news found
        print(f"\n--- ANALYZING LIVE DATA ---")
        for p in picks[:10]:
            print(f"Found: {p['ticker']} | Sentiment: {p['sentiment']} | News: {p['news']}")

if __name__ == "__main__":
    asyncio.run(get_pick())
