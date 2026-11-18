"""Post a video to X with the v2 chunked media upload + POST /2/tweets.

Billing: X is pay-per-use (about $0.015 per post, $0.20 if the post contains a link).
Needs an OAuth 2.0 user token with: tweet.read tweet.write users.read media.write offline.access
"""
from __future__ import annotations

import base64
import re
import time
from pathlib import Path

import requests

from common import PlatformError, env, get_token, probe_video, save_token, truncate

API = "https://api.x.com/2"
SEGMENT = 4 * 1024 * 1024  # keep each segment <= 5 MB
URL_RE = re.compile(r"https?://\S+")


def _refresh() -> str:
    refresh = get_token("x", "refresh_token", "X_REFRESH_TOKEN")
    if not refresh:
        raise PlatformError("No X refresh token. Run: python scripts/auth.py x")
    client_id = env("X_CLIENT_ID", required=True)
    secret = env("X_CLIENT_SECRET")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "refresh_token", "refresh_token": refresh, "client_id": client_id}
    if secret:  # confidential client
        basic = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
        headers["Authorization"] = f"Basic {basic}"
    r = requests.post(f"{API}/oauth2/token", data=data, headers=headers, timeout=30)
    body = r.json() if r.content else {}
    if not r.ok or "access_token" not in body:
        raise PlatformError(f"X token refresh failed: {r.status_code} {r.text[:300]}")
    save_token("x", {"access_token": body["access_token"],
                     "refresh_token": body.get("refresh_token", refresh)})
    return body["access_token"]


def build_text(caption: str, override: dict | None = None) -> str:
    text = (override or {}).get("text") or caption or ""
    if env("X_STRIP_LINKS", "true").lower() == "true":
        text = URL_RE.sub("", text)  # links raise the per-post price to $0.20
    return truncate(re.sub(r"[ \t]+", " ", text), 280)


def upload(video: Path, caption: str, override: dict | None = None) -> dict:
    info = probe_video(video)
    max_len = float(env("X_MAX_SECONDS", "140"))
    if info.get("duration") and info["duration"] > max_len:
        raise PlatformError(f"Video is {info['duration']:.0f}s; X limit set to {max_len:.0f}s (X_MAX_SECONDS).")

    token = _refresh()
    auth = {"Authorization": f"Bearer {token}"}
    size = video.stat().st_size

    r = requests.post(f"{API}/media/upload/initialize", headers=auth, timeout=30, json={
        "media_type": "video/mp4", "total_bytes": size, "media_category": "tweet_video"})
    if not r.ok:
        raise PlatformError(f"X upload init failed: {r.status_code} {r.text[:300]}")
    media_id = r.json()["data"]["id"]

    with open(video, "rb") as f:
        index = 0
        while True:
            blob = f.read(SEGMENT)
            if not blob:
                break
            r = requests.post(f"{API}/media/upload/{media_id}/append", headers=auth, timeout=300,
                              data={"segment_index": str(index)},
                              files={"media": ("chunk", blob, "application/octet-stream")})
            if not r.ok:
                raise PlatformError(f"X append {index} failed: {r.status_code} {r.text[:300]}")
            index += 1

    r = requests.post(f"{API}/media/upload/{media_id}/finalize", headers=auth, timeout=60)
    if not r.ok:
        raise PlatformError(f"X finalize failed: {r.status_code} {r.text[:300]}")
    proc = (r.json().get("data") or {}).get("processing_info")
    while proc and proc.get("state") in ("pending", "in_progress"):
        time.sleep(max(1, proc.get("check_after_secs", 3)))
        s = requests.get(f"{API}/media/upload", headers=auth, timeout=30,
                         params={"command": "STATUS", "media_id": media_id})
        proc = (s.json().get("data") or {}).get("processing_info") if s.ok else None
    if proc and proc.get("state") == "failed":
        raise PlatformError(f"X video processing failed: {proc.get('error')}")

    text = build_text(caption, override)
    r = requests.post(f"{API}/tweets", headers={**auth, "Content-Type": "application/json"},
                      timeout=30, json={"text": text, "media": {"media_ids": [media_id]}})
    if not r.ok:
        raise PlatformError(f"X post failed: {r.status_code} {r.text[:300]}")
    post_id = r.json()["data"]["id"]
    return {"id": post_id, "url": f"https://x.com/i/status/{post_id}"}
