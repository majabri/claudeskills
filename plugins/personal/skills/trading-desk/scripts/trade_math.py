#!/usr/bin/env python3
"""Deterministic trading math. Advisory calculations only — no orders.

Usage:
  trade_math.py size --equity 120000 --risk-pct 0.75 --entry 152.4 --stop 147.9
  trade_math.py size-options --equity 120000 --risk-pct 0.75 --max-loss-per-contract 340
  trade_math.py rmultiple --entry 152.4 --stop 147.9 --exit 161.4 [--short]
  trade_math.py expectancy --win-rate 0.4 --avg-win 2.5 --avg-loss 1
  trade_math.py expected-move --price 150 --iv 0.35 --dte 30
  trade_math.py greeks --price 150 --strike 155 --dte 45 --iv 0.32 --rate 0.04 --type call [--div 0.0]
  trade_math.py breakeven --type call --strike 155 --premium 4.2
  trade_math.py margin-cost --debit 20000 --rate-pct <from ips_lite> --days 30
  trade_math.py hedge --beta-exposure 90000 --index-price 600 --hedge-ratio 0.5 [--put-delta 0.35]
  trade_math.py streak --risk-pct 1 --losses 10
  trade_math.py montecarlo --risk-pct 1 --win-rate 0.4 --avg-win 2 [--trades 100 --gap-share 0.15]
"""
import argparse, math, sys

def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def npdf(x): return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def bs(S, K, T, sigma, r, q, kind):
    if T <= 0 or sigma <= 0:
        raise ValueError("dte and iv must be > 0")
    d1 = (math.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    dq, dr = math.exp(-q * T), math.exp(-r * T)
    if kind == "call":
        price = S * dq * ncdf(d1) - K * dr * ncdf(d2)
        delta = dq * ncdf(d1)
        theta = (-S * dq * npdf(d1) * sigma / (2 * math.sqrt(T)) - r * K * dr * ncdf(d2) + q * S * dq * ncdf(d1)) / 365
        rho = K * T * dr * ncdf(d2) / 100
        p_itm = ncdf(d2)
    else:
        price = K * dr * ncdf(-d2) - S * dq * ncdf(-d1)
        delta = -dq * ncdf(-d1)
        theta = (-S * dq * npdf(d1) * sigma / (2 * math.sqrt(T)) + r * K * dr * ncdf(-d2) - q * S * dq * ncdf(-d1)) / 365
        rho = -K * T * dr * ncdf(-d2) / 100
        p_itm = ncdf(-d2)
    gamma = dq * npdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * dq * npdf(d1) * math.sqrt(T) / 100
    return dict(price=price, delta=delta, gamma=gamma, theta_per_day=theta,
                vega_per_1pt_iv=vega, rho_per_1pt_rate=rho, prob_itm_risk_neutral=p_itm)

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("size"); a.add_argument("--equity", type=float, required=True)
    a.add_argument("--risk-pct", type=float, required=True); a.add_argument("--entry", type=float, required=True)
    a.add_argument("--stop", type=float, required=True)
    a = sub.add_parser("size-options"); a.add_argument("--equity", type=float, required=True)
    a.add_argument("--risk-pct", type=float, required=True); a.add_argument("--max-loss-per-contract", type=float, required=True)
    a = sub.add_parser("rmultiple"); [a.add_argument(f"--{k}", type=float, required=True) for k in ("entry", "stop", "exit")]
    a.add_argument("--short", action="store_true")
    a = sub.add_parser("expectancy"); [a.add_argument(f"--{k}", type=float, required=True) for k in ("win-rate", "avg-win", "avg-loss")]
    a = sub.add_parser("expected-move"); [a.add_argument(f"--{k}", type=float, required=True) for k in ("price", "iv", "dte")]
    a = sub.add_parser("greeks"); [a.add_argument(f"--{k}", type=float, required=True) for k in ("price", "strike", "dte", "iv")]
    a.add_argument("--rate", type=float, default=0.04); a.add_argument("--div", type=float, default=0.0)
    a.add_argument("--type", choices=["call", "put"], required=True)
    a = sub.add_parser("breakeven"); a.add_argument("--type", choices=["call", "put"], required=True)
    a.add_argument("--strike", type=float, required=True); a.add_argument("--premium", type=float, required=True)
    a = sub.add_parser("margin-cost"); a.add_argument("--debit", type=float, required=True)
    a.add_argument("--rate-pct", type=float, required=True, help="annual %, from ips_lite — never assumed")
    a.add_argument("--days", type=float, default=30)
    a = sub.add_parser("hedge"); a.add_argument("--beta-exposure", type=float, required=True,
        help="sum of position $ x beta vs the hedge index")
    a.add_argument("--index-price", type=float, required=True); a.add_argument("--hedge-ratio", type=float, default=1.0)
    a.add_argument("--put-delta", type=float, default=1.0, help="|delta| for delta-matched hedge; 1 = protection at expiry")
    a = sub.add_parser("streak"); a.add_argument("--risk-pct", type=float, required=True); a.add_argument("--losses", type=int, required=True)
    a = sub.add_parser("montecarlo"); a.add_argument("--risk-pct", type=float, required=True)
    a.add_argument("--win-rate", type=float, required=True); a.add_argument("--avg-win", type=float, required=True)
    a.add_argument("--trades", type=int, default=100); a.add_argument("--gap-share", type=float, default=0.15)
    a.add_argument("--runs", type=int, default=10000); a.add_argument("--seed", type=int, default=7)
    x = p.parse_args(argv)

    if x.cmd == "size":
        R = abs(x.entry - x.stop)
        if R == 0: sys.exit("entry == stop")
        budget = x.equity * x.risk_pct / 100
        sh = math.floor(budget / R)
        print(f"R/share={R:.2f} budget=${budget:,.2f} shares={sh} position=${sh*x.entry:,.2f} "
              f"({sh*x.entry/x.equity*100:.1f}% of equity) actual_risk=${sh*R:,.2f}")
    elif x.cmd == "size-options":
        budget = x.equity * x.risk_pct / 100
        n = math.floor(budget / x.max_loss_per_contract)
        print(f"budget=${budget:,.2f} contracts={n} max_loss=${n*x.max_loss_per_contract:,.2f}")
    elif x.cmd == "rmultiple":
        R = abs(x.entry - x.stop); pnl = (x.entry - x.exit) if x.short else (x.exit - x.entry)
        print(f"R={R:.2f} pnl/share={pnl:.2f} R-multiple={pnl/R:+.2f}R")
    elif x.cmd == "expectancy":
        w = x.win_rate; e = w * x.avg_win - (1 - w) * x.avg_loss
        b = x.avg_win / x.avg_loss; kelly = w - (1 - w) / b
        print(f"expectancy={e:+.3f}R/trade kelly={kelly:.3f} quarter_kelly={kelly/4:.3f} (ceiling, not target)")
    elif x.cmd == "expected-move":
        m = x.price * x.iv * math.sqrt(x.dte / 365)
        print(f"1SD move ≈ ±{m:.2f} ({m/x.price*100:.1f}%) → range {x.price-m:.2f}–{x.price+m:.2f} (~68%)")
    elif x.cmd == "greeks":
        g = bs(x.price, x.strike, x.dte / 365, x.iv, x.rate, x.div, x.type)
        for k, v in g.items(): print(f"{k}={v:.4f}")
        print("(Black-Scholes European approximation; per-share values, ×100 per contract)")
    elif x.cmd == "breakeven":
        be = x.strike + x.premium if x.type == "call" else x.strike - x.premium
        print(f"breakeven at expiry={be:.2f} max_loss_long=${x.premium*100:,.2f}/contract")
    elif x.cmd == "margin-cost":
        c = x.debit * x.rate_pct / 100 / 360 * x.days
        print(f"interest over {x.days:g} days ≈ ${c:,.2f} (actual/360 convention)")

    elif x.cmd == "hedge":
        notional = x.beta_exposure * x.hedge_ratio
        raw = notional / (x.index_price * 100) / abs(x.put_delta)
        print(f"hedge notional=${notional:,.0f} contracts_exact={raw:.2f} round_down={math.floor(raw)} "
              f"(one contract = ${x.index_price*100/1:,.0f} notional; if round_down is 0 consider a spread, "
              f"single-name hedge, or de-grossing)")
    elif x.cmd == "streak":
        left = (1 - x.risk_pct / 100) ** x.losses
        print(f"{x.losses} straight losses at {x.risk_pct}% = {(1-left)*100:.1f}% drawdown; "
              f"recovery needs +{(1/left-1)*100:.1f}%")
    elif x.cmd == "montecarlo":
        import random, statistics
        random.seed(x.seed); r = x.risk_pct / 100; dds = []; ends = []
        for _ in range(x.runs):
            eq = peak = 1.0; mdd = 0
            for _ in range(x.trades):
                if random.random() < x.win_rate:
                    R = x.avg_win * random.uniform(0.5, 1.5)
                else:
                    R = -random.uniform(1.5, 3.0) if random.random() < x.gap_share else -1.0
                eq *= 1 + r * R; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
            dds.append(mdd); ends.append(eq)
        dds.sort(); ends.sort(); n = x.runs
        print(f"median maxDD={statistics.median(dds)*100:.1f}% p95 maxDD={dds[int(.95*n)]*100:.1f}% "
              f"median end={(statistics.median(ends)-1)*100:+.1f}% p5 end={(ends[int(.05*n)]-1)*100:+.1f}% "
              f"P(end<=-30%)={sum(e<=0.7 for e in ends)/n*100:.1f}%")

if __name__ == "__main__":
    main()
