from xgboost import XGBClassifier

def get_xgboost_model():
    return XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=3,  # Adjusted for class imbalance
        eval_metric="logloss",
        use_label_encoder=False,
        random_state=42
    )
