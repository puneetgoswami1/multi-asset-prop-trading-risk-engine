-- =====================================================================
-- MULTI-ASSET TRADING RISK & DRAWDOWN ENGINE
-- Author: Puneet Goswami
-- Description: Calculates daily mark-to-market returns, high-water marks (HWM),
--              and rolling drawdown percentages across asset allocations.
-- =====================================================================

WITH daily_asset_pnl AS (
    SELECT 
        trade_date,
        asset_class,
        ticker_symbol,
        realized_pnl_usd,
        unrealized_pnl_usd,
        (realized_pnl_usd + unrealized_pnl_usd) AS net_daily_pnl_usd,
        gross_position_exposure_usd
    FROM trading_dw.fct_daily_positions
    WHERE trade_date >= CURRENT_DATE - INTERVAL '180 DAYS'
),

portfolio_daily_aggregation AS (
    SELECT 
        trade_date,
        SUM(net_daily_pnl_usd) AS portfolio_pnl_usd,
        SUM(gross_position_exposure_usd) AS total_gross_exposure_usd
    FROM daily_asset_pnl
    GROUP BY trade_date
),

portfolio_equity_curve AS (
    SELECT 
        trade_date,
        portfolio_pnl_usd,
        total_gross_exposure_usd,
        
        -- Starting with $100,000 standard prop firm funded account baseline
        100000.0 + SUM(portfolio_pnl_usd) OVER (
            ORDER BY trade_date ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS current_account_equity_usd
    FROM portfolio_daily_aggregation
),

high_water_mark_engine AS (
    SELECT 
        trade_date,
        portfolio_pnl_usd,
        total_gross_exposure_usd,
        current_account_equity_usd,
        
        -- High Water Mark: Peak equity achieved up to this trading day
        MAX(current_account_equity_usd) OVER (
            ORDER BY trade_date ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS high_water_mark_usd
    FROM portfolio_equity_curve
)

SELECT 
    trade_date,
    current_account_equity_usd,
    high_water_mark_usd,
    portfolio_pnl_usd,
    ROUND((portfolio_pnl_usd / LAG(current_account_equity_usd, 1, 100000.0) OVER (ORDER BY trade_date)) * 100, 3) AS daily_return_pct,
    
    -- Absolute drawdown in USD
    ROUND((current_account_equity_usd - high_water_mark_usd), 2) AS drawdown_usd,
    
    -- Drawdown percentage from Peak Equity
    ROUND(((current_account_equity_usd - high_water_mark_usd) / high_water_mark_usd) * 100, 2) AS drawdown_percentage,
    
    -- Prop firm compliance guardrail (Max 10% Trailing Drawdown, Max 5% Daily Loss)
    CASE 
        WHEN ((current_account_equity_usd - high_water_mark_usd) / high_water_mark_usd) <= -0.10 THEN 'BREACH_TRAILING_MAX_LIMIT'
        WHEN (portfolio_pnl_usd / LAG(current_account_equity_usd, 1, 100000.0) OVER (ORDER BY trade_date)) <= -0.05 THEN 'BREACH_DAILY_LOSS_LIMIT'
        WHEN ((current_account_equity_usd - high_water_mark_usd) / high_water_mark_usd) <= -0.07 THEN 'WARNING_7PCT_EXPOSURE'
        ELSE 'RISK_TOLERANCE_NORMAL'
    END AS risk_breach_flag
FROM high_water_mark_engine
ORDER BY trade_date DESC;