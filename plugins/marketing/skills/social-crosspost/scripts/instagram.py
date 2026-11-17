"""Read your own Instagram Professional (Business/Creator) videos via the official API.

Two token types work:
  * Facebook Login for Business / Unified login (newer Meta apps): set IG_USER_ID too.
    Calls go to graph.facebook.com/<IG_USER_ID>/media. System-user tokens never expire.
  * Instagram Login (older apps): no IG_USER_ID. Calls go to graph.instagram.com/me/media,
    and the ~60-day token is refreshed automatically.
"""
from __future__ import annotations

import time
from pathlib import Path

import requests

from common import PlatformError, env, get_token, log, save_token

FIELDS = "id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp"


def _ig_user_id() -> str | None:
    return env("IG_USER_ID") or None


def _base() -> str:
    version = env("IG_API_VERSION", "v25.0" if _ig_user_id() else "")
    host = "https://graph.facebook.com" if _ig_user_id() else "https://graph.instagram.com"
    return host + (f"/{version}" if version else "")


def access_token() -> str:
    tok = get_token("instagram", "access_token", "IG_ACCESS_TOKEN")
    if not tok:
        raise PlatformError("No Instagram token. Set IG_ACCESS_TOKEN (see references/setup.md).")
    return tok


def refresh_if_due(max_age_days: int = 7) -> None:
    """Long-lived tokens last ~60 days; refreshing extends them. Must be >24h old to refresh."""
    from common import load_tokens

    if _ig_user_id():
        return  # Facebook-login / system-user tokens are not refreshed this way
    saved = load_tokens().get("instagram", {})
    last = saved.get("saved_at", 0)
    if time.time() - last < max_age_days * 86400:
        return
    r = requests.get(
        "https://graph.instagram.com/refresh_access_token",
        params={"grant_type": "ig_refresh_token", "access_token": access_token()},
        timeout=30,
    )
    if r.ok and r.json().get("access_token"):
        save_token("instagram", {"access_token": r.json()["access_token"]})
        log("Instagram token refreshed.")
    else:
        log(f"Instagram token refresh skipped: {r.status_code} {r.text[:200]}")


def list_videos(limit: int = 25) -> list[dict]:
    """Newest-first list of the account's video posts (reels + feed videos)."""
    r = requests.get(
        f"{_base()}/{_ig_user_id() or 'me'}/media",
        params={"fields": FIELDS, "limit": limit, "access_token": access_token()},
        timeout=30,
    )
    if not r.ok:
        raise PlatformError(f"Instagram list failed: {r.status_code} {r.text[:300]}")
    items = r.json().get("data", [])
    return [m for m in items if m.get("media_type") == "VIDEO"]


def download(media: dict, dest_dir: Path) -> Path:
    url = media.get("media_url")
    if not url:
        # Instagram omits media_url when the media contains copyrighted audio/material.
        raise PlatformError(
            "Instagram did not return a download link for this video "
            "(usually licensed music on the reel). Use the original file instead."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"ig_{media['id']}.mp4"
    if path.exists() and path.stat().st_size > 0:
        return path
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    return path
