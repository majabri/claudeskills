#!/usr/bin/env python3
"""Weekly Snapchat pack: new Kings episodes + ready captions, for scheduling by hand.

Snapchat's posting API is allowlist-only, so until Snap enables it this builds a folder
the user uploads in Snapchat's Profile Manager (profile.snapchat.com), which can schedule
Spotlight/Story posts up to 30 days ahead.

  python3 scripts/snapchat_pack.py [--out ~/Movies/"Snapchat Kings"] [--days 7]

Reads IG_ACCESS_TOKEN / IG_USER_ID from .data/.env. Standard library only.
Each reel is packed once (remembered in <out>/.packed.json).
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TAG = "#dadandhislittlekings"
SPOTLIGHT_MAX = 160          # Spotlight description limit
SLOTS = ["8:30 AM", "4:30 PM", "7:30 PM"]


def _env() -> dict:
    out = {}
    for line in (SKILL / ".data" / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _videos(env: dict) -> list[dict]:
    uid = env.get("IG_USER_ID")
    base = f"https://graph.facebook.com/v25.0/{uid}" if uid else "https://graph.instagram.com/me"
    url = base + "/media?" + urllib.parse.urlencode({
        "fields": "id,caption,media_type,media_url,permalink,timestamp",
        "limit": 100, "access_token": env["IG_ACCESS_TOKEN"]})
    vids = []
    for _ in range(50):
        body = json.load(urllib.request.urlopen(url, timeout=60))
        vids += [m for m in body.get("data", []) if m.get("media_type") == "VIDEO"]
        url = body.get("paging", {}).get("next")
        if not url:
            break
    return vids


def spotlight_caption(caption: str) -> str:
    """First line + up to 3 hashtags (always #DadAndHisLittleKings), within 160 chars."""
    caption = (caption or "").strip()
    tags = re.findall(r"#\w+", caption)
    first = re.sub(r"#\w+", "", caption.splitlines()[0] if caption else "").strip()
    keep = ["#DadAndHisLittleKings"] + [t for t in tags if t.lower() != TAG][:2]
    text = (first + " " + " ".join(keep)).strip()
    if len(text) > SPOTLIGHT_MAX:
        room = SPOTLIGHT_MAX - len(" ".join(keep)) - 2
        text = first[:max(room, 0)].rstrip() + "… " + " ".join(keep)
    return text[:SPOTLIGHT_MAX]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path.home() / "Movies" / "Snapchat Kings"))
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    seen_file = out / ".packed.json"
    seen = set(json.loads(seen_file.read_text())) if seen_file.exists() else set()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    todo = []
    for v in _videos(_env()):
        ts = datetime.strptime(v["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if ts < since or v["id"] in seen or TAG not in (v.get("caption") or "").lower():
            continue
        todo.append((ts, v))
    todo.sort(key=lambda x: x[0])

    # Suggested times continue after the last slot handed out, so batches never overlap.
    sched_file = out / ".schedule.json"
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    try:
        nxt = json.loads(sched_file.read_text())          # first free slot: {"day", "slot"}
        next_day = datetime.strptime(nxt["day"], "%Y-%m-%d").date()
        next_slot = int(nxt["slot"])
        if next_day < tomorrow:
            next_day, next_slot = tomorrow, 0
    except Exception:
        next_day, next_slot = tomorrow, 0

    week = out / datetime.now().strftime("Week of %Y-%m-%d")
    lines, skipped, packed = [], [], 0
    for i, (ts, v) in enumerate(todo, 1):
        if not v.get("media_url"):
            skipped.append(v.get("permalink"))  # licensed music: Instagram withholds the file
            continue
        week.mkdir(exist_ok=True)
        name = f"{i:02d} - {ts.astimezone().strftime('%b %d')}.mp4"
        urllib.request.urlretrieve(v["media_url"], week / name)
        day, slot = divmod(next_slot + packed, len(SLOTS))
        when = (next_day + timedelta(days=day)).strftime("%a %b %d")
        lines.append(f"{name}\n  Schedule: {when}, {SLOTS[slot]}\n  Caption: {spotlight_caption(v.get('caption'))}\n")
        seen.add(v["id"])
        packed += 1

    if packed:
        (week / "CAPTIONS - read me.txt").write_text(
            "Upload in Snapchat Profile Manager (profile.snapchat.com) -> Spotlight -> Schedule.\n"
            "Copy each caption below. Suggested times spread 3 a day.\n\n" + "\n".join(lines) +
            (("\nSkipped (licensed music, no file from Instagram):\n" + "\n".join(skipped)) if skipped else ""))
    if packed:
        day, slot = divmod(next_slot + packed, len(SLOTS))
        sched_file.write_text(json.dumps({"day": str(next_day + timedelta(days=day)), "slot": slot}))
    seen_file.write_text(json.dumps(sorted(seen)))
    print(json.dumps({"folder": str(week) if packed else None, "packed": packed,
                      "skipped_licensed_music": len(skipped)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
