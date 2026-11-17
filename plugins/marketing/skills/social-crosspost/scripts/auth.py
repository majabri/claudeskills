#!/usr/bin/env python3
"""Sign-in helper, two steps so it works without a local browser on the same machine.

  python scripts/auth.py start <instagram|youtube|tiktok|x>
      -> prints {"url": ...}. Open it in a browser and sign in.
  python scripts/auth.py finish "<the full address the browser landed on>"
      -> exchanges the code and saves tokens to <data dir>/tokens.json

  python scripts/auth.py instagram-exchange <short-lived token>   # optional alternative

Redirect addresses (register exactly these in each developer app, or override in .env):
  YT_REDIRECT_URI      default http://localhost:8765/callback
  X_REDIRECT_URI       default http://localhost:8765/callback
  TIKTOK_REDIRECT_URI  default https://icareeros.com/oauth/callback
  IG_REDIRECT_URI      default https://icareeros.com/oauth/callback
The page you land on may show an error ("can't connect" / 404). That's expected:
only its address is needed.
"""
from __future__ import annotations

import base64
import hashlib
import json
import secrets
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402  (also puts .pylib on sys.path)
from common import data_dir, env, save_token  # noqa: E402

import requests  # noqa: E402

DEFAULT_REDIRECTS = {
    "youtube": "http://localhost:8765/callback",
    "x": "http://localhost:8765/callback",
    "tiktok": "https://icareeros.com/oauth/callback",
    "instagram": "https://icareeros.com/oauth/callback",
}
ENV_REDIRECT = {"youtube": "YT_REDIRECT_URI", "x": "X_REDIRECT_URI",
                "tiktok": "TIKTOK_REDIRECT_URI", "instagram": "IG_REDIRECT_URI"}


def redirect_uri(platform: str) -> str:
    return env(ENV_REDIRECT[platform], DEFAULT_REDIRECTS[platform])


def _pending_path() -> Path:
    return data_dir() / "pending_auth.json"


def _pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)[:96]
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def start(platform: str) -> dict:
    state = secrets.token_urlsafe(16)
    verifier, challenge = _pkce()
    redirect = redirect_uri(platform)
    if platform == "youtube":
        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
            "client_id": env("YT_CLIENT_ID", required=True), "redirect_uri": redirect,
            "response_type": "code", "scope": "https://www.googleapis.com/auth/youtube.upload",
            "access_type": "offline", "prompt": "consent", "state": state,
            "code_challenge": challenge, "code_challenge_method": "S256"})
    elif platform == "tiktok":
        url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode({
            "client_key": env("TIKTOK_CLIENT_KEY", required=True),
            "scope": "user.info.basic,video.upload,video.publish",
            "response_type": "code", "redirect_uri": redirect, "state": state})
    elif platform == "x":
        url = "https://x.com/i/oauth2/authorize?" + urllib.parse.urlencode({
            "response_type": "code", "client_id": env("X_CLIENT_ID", required=True),
            "redirect_uri": redirect,
            "scope": "tweet.read tweet.write users.read media.write offline.access",
            "state": state, "code_challenge": challenge, "code_challenge_method": "S256"})
    elif platform == "instagram":
        url = "https://www.instagram.com/oauth/authorize?" + urllib.parse.urlencode({
            "client_id": env("IG_APP_ID", required=True), "redirect_uri": redirect,
            "response_type": "code", "scope": "instagram_business_basic", "state": state,
            "enable_fb_login": "0", "force_authentication": "1"})
    else:
        sys.exit(f"Unknown platform {platform}")
    pending = json.loads(_pending_path().read_text()) if _pending_path().exists() else {}
    pending[state] = {"platform": platform, "verifier": verifier, "redirect": redirect,
                      "created": int(time.time())}
    _pending_path().write_text(json.dumps(pending))
    return {"platform": platform, "url": url, "redirect_uri": redirect}


def finish(landed_url: str) -> dict:
    q = urllib.parse.parse_qs(urllib.parse.urlparse(landed_url.strip()).query)
    if q.get("error"):
        sys.exit(f"Sign-in was refused: {q.get('error_description', q['error'])[0]}")
    code = (q.get("code") or [None])[0]
    state = (q.get("state") or [None])[0]
    pending = json.loads(_pending_path().read_text()) if _pending_path().exists() else {}
    entry = pending.pop(state, None) if state else None
    if not code or not entry:
        sys.exit("No matching sign-in found. Run `start` again and use the newest address.")
    if time.time() - entry["created"] > 900:
        sys.exit("That sign-in is older than 15 minutes. Run `start` again.")
    _pending_path().write_text(json.dumps(pending))
    platform, verifier, redirect = entry["platform"], entry["verifier"], entry["redirect"]
    code = code.split("#")[0]

    if platform == "youtube":
        r = requests.post("https://oauth2.googleapis.com/token", timeout=30, data={
            "code": code, "client_id": env("YT_CLIENT_ID", required=True),
            "client_secret": env("YT_CLIENT_SECRET", required=True), "redirect_uri": redirect,
            "grant_type": "authorization_code", "code_verifier": verifier})
        data = r.json()
        if "refresh_token" not in data:
            sys.exit(f"YouTube sign-in failed: {r.status_code} {_safe(data)}")
        save_token("youtube", {"refresh_token": data["refresh_token"]})
    elif platform == "tiktok":
        r = requests.post("https://open.tiktokapis.com/v2/oauth/token/", timeout=30, data={
            "client_key": env("TIKTOK_CLIENT_KEY", required=True),
            "client_secret": env("TIKTOK_CLIENT_SECRET", required=True),
            "code": code, "grant_type": "authorization_code", "redirect_uri": redirect})
        data = r.json()
        if "refresh_token" not in data:
            sys.exit(f"TikTok sign-in failed: {r.status_code} {_safe(data)}")
        save_token("tiktok", {"access_token": data["access_token"], "refresh_token": data["refresh_token"]})
    elif platform == "x":
        cid, secret = env("X_CLIENT_ID", required=True), env("X_CLIENT_SECRET")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if secret:
            headers["Authorization"] = "Basic " + base64.b64encode(f"{cid}:{secret}".encode()).decode()
        r = requests.post("https://api.x.com/2/oauth2/token", headers=headers, timeout=30, data={
            "grant_type": "authorization_code", "code": code, "redirect_uri": redirect,
            "code_verifier": verifier, "client_id": cid})
        data = r.json()
        if "refresh_token" not in data:
            sys.exit(f"X sign-in failed: {r.status_code} {_safe(data)}")
        save_token("x", {"access_token": data["access_token"], "refresh_token": data["refresh_token"]})
    elif platform == "instagram":
        r = requests.post("https://api.instagram.com/oauth/access_token", timeout=30, data={
            "client_id": env("IG_APP_ID", required=True),
            "client_secret": env("IG_APP_SECRET", required=True),
            "grant_type": "authorization_code", "redirect_uri": redirect, "code": code})
        short = r.json()
        if "access_token" not in short:
            sys.exit(f"Instagram sign-in failed: {r.status_code} {_safe(short)}")
        _instagram_long_lived(short["access_token"])
    return {"connected": platform}


def _instagram_long_lived(short_token: str) -> None:
    r = requests.get("https://graph.instagram.com/access_token", timeout=30, params={
        "grant_type": "ig_exchange_token", "client_secret": env("IG_APP_SECRET", required=True),
        "access_token": short_token})
    data = r.json()
    if "access_token" not in data:
        sys.exit(f"Instagram long-lived exchange failed: {r.status_code} {_safe(data)}")
    save_token("instagram", {"access_token": data["access_token"]})


def _safe(data: dict) -> str:
    """Error text without any token values."""
    return json.dumps({k: v for k, v in data.items() if "token" not in k})[:300]


if __name__ == "__main__":
    common.load_config()
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "start":
        print(json.dumps(start(args[1].lower()), indent=2))
    elif len(args) == 2 and args[0] == "finish":
        print(json.dumps(finish(args[1]), indent=2))
    elif len(args) == 2 and args[0] == "instagram-exchange":
        _instagram_long_lived(args[1])
        print(json.dumps({"connected": "instagram"}))
    else:
        sys.exit(__doc__)
