#!/usr/bin/env python3
"""Instagram -> YouTube / TikTok / X cross-poster.

Commands (all print JSON to stdout, progress to stderr):
  doctor                 check which platforms are configured
  baseline               mark every current Instagram video as already handled (run once)
  include-old            undo baseline: make the back catalog eligible (backfill)
  backlog                how many videos each platform still owes; "caught_up": true/false
  cooldown               platforms resting after a limit (no API calls)
  list [--limit N]       videos still owed (recent first, then the backlog oldest-first)
  run  [--ids A,B]       DRY RUN: show exactly what would be posted where
  run  ... --publish     actually download and post
  status                 what has been posted so far

Options for run:
  --platforms youtube,tiktok,x   (default: CROSSPOST_PLATFORMS or all three)
  --overrides FILE.json          per-video, per-platform captions:
        {"<ig_media_id>": {"youtube": {"title": "...", "description": "..."},
                           "tiktok": {"title": "..."}, "x": {"text": "..."}}}
  --limit N                      at most N videos this run (default 3)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
from common import ConfigError, PlatformError, data_dir, env, load_state, log, save_state  # noqa: E402

ALL_PLATFORMS = ["youtube", "tiktok", "x"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _platforms(arg: str | None) -> list[str]:
    raw = arg or env("CROSSPOST_PLATFORMS", ",".join(ALL_PLATFORMS))
    picked = [p.strip().lower() for p in raw.split(",") if p.strip()]
    bad = [p for p in picked if p not in ALL_PLATFORMS]
    if bad:
        raise ConfigError(f"Unknown platform(s): {', '.join(bad)}. Use {', '.join(ALL_PLATFORMS)}.")
    return picked


def _module(platform: str):
    if platform == "youtube":
        import youtube as m
    elif platform == "tiktok":
        import tiktok as m
    else:
        import x_twitter as m
    return m


def _out(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


# ---------------- commands ----------------

def cmd_doctor(_args) -> int:
    checks = {
        "instagram": ["IG_ACCESS_TOKEN"],
        "youtube": ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"],
        "tiktok": ["TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_REFRESH_TOKEN"],
        "x": ["X_CLIENT_ID", "X_REFRESH_TOKEN"],
    }
    tokens = common.load_tokens()
    store_key = {"IG_ACCESS_TOKEN": ("instagram", "access_token"),
                 "YT_REFRESH_TOKEN": ("youtube", "refresh_token"),
                 "TIKTOK_REFRESH_TOKEN": ("tiktok", "refresh_token"),
                 "X_REFRESH_TOKEN": ("x", "refresh_token")}
    report = {}
    for platform, names in checks.items():
        missing = []
        for n in names:
            have = bool(env(n))
            if not have and n in store_key:
                p, k = store_key[n]
                have = bool(tokens.get(p, {}).get(k))
            if not have:
                missing.append(n)
        report[platform] = {"ready": not missing, "missing": missing}
    import shutil
    report["ffprobe"] = bool(shutil.which("ffprobe"))
    import instagram
    report["instagram_connection"] = instagram.connection_type()
    report["data_dir"] = str(data_dir())
    report["settings"] = {"TIKTOK_MODE": env("TIKTOK_MODE", "inbox"),
                          "YT_PRIVACY": env("YT_PRIVACY", "public"),
                          "platforms": _platforms(None)}
    _out(report)
    return 0


RECENT_HOURS = 72  # reels newer than this go before the backlog
# Error text that means "this platform is at its cap for now": stop it for the rest of the run.
CAP_MARKERS = {
    "youtube": ("uploadLimitExceeded", "quotaExceeded", "rateLimitExceeded", "dailyLimitExceeded"),
    "tiktok": ("spam_risk", "reached_active_user_cap", "rate_limit_exceeded", "too_many"),
    "x": ("429", "Too Many Requests", "402"),
}


def _age_hours(ts: str | None) -> float:
    if not ts:
        return 1e9
    try:
        t = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return 1e9
    return (datetime.now(timezone.utc) - t).total_seconds() / 3600


def _new_videos(limit: int, platforms: list[str] | None = None) -> list[dict]:
    """Videos still owed to at least one platform.

    Order: reels from the last RECENT_HOURS first (oldest of those first), then the
    backlog oldest-first, so today's episodes never wait behind a catch-up.
    """
    import instagram
    instagram.refresh_if_due()
    platforms = platforms or _platforms(None)
    handled = load_state().get("media", {})
    owed = []
    for v in instagram.list_videos(all_pages=True):
        rec = handled.get(v["id"], {})
        if rec.get("baseline") or rec.get("skipped"):
            continue
        if all(p in rec.get("posts", {}) for p in platforms):
            continue
        owed.append(v)
    owed.sort(key=lambda v: v.get("timestamp") or "")
    recent = [v for v in owed if _age_hours(v.get("timestamp")) <= RECENT_HOURS]
    backlog = [v for v in owed if _age_hours(v.get("timestamp")) > RECENT_HOURS]
    return (recent + backlog)[:limit]


def _record(mid: str, meta: dict, platform: str | None = None, result: dict | None = None,
            skipped: str | None = None) -> None:
    """Re-read state, change one video, save: safe when the YouTube and TikTok runs overlap."""
    with common.state_lock():
        state = load_state()
        rec = state["media"].setdefault(mid, {"permalink": meta.get("permalink"),
                                              "timestamp": meta.get("timestamp"), "posts": {}})
        rec.setdefault("posts", {})
        if platform and result is not None:
            rec["posts"][platform] = result
        if skipped:
            rec["skipped"] = {"reason": skipped, "at": _now()}
        save_state(state)


# After a platform hits its cap, don't touch Instagram for it again until this many hours pass.
COOLDOWN_HOURS = {"youtube": 12, "tiktok": 3, "x": 6}


def _set_cooldown(platform: str, reason: str | None) -> None:
    with common.state_lock():
        state = load_state()
        cd = state.setdefault("cooldown", {})
        if reason:
            cd[platform] = {"at": _now(), "reason": reason[:200]}
        else:
            cd.pop(platform, None)
        save_state(state)


def cmd_cooldown(args) -> int:
    """Which platforms are resting after hitting a limit. Reads only local state (no API calls)."""
    platforms = _platforms(args.platforms)
    cd = load_state().get("cooldown", {})
    out = {}
    for p in platforms:
        rec = cd.get(p)
        hrs = float(env(f"{p.upper()}_COOLDOWN_HOURS", str(COOLDOWN_HOURS.get(p, 6))))
        resting = bool(rec) and _age_hours(rec["at"].replace("+00:00", "+0000")) < hrs
        out[p] = {"resting": resting, **({"since": rec["at"], "reason": rec["reason"]} if rec else {})}
    out["all_resting"] = all(v["resting"] for v in out.values())
    _out(out)
    return 0


def cmd_include_old(_args) -> int:
    """Make videos marked by `baseline` eligible again (to backfill the back catalog)."""
    with common.state_lock():
        state = load_state()
        n = 0
        for rec in state["media"].values():
            if rec.pop("baseline", None):
                n += 1
        state["backfill_since"] = _now()
        save_state(state)
    _out({"now_eligible": n})
    return 0


def cmd_backlog(args) -> int:
    """How many videos each platform still owes (drives the catch-up schedule)."""
    import instagram
    platforms = _platforms(args.platforms)
    handled = load_state().get("media", {})
    vids = instagram.list_videos(all_pages=True)
    out = {"videos_on_instagram": len(vids), "platforms": {}}
    for p in platforms:
        owed = owed_old = skipped = done = 0
        for v in vids:
            rec = handled.get(v["id"], {})
            if rec.get("skipped"):
                skipped += 1
            elif p in rec.get("posts", {}):
                done += 1
            elif not rec.get("baseline"):
                owed += 1
                if _age_hours(v.get("timestamp")) > RECENT_HOURS:
                    owed_old += 1
        out["platforms"][p] = {"owed": owed, "owed_backlog": owed_old, "posted": done, "skipped": skipped}
    # caught_up = no backlog left (recent reels are handled by the normal schedule)
    out["caught_up"] = all(v["owed_backlog"] == 0 for v in out["platforms"].values())
    _out(out)
    return 0


def cmd_baseline(_args) -> int:
    import instagram
    state = load_state()
    count = 0
    for v in instagram.list_videos(all_pages=True):
        if v["id"] not in state["media"]:
            state["media"][v["id"]] = {"baseline": True, "permalink": v.get("permalink"),
                                       "timestamp": v.get("timestamp"), "posts": {}}
            count += 1
    state["baseline_at"] = _now()
    save_state(state)
    _out({"marked_as_handled": count, "baseline_at": state["baseline_at"]})
    return 0


def cmd_list(args) -> int:
    state = load_state()
    platforms = _platforms(args.platforms)
    rows = []
    for v in _new_videos(args.limit, platforms):
        done = state["media"].get(v["id"], {}).get("posts", {})
        pending = [p for p in platforms if p not in done]
        if not pending:
            continue
        rows.append({
            "id": v["id"], "timestamp": v.get("timestamp"), "permalink": v.get("permalink"),
            "caption": v.get("caption", ""), "downloadable": bool(v.get("media_url")),
            "already_posted_to": sorted(done), "pending": pending,
        })
    if state.get("baseline_at") is None:
        log("Note: no baseline yet. Run `baseline` first or every old video counts as new.")
    _out(rows)
    return 0


def cmd_run(args) -> int:
    import instagram

    platforms = _platforms(args.platforms)
    overrides = json.loads(Path(args.overrides).read_text()) if args.overrides else {}
    candidates = _new_videos(10_000, platforms)
    if args.ids:
        wanted = {i.strip() for i in args.ids.split(",")}
        candidates = [v for v in candidates if v["id"] in wanted]
    candidates = candidates[: args.limit]

    capped: dict[str, str] = {}
    results = []
    for v in candidates:
        if len(capped) == len(platforms):
            break  # every platform is at its cap; the rest waits for the next run
        rec = load_state()["media"].get(v["id"], {})
        caption = v.get("caption", "") or ""
        todo = [p for p in platforms if p not in rec.get("posts", {}) and p not in capped]
        entry = {"id": v["id"], "timestamp": v.get("timestamp"),
                 "permalink": v.get("permalink"), "results": {}}
        if not todo:
            continue
        if not args.publish:
            for p in todo:
                ov = overrides.get(v["id"], {}).get(p)
                entry["results"][p] = {"would_post": _preview(p, caption, ov)}
            results.append(entry)
            continue
        if not v.get("media_url"):
            _record(v["id"], v, skipped="no_download_link")  # licensed audio: Instagram withholds the file
            entry["skipped"] = "Instagram gives no download link for this reel (usually licensed music)"
            results.append(entry)
            continue
        try:
            path = instagram.download(v, data_dir() / "videos")
        except Exception as e:  # noqa: BLE001
            entry["error"] = str(e)
            results.append(entry)
            continue
        for p in todo:
            ov = overrides.get(v["id"], {}).get(p)
            log(f"Posting {v['id']} to {p} ...")
            try:
                res = _module(p).upload(path, caption, ov)
                _record(v["id"], v, p, {**res, "at": _now()})  # saved per platform: no double posts
                if load_state().get("cooldown", {}).get(p):
                    _set_cooldown(p, None)
                entry["results"][p] = {"ok": True, **res}
            except (PlatformError, ConfigError) as e:
                msg = str(e)
                entry["results"][p] = {"ok": False, "error": msg}
                if any(m in msg for m in CAP_MARKERS.get(p, ())):
                    capped[p] = msg[:200]
                    if args.publish:
                        _set_cooldown(p, msg)
                    entry["results"][p]["capped"] = True
            except Exception as e:  # noqa: BLE001
                entry["results"][p] = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        done = load_state()["media"].get(v["id"], {}).get("posts", {})
        if args.cleanup and all(p in done for p in platforms):
            common.free_space(path)
        results.append(entry)

    posted = sum(1 for r in results for x in r["results"].values() if x.get("ok"))
    _out({"mode": "publish" if args.publish else "dry_run", "posted": posted,
          "capped": capped, "videos": results})
    return 0


def _preview(platform: str, caption: str, ov: dict | None) -> dict:
    from common import truncate
    ov = ov or {}
    if platform == "youtube":
        first = caption.strip().splitlines()[0] if caption.strip() else env("YT_FALLBACK_TITLE", "New video")
        return {"title": truncate(ov.get("title") or first, 100),
                "description": truncate(ov.get("description") or caption, 300),
                "privacy": ov.get("privacy") or env("YT_PRIVACY", "public")}
    if platform == "tiktok":
        return {"title": truncate(ov.get("title") or caption, 300),
                "mode": ov.get("mode") or env("TIKTOK_MODE", "inbox")}
    import x_twitter
    return {"text": x_twitter.build_text(caption, ov), "estimated_cost_usd": 0.015}


def cmd_status(_args) -> int:
    state = load_state()
    posted = {k: v["posts"] for k, v in state["media"].items() if v.get("posts")}
    _out({"baseline_at": state.get("baseline_at"),
          "videos_tracked": len(state["media"]), "posted": posted})
    return 0


def main() -> int:
    common.load_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("baseline")
    sub.add_parser("include-old")
    sub.add_parser("status")
    p_cool = sub.add_parser("cooldown")
    p_cool.add_argument("--platforms")
    p_back = sub.add_parser("backlog")
    p_back.add_argument("--platforms")
    p_list = sub.add_parser("list")
    p_list.add_argument("--limit", type=int, default=10)
    p_list.add_argument("--platforms")
    p_run = sub.add_parser("run")
    p_run.add_argument("--ids")
    p_run.add_argument("--platforms")
    p_run.add_argument("--overrides")
    p_run.add_argument("--limit", type=int, default=3)
    p_run.add_argument("--publish", action="store_true")
    p_run.add_argument("--cleanup", action="store_true", help="delete local video after all posts succeed")
    args = ap.parse_args()
    try:
        return {"doctor": cmd_doctor, "baseline": cmd_baseline, "include-old": cmd_include_old,
                "backlog": cmd_backlog, "cooldown": cmd_cooldown, "list": cmd_list, "run": cmd_run,
                "status": cmd_status}[args.cmd](args)
    except (ConfigError, PlatformError) as e:
        _out({"error": str(e)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
