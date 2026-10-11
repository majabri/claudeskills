# Rules, Margin, Taxes & Account Types

Verify current rules before relying on them — regulation and broker policy change.
Not tax or legal advice; confirm specifics with a CPA / Fidelity.

## 1. Day trading: the PDT rule was replaced (verified Sept 2026)
- SEC approved FINRA's Rule 4210 amendments on 2026-04-14 (Regulatory Notice 26-10).
  Effective 2026-06-04: the "pattern day trader" designation, the 4-in-5-days trade
  count, day-trading buying power, and the $25,000 minimum equity requirement are
  eliminated, replaced by an **intraday margin standard** based on real-time exposure.
- Brokers may phase in until **2027-10-20** and can keep stricter house rules.
  **Confirm Fidelity's implementation status** before assuming the old limits are gone.
- The $2,000 minimum equity to use margin still applies. Intraday margin deficits can
  bring restrictions (e.g. 90-day limits) — speed doesn't remove margin discipline.
- Cash accounts: no margin, but settlement rules apply (T+1): buying with unsettled
  proceeds and selling before settlement = good-faith violation; repeated → restriction.

## 2. Margin
- Reg T initial: 50% for long stock; 150% for shorts. Maintenance: FINRA floor 25% long
  (brokers often 30%+, higher for concentrated/volatile names).
- Margin call risk rises sharply in selloffs exactly when you least want forced sales.
- Cost: debit balance × annual rate ÷ 360 per day (broker convention). Rate must come
  from ips_lite / Fidelity statement, never a hardcoded literal (ADR-APP-007).
- IPS C3 margin cap governs total margin usage.
- Balance identity (verified from Amir's Fidelity data): cash market value + margin
  market value − net debit = total portfolio value.

## 3. Wash sale rule (IRC §1091)
- A loss is disallowed if you buy "substantially identical" securities within 30 days
  before or after the sale (61-day window). Disallowed loss is added to the new lot's basis.
- Traps: buying back via **call options** or selling ITM puts on the same stock; buying
  in a *different account you control* — including IRAs (loss permanently lost when
  the IRA buys) and arguably spouse accounts. Family accounts managed together need a
  cross-account check.
- Buy-back zones (ADR-APP-003) can trigger wash sales after a losing sale inside 30 days
  — flag this in the plan.

## 4. Capital gains
- ≤1 year = short-term (ordinary income rates); >1 year = long-term (lower rates).
  Swing trading is overwhelmingly short-term — factor after-tax return, and weigh
  trimming a nearly-long-term lot (A5 invalidation note: short-term tax cost can
  override a trim).
- Section 1256 contracts (broad-based index options like SPX, futures): 60/40 LT/ST and
  marked-to-market at year end.
- Short sales: gain/loss is generally short-term; constructive-sale rules apply to
  shorting against a held gain.
- Covered calls: qualified vs unqualified covered calls can affect holding period of the
  stock (deep ITM calls can suspend it).

## 5. Account-type eligibility
| Account | Shorting | Margin | Long options | Covered calls / CSP | Spreads | Naked |
|---|---|---|---|---|---|---|
| Individual brokerage (margin) | Yes | Yes | By level | Yes | By level | Highest level only |
| Traditional/Roth IRA | No | No (limited margin at some brokers, no shorting) | Usually | Yes | Sometimes (defined risk) | No |
| Custodial (UTMA/UGMA) | No | No | Limited/often no | Covered calls sometimes | Rarely | No |
| 529 | No trading of individual stocks/options | — | — | — | — | — |
Confirm per-account approvals at Fidelity; kids' accounts are held for the minor and
should be managed conservatively.

## 6. Order types to use well
Limit (default), stop (becomes market — can gap), stop-limit (can fail to fill on gaps),
trailing stop, OTO/OCO brackets (see fidelity-ticket notes: OTO resets to OCO on each
new ticket; verify Order B type), GTC vs day. Avoid market orders on options and on
illiquid stocks.
