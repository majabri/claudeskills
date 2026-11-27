"""Briefly host a file at a public URL so Buffer can fetch it.

Buffer only takes a video by URL. A re-mixed video has no Instagram link, so it goes up
as an asset on one GitHub release of this repo (tag GH_HOST_TAG, default
"tiktok-sound-swaps") and is deleted again once Buffer has published it (see
crosspost.py verify). Needs GITHUB_TOKEN (contents: write) and GITHUB_REPOSITORY,
both present in GitHub Actions.
"""
from __future__ import annotations

import requests

from common import PlatformError, env

API = "https://api.github.com"


def _h() -> dict:
    tok = env("GITHUB_TOKEN", required=True)
    return {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}


def _repo() -> str:
    return env("GITHUB_REPOSITORY", required=True)


def _release() -> dict:
    tag = env("GH_HOST_TAG", "tiktok-sound-swaps")
    r = requests.get(f"{API}/repos/{_repo()}/releases/tags/{tag}", headers=_h(), timeout=30)
    if r.status_code == 200:
        return r.json()
    if r.status_code != 404:
        raise PlatformError(f"GitHub release lookup {r.status_code}: {r.text[:200]}")
    r = requests.post(f"{API}/repos/{_repo()}/releases", headers=_h(), timeout=30, json={
        "tag_name": tag, "name": "TikTok sound swaps (temporary files)", "prerelease": True,
        "body": "Temporary videos handed to Buffer for TikTok after their background music was "
                "replaced. Each file is deleted once the TikTok post goes out."})
    if not r.ok:
        raise PlatformError(f"GitHub release create {r.status_code}: {r.text[:200]}")
    return r.json()


def upload(path, name: str) -> dict:
    rel = _release()
    for a in rel.get("assets", []):
        if a["name"] == name:
            delete(a["id"])
    url = rel["upload_url"].split("{")[0]
    with open(path, "rb") as f:
        r = requests.post(url, params={"name": name}, data=f, timeout=600,
                          headers={**_h(), "Content-Type": "video/mp4"})
    if not r.ok:
        raise PlatformError(f"GitHub asset upload {r.status_code}: {r.text[:200]}")
    a = r.json()
    return {"asset_id": a["id"], "url": a["browser_download_url"]}


def delete(asset_id: int) -> None:
    r = requests.delete(f"{API}/repos/{_repo()}/releases/assets/{asset_id}", headers=_h(), timeout=30)
    if r.status_code not in (204, 404):
        raise PlatformError(f"GitHub asset delete {r.status_code}: {r.text[:200]}")
