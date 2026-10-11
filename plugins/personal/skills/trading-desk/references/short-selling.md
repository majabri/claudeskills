# Short Selling & Bearish Positioning

## 1. Mechanics
- You borrow shares, sell them, and must buy back later. Profit is capped at 100%
  (stock → 0); **loss is theoretically unlimited**.
- Requires a **margin account** (never IRA/custodial/529). Reg T initial margin for
  shorts is 150% of the short value (the 100% proceeds + 50%); maintenance at FINRA
  floor is higher for low-priced stocks and brokers set house minimums often 30–40%+,
  and much higher for volatile/HTB names. Check Fidelity's requirement per symbol.
- **Locate/borrow**: broker must locate shares. Easy-to-borrow (ETB) vs hard-to-borrow
  (HTB). HTB carries a daily borrow fee (annualized rate can be 20–100%+), and shares
  can be **recalled** — you may be bought in at a bad price.
- **Dividends**: short owes the dividend (paid out of your account) on the ex-date.
- **SEC Rule 201 (alternative uptick rule)**: when a stock falls ≥10% from prior close,
  short sales are restricted to prices above the national best bid for the rest of
  that day and the next. You can't press a short into a crash.
- **Constructive sale** (IRC §1259): shorting a stock you hold at a gain ("against the
  box") triggers gain recognition — not a tax dodge.

## 2. What makes a good short (and why it's harder than longs)
Markets drift up over time and short squeezes are violent, so the bar is higher.
Prefer shorts with several of:
- Stage-4 trend: below falling 50 and 200-day MAs, RS line at lows
- Broken thesis catalyst: guidance cut, lost customer, accounting/regulatory issue,
  failed product, dilution (secondary offering, ATM program)
- Failed rallies into declining MAs or anchored VWAP from a breakdown gap
- Sector weakness and risk-off regime
- Adequate liquidity; ETB; low-to-moderate short interest

## 3. Squeeze risk — screen every short for it
- **Short interest % of float** >15–20% and **days to cover** (SI ÷ avg daily vol) >5 = crowded
- High borrow fee / utilization near 100% = fragile
- Small float, retail/social attention, heavy call-option buying (gamma squeeze)
- Upcoming catalyst that could surprise positively
If crowded, express the view with **defined risk** (puts/put spreads) or pass.

## 4. Short-trade rules
- Stops above structure (the failed-rally high); gaps against shorts are common, so size
  on a *gap-adjusted* loss, not just the stop distance.
- Take profits faster than longs — downside moves are fast but mean-revert with
  short-covering rallies. Cover partials at support levels.
- Avoid holding shorts through the target's earnings unless that's the thesis.
- Never add to a losing short.

## 5. Bearish alternatives (often better for a personal account)

| Instrument | Pros | Cons |
|---|---|---|
| Long put | Defined max loss (premium), no borrow, no squeeze liquidation | Theta decay, IV cost; must be right on timing |
| Bear put spread | Cheaper, less vega/theta | Capped profit |
| Bear call spread (credit) | Profits if stock stays below short strike; theta positive | Requires spread approval; max loss = width − credit |
| Inverse ETF (e.g. SH, PSQ) | Allowed in more account types, no borrow | Daily reset → decay over time, esp. leveraged (SQQQ); for days–weeks only |
| Trim/sell existing longs | Simplest "short" is less long | — |
| Protective put on holding | Hedges a position you want to keep | Premium drag |
| Collar (long put + short call) | Low/no-cost hedge | Caps upside; call can be assigned |

Rule of thumb: if the account can't short, or the name is crowded/HTB, or the loss
must be strictly capped — use puts or put spreads.
