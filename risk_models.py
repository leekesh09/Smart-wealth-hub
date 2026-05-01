import numpy as np
import pandas as pd


def calculate_returns(close_series: pd.Series) -> pd.Series:
    return close_series.pct_change().dropna()


def calculate_beta(stock_returns: pd.Series, market_returns: pd.Series) -> float:
    combined = pd.concat([stock_returns, market_returns], axis=1).dropna()
    if combined.empty or combined.shape[0] < 2:
        return 0.0

    combined.columns = ["Stock", "Market"]
    cov_matrix = np.cov(combined["Stock"], combined["Market"])

    market_var = cov_matrix[1][1]
    if market_var == 0:
        return 0.0

    return float(cov_matrix[0][1] / market_var)


def calculate_capm_return(beta: float, risk_free_rate: float = 4.2, market_return: float = 10.8) -> float:
    return float(risk_free_rate + beta * (market_return - risk_free_rate))


def annualized_return(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    return float(returns.mean() * 252 * 100)


def annualized_volatility(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0
    return float(returns.std() * np.sqrt(252) * 100)


def rolling_beta(stock_returns: pd.Series, market_returns: pd.Series, window: int = 30) -> pd.Series:
    combined = pd.concat([stock_returns, market_returns], axis=1).dropna()
    if combined.empty:
        return pd.Series(dtype=float)

    combined.columns = ["Stock", "Market"]
    rolling_cov = combined["Stock"].rolling(window).cov(combined["Market"])
    rolling_var = combined["Market"].rolling(window).var()

    beta_series = rolling_cov / rolling_var
    return beta_series.dropna()