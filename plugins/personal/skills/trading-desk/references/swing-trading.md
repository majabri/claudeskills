# Swing Trading

Holding period: ~2 days to ~6 weeks. Edge comes from trading *with* the
intermediate trend, entering at low-risk points, and cutting losers fast.

## 1. Universe & trend filter (do this before looking at any chart pattern)

A long swing candidate should pass a trend template. Common version:
- Price > 50-day MA > 150-day MA > 200-day MA; 200-day rising ≥1 month
- Price within ~25% of its 52-week high and ≥30% above its 52-week low
- **Relative strength**: outperforming SPY (or its sector ETF) over 3 and 6 months.
  Compute RS line = stock / SPY; rising RS line near highs is a leader.
- Liquidity: avg daily $ volume comfortably large (e.g. >$20M) so stops fill near price.

Shorts mirror this: price < 50 < 200, falling 200-day, RS line making new lows,
underperforming sector.

Why: most big swing moves come from stocks already in stage-2 uptrends; fighting
the trend lowers win rate and forces wider stops.

## 2. Market stages (Weinstein)
- Stage 1 basing (flat 30-week MA) — watch, don't buy
- Stage 2 advancing (price above rising 30-week/150-day MA) — long setups
- Stage 3 topping (MA flattening, wide swings, failed breakouts) — trim, tighten
- Stage 4 declining (below falling MA) — short setups or cash

## 3. The setups

| Setup | What it looks like | Entry trigger | Stop (invalidation) |
|---|---|---|---|
| Pullback to MA | Uptrend pulls back 3–8 days on declining volume to rising 20-EMA or 50-SMA | Reversal bar: close above prior day's high, ideally on rising volume | Below the pullback low (or 1–1.5 ATR below MA) |
| Base breakout | Tightening range 3–12+ weeks (flat base, cup-handle, VCP contractions each shallower) | Close/move above pivot on volume ≥1.4–1.5× 50-day avg | Below the last contraction low / back inside base by >3–5% |
| Bull flag / high-tight flag | Sharp pole, then 1–3 week tight drift down/sideways | Break of flag's upper line | Below flag low |
| Gap-and-go / earnings gap | Gap up on strong earnings/guidance, holds gap first days | Break of first-day high or opening-range high | Below gap-day low (gap failure = thesis broken) |
| Failed breakdown (spring) | Undercuts obvious support, reclaims it fast | Reclaim of support level | Below the undercut low |
| Inside-day / NR7 compression | Range contraction in trend | Break of the inside bar's high | Below the inside bar's low |

Short-side analogs: rally into falling 20/50 MA that fails (bear flag), breakdown
from a topping base on volume, failed breakout (bull trap), earnings gap-down that
can't reclaim.

## 4. Confirmation signals (weigh, don't worship)
- **Volume**: breakouts on expanding volume; pullbacks on contracting volume.
- **Momentum**: RSI(14) 40–50 holding in uptrends = healthy pullback; bearish
  divergence (higher price, lower RSI) at highs = caution. RSI >70 alone is NOT a sell
  in a strong trend (same reasoning as Swing Score A1 cap).
- **MACD** crossovers are lagging; use as confirmation, not trigger.
- **Anchored VWAP** from the last earnings gap or major low: price above = buyers in control.
- **Multiple-timeframe**: weekly trend up, daily setup, 60-min trigger.

## 5. Entries
- Prefer *buy-stop above trigger* over guessing the low — you pay a little more for
  confirmation.
- Avoid chasing: >5% above the pivot/breakout point = extended; wait for the next setup.
- First 30 minutes are noisy; for breakouts, a close above the pivot is more reliable
  than an intraday poke.

## 6. Stops
- Structural stop (below the swing low / base) is primary.
- ATR sanity check: stop distance typically 1–2.5× ATR(14). Tighter than ~1 ATR gets
  stopped by noise; much wider means the entry was late — reduce size or pass.
- Hard rule of thumb for breakouts: exit if it falls 7–8% below entry or back deep
  into the base, whichever first.
- Stops are placed in the market (or alerts with discipline). Moving a stop *down* is
  never allowed; moving it up is how you protect gains.

## 7. Exits & trade management
- **Targets in R** (R = entry − stop). Minimum planned reward 2R; many plans take
  ⅓–½ off at 2R, move stop to breakeven, trail the rest.
- **Trailing**: close below 10-EMA (fast leaders) or 20-EMA (normal) or 50-SMA
  (position-style). Or chandelier stop: highest high − 3×ATR.
- **Time stop**: if the trade hasn't worked in ~5–10 sessions, capital is better elsewhere.
- **Into strength**: sell partial when extended (e.g. >20–25% above 50-day, climax
  volume, widest-range day of the move) — this is exactly what Swing Score A2/A3
  measure; A5/A6 bands suggest 10–25% / 25–50% trims.
- **Earnings**: decide before the date — close, trim to a size whose gap loss you
  can tolerate, or hedge with a put. Don't let the calendar decide for you.
- After trims on valuation/overbought, buy-back zones (ADR-APP-003: −5/−10/−15%)
  provide re-entry levels; never attach them to thesis-break sells.

## 8. Common failure modes
- Buying a "cheap" stock in a downtrend (catching knives)
- Averaging down on a swing trade (turns trades into bag-holding "investments")
- Oversizing a favorite; undersizing the best setup out of fear
- Taking profits too early and losses too late (negative skew) — track avg win/avg loss
- Trading every day because the rule changed — fewer, higher-quality setups win
