from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from utils.logger import logger

def evaluate_model(y_true, y_pred):
    logger.info("Evaluating model performance...")
    print(classification_report(y_true, y_pred))
    print(confusion_matrix(y_true, y_pred))

def plot_importance(model, feature_names):
    # For XGBoost
    importance = model.feature_importances_
    sorted_idx = importance.argsort()
    plt.barh(np.array(feature_names)[sorted_idx], importance[sorted_idx])
    plt.xlabel("Xgboost Feature Importance")
