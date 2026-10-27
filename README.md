# Multi-Asset Prop Trading Risk & Volatility Dashboard

An automated quantitative risk management system designed for proprietary trading desks and funded accounts to monitor daily portfolio drawdowns, VaR tail exposure, and risk-adjusted efficiency ratios across spot and derivative holdings.

## Overview
Proprietary trading accounts operate under strict risk compliance rules (such as max 5% daily loss and 10% maximum trailing drawdown). This engine computes rolling portfolio returns across multi-asset allocations (Gold, Forex, Indices, Crypto) to ensure capital preservation and audit risk metrics before broker margin breaches occur.

## Project Structure
- `portfolio_risk_drawdown.sql`: Windowed SQL pipeline calculating daily mark-to-market equity curves, High-Water Mark (HWM), and automated breach notifications.
- `prop_risk_engine.py`: Quantitative Python engine computing Sharpe ratios, Sortino ratios, 95%/99% Value-at-Risk (Historical & Parametric), and maximum peak-to-trough drawdowns.
- `requirements.txt`: Python dependencies.

## Core Quantitative Metrics
1. **Sharpe & Sortino Ratios:** Benchmarked against the 4.5% risk-free rate, penalizing downside volatility over standard standard deviation.
2. **Value-at-Risk (VaR):** Evaluates 1-day extreme tail risk at both 95% and 99% confidence intervals to size trade leverage appropriately.
3. **High-Water Mark (HWM) Drawdown:** Tracks dynamic equity peaks (`MAX(equity) OVER (...)`) to calculate real-time trailing drawdown percentages.

## How to Run

```bash
# Clone the repository
git clone [https://github.com/puneetgoswami1/multi-asset-prop-trading-risk-engine.git](https://github.com/puneetgoswami1/multi-asset-prop-trading-risk-engine.git)
cd multi-asset-prop-trading-risk-engine

# Install dependencies
pip install -r requirements.txt

# Run risk engine
python prop_risk_engine.py