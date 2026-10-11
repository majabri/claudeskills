# Market Regime, Catalysts & Data

## 1. Regime checklist (score it before any new trade)
| Signal | Risk-on | Risk-off |
|---|---|---|
| SPY & QQQ vs 50/200-day MA | Above, MAs rising | Below, 50 < 200 |
| Breadth (% of S&P 500 above 50-day; A/D line) | >60%, A/D rising | <40%, A/D falling / diverging |
| New highs vs new lows | Highs dominate | Lows dominate |
| VIX | <~18 and falling | >~25 or spiking; term structure inverted (VIX > VIX3M) |
| Distribution days (index down ≥0.2% on higher volume) in 25 sessions | ≤3 | ≥5–6 |
| Credit (HYG vs IEF), dollar, 10y yield trend | Credit firm | Credit spreads widening |
| Leadership | Growth/cyclicals leading | Defensives (XLU, XLP) leading |

Mapping: Risk-on → full-size longs, few shorts. Mixed → half size, only A+ setups.
Risk-off → small/no new longs, shorts & hedges allowed, raise cash.

## 2. Catalyst calendar (always check the trade window)
- Company: earnings (Nasdaq calendar), ex-dividend, investor day, FDA/regulatory dates,
  lockup expiries, index rebalances, secondary offerings.
- Macro: FOMC decisions & minutes, CPI/PPI, jobs report (first Friday), GDP, PCE,
  Treasury refunding, major geopolitical events (RSS feeds).
- Market structure: monthly options expiration (3rd Friday), quarterly "quad witching",
  end-of-quarter rebalancing, holiday-thin sessions.

## 3. Fundamental overlay for swing trades
Swing trades are technical-first, but fundamentals improve odds: accelerating EPS and
revenue growth, positive estimate revisions, strong guidance, institutional
accumulation (13F trends), insider buying (Form 4 via EDGAR). For shorts, the mirror:
decelerating growth, negative revisions, insider selling clusters, dilution.

## 4. Data sources (free tier — OD-002)
| Need | Source |
|---|---|
| Daily OHLCV / backfill | Yahoo chart endpoint (current price_history source; Stooq retired after bot challenges) |
| Earnings & economic calendar | Nasdaq public API |
| Filings, insider trades, 13F | SEC EDGAR |
| Macro series (rates, credit spreads, VIX history) | FRED |
| Quotes, basic fundamentals, news | Finnhub / AlphaVantage free tiers |
| Breadth proxy | RSP/SPY ratio (equal-weight vs cap-weight) |
| Short interest | Exchange/FINRA bi-monthly publications (lagged ~2 weeks) |
| Options chains/IV | Broker (Fidelity) chain is the reliable source; free APIs are thin |

Always state data as-of time. Short interest and 13F data are lagged — treat as context,
not timing signals.
