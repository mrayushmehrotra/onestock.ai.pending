from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/stockdb"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # API Keys
    ZERODHA_API_KEY: Optional[str] = None
    ZERODHA_ACCESS_TOKEN: Optional[str] = None
    ANGEL_ONE_API_KEY: Optional[str] = None

    # Alerts
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    # Model
    MODEL_PATH: str = "model/saved/model.pkl"
    SCALER_PATH: str = "model/saved/scaler.pkl"

    # Trading universe
    DEFAULT_UNIVERSE: str = "NIFTY500"

    # Prediction config
    FORWARD_DAYS: int = 10
    BOOM_THRESHOLD: float = 0.08

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
