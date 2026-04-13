import joblib
import numpy as np
from agents.base_agent import BaseAgent
from utils.logger import logger
from config.settings import settings

class PredictionAgent(BaseAgent):
    """
    Inference agent using locally trained models.
    Primary recommendation: LightGBM (fast, accurate on tabular data).
    Secondary options: XGBoost, PatchTST (Time-Series Transformer).
    """

    def __init__(self, model_type="lightgbm"):
        super().__init__()
        self.model_type = model_type
        self.model = None
        try:
            self.model = joblib.load(settings.MODEL_PATH)
            logger.info(f"Loaded {model_type} model for prediction.")
        except:
            logger.warning(f"Model file {settings.MODEL_PATH} not found. Prediction will fail.")

    async def run(self, feature_vectors: list[dict]) -> list[dict]:
        if not self.model:
            logger.error("Model not loaded. Skipping prediction.")
            return []

        results = []
        for item in feature_vectors:
            symbol = item["symbol"]
            X = np.array(item["features"]).reshape(1, -1)
            
            # Assuming classification model with predict_proba
            try:
                prob = self.model.predict_proba(X)[0, 1]
                results.append({
                    "symbol": symbol,
                    "boom_score": round(float(prob), 4),
                    "confidence": "high" if prob > 0.8 else "medium" if prob > 0.5 else "low"
                })
            except Exception as e:
                logger.error(f"Prediction failed for {symbol}: {e}")
        
        return sorted(results, key=lambda x: x["boom_score"], reverse=True)
