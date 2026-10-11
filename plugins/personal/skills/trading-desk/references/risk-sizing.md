# Risk & Position Sizing

The single most important skill. Setups decide *whether*; sizing decides *survival*.

## 1. The core formula
- R (per-share risk) = |entry − stop|  (use gap-adjusted stop for shorts/earnings)
- Risk budget ($) = account equity × risk % per trade
- Shares = floor(risk budget ÷ R)
- Options: contracts = floor(risk budget ÷ (max loss per contract))
Then cap by: IPS concentration (C2), margin cap (C3), liquidity, and heat.

Risk % per trade is a policy number for Amir to set and sign off (money-adjacent).
Compute it on **equity (net liquidation value)**, never on margin buying power.

## 1a. How to choose the risk % (evidence, not vibes)
Risk % is set by the drawdown you can live through, not by the return you want.
Losing streaks are normal: at a 40% win rate, a streak of 8 straight losses shows up
in about half of all 100-trade sequences, and 10 in a row in about 1 of 5. A 10-loss
streak costs about −10% at 1% risk, −18% at 2%, −26% at 3%.

Monte Carlo (20,000 runs × 100 trades; 40% win rate, wins 1–3R, 15% of losses gap to
1.5–3R; a modest real edge ≈ +0.09R/trade):

| Risk/trade | Median max DD | Bad-case (95th) max DD | Median result | Bad-case (5th) result | P(end −30% or worse) |
|---|---|---|---|---|---|
| 0.25% | 3.5% | 7% | +2% | −4% | ~0% |
| 0.5% | 7% | 14% | +4% | −9% | ~0% |
| 1% | 13.5% | 26% | +8% | −18% | 0.4% |
| 2% | 26% | 46% | +13% | −34% | 7% |
| 3% | 37% | 61% | +15% | −49% | 16% |

Same test with **no proven edge** (33% win rate): 1% → median −14%, 10% chance of
−30%+; 2% → median −28%, 45% chance of −30%+.

Takeaways:
- Doubling risk from 1% → 2% barely raises the median outcome but roughly doubles
  the typical drawdown and multiplies the blow-up odds. Tail risk grows much faster
  than reward.
- Until the journal shows positive expectancy over ≥30 graded trades, the edge is
  **unproven** and the no-edge table is the honest one to plan against.
- A deadline or return target is not an input to risk %. Raising risk to "catch up" is
  the classic path from drawdown to ruin.
- Margin multiplies all of these relative to equity.

Proposed policy ladder (for sign-off; practitioner-consistent, not a guarantee):
- **Phase A: unproven edge** (<30 graded trades or expectancy ≤0): 0.5% per trade,
  max heat 3%.
- **Phase B: proven edge** (≥30 trades, expectancy >0, plan-followed rate ≥80%): up to
  1% per trade, max heat 5–6%.
- **Drawdown brake:** at −5% from equity peak drop one phase (or halve risk); at −10%
  stop new entries and review; restart at 0.25–0.5%.
- **Cap:** never above 1% per trade while margin debit is outstanding. Single-name
  earnings holds size to the implied move, not the stop.
The same ladder is meant to parameterize Swing Engine phase 7 (§16 sizing).

## 2. Portfolio heat
- Heat = sum of open risk (distance to stops × size) across all trades.
- Typical practitioner caps: total heat ≤ ~5–6% of equity; ≤ ~2–3% in one sector
  or correlated cluster (e.g. several semis = one bet).
- Leverage (margin) multiplies heat against equity; compute margin-adjusted exposure
  and borrowing cost using the rate from ips_lite (never assumed).

## 3. Expectancy — know your edge
- Expectancy per trade (in R) = win% × avg win(R) − loss% × avg loss(R)
- Example: 40% winners averaging 2.5R, losers averaging 1R → 0.4×2.5 − 0.6×1 = +0.4R
- Need ≥20–30 trades per setup before trusting the numbers.
- Kelly fraction = W − (1−W)/B (W = win rate, B = avg win/avg loss). Full Kelly is
  far too aggressive given estimation error; if used at all, ¼ Kelly as a ceiling.

## 4. Drawdown rules (circuit breakers)
- Losses compound asymmetrically: −10% needs +11%, −25% needs +33%, −50% needs +100%.
- Practical ladder: after a ~5% equity drawdown halve risk per trade; after ~10% stop
  new trades and review the journal; resume at reduced size after process fixes.
- Several consecutive stop-outs = regime mismatch signal, not bad luck to fight.

## 5. Correlation & concentration
- Check new trade against existing holdings (same sector, factor, index weight).
  Buying QQQ calls while long NVDA/MSFT/AAPL is adding to the same bet.
- Enforce IPS C2 (single-position soft cap) including option delta-equivalent exposure.

## 6. Gap risk
- Stops don't protect against overnight gaps (earnings, news, macro). For positions
  held through known events, size so the *plausible gap* (≈ implied move, or 2×) is
  within tolerance, or hedge.

## 7. Journal fields (feed outcome grading)
Date, ticker, account, setup, thesis, entry/stop/target, size, R, risk %, regime,
IV (options), exit reason, R-multiple result, plan followed (Y/N), mistake tag,
lesson, screenshot/link.
