from model.train import create_labels
import pandas as pd
import numpy as np

def test_create_labels():
    df = pd.DataFrame({
        "Close": [100, 105, 110, 115, 120, 100, 100, 100, 100, 100, 150]
    })
    labels = create_labels(df, forward_days=10, threshold=0.1)
    # 150 / 100 = 1.5 (50% return) > 10%
    assert labels.iloc[0] == 1
    # 100/100 = 0 < 10%
    assert labels.iloc[5] == 0
