# Trade Plan Template (maps to recommendation.schema.json)

```
STATE: [ACTION RECOMMENDED | MONITOR | NO CHANGE | RISK REVIEW]
Ticker / account:            (which account — eligibility checked)
Strategy:                    (swing long | short | option structure)
Thesis (timeframe):          one sentence + expected holding period
Data as-of:                  timestamp + sources

Instrument & structure:      e.g. 100 sh, or "Buy 1 NOV-20 150C / Sell 1 NOV-20 160C"
Entry trigger:               e.g. buy-stop 152.40 above flag high, only if SPY > 50d
Stop / invalidation (price): e.g. 147.90 (below flag low, 1.6 ATR)
Invalidation (non-price):    e.g. guidance cut, sector leader breaks down, regime flips
Targets:                     T1 = 2R (161.40) sell 1/3; trail rest on 20-EMA close
Size:                        N shares/contracts; $ risk; % of equity; resulting position %
Max loss incl. gap:          $ (and assumption)
Reward : risk:               x.x : 1
Supporting evidence:         [source_id, claim] pairs
Counterargument:             strongest case against
Key risks:                   list
Probability / impact:        e.g. "~45% reach T1 before stop (judgment); impact +2R / −1R"
IPS check:                   C2 concentration __% (cap 30%) | margin __% (cap 25%) | account OK
Calendar:                    earnings __ | ex-div __ | macro events in window
Management plan:             at +1R / at T1 / gap down / pre-earnings / time stop
Tax note:                    wash-sale window, ST vs LT
```

## Worked example A — swing long (illustrative numbers, not a recommendation)
Account equity $120,000; risk policy 0.75% → budget $900.
Stock in stage 2, 5-day bull flag above rising 20-EMA; flag high 152.40, low 148.00,
ATR 2.80. Entry 152.40 (buy-stop), stop 147.90 → R = 4.50.
Shares = 900 / 4.50 = 200 → $30,480 position = 25.4% of equity → passes 30% C2 soft
cap but is large; check correlation with existing holdings. T1 = 152.40 + 2×4.50 = 161.40.
Earnings in 18 trading days → plan exits or trims before; not an earnings play.
State: MONITOR until trigger hits, then ACTION RECOMMENDED if regime still risk-on.

## Worked example B — bearish view in an IRA (can't short)
Thesis: XYZ breaks down after guidance cut; IV rank 70 (rich).
Shorting not allowed in IRA → consider bear call spread (if approved) or a small put
debit spread. With high IV, credit spread: sell 0.25Δ call, buy call $5 higher, credit
$1.60 → max loss $340/contract. Budget $900 → 2 contracts ($680 max loss).
Exit at 50% of max profit or if price closes above short strike.

## Worked example C — covered call on an extended holding
Holding shows Swing Score 72 (A5: consider trimming 10–25%). Alternative to trimming:
sell a 30–45 DTE call ~0.25Δ on 20% of shares — collects premium, trims only if
called away. Check ex-dividend date (early assignment) and short-term vs long-term
tax status of the lot before choosing.
