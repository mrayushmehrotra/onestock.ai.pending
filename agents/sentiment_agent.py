from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from agents.base_agent import BaseAgent
from data.collectors.news_collector import NewsCollector
from utils.logger import logger
import asyncio

class SentimentAgent(BaseAgent):
    name = "SentimentAgent"

    def __init__(self, mode="vader"):
        """
        mode: "vader" (fast, CPU), "finbert" (accurate, GPU/CPU), "llm" (fine-tuned LLM)
        """
        super().__init__()
        self.mode = mode
        self._nlp = None
        self._vader = None

    @property
    def vader(self):
        if self._vader is None:
            self._vader = SentimentIntensityAnalyzer()
        return self._vader

    @property
    def nlp(self):
        if self._nlp is None:
            if self.mode == "finbert":
                logger.info("Loading FinBERT sentiment model...")
                self._nlp = pipeline(
                    "sentiment-analysis",
                    model="ProsusAI/finbert",
                    tokenizer="ProsusAI/finbert"
                )
            elif self.mode == "llm":
                logger.info("LLM mode selected. Ensure model/saved/llm_adapter is present.")
                # Placeholder for fine-tuned LLM inference
                # In practice, this would use PeftModel.from_pretrained
                pass
        return self._nlp

    async def run(self, symbols: list[str]) -> dict[str, float]:
        results = {}
        for symbol in symbols:
            headlines = await NewsCollector.fetch_et_headlines(symbol)
            if not headlines:
                results[symbol] = 0.0
                continue
            
            try:
                if self.mode == "vader":
                    # FAST, CPU-friendly baseline
                    scores = [self.vader.polarity_scores(h)["compound"] for h in headlines]
                    avg_sentiment = sum(scores) / len(scores)
                else:
                    # ML-based analysis
                    scores = self.nlp(headlines[:10])
                    numeric_scores = [
                        1.0 if s["label"] == "positive" else
                        -1.0 if s["label"] == "negative" else 0.0
                        for s in scores
                    ]
                    avg_sentiment = sum(numeric_scores) / len(numeric_scores)
                
                results[symbol] = round(avg_sentiment, 2)
                logger.info(f"Sentiment ({self.mode}) for {symbol}: {avg_sentiment}")
            except Exception as e:
                logger.error(f"Sentiment analysis failed for {symbol}: {e}")
                results[symbol] = 0.0
        
        return results
