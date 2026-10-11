# Options

## Contents
1. Contract basics  2. Pricing & greeks  3. Implied volatility  4. Strategy selection
5. Strategy playbook  6. Trade selection (strike/expiry/liquidity)  7. Management
8. Assignment, exercise, expiration  9. Earnings  10. Common mistakes

## 1. Contract basics
- US equity options: 1 contract = 100 shares, American-style (exercisable any time).
  Index options (SPX, NDX, RUT) are European-style, cash-settled, and get Section 1256
  tax treatment (60% LT / 40% ST regardless of holding period).
- Call = right to buy at strike; put = right to sell. Buyer pays premium (max loss);
  seller collects premium and takes the obligation.
- Premium = intrinsic value + extrinsic (time value). Only extrinsic decays.
- Weeklies and 0DTE exist on many names; short-dated = high gamma, fast decay.
- Brokers gate strategies by **option approval level** (covered → long options →
  spreads → uncovered). Confirm Amir's Fidelity level before proposing a structure.
  IRAs typically allow covered calls, cash-secured puts, long options, and sometimes
  defined-risk spreads — never naked calls.

## 2. Greeks (what each one means for P&L)
| Greek | Meaning | Practical read |
|---|---|---|
| Delta | $ change per $1 move in stock; also ≈ probability ITM at expiry | 0.30Δ call ≈ 30% chance ITM; position delta × 100 = share-equivalent |
| Gamma | Change in delta per $1 | Highest ATM near expiry → short-dated options swing wildly |
| Theta | $ lost per day from time decay | Accelerates in last ~30–45 days; long options bleed, short options earn |
| Vega | $ change per 1-pt IV change | Long options = long vol; IV crush after events hurts buyers |
| Rho | Rate sensitivity | Minor except for LEAPS |

Use `scripts/trade_math.py greeks` for Black-Scholes estimates when the chain lacks them.

## 3. Implied volatility
- IV = market's priced expected move. **Expected move ≈ S × IV × √(DTE/365)** (1 SD,
  ~68% probability). Around earnings, the ATM straddle price ≈ implied earnings move.
- **IV rank** = (IV − 52w low) / (52w high − 52w low). **IV percentile** = % of days
  IV was lower. High (>50) → favor *selling* premium / spreads; low (<25) → favor
  *buying* options.
- Compare IV to realized (historical) volatility: IV ≫ HV means options are rich.
- Skew: puts usually carry higher IV than calls (crash protection demand).

## 4. Strategy selection matrix
| View \ IV | Low IV (buy premium) | High IV (sell premium / defined risk) |
|---|---|---|
| Bullish, strong | Long call (≥60 DTE, 0.60–0.70Δ), bull call spread | Bull put spread, cash-secured put |
| Bullish, mild/stock-replacement | Deep ITM call (0.80Δ) or LEAPS | Covered call on shares, put credit spread |
| Bearish | Long put, bear put spread | Bear call spread |
| Neutral / range | Calendar spread | Iron condor, short strangle (not for most personal accounts) |
| Big move, direction unknown | Long straddle/strangle (pay for it) | Avoid — you're buying expensive vol |
| Hedge a holding | Protective put (buy when IV low) | Collar (sell call to fund put) |

## 5. Strategy playbook
- **Long call/put**: max loss = premium; breakeven = strike ± premium. For swing
  trades use 45–120 DTE so theta doesn't kill a slow-developing thesis. Exit at the
  swing plan's stop on the *underlying*, or at ~50% premium loss, whichever first.
- **Vertical debit spread** (buy near strike, sell farther strike, same expiry):
  cheaper, lower vega/theta; max gain = width − debit. Good default for directional
  swings when IV is moderate/high.
- **Vertical credit spread**: collect credit; max loss = width − credit. Choose short
  strike ~0.20–0.30Δ; take profit at 50% of max; exit/roll if short strike is breached.
- **Covered call**: own 100 shares, sell OTM call (~0.20–0.30Δ, 30–45 DTE). Income in
  exchange for capped upside and assignment risk. Don't sell calls below your cost
  basis unless you're fine selling there. Avoid across ex-dividend if ITM (early
  assignment).
- **Cash-secured put**: sell put at a price you'd happily own; cash reserved =
  strike × 100. Pairs with buy-back zones (ADR-APP-003): a CSP at a buy-back level
  gets paid to wait. Wheel = CSP → assigned → covered call.
- **Protective put / collar**: insurance on a concentrated or earnings-exposed
  holding. Costs premium; collars trade upside for cheap protection.
- **Calendars/diagonals**: sell near-term, buy longer-term; profit from theta
  differential and IV term structure — advanced, needs active management.
- **Undefined-risk short options (naked calls, short strangles)**: out of scope for
  this account set unless Amir explicitly sets it as policy.

## 6. Picking the contract
- **Liquidity first**: bid-ask spread ≤ ~5–10% of mid (tighter for large trades),
  open interest in the hundreds+, decent volume. Illiquid chains silently cost more
  than commissions.
- Always use **limit orders at/near mid**; walk the price in small steps.
- Strike by delta, expiry by thesis duration × 1.5–2 (give the trade time).
- Size options on **max loss**, not share-equivalents: premium paid (or spread max
  loss) = the R for the sizing formula.

## 7. Management rules
- Plan exits before entry: profit target (e.g. 50–100% for debits, 50% for credits),
  loss exit, and time exit (close or roll with ~21 DTE on short premium to avoid gamma).
- Roll only when the thesis is intact — rolling a loser to avoid realizing a loss is
  averaging down in disguise.
- Watch position delta across the whole portfolio, not just per trade.

## 8. Assignment, exercise, expiration
- Short options can be assigned any time (American). Most common: short ITM calls
  the day before ex-dividend when the remaining extrinsic < dividend; deep ITM puts
  near expiry.
- OCC auto-exercises options ≥$0.01 ITM at expiry. Long options you can't afford to
  exercise must be closed first. **Pin risk**: short strike near price at expiry —
  close it instead of guessing.
- Spreads: if the short leg is assigned early, you hold stock + the long leg; the
  max-loss math still holds but margin can spike — manage same day.

## 9. Earnings
- IV inflates into the event and collapses after ("IV crush"). Buyers need a move
  larger than the implied move to profit.
- Defined-risk structures only across earnings; size so a max loss is tolerable.
- Consistent with Swing Score A4: an earnings position is a *separate, intentional*
  decision — label it as such in the plan.

## 10. Common mistakes
Buying cheap far-OTM weeklies (lottery tickets), ignoring IV, market orders on wide
spreads, sizing by contracts not dollars at risk, holding short options into expiry
week, forgetting dividends/assignment, averaging down on decaying options.
