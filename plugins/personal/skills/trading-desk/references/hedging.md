# Portfolio Hedging

Hedging is insurance, not a profit center. Every hedge has a cost, paid in premium,
capped upside, or lagging returns in rallies. Decide what you are protecting against
before you choose a tool.

## 1. First question: what is the risk, exactly?
| Risk | Best-matched tool |
|---|---|
| Too much exposure overall / margin too high | **De-gross first**: trim, pay down margin. The cheapest hedge. It removes interest cost instead of adding premium. |
| Broad market selloff (beta) | Index puts or put spreads on the index the book actually tracks (QQQ for a tech-heavy book, SPY for a broad one) |
| One concentrated / extended winner | Collar or protective put on that name, or trim (Swing Score A5/A6) |
| Single-name event (earnings, FDA, lawsuit) | Short-dated put or put spread on that name, or reduce size before the event |
| Slow grinding bear market | Trend rule (cut exposure below the 200-day / on regime flip) |
| Crash / gap (−20% in days) | Small far-OTM index puts ("tail"), bought when volatility is cheap |

Index hedges do **not** cover stock-specific risk. A QQQ put won't help if one holding
gaps −30% on its own earnings while the market is flat.

## 2. The tool kit
**De-grossing / margin reduction.** Selling 10% of the book cuts beta exposure 10%
with no premium, no decay, no assignment. It is taxable if the lots are at a gain. On
margin, it also cuts interest cost at the ips_lite rate. Consider it first whenever
margin usage is near the IPS cap.

**Protective put.** Buy a put under a holding or index. It gives a floor with
unlimited upside, and it is the most expensive form. Systematic rolling of index puts
has historically lost money over long samples. Index implied volatility tends to
exceed realized volatility, so insurance is structurally overpriced on average. Use
protective puts tactically (event, known risk window) or small (tail), not as a
permanent overlay.

**Put spread (debit).** Buy a put about 3–5% OTM and sell one about 10–15% further
down. It costs much less. It covers a moderate correction (10–20%) but not the move
beyond the short strike. For most individual portfolios this is the default
compromise.

**Collar.** Own shares, buy a put, sell an OTM call to pay for it. It can be close to
zero cost. The trade-off is capped upside and the call can be assigned. It fits best
on positions you'd trim at the call strike anyway (extended names, Swing Score ≥65).
Check ex-dividend dates and lot tax status first; a called-away short-term lot is a
short-term gain.

**Put-spread collar.** Buy a put spread and sell a call. It is cheaper still, with
protection only for the band between the two put strikes.

**Tail hedge.** Small allocation to far-OTM (10–20% OTM) index puts, 3–6 months out.
Budget it as a fixed premium (e.g. a fraction of a percent per quarter). It expires
worthless most of the time; that is the cost of crash convexity.

**Trend / regime rule.** Reduce exposure when the governing index closes below its
200-day MA or the regime checklist flips risk-off. It has no premium, and research
finds trend following has done well in prolonged bear markets. It is slower than
puts: it won't protect a one-day gap and can whipsaw in choppy markets.
Own test on QQQ 1999–2026 (backtesting.md §3): max drawdown fell from 83% to 41–59%
depending on MA length, at a cost of ~1–4%/yr of return in strong bull markets.
Better as a gross-exposure dial than all-in/all-out.

**Inverse ETFs (SH, PSQ; avoid leveraged SQQQ/SPXU for anything beyond days).** Simple,
and allowed in more account types. Daily reset causes decay over longer holds.

**Diversifiers.** Assets that don't move with the book: Treasuries (in deflationary
selloffs), gold, cash. Owning five high-beta growth names in five "industries" is one
bet in a risk-off week.

## 3. Sizing an index hedge (beta-weighting)
1. Portfolio beta-weighted exposure = Σ (position $ × position beta vs the index).
   Estimate beta from 6–12 months of daily returns (price_history), or use published beta.
2. Hedge notional = beta-weighted exposure × hedge ratio (e.g. 50% partial, 100% full).
3. Contracts = hedge notional ÷ (index ETF price × 100) × (1 ÷ |put delta|) for a
   delta-matched hedge. Use delta = 1 for protection at expiry below the strike.
   `scripts/trade_math.py hedge` does this.
4. Round **down** for small books. One SPY/QQQ contract controls 100 × the ETF price,
   often a large share of a personal portfolio, so hedges come in coarse steps. If one
   contract over-hedges, use a narrower put spread, a single-name hedge on the biggest
   risk, or de-gross instead.

## 4. Choosing strike and expiry
- 60–120 DTE for tactical hedges (lower daily theta than 30 DTE). Roll at ~30–45 DTE.
- Strike by the loss you're willing to absorb first (the deductible): 5% OTM is common
  for tactical, 10–20% OTM for tail.
- Buy protection when implied volatility is low (VIX calm, IV rank low), not in a panic
  when puts are most expensive. In panics, spreads and collars (selling rich premium)
  work better than outright puts.
- Set a **hedge budget** per year (as % of portfolio) and track it like any other
  expense. Common practitioner ranges are around 1–2%/yr for partial protection.
  Full permanent put coverage has historically cost much more.

## 5. Monetizing and managing
- Decide in advance when to take profits on a hedge. Example: at +100–200% or when
  the index hits the short put strike. A hedge that pays off and is held to expiry
  often gives the gain back.
- After monetizing, re-hedge smaller/cheaper or redeploy per the plan. Don't buy the
  dip with the whole hedge gain at once.
- Hedges expiring worthless in a rally is the expected outcome, not a mistake. Judge
  the hedge program over a full cycle.

## 6. Account notes
- IRAs can usually buy puts and write covered calls (collars on held shares) but not
  short or write naked calls. Kids' custodial accounts: keep it simple; de-grossing
  or diversifiers over options.
- Hedging a position in account A with an option in account B: effective economically,
  but check wash-sale interactions if either side is closed at a loss.
- Collars on appreciated stock: very tight/deep-ITM collars can raise constructive-sale
  and qualified-covered-call issues. Keep reasonable width; confirm with a CPA.

## 7. A layered program (template for the committee)
Layered structure from the literature: diversification absorbs small losses, trend
rules handle moderate declines, puts handle severe crashes, and cash covers extreme
dislocation.
1. Base layer: IPS limits (C2 concentration, C3 margin) + correlation check. No cost.
2. Trend layer: regime rule reduces gross exposure when the governing index loses
   its 200-day / regime flips risk-off. No premium.
3. Event layer: single-name puts/spreads or pre-event trims around earnings on
   large positions.
4. Tail layer: small, budgeted far-OTM index puts, bought when IV is low.
5. Review: quarterly hedge P&L vs budget; did the hedge fire when needed?
Every numeric parameter here (hedge ratio, budget, trend trigger) is money-adjacent
→ proposed ADR line items for Amir's sign-off.
