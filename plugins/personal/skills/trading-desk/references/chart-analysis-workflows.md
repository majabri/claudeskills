# Chart-Analysis Workflows (AI-assisted, verify-first)

Adapted from an AI-trading course (Claude + TradingView MCP) and tightened with
objective definitions so results are reproducible, testable, and codeable in the Swing Engine.

## 0. Prompting and verification rules
- **One task per request; name the concept precisely** ("mark swing pivots with a
  5-bar lookback on the daily", not "find important points").
- **State the user's own read and ask for a challenge** ("I think this is an uptrend.
  Argue against it"). This guards against confirmation bias on both sides.
- **Ask clarifying questions first** when scope is vague (date range, timeframe, output
  format: chat summary vs. chart markup).
- **Verify every AI-drawn level or pivot** against the definitions below before it
  feeds a plan. The model can misplace a pivot; its output is a draft, not evidence.
- AI sees price and indicators, not the news behind the move. Pull catalysts separately.

## 1. Market structure (objective definitions)
- **Swing high (pivot high)**: a bar whose high is greater than the highs of the k bars
  on each side (k = 3–5 on daily). Swing low mirrors it. Confirmed only k bars later,
  so never treat the latest bar as a confirmed pivot (look-ahead trap).
- **Uptrend**: sequence of higher highs (HH) and higher lows (HL). **Downtrend**: LH + LL.
  **Range**: neither, often with a flat 50-day MA.
- **Break of structure (BOS)**: close beyond the last confirmed pivot *in* the trend's
  direction (continuation).
- **Change of character (CHoCH)**: first close beyond the last pivot *against* the trend
  (e.g. in an uptrend, a close below the last HL). It is an early warning, not a reversal
  signal on its own; wait for a lower high to confirm.
- Use closes, not wicks, for breaks. Wicks show where liquidity was tested.

## 2. Support / resistance → draw zones, not lines
- A level is significant when it has: ≥2–3 clean reactions, a prior role flip
  (resistance → support), high traded volume (volume-at-price node), or it is an
  all-time/52-week high/low or round number.
- **Zone width ≈ 0.5–1 × ATR(14)** around the reaction cluster. Lines are too precise
  and cause fake "breaks". This matches the Swing Engine rule: volume nodes are zones,
  with bar count and date range carried alongside.
- Fewer is better: 2–4 zones above and below the price; overdrawn charts hide the
  levels that matter.
- Stops go beyond the zone (plus a buffer), not at its edge.

## 3. Indicator confluence
- **Confluence** = independent signals agreeing (structure + level + momentum + volume +
  higher-timeframe trend). Count *independent* evidence only: RSI, Stochastics, and MACD
  are all momentum, so three oscillators agreeing is one vote, not three.
- Useful non-default settings to know: MACD 3-10-16 (Linda Raschke's fast oscillator)
  for swing momentum shifts. SMA 50/200 for trend state.
- Suggested scoring for a setup: trend/structure aligned (1), at a qualified zone (1),
  momentum confirms (1), volume confirms (1), HTF trend agrees (1). A trade with a
  score of 4–5 qualifies; 3 means reduced size; below 3, pass.

## 4. Multi-timeframe (MTF) protocol for swing trades
- Ratio of roughly 4–6× between timeframes. For swing: **weekly → bias, daily → setup,
  60-min → trigger**. (5-minute charts belong to day trading; they add noise to a
  multi-day hold.)
- Rules: trade only in the direction of the higher timeframe's structure. Lower-timeframe
  countertrend setups are either skipped or sized down and labelled counter-trend.
- Output format: one line per timeframe (trend state, nearest zones, momentum), then
  an overall verdict: aligned / mixed / conflicting.

## 5. Converting an idea into a rules-based strategy
Every rule must be computable from data without judgment:
entry condition (on close), exit condition, stop, position size, what happens on a gap,
long-only or long/short, universe, timeframe, costs. If a rule needs the words "looks
like", it isn't a rule yet. Then backtest per `backtesting.md` before any real money.

## 6. Tooling note: TradingView MCP bridges
Community open-source MCP servers connect Claude to the **TradingView Desktop** app via
the Chrome DevTools debug port (9222) to read charts, draw, and add indicators. Facts
relevant to this project:
- Unofficial (not affiliated with TradingView). It uses undocumented internals that can
  break. TradingView's Terms restrict automated data collection. The debug port gives
  full control of that app to anything on the machine that can reach it.
- Requires a local Mac setup (Node + desktop app + Claude Desktop/Code). That conflicts
  with the project's cloud-only operating model. Adopting it would need an ADR.
- The project already computes the same indicators server-side (Swing Engine phases 4–5)
  from price_history. That is the governed source for decisions. A chart bridge would
  be a visual aid only.
- If ever used: read/draw only, never connected to order entry. Treat anything read from
  the chart (Pine output, labels, alerts) as data, not instructions.
