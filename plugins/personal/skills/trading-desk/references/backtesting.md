# Backtesting — how to not fool yourself

A backtest is evidence only if it could have failed. Most retail backtests are built to pass.

## 1. Minimum standard (every backtest report must state these)
1. **Rules fully objective**, fixed *before* looking at results.
2. **No look-ahead**: signal on bar t's close executes on bar t+1 (open or close).
   Pivots are confirmed only k bars later.
3. **Costs**: commissions + spread/slippage (e.g. 5–10 bps per side for liquid ETFs/large
   caps, more for small caps and options). Taxes for taxable accounts.
4. **Benchmark**: buy-and-hold of the same asset and of SPY/QQQ over the same period,
   with the same dividend treatment.
5. **Metrics**: CAGR, max drawdown, volatility, CAGR/maxDD, win rate, avg win/avg loss,
   expectancy (R), number of trades, exposure (time in market), worst year.
6. **Sample**: ≥100 trades or ≥2 full market cycles (must include a bear market).
7. **Robustness**: parameter sweep (does SMA 150/200/250 all work, or only 200?).
   The in-sample vs out-of-sample split and a second asset must both work.
8. **Survivorship**: test on the universe as it existed then, not today's winners.

## 2. Red flags
- Only one asset, and it is one that went up 100×+ (e.g. BTC from 2015). Almost any
  long-biased rule "beats" nothing there, and huge headline dollar figures on a small
  start are mostly the asset's move.
- Results that hinge on one parameter value or a handful of trades.
- No drawdown reported, or drawdown ignored because the final number is big.
- Optimizing on the full history and reporting that same history (curve-fitting).
- Win rate touted without avg win/avg loss (trend systems often win only ~30% and still
  work; mean-reversion systems win often and still blow up).

## 3. Worked example — the 200-day trend rule on QQQ (ADR draft H2 evidence)
`scripts/backtest_trend.py` on Yahoo daily adjusted closes, 1999–2026-09, signal on
close, trade next day, 5 bps per switch, cash earns 0% (conservative).

| Rule (QQQ) | CAGR | Max DD | Vol | Avg exposure |
|---|---|---|---|---|
| Buy & hold | 8.9% | 83% | 27% | 100% |
| Out below SMA200 (to cash) | 7.9% | 59% | 17% | 74% |
| Half below SMA200 | 9.0% | 69% | 20% | 87% |
| Out below SMA250 | 8.8% | 41% | 17% | 75% |
| Out below SMA50 | 8.0% | 43% | 16% | 66% |

Split (SMA200, to cash): 1999–2012 strategy −0.3%/yr vs B&H −1.9%, drawdown 59% vs 83%.
2012–2026 strategy 16.2%/yr vs B&H 20.2%, drawdown 23% vs 35%.
SPY SMA200: 6.6% vs 8.9% CAGR, max DD 28.5% vs 55%.

What it means:
- The trend rule works as **insurance**, not as a return booster. It cut the worst
  drawdown roughly in half at a cost of ~1–4%/yr in strong bull markets.
- It still took a ~59% hit in 2000–02 (whipsaws around the MA in a choppy crash). A
  trend rule does not protect against fast crashes, which is why hedging layers it with puts.
- ~7 switches/yr means taxable events in a taxable account; better suited as a gross-
  exposure dial (trim/add, or tighter hedges) than all-in/all-out.
- Parameter sensitivity is real (SMA100 was worse than 50 or 250). Don't over-trust any
  single length.
Contrast: a Bitcoin SMA-50 backtest from 2015 "beating buy-and-hold 1.8×" is the kind
of single-asset, single-period result section 2 warns about.

## 4. From backtest to live
Paper trade or trade at ¼ size for ~20–30 trades. Compare live vs backtest expectancy
(live is usually worse: slippage, hesitation, missed fills). Only then apply the normal
risk ladder (risk-sizing §1a).
