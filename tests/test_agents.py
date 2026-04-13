import pytest
from agents.data_fetcher import DataFetcherAgent
from agents.technical_analyst import TechnicalAnalystAgent

@pytest.mark.asyncio
async def test_data_fetcher():
    agent = DataFetcherAgent()
    results = await agent.run(["RELIANCE"])
    assert "RELIANCE" in results
    assert len(results["RELIANCE"]) > 0

@pytest.mark.asyncio
async def test_technical_analyst():
    # Mock data setup
    import pandas as pd
    import numpy as np
    dates = pd.date_range(start="2023-01-01", periods=300)
    df = pd.DataFrame(index=dates)
    df["Open"] = np.random.uniform(100, 200, 300)
    df["High"] = df["Open"] + 5
    df["Low"] = df["Open"] - 5
    df["Close"] = np.random.uniform(100, 200, 300)
    df["Volume"] = np.random.randint(1000, 10000, 300)
    
    agent = TechnicalAnalystAgent()
    results = await agent.run({"MOCK": df})
    assert "MOCK" in results
    assert "rsi" in results["MOCK"]
