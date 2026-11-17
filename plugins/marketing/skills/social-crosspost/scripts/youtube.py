"""Upload to YouTube with the YouTube Data API v3 (videos.insert, resumable)."""
from __future__ import annotations

from pathlib import Path

from common import PlatformError, env, get_token, log, probe_video, truncate

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    refresh = get_token("youtube", "refresh_token", "YT_REFRESH_TOKEN")
    if not refresh:
        raise PlatformError("No YouTube refresh token. Run: python scripts/auth.py youtube")
    creds = Credentials(
        token=None,
        refresh_token=refresh,
        client_id=env("YT_CLIENT_ID", required=True),
        client_secret=env("YT_CLIENT_SECRET", required=True),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def build_metadata(caption: str, video: Path, override: dict | None = None) -> dict:
    override = override or {}
    first_line = (caption or "").strip().splitlines()[0] if caption and caption.strip() else "New video"
    title = override.get("title") or first_line
    description = override.get("description") or (caption or "")
    info = probe_video(video)
    is_short = bool(info.get("duration") and info["duration"] <= 180 and
                    info.get("height", 0) >= info.get("width", 1))
    if is_short and "#shorts" not in (title + description).lower():
        description = (description + "\n\n#Shorts").strip()
    return {
        "title": truncate(title.replace("<", "").replace(">", ""), 100),
        "description": truncate(description.replace("<", "").replace(">", ""), 5000),
        "privacy": override.get("privacy") or env("YT_PRIVACY", "public"),
        "category": env("YT_CATEGORY_ID", "22"),  # 22 = People & Blogs
        "is_short": is_short,
    }


def upload(video: Path, caption: str, override: dict | None = None) -> dict:
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    meta = build_metadata(caption, video, override)
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"],
                    "categoryId": meta["category"]},
        "status": {"privacyStatus": meta["privacy"], "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(video), mimetype="video/*", chunksize=8 << 20, resumable=True)
    try:
        req = _service().videos().insert(part="snippet,status", body=body, media_body=media)
        resp = None
        while resp is None:
            status, resp = req.next_chunk()
            if status:
                log(f"  YouTube upload {int(status.progress() * 100)}%")
    except HttpError as e:
        raise PlatformError(f"YouTube upload failed: {e}") from e
    vid = resp["id"]
    return {"id": vid, "url": f"https://youtu.be/{vid}",
            "privacy": resp.get("status", {}).get("privacyStatus")}
