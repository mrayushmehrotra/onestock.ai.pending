from fastapi import FastAPI
from api.routes import health, predictions, stocks
from utils.logger import logger

app = FastAPI(
    title="OneStock.ai Prediction API",
    description="Backend for Indian Stock Market Momentum Prediction",
    version="1.0.0"
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["System"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
app.include_router(stocks.router, prefix="/stocks", tags=["Market Data"])

@app.on_event("startup")
async def startup_event():
    logger.info("OneStock.ai API is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("OneStock.ai API is shutting down...")
