# OneStock.ai Backend

Multi-agent Indian stock market prediction system using a locally trained XGBoost model to find high-momentum stocks on NSE/BSE.

## 🚀 Quick Start

1. **Clone the repository**
2. **Setup environment**
   ```bash
   cp .env.example .env
   # Fill in your API keys
   ```
3. **Run with Docker**
   ```bash
   docker-compose up -d
   ```

## 🛠 Tech Stack

- **Framework**: FastAPI (Async)
- **Database**: PostgreSQL (SQLAlchemy + Alembic)
- **ML**: XGBoost, Scikit-learn, Pandas-TA
- **NLP**: Transfomers (FinBERT)
- **Agents**: Custom Async Multi-Agent System
- **Job Scheduling**: APScheduler

## 🤖 Agents

- **Orchestrator**: Coordinates the workflow.
- **Data Fetcher**: Pulls live/historical data (yfinance).
- **Technical Analyst**: Computes RSI, MACD, Bollinger, etc.
- **Fundamental Analyst**: Scrapes Screener.in for financial ratios.
- **Sentiment Agent**: Analyzes news using FinBERT.
- **Risk Agent**: Filters out low-liquidity and near-circuit stocks.

## 📊 Endpoints

- `GET /health`: System status.
- `GET /predictions`: Latest momentum picks.
- `POST /predictions/run`: Manually trigger analysis.
- `GET /stocks/{symbol}`: Full fundamental analysis.

## ⚖️ Disclaimer

Investing in stocks is subject to market risks. This AI is for informational purposes only and does not constitute financial advice. OneStock.ai is not responsible for any financial losses.
