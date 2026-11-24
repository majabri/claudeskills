"""Publish through Buffer (https://buffer.com), an audited TikTok partner.

Used for TikTok when TIKTOK_MODE=buffer: our own TikTok app can only send drafts or
private posts (TikTok's audit is not available to personal tools), while Buffer's
free plan publishes publicly. Buffer fetches the video from a public URL, so we hand
it Instagram's own media_url and schedule the post a few minutes ahead (Instagram's
links expire after a while, so posts are never left waiting in Buffer's queue).

Settings: BUFFER_API_KEY (secret, from publish.buffer.com/settings/api),
BUFFER_TIKTOK_CHANNEL_ID (the channel id in the Buffer URL), BUFFER_DELAY_MINUTES (default 3).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import requests

import re

from common import PlatformError, env, truncate

TIKTOK_MAX_TAGS = 5
_TAG = re.compile(r"(?<!\w)#\w+")


def tiktok_caption(caption: str) -> str:
    """TikTok flags hashtag-stuffed captions and call-to-action lines as spam.
    Keep the story text, drop "follow for..." lines, keep the first few hashtags."""
    lines = []
    for line in (caption or "").splitlines():
        text = _TAG.sub("", line).strip()
        if text and not re.match(r"(?i)^(follow|like|share|subscribe)\b", text):
            lines.append(text)
    tags = []
    for t in _TAG.findall(caption or ""):
        if t.lower() not in {x.lower() for x in tags}:
            tags.append(t)
    max_tags = int(env("TIKTOK_MAX_HASHTAGS", str(TIKTOK_MAX_TAGS)))
    return ("\n".join(lines) + "\n\n" + " ".join(tags[:max_tags])).strip()

API = "https://api.buffer.com"

_CREATE = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id dueAt } }
    ... on MutationError { message }
  }
}"""


def _gql(query: str, variables: dict | None = None) -> dict:
    key = env("BUFFER_API_KEY", required=True)
    r = requests.post(API, json={"query": query, "variables": variables or {}}, timeout=60,
                      headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        body = r.json()
    except ValueError:
        raise PlatformError(f"Buffer API {r.status_code}: {r.text[:300]}") from None
    if not r.ok or body.get("errors"):
        raise PlatformError(f"Buffer API {r.status_code}: {str(body.get('errors') or body)[:300]}")
    return body.get("data") or {}


def channels() -> list[dict]:
    """Every channel the API key can see (used by `doctor` and setup)."""
    orgs = _gql("query { account { organizations { id name } } }")["account"]["organizations"]
    out = []
    for o in orgs:
        q = "query($id: OrganizationId!) { channels(input: {organizationId: $id}) { id name service } }"
        for c in _gql(q, {"id": o["id"]}).get("channels", []):
            out.append({**c, "organization": o["name"]})
    return out


def post_video(channel_id: str, video_url: str, text: str) -> dict:
    if not video_url:
        raise PlatformError("Buffer needs a public video URL (Instagram gave none for this reel)")
    due = datetime.now(timezone.utc) + timedelta(minutes=int(env("BUFFER_DELAY_MINUTES", "3")))
    data = _gql(_CREATE, {"input": {
        "channelId": channel_id,
        "text": text,
        "schedulingType": "automatic",
        "mode": "customScheduled",
        "dueAt": due.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "assets": [{"video": {"url": video_url}}],
    }})
    res = data.get("createPost") or {}
    if res.get("message") or not res.get("post"):
        raise PlatformError(f"Buffer createPost failed: {res.get('message') or data}")
    post = res["post"]
    return {"id": post["id"], "status": "SCHEDULED_IN_BUFFER", "due_at": post.get("dueAt"),
            "mode": "buffer", "privacy": "public (published by Buffer)"}


def post_status(post_id: str) -> dict:
    q = """query($id: PostId!) { post(input: {id: $id}) { status sentAt externalLink error { message } } }"""
    p = _gql(q, {"id": post_id}).get("post") or {}
    return {"status": p.get("status"), "sent_at": p.get("sentAt"), "link": p.get("externalLink"),
            "error": (p.get("error") or {}).get("message")}


def upload_tiktok(caption: str, video_url: str, override: dict | None = None) -> dict:
    override = override or {}
    channel = env("BUFFER_TIKTOK_CHANNEL_ID", required=True)
    text = truncate(override.get("title") or tiktok_caption(caption), 2200)
    return post_video(channel, video_url, text)
