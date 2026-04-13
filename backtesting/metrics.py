import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0.07):
    if len(returns) < 2: return 0
    # Annualized Sharpe (assuming returns are per forward period)
    excess_returns = returns - (risk_free_rate / 252 * 10) # rough estimate
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252/10)

def calculate_max_drawdown(returns):
    if len(returns) == 0: return 0
    cumulative = (1 + returns).cumprod()
    peak = cumulative.expanding(min_periods=1).max()
    dd = (cumulative - peak) / peak
    return dd.min()
