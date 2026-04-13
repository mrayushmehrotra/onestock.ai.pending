import joblib
from utils.logger import logger
from config.settings import settings

def export_model_artifact(model, scaler, version: str):
    logger.info(f"Exporting model version {version}")
    joblib.dump(model, settings.MODEL_PATH)
    joblib.dump(scaler, settings.SCALER_PATH)
    logger.info("Artifacts saved successfully.")
