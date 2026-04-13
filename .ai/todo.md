# Stock Prediction Backend - Todo Checklist

> **Note:** Using only free tools and APIs. No paid subscriptions required.

## 1. Project Setup
- [ ] Create `stock_prediction/` directory structure
- [ ] Create all subdirectories (agents, model, data, api, db, scheduler, backtesting, utils, config, tests)
- [ ] Create `__init__.py` files for all Python packages
- [ ] Create `.env.example` file with all environment variables
- [ ] Create `requirements.txt` with all dependencies

## 2. Configuration & Settings
- [ ] Create `config/settings.py` with Pydantic BaseSettings
- [ ] Define DATABASE_URL, REDIS_URL settings
- [ ] ~~Define API keys settings (Zerodha, Angel One)~~ - Removed (paid)
- [ ] Define Telegram alert settings (free)
- [ ] Define model paths
- [ ] Define prediction config (FORWARD_DAYS, BOOM_THRESHOLD)

## 3. Database Layer
- [ ] Create `db/models.py` with SQLAlchemy ORM models
  - [ ] `prediction_runs` table
  - [ ] `predictions` table
  - [ ] `outcomes` table
  - [ ] `daily_prices` table
- [ ] Create `db/session.py` for DB session management
- [ ] Set up Alembic for migrations
- [ ] Create initial migration

## 4. Utility Layer
- [ ] Create `utils/logger.py` with Loguru setup
- [ ] Create `utils/alerts.py` for Telegram notifications (free)
- [ ] Create `utils/cache.py` for Redis caching layer (free)

## 5. Base Agent Class
- [ ] Create `agents/base_agent.py`
- [ ] Implement `AgentResult` dataclass
- [ ] Implement `BaseAgent` abstract class with `safe_run` method

## 6. Data Collection Layer (Free Sources Only)
- [ ] Create `data/collectors/nse_collector.py` (using yfinance - free)
- [ ] Create `data/collectors/bse_collector.py` (using yfinance - free)
- [ ] Create `data/collectors/news_collector.py` (web scraping - free)
- [ ] Create `data/collectors/screener_collector.py` (scraping - free)
- [ ] Set up `data/raw/` directory structure

## 7. Agent Implementations

### 7.1 Data Fetcher Agent
- [ ] Create `agents/data_fetcher.py`
- [ ] Implement `fetch()` method using yfinance (free)
- [ ] Add support for NSE (.NS) and BSE (.BO) tickers

### 7.2 Technical Analyst Agent
- [ ] Create `agents/technical_analyst.py`
- [ ] Implement RSI, MACD, Bollinger Bands
- [ ] Implement EMA (20, 50, 200)
- [ ] Implement ATR, OBV, ADX, Stochastic
- [ ] Implement derived signals (golden_cross, volume_spike)

### 7.3 Fundamental Analyst Agent
- [ ] Create `agents/fundamental_analyst.py`
- [ ] Implement Screener.in scraping (free)
- [ ] Extract P/E, P/B, EPS, ROE, ROCE, Debt/Equity
- [ ] Extract promoter/FII holding, revenue/profit growth

### 7.4 Sentiment Agent
- [ ] Create `agents/sentiment_agent.py`
- [ ] Set up VADER (free, local, no API key needed)
- [ ] ~~Set up FinBERT pipeline~~ - Optional (heavy, uses local GPU)
- [ ] Implement headline fetching from free sources (Economic Times, Moneycontrol)
- [ ] Implement VADER fallback for reliability

### 7.5 Feature Engineer Agent
- [ ] Create `agents/feature_engineer.py`
- [ ] Define FEATURE_KEYS list
- [ ] Implement `build()` method for feature vectors
- [ ] Implement normalization and scaling
- [ ] Load and use scaler

### 7.6 Prediction Agent
- [ ] Create `agents/prediction_agent.py`
- [ ] Implement model loading from pickle
- [ ] Implement `predict()` method
- [ ] Add confidence levels

### 7.7 Risk Agent
- [ ] Create `agents/risk_agent.py`
- [ ] Implement volatility check (ATR %)
- [ ] Implement liquidity check
- [ ] Implement circuit breaker filter

### 7.8 Orchestrator Agent
- [ ] Create `agents/orchestrator.py`
- [ ] Implement 5-phase execution flow
- [ ] Add parallel async execution
- [ ] Implement result aggregation

## 8. Model Training Pipeline

### 8.1 Model Architecture (XGBoost - Recommended, Free)
- [ ] Create `model/architectures/xgboost_model.py`
- [ ] ~~Create LSTM model~~ - Skip (needs more data/compute)
- [ ] ~~Create Transformer model~~ - Skip (complex, compute-heavy)

### 8.2 Training Pipeline
- [ ] Create `model/train.py`
- [ ] Implement `create_labels()` function
- [ ] Implement TimeSeriesSplit cross-validation
- [ ] Implement XGBoost training with class imbalance handling
- [ ] Save model and scaler artifacts

### 8.3 Evaluation
- [ ] Create `model/evaluate.py`
- [ ] Implement classification metrics
- [ ] Implement confusion matrix
- [ ] Implement feature importance

### 8.4 Export
- [ ] Create `model/export.py`
- [ ] Implement model artifact saving
- [ ] Create `model/saved/` directory

## 9. API Layer

### 9.1 FastAPI Setup
- [ ] Create `api/main.py` with FastAPI app
- [ ] Include routers with prefix

### 9.2 Routes
- [ ] Create `api/routes/health.py` - GET /health
- [ ] Create `api/routes/predictions.py` - GET /predictions, POST /predictions/run
- [ ] Create `api/routes/stocks.py` - GET /stocks/{symbol}

### 9.3 Schemas
- [ ] Create `api/schemas.py` with Pydantic models

## 10. Scheduler & Job Queue
- [ ] Create `scheduler/jobs.py`
- [ ] Set up APScheduler with AsyncIOScheduler
- [ ] Configure morning run (9:30 AM IST weekdays)
- [ ] Configure midday run (1:00 PM IST weekdays)
- [ ] Implement NSE holiday detection
- [ ] Implement result saving and Telegram alerts (free)

## 11. Backtesting Module
- [ ] Create `backtesting/engine.py`
- [ ] Implement backtest runner
- [ ] Create `backtesting/metrics.py`
- [ ] Implement Sharpe ratio calculation
- [ ] Implement max drawdown calculation

## 12. Docker Setup
- [ ] Create `docker-compose.yml`
  - [ ] API service
  - [ ] Scheduler service
  - [ ] PostgreSQL service (free)
  - [ ] Redis service (free)
- [ ] Create Dockerfile

## 13. Testing
- [ ] Create `tests/test_agents.py`
- [ ] Create `tests/test_model.py`
- [ ] Create `tests/test_api.py`
- [ ] Ensure pytest-asyncio configuration

## 14. Documentation
- [ ] Create README.md with setup instructions
- [ ] Add usage examples
- [ ] Add API documentation

## 15. Deployment Checklist
- [ ] Fill `.env` file with Telegram bot token (free)
- [ ] Train model and verify `model/saved/model.pkl` exists
- [ ] Run database migrations (`alembic upgrade head`)
- [ ] Load NSE holiday calendar
- [ ] Create Telegram bot and set token (free)
- [ ] Run backtesting on last 6 months
- [ ] ~~Verify rate limits for paid APIs~~ - Removed
- [ ] Test Docker Compose deployment locally

---

## Free Data Sources Used
| Source | Data | Cost |
|--------|------|------|
| `yfinance` | OHLCV 1y+ daily/hourly | Free |
| NSE Bhav Copy | Delivery %, circuit limits | Free |
| Screener.in | Fundamentals (P/E, EPS, etc.) | Free (scraping) |
| Economic Times | News headlines | Free (scraping) |
| VADER | Sentiment analysis | Free (local) |
| PostgreSQL | Database | Free |
| Redis | Caching | Free |
| Telegram | Alerts | Free |
