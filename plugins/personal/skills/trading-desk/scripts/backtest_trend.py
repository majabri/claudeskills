#!/usr/bin/env python3
"""Honest trend-rule backtest: 'hold when close > SMA(n), else reduce exposure'.

Built to test the hedging trend layer (ADR draft H2) and any MA-cross idea with the
discipline a real backtest needs: next-day execution (no look-ahead), costs, buy-and-hold
benchmark, max drawdown, parameter sweep, and in-sample vs out-of-sample split.

Input: Yahoo chart JSON (v8/finance/chart, interval=1d) or CSV with date,close columns.
Uses adjusted close when present (dividends reinvested for both strategy and benchmark).

Usage:
  backtest_trend.py QQQ.json --sma 200 --below-exposure 0 --cost-bps 5
  backtest_trend.py QQQ.json --sweep 50,100,150,200,250 --below-exposure 0.5
Cash earns 0% here (conservative: real T-bill yield would help the strategy).
Educational analysis only — past results do not guarantee future results.
"""
import argparse, csv, json, math, datetime as dt

def load(path):
    if path.endswith(".json"):
        r = json.load(open(path))["chart"]["result"][0]
        ts = r["timestamp"]
        adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose")
        px = adj or r["indicators"]["quote"][0]["close"]
        rows = [(dt.date.fromtimestamp(t), p) for t, p in zip(ts, px) if p]
    else:
        rows = [(dt.date.fromisoformat(d["date"]), float(d["close"])) for d in csv.DictReader(open(path))]
    return rows

def stats(dates, eq):
    yrs = (dates[-1] - dates[0]).days / 365.25
    cagr = eq[-1] ** (1 / yrs) - 1
    peak, mdd = eq[0], 0
    for v in eq:
        peak = max(peak, v); mdd = max(mdd, 1 - v / peak)
    rets = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
    vol = (sum(r * r for r in rets) / len(rets) - (sum(rets) / len(rets)) ** 2) ** 0.5 * math.sqrt(252)
    return cagr, mdd, vol, (cagr / mdd if mdd else float("nan"))

def run(rows, n, below, cost_bps):
    dates = [d for d, _ in rows][n:]
    px = [p for _, p in rows]
    eq_s, eq_b = [1.0], [1.0]
    expo_prev = 1.0; trades = 0; time_in = 0
    for i in range(n, len(px) - 1):
        sma = sum(px[i - n + 1:i + 1]) / n
        expo = 1.0 if px[i] > sma else below          # signal on today's close...
        r = px[i + 1] / px[i] - 1                      # ...applied to NEXT day's return
        cost = abs(expo - expo_prev) * cost_bps / 1e4
        if expo != expo_prev: trades += 1
        eq_s.append(eq_s[-1] * (1 + expo * r - cost)); eq_b.append(eq_b[-1] * (1 + r))
        expo_prev = expo; time_in += expo
    dates = dates[:len(eq_s)]
    return dates, eq_s, eq_b, trades, time_in / (len(eq_s) - 1)

def report(label, dates, eq_s, eq_b, trades, expo):
    s, b = stats(dates, eq_s), stats(dates, eq_b)
    print(f"{label}: {dates[0]}→{dates[-1]} | strategy CAGR {s[0]*100:5.1f}% maxDD {s[1]*100:5.1f}% vol {s[2]*100:4.1f}% "
          f"| buy&hold CAGR {b[0]*100:5.1f}% maxDD {b[1]*100:5.1f}% vol {b[2]*100:4.1f}% | switches {trades} avg exposure {expo*100:.0f}%")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file"); ap.add_argument("--sma", type=int, default=200)
    ap.add_argument("--below-exposure", type=float, default=0.0, help="exposure when below SMA (0 = cash, 0.5 = half)")
    ap.add_argument("--cost-bps", type=float, default=5.0, help="cost per 100% exposure change, basis points")
    ap.add_argument("--sweep", help="comma list of SMA lengths to test robustness")
    a = ap.parse_args()
    rows = load(a.file)
    for n in ([int(x) for x in a.sweep.split(",")] if a.sweep else [a.sma]):
        d, s, b, t, e = run(rows, n, a.below_exposure, a.cost_bps)
        report(f"SMA{n} below={a.below_exposure:g} FULL", d, s, b, t, e)
        mid = len(rows) // 2
        for lab, sub in (("  1st half", rows[:mid]), ("  2nd half", rows[mid - n:])):
            d, s, b, t, e = run(sub, n, a.below_exposure, a.cost_bps)
            report(f"{lab}", d, s, b, t, e)

if __name__ == "__main__":
    main()
