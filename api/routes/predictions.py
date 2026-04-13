from fastapi import APIRouter, BackgroundTasks
from agents.orchestrator import OrchestratorAgent
from utils.logger import logger

router = APIRouter()

@router.get("/")
async def get_latest_predictions():
    # In a real app, this would fetch from PostgreSQL
    return {"predictions": [], "count": 0}

@router.post("/run")
async def run_prediction_job(background_tasks: BackgroundTasks):
    # This symbols list would normally come from NIFTY 500
    symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
    
    async def run_job():
        orchestrator = OrchestratorAgent(symbols)
        results = await orchestrator.run()
        # Save results to DB logic here
        logger.info(f"Manual run finished with {len(results)} picks")
    
    background_tasks.add_task(run_job)
    return {"message": "Prediction job started in background"}
