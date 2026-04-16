# OneStock AI: Intelligent Indian Stock Market Analysis

## Project Overview
OneStock AI is a high-performance, reasoning-focused AI engine tailored specifically for the Indian Stock Market (NSE/BSE). It combines real-time news scraping with seasonal/weather-aware reasoning to provide actionable market directions and individual stock insights.

## Core Philosophical Principles
- **Reasoning First**: The model MUST perform internal chain-of-thought (CoT) reasoning before delivering any market advice.
- **Small & Quick**: Optimized for low latency and high throughput, allowing for real-time analysis without massive infrastructure costs.
- **Context Awareness**: Beyond numbers, the model understands environmental factors (weather, seasons) and their impact on consumer behavior and industry performance in India.

## Key Features

### 1. Fine-tuned Reasoning Model
- **Base Architecture**: A small-parameter LLM (e.g., Phi-3, SmolLM, or Mistral-7B) fine-tuned on financial data, NSE/BSE historical filings, and Indian economic news.
- **Reasoning Engine**: Built-in prompts to enforce step-by-step logic:
    1.  Sentiment Analysis (from News/Socials)
    2.  Macro-economic Context (Seasons/Weather)
    3.  Technical Indicators (Volume/Price Action)
    4.  Conclusion & Recommendation

### 2. Seasonal & Weather-Driven Intelligence
The model identifies shifts in demand based on climate and time of year:
- **Summer Transition**: Focus on Solar Energy companies, cooling/appliance manufacturers (ACs, Refrigerators), and beverage industries.
- **Winter Transition**: Focus on Thermal wear, heating solutions, and power-intensive sectors.
- **Monsoon**: Focus on Agriculture-linked stocks, fertilizers, and logistics.

### 3. Automated News Scraping & Learning
- **Sources**: Real-time scraping of major Indian newspapers (Economic Times, LiveMint, MoneyControl, Business Standard).
- **Directional Analysis**: Aggregates sentiment to predict overall market movement (Bullish/Bearish/Neutral) for the day.

### 4. Backend Architecture
- **API**: FastAPI-based backend serving model inferences.
- **Web Scraper Pipeline**: Celery/Redis for asynchronous newspaper scraping and embedding generation.
- **Database**: Vector DB (e.g., Pinecone or Chroma) to store historical news context for RAG-enhanced reasoning.

## Implementation Roadmap
1. [ ] **Phase 1**: News Scraper setup and initial dataset curation for Indian Market.
2. [ ] **Phase 2**: Fine-tuning the small-parameter reasoning model.
3. [ ] **Phase 3**: Developing the Seasonal/Weather weightage algorithm.
4. [ ] **Phase 4**: FastAPI Backend integration and real-time inference testing.
5. [ ] **Phase 5**: UI/Dashboard for visualization of reasoning and stock picks.
