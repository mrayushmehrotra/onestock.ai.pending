# 🇮🇳 Indian Stock Market Prediction — Multi-Agent Backend Architecture

> Python-based multi-agent system using a locally trained AI model to predict high-momentum stocks on NSE/BSE.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Project Structure](#2-project-structure)
3. [Tech Stack](#3-tech-stack)
4. [Agent Architecture](#4-agent-architecture)
   - [Orchestrator Agent](#41-orchestrator-agent)
   - [Data Fetcher Agent](#42-data-fetcher-agent)
   - [Technical Analyst Agent](#43-technical-analyst-agent)
   - [Fundamental Analyst Agent](#44-fundamental-analyst-agent)
   - [Sentiment Agent](#45-sentiment-agent)
   - [Feature Engineering Agent](#46-feature-engineering-agent)
   - [Prediction Agent](#47-prediction-agent)
   - [Risk Agent](#48-risk-agent)
5. [Local AI Model](#5-local-ai-model)
   - [Model Options](#51-model-options)
   - [Training Pipeline](#52-training-pipeline)
   - [Data Sources for Training](#53-data-sources-for-training)
6. [Data Flow](#6-data-flow)
7. [API Layer](#7-api-layer)
8. [Scheduler & Job Queue](#8-scheduler--job-queue)
9. [Database Schema](#9-database-schema)
10. [Configuration & Environment](#10-configuration--environment)
11. [Installation & Setup](#11-installation--setup)
12. [Agent Communication Protocol](#12-agent-communication-protocol)
13. [Error Handling Strategy](#13-error-handling-strategy)
14. [Backtesting Module](#14-backtesting-module)
15. [Deployment](#15-deployment)

---

## 1. System Overview

```
NSE / BSE / News / Social Media
           │
           ▼
  ┌─────────────────────┐
  │  Orchestrator Agent │  ◄── Scheduler (APScheduler)
  └──────────┬──────────┘
             │ coordinates
    ┌────────┴────────────────────────────┐
    │         │            │              │
    ▼         ▼            ▼              ▼
 Data      Technical   Fundamental    Sentiment
 Fetcher   Analyst     Analyst        Agent
 Agent     Agent       Agent
    │         │            │              │
    └────────┬────────────────────────────┘
             │ feature vectors
             ▼
  ┌──────────────────────┐
  │ Feature Engineering  │
  │       Agent          │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────┐
  │  Local AI Model      │  (LSTM / XGBoost / Transformer)
  └──────────┬───────────┘
             │
      ┌──────┴──────┐
      ▼             ▼
 Prediction      Risk
 Agent           Agent
      │             │
      └──────┬──────┘
             ▼
      Final Report / Alert
      (FastAPI endpoint + Telegram/Email)
```

---

## 2. Project Structure

```
stock_prediction/
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py              # Abstract base class for all agents
│   ├── orchestrator.py            # Master controller
│   ├── data_fetcher.py            # NSE/BSE data fetching
│   ├── technical_analyst.py       # Technical indicator computation
│   ├── fundamental_analyst.py     # Fundamental data analysis
│   ├── sentiment_agent.py         # News & social sentiment scoring
│   ├── feature_engineer.py        # Feature vector construction
│   ├── prediction_agent.py        # Model inference
│   └── risk_agent.py              # Risk validation
│
├── model/
│   ├── train.py                   # Training pipeline
│   ├── evaluate.py                # Model evaluation
│   ├── export.py                  # Save model artifacts
│   ├── architectures/
│   │   ├── lstm_model.py
│   │   ├── xgboost_model.py
│   │   └── transformer_model.py
│   └── saved/
│       ├── model.pkl              # Trained model artifact
│       └── scaler.pkl             # Feature scaler
│
├── data/
│   ├── collectors/
│   │   ├── nse_collector.py       # NSE data via nsepy / Kite API
│   │   ├── bse_collector.py       # BSE data
│   │   ├── news_collector.py      # Moneycontrol / ET scraper
│   │   └── screener_collector.py  # Fundamentals from Screener.in
│   └── raw/                       # Raw CSV / Parquet data
│
├── api/
│   ├── main.py                    # FastAPI app entrypoint
│   ├── routes/
│   │   ├── predictions.py         # GET /predictions
│   │   ├── stocks.py              # GET /stocks/{symbol}
│   │   └── health.py              # GET /health
│   └── schemas.py                 # Pydantic models
│
├── db/
│   ├── models.py                  # SQLAlchemy ORM models
│   ├── session.py                 # DB session management
│   └── migrations/                # Alembic migrations
│
├── scheduler/
│   └── jobs.py                    # APScheduler job definitions
│
├── backtesting/
│   ├── engine.py                  # Backtesting runner
│   └── metrics.py                 # Sharpe ratio, drawdown etc.
│
├── utils/
│   ├── logger.py                  # Structured logging
│   ├── alerts.py                  # Telegram / email alerts
│   └── cache.py                   # Redis caching layer
│
├── config/
│   └── settings.py                # Pydantic settings (env-based)
│
├── tests/
│   ├── test_agents.py
│   ├── test_model.py
│   └── test_api.py
│
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 3. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11+ | Core runtime |
| Agent Framework | Custom async agents + `asyncio` | Multi-agent orchestration |
| Market Data | `nsepy`, `yfinance`, Zerodha Kite API | NSE/BSE OHLCV data |
| Technical Analysis | `pandas-ta`, `ta` | RSI, MACD, Bollinger etc. |
| Fundamental Data | `Screener.in` API / `requests` scraper | P/E, EPS, financials |
| Sentiment NLP | `transformers` (FinBERT) / `VADER` | News scoring |
| ML Model | `scikit-learn`, `xgboost`, `pytorch` | Prediction model |
| Feature Engineering | `pandas`, `numpy`, `scikit-learn` | Normalization, encoding |
| API | `FastAPI` + `uvicorn` | REST endpoints |
| Database | `PostgreSQL` + `SQLAlchemy` + `Alembic` | Persistence |
| Caching | `Redis` | Feature vector cache |
| Scheduler | `APScheduler` | Market-hours job scheduling |
| Task Queue | `Celery` + `Redis` | Async heavy tasks |
| Alerts | `python-telegram-bot` / `smtplib` | Notifications |
| Logging | `loguru` | Structured logs |
| Testing | `pytest` + `pytest-asyncio` | Unit & integration tests |
| Containerization | `Docker` + `docker-compose` | Deployment |

---

## 4. Agent Architecture

### 4.1 Orchestrator Agent

The master controller. Runs on a schedule tied to market hours (IST), coordinates all sub-agents, aggregates results, and triggers final output.

```python
# agents/orchestrator.py

import asyncio
from agents.data_fetcher import DataFetcherAgent
from agents.technical_analyst import TechnicalAnalystAgent
from agents.fundamental_analyst import FundamentalAnalystAgent
from agents.sentiment_agent import SentimentAgent
from agents.feature_engineer import FeatureEngineerAgent
from agents.prediction_agent import PredictionAgent
from agents.risk_agent import RiskAgent
from utils.logger import logger

class OrchestratorAgent:
    def __init__(self, symbols: list[str]):
        self.symbols = symbols

    async def run(self) -> list[dict]:
        logger.info(f"Orchestrator starting run for {len(self.symbols)} symbols")

        # Phase 1: Parallel data collection
        data_agent = DataFetcherAgent()
        sentiment_agent = SentimentAgent()

        market_data, sentiment_scores = await asyncio.gather(
            data_agent.fetch(self.symbols),
            sentiment_agent.analyze(self.symbols)
        )

        # Phase 2: Technical + Fundamental (depends on market data)
        tech_agent = TechnicalAnalystAgent()
        fund_agent = FundamentalAnalystAgent()

        technical_data, fundamental_data = await asyncio.gather(
            tech_agent.compute(market_data),
            fund_agent.analyze(self.symbols)
        )

        # Phase 3: Feature engineering
        feature_agent = FeatureEngineerAgent()
        feature_vectors = await feature_agent.build(
            market_data, technical_data, fundamental_data, sentiment_scores
        )

        # Phase 4: Prediction
        prediction_agent = PredictionAgent()
        predictions = await prediction_agent.predict(feature_vectors)

        # Phase 5: Risk filtering
        risk_agent = RiskAgent()
        final_picks = await risk_agent.filter(predictions, market_data)

        logger.info(f"Run complete. Top picks: {[p['symbol'] for p in final_picks[:5]]}")
        return final_picks
```

---

### 4.2 Data Fetcher Agent

Collects OHLCV, delivery %, FII/DII data from NSE/BSE.

```python
# agents/data_fetcher.py

import yfinance as yf
import pandas as pd
from agents.base_agent import BaseAgent

class DataFetcherAgent(BaseAgent):
    """
    Fetches OHLCV + volume data for NSE symbols.
    Primary: yfinance (suffix .NS for NSE, .BO for BSE)
    Alternative: Zerodha Kite API (real-time, requires subscription)
    """

    async def fetch(self, symbols: list[str]) -> dict[str, pd.DataFrame]:
        results = {}
        for symbol in symbols:
            ticker = yf.Ticker(f"{symbol}.NS")
            df = ticker.history(period="1y", interval="1d")
            df.dropna(inplace=True)
            results[symbol] = df
        return results

    # Data collected per symbol:
    # - Open, High, Low, Close, Volume (daily, 1 year)
    # - Delivery percentage (via NSE bhav copy parsing)
    # - 52-week high/low
    # - FII/DII net buy/sell (from NSE website or Trendlyne API)
```

**Key data sources:**

| Source | Data | Access |
|---|---|---|
| `yfinance` | OHLCV 1y+ daily/hourly | Free, no auth |
| NSE Bhav Copy | Delivery %, circuit limits | Free, daily CSV download |
| Zerodha Kite API | Real-time tick data | Paid, official SDK |
| Angel One SmartAPI | Real-time + historical | Free tier available |
| Trendlyne API | FII/DII, bulk/block deals | Paid |

---

### 4.3 Technical Analyst Agent

Computes indicators on OHLCV data using `pandas-ta`.

```python
# agents/technical_analyst.py

import pandas as pd
import pandas_ta as ta
from agents.base_agent import BaseAgent

class TechnicalAnalystAgent(BaseAgent):

    async def compute(self, market_data: dict[str, pd.DataFrame]) -> dict[str, dict]:
        results = {}
        for symbol, df in market_data.items():
            df.ta.rsi(length=14, append=True)
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            df.ta.bbands(length=20, std=2, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.ema(length=200, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.obv(append=True)                   # On-Balance Volume
            df.ta.adx(length=14, append=True)        # Trend strength
            df.ta.stoch(k=14, d=3, append=True)      # Stochastic

            latest = df.iloc[-1]
            results[symbol] = {
                "rsi": latest.get("RSI_14"),
                "macd": latest.get("MACD_12_26_9"),
                "macd_signal": latest.get("MACDs_12_26_9"),
                "macd_hist": latest.get("MACDh_12_26_9"),
                "bb_upper": latest.get("BBU_20_2.0"),
                "bb_lower": latest.get("BBL_20_2.0"),
                "bb_mid": latest.get("BBM_20_2.0"),
                "ema_20": latest.get("EMA_20"),
                "ema_50": latest.get("EMA_50"),
                "ema_200": latest.get("EMA_200"),
                "atr": latest.get("ATRr_14"),
                "obv": latest.get("OBV"),
                "adx": latest.get("ADX_14"),
                "stoch_k": latest.get("STOCHk_14_3_3"),
                "stoch_d": latest.get("STOCHd_14_3_3"),
                # Derived signals
                "golden_cross": latest.get("EMA_50", 0) > latest.get("EMA_200", 0),
                "price_above_ema20": latest["Close"] > latest.get("EMA_20", 0),
                "volume_spike": latest["Volume"] > df["Volume"].rolling(20).mean().iloc[-1] * 1.5,
            }
        return results
```

---

### 4.4 Fundamental Analyst Agent

Pulls fundamentals from Screener.in or Tijori Finance.

```python
# agents/fundamental_analyst.py

import httpx
from agents.base_agent import BaseAgent

class FundamentalAnalystAgent(BaseAgent):
    """
    Collects fundamental data per symbol.
    Primary: Screener.in (free, scraping)
    Alternative: Tijori Finance API (paid, cleaner)
    """

    async def analyze(self, symbols: list[str]) -> dict[str, dict]:
        results = {}
        async with httpx.AsyncClient() as client:
            for symbol in symbols:
                data = await self._fetch_screener(client, symbol)
                results[symbol] = data
        return results

    async def _fetch_screener(self, client, symbol: str) -> dict:
        # Screener.in JSON endpoint (unofficial but stable)
        url = f"https://www.screener.in/api/company/{symbol}/?format=json"
        resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return {}
        data = resp.json()
        return {
            "pe_ratio": data.get("ratios", {}).get("Price to Earning"),
            "pb_ratio": data.get("ratios", {}).get("Price to book value"),
            "eps": data.get("ratios", {}).get("EPS in Rs"),
            "roe": data.get("ratios", {}).get("Return on equity"),
            "roce": data.get("ratios", {}).get("Return on capital employed"),
            "debt_equity": data.get("ratios", {}).get("Debt to equity"),
            "promoter_holding": data.get("shareholding", {}).get("promoter"),
            "fii_holding": data.get("shareholding", {}).get("fii"),
            "revenue_growth_3y": data.get("growth", {}).get("revenue_3y"),
            "profit_growth_3y": data.get("growth", {}).get("profit_3y"),
            "market_cap": data.get("market_cap"),
            "sector": data.get("industry"),
        }
```

---

### 4.5 Sentiment Agent

Scores news and social media sentiment using FinBERT (a finance-specific BERT model).

```python
# agents/sentiment_agent.py

import httpx
from bs4 import BeautifulSoup
from transformers import pipeline
from agents.base_agent import BaseAgent

class SentimentAgent(BaseAgent):
    """
    Sources: Moneycontrol, Economic Times, Reddit r/IndiaInvestments
    Model: ProsusAI/finbert (finance-specific BERT)
    Fallback: VADER (fast, rule-based)
    """

    def __init__(self):
        # Load FinBERT locally — runs offline after first download
        self.nlp = pipeline(
            "sentiment-analysis",
            model="ProsusAI/finbert",
            tokenizer="ProsusAI/finbert"
        )

    async def analyze(self, symbols: list[str]) -> dict[str, float]:
        results = {}
        async with httpx.AsyncClient() as client:
            for symbol in symbols:
                headlines = await self._fetch_headlines(client, symbol)
                if not headlines:
                    results[symbol] = 0.0
                    continue
                scores = self.nlp(headlines[:10])  # batch limit
                # positive=+1, negative=-1, neutral=0
                numeric = [
                    1.0 if s["label"] == "positive" else
                    -1.0 if s["label"] == "negative" else 0.0
                    for s in scores
                ]
                results[symbol] = sum(numeric) / len(numeric)
        return results

    async def _fetch_headlines(self, client, symbol: str) -> list[str]:
        url = f"https://economictimes.indiatimes.com/topic/{symbol}"
        resp = await client.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        headlines = [h.get_text(strip=True) for h in soup.select("h3.clr a")]
        return headlines[:15]
```

---

### 4.6 Feature Engineering Agent

Normalizes and assembles the feature vector fed into the model.

```python
# agents/feature_engineer.py

import numpy as np
import joblib
from agents.base_agent import BaseAgent

FEATURE_KEYS = [
    # Price action
    "close_norm", "volume_norm", "price_change_5d", "price_change_20d",
    # Technical
    "rsi", "macd_hist", "bb_position", "ema_slope_20",
    "adx", "stoch_k", "atr_norm", "volume_spike",
    "golden_cross", "price_above_ema20",
    # Fundamental
    "pe_ratio", "pb_ratio", "roe", "debt_equity",
    "promoter_holding", "revenue_growth_3y", "profit_growth_3y",
    # Sentiment
    "sentiment_score",
    # Market context
    "nifty_ret_5d", "sector_ret_5d",
]

class FeatureEngineerAgent(BaseAgent):

    def __init__(self):
        self.scaler = joblib.load("model/saved/scaler.pkl")

    async def build(self, market_data, tech_data, fund_data, sentiment) -> list[dict]:
        feature_vectors = []
        for symbol in market_data:
            df = market_data[symbol]
            tech = tech_data.get(symbol, {})
            fund = fund_data.get(symbol, {})
            sent = sentiment.get(symbol, 0.0)

            close = df["Close"].iloc[-1]
            close_5d_ago = df["Close"].iloc[-5] if len(df) >= 5 else close
            close_20d_ago = df["Close"].iloc[-20] if len(df) >= 20 else close
            bb_range = (tech.get("bb_upper", close) - tech.get("bb_lower", close)) or 1
            bb_pos = (close - tech.get("bb_lower", close)) / bb_range

            raw = [
                close / df["Close"].mean(),                              # close_norm
                df["Volume"].iloc[-1] / df["Volume"].mean(),             # volume_norm
                (close - close_5d_ago) / close_5d_ago,                  # price_change_5d
                (close - close_20d_ago) / close_20d_ago,                # price_change_20d
                (tech.get("rsi") or 50) / 100,
                tech.get("macd_hist") or 0,
                bb_pos,
                (tech.get("ema_20", close) - df["Close"].iloc[-20:].mean()) / close,
                (tech.get("adx") or 0) / 100,
                (tech.get("stoch_k") or 50) / 100,
                (tech.get("atr") or 0) / close,
                float(tech.get("volume_spike") or False),
                float(tech.get("golden_cross") or False),
                float(tech.get("price_above_ema20") or False),
                self._safe(fund.get("pe_ratio"), 25, 100),
                self._safe(fund.get("pb_ratio"), 1, 20),
                self._safe(fund.get("roe"), 0, 100) / 100,
                self._safe(fund.get("debt_equity"), 0, 5) / 5,
                self._safe(fund.get("promoter_holding"), 0, 100) / 100,
                self._safe(fund.get("revenue_growth_3y"), -50, 100) / 100,
                self._safe(fund.get("profit_growth_3y"), -50, 100) / 100,
                max(-1.0, min(1.0, sent)),
                0.0,  # nifty_ret_5d — fill from market context
                0.0,  # sector_ret_5d — fill from market context
            ]
            feature_vectors.append({"symbol": symbol, "features": raw})
        return feature_vectors

    def _safe(self, val, min_v, max_v):
        if val is None: return (min_v + max_v) / 2
        return max(min_v, min(max_v, float(val)))
```

---

### 4.7 Prediction Agent

Loads your locally trained model and runs inference.

```python
# agents/prediction_agent.py

import joblib
import numpy as np
from agents.base_agent import BaseAgent

class PredictionAgent(BaseAgent):
    """
    Loads model from model/saved/model.pkl
    Returns boom probability score (0.0 to 1.0) per symbol
    """

    def __init__(self):
        self.model = joblib.load("model/saved/model.pkl")

    async def predict(self, feature_vectors: list[dict]) -> list[dict]:
        results = []
        X = np.array([fv["features"] for fv in feature_vectors])
        # model.predict_proba returns [P(no_boom), P(boom)]
        probs = self.model.predict_proba(X)[:, 1]

        for fv, prob in zip(feature_vectors, probs):
            results.append({
                "symbol": fv["symbol"],
                "boom_score": round(float(prob), 4),
                "confidence": "high" if prob > 0.75 else "medium" if prob > 0.5 else "low"
            })

        return sorted(results, key=lambda x: x["boom_score"], reverse=True)
```

---

### 4.8 Risk Agent

Filters predictions through safety checks before surfacing them.

```python
# agents/risk_agent.py

from agents.base_agent import BaseAgent

# Risk thresholds tuned for Indian market
MAX_VOLATILITY_ATR_PCT = 0.05       # ATR > 5% of price = too volatile
MIN_AVG_DAILY_VOLUME = 100_000      # Liquidity filter
CIRCUIT_BREAKER_THRESHOLD = 0.095   # Near 10% circuit limit
MIN_PROMOTER_HOLDING = 30.0         # Promoter skin in the game

class RiskAgent(BaseAgent):

    async def filter(self, predictions: list[dict], market_data: dict) -> list[dict]:
        safe_picks = []
        for pred in predictions:
            symbol = pred["symbol"]
            df = market_data.get(symbol)
            if df is None or df.empty:
                continue

            close = df["Close"].iloc[-1]
            prev_close = df["Close"].iloc[-2]
            day_change = abs(close - prev_close) / prev_close
            avg_volume = df["Volume"].rolling(20).mean().iloc[-1]

            # Reject near circuit breaker
            if day_change >= CIRCUIT_BREAKER_THRESHOLD:
                pred["risk_flag"] = "near_circuit_breaker"
                pred["cleared"] = False
            # Reject illiquid stocks
            elif avg_volume < MIN_AVG_DAILY_VOLUME:
                pred["risk_flag"] = "low_liquidity"
                pred["cleared"] = False
            else:
                pred["risk_flag"] = None
                pred["cleared"] = True

            safe_picks.append(pred)

        return [p for p in safe_picks if p["cleared"]]
```

---

## 5. Local AI Model

### 5.1 Model Options

| Model | Pros | Cons | Best For |
|---|---|---|---|
| **XGBoost** | Fast, interpretable, great on tabular data, handles missing values | No native sequence modeling | Recommended starting point |
| **LightGBM** | Faster than XGBoost, lower memory | Similar limitations | Large Nifty 500 universe |
| **LSTM** | Captures time-series patterns | Needs more data, slower to train | If you have 5+ years tick data |
| **Transformer (TFT)** | State-of-the-art time series | Complex, compute-heavy | Advanced stage |

**Recommendation:** Start with XGBoost. It consistently outperforms deep learning on structured/tabular stock data when training data is limited.

---

### 5.2 Training Pipeline

```python
# model/train.py

import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

def create_labels(df: pd.DataFrame, forward_days=10, threshold=0.08) -> pd.Series:
    """
    Label = 1 if price rises >= threshold% within forward_days, else 0.
    Threshold of 8% captures genuine momentum moves in Indian mid/small caps.
    """
    future_returns = df["Close"].shift(-forward_days) / df["Close"] - 1
    return (future_returns >= threshold).astype(int)

def train():
    # Load your historical data (Nifty 500, 5 years daily)
    df = pd.read_parquet("data/raw/nifty500_daily.parquet")

    # Build features (same logic as FeatureEngineerAgent)
    X = build_feature_matrix(df)  # your feature engineering function
    y = create_labels(df)

    # Remove last forward_days rows (no label possible)
    X = X.iloc[:-10]
    y = y.iloc[:-10]

    # Time-series cross validation (NO random shuffle — data leakage!)
    tscv = TimeSeriesSplit(n_splits=5)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=3,      # handle class imbalance (few "boom" stocks)
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42
    )

    # Train on last fold as final model
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X_scaled)):
        X_train, X_val = X_scaled[train_idx], X_scaled[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=100)
        print(f"\nFold {fold+1}:")
        print(classification_report(y_val, model.predict(X_val)))

    joblib.dump(model, "model/saved/model.pkl")
    joblib.dump(scaler, "model/saved/scaler.pkl")
    print("Model saved.")

if __name__ == "__main__":
    train()
```

---

### 5.3 Data Sources for Training

| Dataset | Content | Access |
|---|---|---|
| NSE Bhav Copy (2010–present) | Daily OHLCV for all NSE stocks | Free download from nseindia.com |
| `nsepy` library | Historical data via Python | Free |
| `yfinance` | 10+ years daily for .NS tickers | Free |
| Screener.in exports | Fundamental data per quarter | Free (manual) / Paid API |
| Kaggle NSE datasets | Pre-cleaned historical data | Free |

> **Minimum recommended training data:** 3 years of daily data across Nifty 500 universe (~500 stocks × 750 days = 375,000 rows).

---

## 6. Data Flow

```
Market Open (9:15 AM IST)
        │
        ▼
[APScheduler triggers OrchestratorAgent]
        │
        ├─── DataFetcherAgent.fetch()         → raw OHLCV (async)
        ├─── SentimentAgent.analyze()         → sentiment scores (async)
        │
        ▼ (both complete)
        ├─── TechnicalAnalystAgent.compute()  → indicator dict
        ├─── FundamentalAnalystAgent.analyze()→ fundamental dict
        │
        ▼ (both complete)
        ├─── FeatureEngineerAgent.build()     → feature vectors list
        │
        ▼
        ├─── PredictionAgent.predict()        → boom scores
        │
        ▼
        ├─── RiskAgent.filter()               → filtered + flagged picks
        │
        ▼
[Save to PostgreSQL] → [Cache in Redis] → [POST to FastAPI] → [Alert via Telegram]
```

---

## 7. API Layer

```python
# api/main.py

from fastapi import FastAPI
from api.routes import predictions, stocks, health

app = FastAPI(title="Stock Prediction API", version="1.0.0")

app.include_router(health.router, prefix="/health")
app.include_router(predictions.router, prefix="/predictions")
app.include_router(stocks.router, prefix="/stocks")
```

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `GET` | `/predictions` | Latest top N stock predictions |
| `GET` | `/predictions?date=2024-01-15` | Predictions for a specific date |
| `GET` | `/stocks/{symbol}` | Full analysis for one stock |
| `POST` | `/predictions/run` | Trigger a manual prediction run |
| `GET` | `/predictions/history` | Historical prediction performance |

### Sample Response

```json
{
  "run_at": "2024-01-15T09:30:00+05:30",
  "top_picks": [
    {
      "symbol": "TATAPOWER",
      "boom_score": 0.84,
      "confidence": "high",
      "technical_signal": "bullish",
      "sentiment_score": 0.6,
      "pe_ratio": 22.4,
      "risk_flag": null,
      "cleared": true
    }
  ],
  "total_analyzed": 492,
  "total_cleared": 38
}
```

---

## 8. Scheduler & Job Queue

```python
# scheduler/jobs.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from agents.orchestrator import OrchestratorAgent
from config.settings import settings
import pytz

IST = pytz.timezone("Asia/Kolkata")

def setup_scheduler():
    scheduler = AsyncIOScheduler(timezone=IST)

    # Main prediction run: 9:30 AM IST on weekdays
    scheduler.add_job(
        run_prediction,
        CronTrigger(day_of_week="mon-fri", hour=9, minute=30, timezone=IST),
        id="morning_run",
        name="Morning Prediction Run"
    )

    # Mid-day refresh: 1:00 PM IST
    scheduler.add_job(
        run_prediction,
        CronTrigger(day_of_week="mon-fri", hour=13, minute=0, timezone=IST),
        id="midday_run",
        name="Midday Prediction Run"
    )

    # Skip NSE holidays (load from NSE holiday calendar)
    scheduler.start()
    return scheduler

async def run_prediction():
    symbols = load_nifty500_symbols()  # from DB or static list
    orchestrator = OrchestratorAgent(symbols=symbols)
    results = await orchestrator.run()
    await save_results(results)
    await send_alert(results[:5])      # Top 5 to Telegram
```

---

## 9. Database Schema

```sql
-- Prediction runs
CREATE TABLE prediction_runs (
    id          SERIAL PRIMARY KEY,
    run_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    symbols_analyzed INTEGER,
    model_version TEXT
);

-- Per-stock predictions
CREATE TABLE predictions (
    id              SERIAL PRIMARY KEY,
    run_id          INTEGER REFERENCES prediction_runs(id),
    symbol          TEXT NOT NULL,
    boom_score      FLOAT NOT NULL,
    confidence      TEXT,
    risk_flag       TEXT,
    cleared         BOOLEAN,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Outcomes (filled after forward_days, for retraining)
CREATE TABLE outcomes (
    id              SERIAL PRIMARY KEY,
    prediction_id   INTEGER REFERENCES predictions(id),
    actual_return   FLOAT,
    was_correct     BOOLEAN,
    evaluated_at    TIMESTAMPTZ
);

-- Daily OHLCV cache
CREATE TABLE daily_prices (
    symbol      TEXT NOT NULL,
    date        DATE NOT NULL,
    open        FLOAT, high FLOAT, low FLOAT, close FLOAT, volume BIGINT,
    PRIMARY KEY (symbol, date)
);
```

---

## 10. Configuration & Environment

```python
# config/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/stockdb"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # API Keys
    ZERODHA_API_KEY: str = ""
    ZERODHA_ACCESS_TOKEN: str = ""
    ANGEL_ONE_API_KEY: str = ""

    # Alerts
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Model
    MODEL_PATH: str = "model/saved/model.pkl"
    SCALER_PATH: str = "model/saved/scaler.pkl"

    # Trading universe
    DEFAULT_UNIVERSE: str = "NIFTY500"   # or NIFTY200, NIFTY50

    # Prediction config
    FORWARD_DAYS: int = 10
    BOOM_THRESHOLD: float = 0.08         # 8% return = "boom"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 11. Installation & Setup

```bash
# 1. Clone and set up virtual environment
git clone https://github.com/yourname/stock-prediction
cd stock-prediction
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file and fill in your keys
cp .env.example .env

# 4. Start PostgreSQL and Redis via Docker
docker-compose up -d postgres redis

# 5. Run database migrations
alembic upgrade head

# 6. Download and prepare training data
python data/collectors/nse_collector.py --years 5

# 7. Train the local model
python model/train.py

# 8. Start the API server
uvicorn api.main:app --reload --port 8000

# 9. Start the scheduler (separate process)
python scheduler/jobs.py
```

### requirements.txt

```
fastapi==0.111.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.30
alembic==1.13.1
asyncpg==0.29.0
pydantic-settings==2.2.1
httpx==0.27.0
yfinance==0.2.40
nsepy==0.8
pandas==2.2.2
pandas-ta==0.3.14b
numpy==1.26.4
xgboost==2.0.3
scikit-learn==1.5.0
transformers==4.41.0
torch==2.3.0
beautifulsoup4==4.12.3
apscheduler==3.10.4
celery==5.4.0
redis==5.0.4
joblib==1.4.2
loguru==0.7.2
python-telegram-bot==21.3
pytest==8.2.0
pytest-asyncio==0.23.7
pytz==2024.1
```

---

## 12. Agent Communication Protocol

All agents follow a standard interface:

```python
# agents/base_agent.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from utils.logger import logger

@dataclass
class AgentResult:
    agent_name: str
    success: bool
    data: Any
    error: str | None = None

class BaseAgent(ABC):
    name: str = "BaseAgent"

    async def safe_run(self, *args, **kwargs) -> AgentResult:
        try:
            data = await self.run(*args, **kwargs)
            return AgentResult(agent_name=self.name, success=True, data=data)
        except Exception as e:
            logger.error(f"{self.name} failed: {e}")
            return AgentResult(agent_name=self.name, success=False, data=None, error=str(e))
```

---

## 13. Error Handling Strategy

| Scenario | Handling |
|---|---|
| Data fetch fails for one symbol | Skip symbol, log warning, continue with rest |
| Sentiment API rate limit | Fall back to VADER (local, no API) |
| Model file missing | Raise startup error, block API from serving |
| Database write fails | Log to file, retry 3x with exponential backoff |
| NSE market holiday | Scheduler detects no price update, skips run |
| Circuit breaker hit | Risk agent flags and filters out the stock |

---

## 14. Backtesting Module

```python
# backtesting/engine.py

import pandas as pd
from backtesting.metrics import sharpe_ratio, max_drawdown

def backtest(predictions_df: pd.DataFrame, prices_df: pd.DataFrame,
             forward_days=10) -> dict:
    """
    predictions_df: columns [date, symbol, boom_score, cleared]
    prices_df: columns [date, symbol, close]
    """
    results = []
    for _, row in predictions_df[predictions_df["cleared"]].iterrows():
        entry_price = prices_df.loc[
            (prices_df["symbol"] == row["symbol"]) & (prices_df["date"] == row["date"]),
            "close"
        ].values

        exit_date_idx = prices_df.index[
            (prices_df["symbol"] == row["symbol"]) &
            (prices_df["date"] > row["date"])
        ][:forward_days]

        if not len(entry_price) or not len(exit_date_idx):
            continue

        exit_price = prices_df.loc[exit_date_idx[-1], "close"]
        returns = (exit_price - entry_price[0]) / entry_price[0]
        results.append({"symbol": row["symbol"], "date": row["date"], "return": returns})

    results_df = pd.DataFrame(results)
    return {
        "total_trades": len(results_df),
        "win_rate": (results_df["return"] > 0).mean(),
        "avg_return": results_df["return"].mean(),
        "sharpe_ratio": sharpe_ratio(results_df["return"]),
        "max_drawdown": max_drawdown(results_df["return"]),
    }
```

---

## 15. Deployment

### Docker Compose

```yaml
# docker-compose.yml

version: "3.9"
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [postgres, redis]
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000

  scheduler:
    build: .
    env_file: .env
    depends_on: [postgres, redis]
    command: python scheduler/jobs.py

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: stockdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

volumes:
  pgdata:
```

### Deployment Checklist

- [ ] `.env` file filled with all API keys
- [ ] Model trained and `model/saved/model.pkl` present
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] NSE holiday calendar loaded for scheduler
- [ ] Telegram bot created and `TELEGRAM_BOT_TOKEN` set
- [ ] Backtesting run on last 6 months to validate model
- [ ] Rate limits checked for all external APIs

---
