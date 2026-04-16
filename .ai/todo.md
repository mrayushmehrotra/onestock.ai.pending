# OneStock AI Implementation Checklist

## 1. Project Foundation
- [x] Initialize project structure
- [x] Set up Python environment and `requirements.txt`
- [x] Configure environment variables (`.env`) for scrapers and database
- [x] Initialize Git repository

## 2. Scraping & Data Pipeline (Indian Focus)
- [ ] **News Scrapers**:
    - [ ] Implement scraper for *The Economic Times* (Markets section)
    - [ ] Implement scraper for *LiveMint*
    - [ ] Implement scraper for *MoneyControl*
- [ ] **Stock Data**:
    - [ ] Integration with `nsepy` for NSE/BSE ticker data
    - [ ] Historical data curation for fine-tuning dataset
- [ ] **Weather/Seasonal Data**:
    - [ ] Integration with an OpenWeather API (or similar) to track Indian weather trends
    - [ ] Build a mapping of Indian seasons to NSE/BSE sectors

## 3. Model Fine-Tuning (Small & Quick)
- [ ] **Dataset Preparation**:
    - [ ] Curate 5,000+ samples of Indian financial news paired with market movement
    - [ ] Format data for Chain-of-Thought (CoT) training (Reasoning -> Prediction)
- [ ] **Fine-Tuning**:
    - [ ] Select base model (e.g., SmolLM-135M or Phi-3-mini)
    - [ ] Fine-tune on curated financial & seasonal dataset
    - [ ] Quantize model (GGUF/AWQ) for "Quick" performance
- [ ] **Reasoning Engine**:
    - [ ] Develop internal prompt templates to force CoT steps

## 4. Logic & Intelligence Engine
- [ ] **Seasonal/Weather Module**:
    - [ ] Logic for detecting Summer/Winter transitions
    - [ ] Sector weightage algorithm (e.g., +20% Solar in Summer)
- [ ] **Directional Analyst**:
    - [ ] News-to-Sentiment aggregator
    - [ ] Overall Market Direction predictor (Nifty50/Sensex focus)

## 5. Backend Architecture
- [ ] **Database Setup**:
    - [ ] Vector Database (ChromaDB) for news context
    - [ ] SQLite/PostgreSQL for tracking prediction outcomes
- [ ] **API (FastAPI)**:
    - [ ] `/predict`: Reasoning-first stock prediction endpoint
    - [ ] `/market-direction`: Aggregated daily outlook
    - [ ] `/seasonal-picks`: Top stocks based on weather context
- [ ] **Scheduler**:
    - [ ] Automated scraping every 4 hours
    - [ ] Nightly model retraining/context update

## 6. Testing & Evaluation
- [ ] Unit tests for scrapers
- [ ] Benchmarking model latency (target < 500ms for reasoning)
- [ ] Backtesting seasonal picks against past 2 years of market data

## 7. Deployment
- [ ] Dockerize the entire stack
- [ ] Set up basic monitoring for scraper failures
- [ ] (Optional) Develop simple frontend for OneStock AI visualization


livemint.com, economictimes.com, moneycontrol.com, business-standard.com use this websites for scrapping