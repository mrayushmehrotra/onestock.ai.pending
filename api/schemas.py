from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PredictionResponse(BaseModel):
    symbol: str
    boom_score: float
    confidence: str
    risk_flag: Optional[str] = None
    cleared: bool

class PredictionRunResponse(BaseModel):
    run_at: datetime
    top_picks: List[PredictionResponse]
    total_analyzed: int
    total_cleared: int
