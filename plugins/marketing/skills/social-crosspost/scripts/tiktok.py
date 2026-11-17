"""Post to TikTok with the Content Posting API.

Two modes (TIKTOK_MODE):
  inbox  - uploads as a draft to the TikTok app inbox; you finish and publish in the app.
           Works before your app passes TikTok's audit. (default)
  direct - publishes straight to the profile. Before the audit, TikTok forces
           SELF_ONLY (private) and the account itself must be private.
"""
from __future__ import annotations

import math
import time
from pathlib import Path

import requests

from common import PlatformError, env, get_token, save_token, truncate

API = "https://open.tiktokapis.com/v2"
MIN_CHUNK = 5 * 1024 * 1024
CHUNK = 10 * 1024 * 1024


def _refresh() -> str:
    refresh = get_token("tiktok", "refresh_token", "TIKTOK_REFRESH_TOKEN")
    if not refresh:
        raise PlatformError("No TikTok refresh token. Run: python scripts/auth.py tiktok")
    r = requests.post(
        f"{API}/oauth/token/",
        data={
            "client_key": env("TIKTOK_CLIENT_KEY", required=True),
            "client_secret": env("TIKTOK_CLIENT_SECRET", required=True),
            "grant_type": "refresh_token",
            "refresh_token": refresh,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    data = r.json()
    if not r.ok or "access_token" not in data:
        raise PlatformError(f"TikTok token refresh failed: {r.status_code} {r.text[:300]}")
    save_token("tiktok", {"access_token": data["access_token"],
                          "refresh_token": data.get("refresh_token", refresh)})
    return data["access_token"]


def _post(path: str, token: str, body: dict) -> dict:
    r = requests.post(f"{API}{path}", json=body, timeout=60,
                      headers={"Authorization": f"Bearer {token}",
                               "Content-Type": "application/json; charset=UTF-8"})
    data = r.json() if r.content else {}
    err = data.get("error", {})
    if not r.ok or (err.get("code") not in (None, "ok")):
        raise PlatformError(f"TikTok {path} failed: {r.status_code} {err or r.text[:300]}")
    return data.get("data", {})


def _chunk_plan(size: int) -> tuple[int, int]:
    if size <= MIN_CHUNK:
        return size, 1
    chunk = min(CHUNK, size)
    return chunk, max(1, math.floor(size / chunk))  # last chunk absorbs the remainder


def _upload_file(upload_url: str, video: Path, size: int, chunk: int, count: int) -> None:
    with open(video, "rb") as f:
        for i in range(count):
            start = i * chunk
            end = size - 1 if i == count - 1 else start + chunk - 1
            f.seek(start)
            blob = f.read(end - start + 1)
            r = requests.put(upload_url, data=blob, timeout=300, headers={
                "Content-Type": "video/mp4",
                "Content-Length": str(len(blob)),
                "Content-Range": f"bytes {start}-{end}/{size}",
            })
            if r.status_code not in (200, 201, 206):
                raise PlatformError(f"TikTok chunk {i + 1}/{count} failed: {r.status_code} {r.text[:200]}")


def upload(video: Path, caption: str, override: dict | None = None) -> dict:
    override = override or {}
    token = _refresh()
    size = video.stat().st_size
    chunk, count = _chunk_plan(size)
    source = {"source": "FILE_UPLOAD", "video_size": size,
              "chunk_size": chunk, "total_chunk_count": count}
    mode = override.get("mode") or env("TIKTOK_MODE", "inbox")
    title = truncate(override.get("title") or caption or "", 2200)

    if mode == "direct":
        info = _post("/post/publish/creator_info/query/", token, {})
        options = info.get("privacy_level_options", [])
        wanted = override.get("privacy") or env("TIKTOK_PRIVACY", "PUBLIC_TO_EVERYONE")
        privacy = wanted if wanted in options else ("SELF_ONLY" if "SELF_ONLY" in options else options[0])
        init = _post("/post/publish/video/init/", token, {
            "post_info": {
                "title": title,
                "privacy_level": privacy,
                "disable_comment": False, "disable_duet": False, "disable_stitch": False,
                "brand_content_toggle": False, "brand_organic_toggle": False,
            },
            "source_info": source,
        })
    else:
        privacy = "draft (finish in TikTok app inbox)"
        init = _post("/post/publish/inbox/video/init/", token, {"source_info": source})

    _upload_file(init["upload_url"], video, size, chunk, count)
    publish_id = init["publish_id"]

    status = "PROCESSING_UPLOAD"
    for _ in range(60):
        time.sleep(5)
        st = _post("/post/publish/status/fetch/", token, {"publish_id": publish_id})
        status = st.get("status", status)
        if status in ("PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"):
            break
        if status == "FAILED":
            raise PlatformError(f"TikTok processing failed: {st.get('fail_reason')}")
    return {"id": publish_id, "status": status, "privacy": privacy, "mode": mode}
