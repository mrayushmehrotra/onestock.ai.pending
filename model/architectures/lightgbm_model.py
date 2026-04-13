from lightgbm import LGBMClassifier

def get_lightgbm_model():
    """
    Recommended for Indian stock market tabular data:
    - Faster training than XGBoost
    - Lower memory usage
    - Excellent accuracy on momentum prediction
    """
    return LGBMClassifier(
        n_estimators=1000,
        learning_rate=0.03,
        num_leaves=31,
        max_depth=8,
        min_child_samples=20,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=4,  # High for 'boom' class imbalance
        random_state=42,
        verbosity=-1
    )
