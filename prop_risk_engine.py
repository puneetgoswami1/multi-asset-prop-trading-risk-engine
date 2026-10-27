"""
Multi-Asset Prop Trading Risk & Volatility Analytics Engine
Author: Puneet Goswami
Description: Evaluates cross-asset trading logs (Gold, FX, Indices, Crypto) to compute
             Value-at-Risk (VaR), Sharpe & Sortino ratios, and peak-to-trough drawdowns.
"""

import numpy as np
import pandas as pd
from scipy.stats import norm


def generate_prop_trading_stream(n_days: int = 252) -> pd.DataFrame:
    """Generates 1 trading year of multi-asset daily returns for a funded account."""
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq="B")

    # Multi-asset return distributions (Daily mean and volatility)
    # XAU/USD (Gold), EUR/USD (Forex), US30 (Index), BTC/USD (Crypto)
    returns_gold = np.random.normal(loc=0.0006, scale=0.012, size=n_days)
    returns_fx = np.random.normal(loc=0.0002, scale=0.007, size=n_days)
    returns_index = np.random.normal(loc=0.0005, scale=0.011, size=n_days)
    returns_crypto = np.random.normal(loc=0.0012, scale=0.028, size=n_days)

    # Portfolio weights: 40% Gold, 30% FX, 20% Index, 10% Crypto
    portfolio_daily_returns = (
        0.40 * returns_gold + 
        0.30 * returns_fx + 
        0.20 * returns_index + 
        0.10 * returns_crypto
    )

    initial_capital = 100000.0
    equity_curve = initial_capital * np.cumprod(1 + portfolio_daily_returns)

    return pd.DataFrame({
        "trade_date": dates,
        "daily_return": portfolio_daily_returns,
        "portfolio_equity": equity_curve
    })


def compute_quantitative_risk_metrics(df: pd.DataFrame):
    """Computes professional risk metrics: Sharpe, Sortino, VaR, Max Drawdown."""
    daily_returns = df["daily_return"]
    annual_risk_free_rate = 0.045  # 4.5% US Treasury benchmark
    daily_rf = annual_risk_free_rate / 252

    # 1. Sharpe Ratio (Annualized)
    excess_returns = daily_returns - daily_rf
    mean_excess = excess_returns.mean()
    std_returns = daily_returns.std()
    sharpe_ratio = (mean_excess / std_returns) * np.sqrt(252)

    # 2. Sortino Ratio (Downside volatility penalization)
    downside_returns = daily_returns[daily_returns < 0]
    downside_std = np.sqrt(np.mean(downside_returns**2))
    sortino_ratio = (mean_excess / downside_std) * np.sqrt(252)

    # 3. Value-at-Risk (95% and 99% 1-Day Horizon)
    # Historical VaR
    hist_var_95 = -np.percentile(daily_returns, 5) * 100
    hist_var_99 = -np.percentile(daily_returns, 1) * 100

    # Parametric (Gaussian) VaR
    param_var_95 = -(daily_returns.mean() - norm.ppf(0.95) * std_returns) * 100
    param_var_99 = -(daily_returns.mean() - norm.ppf(0.99) * std_returns) * 100

    # 4. High-Water Mark & Maximum Drawdown (MDD)
    equity = df["portfolio_equity"]
    running_max = np.maximum.accumulate(equity)
    drawdowns = (equity - running_max) / running_max
    max_drawdown = drawdowns.min() * 100

    print("==========================================================================")
    print("PROP TRADING RISK DESK: PORTFOLIO VOLATILITY & CAPITAL INTEGRITY REPORT")
    print("==========================================================================")
    print(f"Trading Sessions Evaluated   : {len(df)} Days (1 Annual Trading Cycle)")
    print(f"Ending Portfolio Equity      : ${equity.iloc[-1]:,.2f} (Base: $100,000.00)")
    print(f"Total Cumulative Return      : {((equity.iloc[-1] / 100000.0) - 1)*100:.2f}%")
    print("\n--- Risk-Adjusted Performance Ratios ---")
    print(f"Sharpe Ratio (Annualized)    : {sharpe_ratio:.2f}")
    print(f"Sortino Ratio (Downside Risk): {sortino_ratio:.2f}")
    print("\n--- Capital Loss Exposure (Value-at-Risk 1-Day Horizon) ---")
    print(f"Historical VaR (95% Conf)    : {hist_var_95:.2f}% (Max daily loss: ${hist_var_95 * 1000:.2f})")
    print(f"Historical VaR (99% Conf)    : {hist_var_99:.2f}% (Max daily loss: ${hist_var_99 * 1000:.2f})")
    print(f"Parametric VaR (95% Conf)    : {param_var_95:.2f}%")
    print(f"Parametric VaR (99% Conf)    : {param_var_99:.2f}%")
    print("\n--- Drawdown Limits (Funded Rule Compliance) ---")
    print(f"Maximum Peak-to-Trough MDD   : {max_drawdown:.2f}%")
    print("Prop Rule Status (10% Cap)   : " + ("PASS (Within safe parameters)" if abs(max_drawdown) < 10.0 else "FAIL (Exceeded limit)"))


if __name__ == "__main__":
    trading_data = generate_prop_trading_stream(252)
    compute_quantitative_risk_metrics(trading_data)