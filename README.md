# Portfolio Drawdown & Value-at-Risk (VaR) Monitor

A quantitative risk tracking workflow that monitors daily mark-to-market equity, trailing High-Water Mark (HWM) drawdowns, and tail risk across multi-asset trading books.

## Problem Context
Funded trading accounts enforce strict daily loss (5%) and maximum trailing drawdown (10%) limits. This project tracks intraday equity peaks in SQL and computes Sharpe, Sortino, and 95%/99% Value-at-Risk metrics in Python.

## Files
- `portfolio_risk_drawdown.sql`: Computes cumulative equity curves, rolling High-Water Marks, and breach alerts.
- `prop_risk_engine.py`: Calculates Sharpe/Sortino ratios, Historical & Parametric VaR, and peak-to-trough drawdowns.
- `requirements.txt`: Python dependencies.

## How It Works
1. **High-Water Mark Tracking:** Uses `MAX(equity) OVER (...)` to measure real-time trailing drawdown from peak equity.
2. **Tail Exposure (VaR):** Estimates 1-day loss thresholds at 95% and 99% confidence levels across Gold, Forex, Indices, and Crypto positions.
3. **Downside Efficiency:** Compares Sortino vs. Sharpe ratios to isolate downside volatility.

## Run Locally

    git clone https://github.com/puneetgoswami1/multi-asset-prop-trading-risk-engine.git
    cd multi-asset-prop-trading-risk-engine
    pip install -r requirements.txt
    python prop_risk_engine.py
