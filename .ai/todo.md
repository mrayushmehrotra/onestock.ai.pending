# OneStock AI Implementation Checklist

## Phase 1: Foundation & Setup (COMPLETE)
- [x] Initialize project structure (src/agents, src/scrapers, etc.)
- [x] Set up `requirements.txt` with essential scraping & ML libraries
- [x] Configure `.env.example` for API keys and environment variables
- [x] Initialize Git repository

## Phase 2: Data Engineering (News & Market Scrapers)
- [ ] **Unified Scraper Framework**:
    - [x] Implement `BaseScraper` class with retry logic and standard headers
    - [x] Create a `ScraperManager` to orchestrate all scrapers
- [ ] **News Sources (BeautifulSoup4)**:
    - [x] Implement `ETScraper` (Economic Times Markets)
    - [x] Implement `MintScraper` (LiveMint Markets)
    - [x] Implement `MoneyControlScraper` (MoneyControl Markets)
    - [x] Implement `BSScraper` (Business Standard Markets)
- [ ] **Content Extraction for Reasoning**:
    - [ ] Extract not just headlines but brief summaries/content snippets
    - [ ] Ticker extraction logic (identifying stock names in text)
- [ ] **Scheduler & Automation**:
    - [ ] Implement a 4-hour background scheduler using `APScheduler` or `Celery`
    - [ ] Ensure deduplication of news items in the database

## Phase 3: Seasonal & Market Intelligence
- [x] **Market Data**:
    - [x] Integration with `nsepy` for NSE/BSE historical/real-time data
- [ ] **Seasonal Intelligence Engine**:
    - [x] Mapping of Indian months/seasons to specific sectors (Solar, Agriculture, Woolens, etc.)
    - [x] Logic to fetch current weather trends and adjust sector weightage
- [x] **Financial Database**:
    - [x] Set up Vector DB (ChromaDB) for storing news embeddings
    - [x] Implement local storage for scraped headlines and market state

## Phase 4: AI Model Fine-Tuning & Reasoning
- [x] **Dataset Preparation**:
    - [x] Create a 'Reasoning' dataset: `[News + Season + Market State] -> [Step-by-Step Logic] -> [Prediction]`
- [ ] **Model Selection & Fine-Tuning**:
    - [x] Select base model (e.g., SmolLM-135M or Phi-3-mini) on Indian stock market context
    - [ ] Implement Chain-of-Thought (CoT) prompting strategy
- [ ] **Inference Optimizer**:
    - [ ] Quantize model for low-latency CPU/Local execution

## Phase 5: Backend & API Development
- [x] **FastAPI Backend**:
    - [x] `/predict`: End-to-end reasoning and stock prediction
    - [x] `/daily-analysis`: Summary of market direction based on news
- [ ] **Frontend (Optional/WIP)**:
    - [ ] Simple dashboard to visualize reasoning steps and stock picks

## Phase 6: Validation & Polish
- [ ] Backtesting the seasonal logic against 2 years of history
- [ ] Evaluation of model reasoning accuracy
- [ ] Final performance optimization for the scraping pipeline