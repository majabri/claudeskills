#!/usr/bin/env python3
"""Instagram -> YouTube / TikTok / X cross-poster.

Commands (all print JSON to stdout, progress to stderr):
  doctor                 check which platforms are configured
  baseline               mark every current Instagram video as already handled (run once)
  list [--limit N]       new Instagram videos not handled yet
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
    report["data_dir"] = str(data_dir())
    report["settings"] = {"TIKTOK_MODE": env("TIKTOK_MODE", "inbox"),
                          "YT_PRIVACY": env("YT_PRIVACY", "public"),
                          "platforms": _platforms(None)}
    _out(report)
    return 0


def _new_videos(limit: int) -> list[dict]:
    import instagram
    instagram.refresh_if_due()
    state = load_state()
    handled = state.get("media", {})
    vids = instagram.list_videos(limit=50)
    fresh = []
    for v in vids:
        rec = handled.get(v["id"])
        if rec and rec.get("baseline"):
            continue
        fresh.append(v)
    return fresh[:limit]


def cmd_baseline(_args) -> int:
    import instagram
    state = load_state()
    count = 0
    for v in instagram.list_videos(limit=50):
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
    for v in _new_videos(args.limit):
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
    state = load_state()
    candidates = _new_videos(50)
    if args.ids:
        wanted = {i.strip() for i in args.ids.split(",")}
        candidates = [v for v in candidates if v["id"] in wanted]
    candidates = candidates[: args.limit]

    results = []
    for v in candidates:
        rec = state["media"].setdefault(v["id"], {"permalink": v.get("permalink"),
                                                  "timestamp": v.get("timestamp"), "posts": {}})
        caption = v.get("caption", "") or ""
        todo = [p for p in platforms if p not in rec["posts"]]
        entry = {"id": v["id"], "permalink": v.get("permalink"), "results": {}}
        if not todo:
            continue
        if not args.publish:
            for p in todo:
                ov = overrides.get(v["id"], {}).get(p)
                entry["results"][p] = {"would_post": _preview(p, caption, ov)}
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
                rec["posts"][p] = {**res, "at": _now()}
                entry["results"][p] = {"ok": True, **res}
            except (PlatformError, ConfigError) as e:
                entry["results"][p] = {"ok": False, "error": str(e)}
            except Exception as e:  # noqa: BLE001
                entry["results"][p] = {"ok": False, "error": f"{type(e).__name__}: {e}"}
            save_state(state)  # save after every platform so a crash never double-posts
        if args.cleanup and all(p in rec["posts"] for p in platforms):
            path.unlink(missing_ok=True)
        results.append(entry)

    _out({"mode": "publish" if args.publish else "dry_run", "videos": results})
    return 0


def _preview(platform: str, caption: str, ov: dict | None) -> dict:
    from common import truncate
    ov = ov or {}
    if platform == "youtube":
        first = caption.strip().splitlines()[0] if caption.strip() else "New video"
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
    sub.add_parser("status")
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
        return {"doctor": cmd_doctor, "baseline": cmd_baseline, "list": cmd_list,
                "run": cmd_run, "status": cmd_status}[args.cmd](args)
    except (ConfigError, PlatformError) as e:
        _out({"error": str(e)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
