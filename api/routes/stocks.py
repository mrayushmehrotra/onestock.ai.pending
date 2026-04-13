from fastapi import APIRouter, HTTPException
from data.collectors.nse_collector import NSECollector
from data.collectors.screener_collector import ScreenerCollector

router = APIRouter()

@router.get("/{symbol}")
async def get_stock_analysis(symbol: str):
    try:
        # Simplified example
        fundamentals = await ScreenerCollector.fetch_fundamentals(symbol)
        return {
            "symbol": symbol,
            "analysis": fundamentals
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
