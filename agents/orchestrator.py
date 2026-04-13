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

        # Phase 1: Parallel data collection & Sentiment
        data_agent = DataFetcherAgent()
        sentiment_agent = SentimentAgent()
        
        results = await asyncio.gather(
            data_agent.safe_run(self.symbols),
            sentiment_agent.safe_run(self.symbols)
        )
        
        market_data_res = results[0]
        sentiment_res = results[1]
        
        if not market_data_res.success:
            logger.error("Data fetching phase failed. Aborting run.")
            return []
            
        market_data = market_data_res.data
        sentiment_scores = sentiment_res.data if sentiment_res.success else {}

        # Phase 2: Technical + Fundamental
        tech_agent = TechnicalAnalystAgent()
        fund_agent = FundamentalAnalystAgent()

        tech_res, fund_res = await asyncio.gather(
            tech_agent.safe_run(market_data),
            fund_agent.safe_run(self.symbols)
        )
        
        technical_data = tech_res.data if tech_res.success else {}
        fundamental_data = fund_res.data if fund_res.success else {}

        # Phase 3: Feature engineering
        feature_agent = FeatureEngineerAgent()
        feature_res = await feature_agent.safe_run(
            market_data, technical_data, fundamental_data, sentiment_scores
        )
        
        if not feature_res.success:
            logger.error("Feature engineering phase failed.")
            return []
            
        feature_vectors = feature_res.data

        # Phase 4: Prediction
        prediction_agent = PredictionAgent()
        pred_res = await prediction_agent.safe_run(feature_vectors)
        
        if not pred_res.success:
            logger.error("Prediction phase failed.")
            return []
            
        predictions = pred_res.data

        # Phase 5: Risk filtering
        risk_agent = RiskAgent()
        safe_res = await risk_agent.safe_run(predictions, market_data)
        
        final_picks = safe_res.data if safe_res.success else []
        
        logger.info(f"Run complete. Generated {len(final_picks)} safe picks.")
        return final_picks
