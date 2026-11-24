#!/usr/bin/env python3
"""Has Snap switched on posting for our app yet?

Refreshes the Snapchat sign-in (saved in .data/tokens.json), reads the Public Profile,
and asks Snap for an upload slot (an empty media container that expires on its own;
nothing is posted). Prints JSON: {"signed_in", "profile", "posting_allowed", "detail"}.
Standard library only.
"""
from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / ".data"
ORG = "b26e0b36-be0f-49e0-b171-bc1f3eef715b"
API = "https://businessapi.snapchat.com/v1/"


def _env() -> dict:
    out = {}
    for line in (DATA / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _call(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return r.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return e.code, {}


def main() -> int:
    env = _env()
    tokens = json.loads((DATA / "tokens.json").read_text())
    snap = tokens.get("snapchat") or {}
    out = {"signed_in": False, "profile": None, "posting_allowed": False, "detail": ""}
    if not snap.get("refresh_token"):
        out["detail"] = "no Snapchat sign-in saved"
        print(json.dumps(out))
        return 0
    status, tok = _call("https://accounts.snapchat.com/login/oauth2/access_token",
                        data=urllib.parse.urlencode({
                            "grant_type": "refresh_token", "refresh_token": snap["refresh_token"],
                            "client_id": env["SNAP_CLIENT_ID"], "client_secret": env["SNAP_CLIENT_SECRET"],
                        }).encode(), headers={"Content-Type": "application/x-www-form-urlencoded"})
    if status != 200 or "access_token" not in tok:
        out["detail"] = f"sign-in refresh failed ({status}); Snapchat needs signing in again"
        print(json.dumps(out))
        return 0
    snap.update(access_token=tok["access_token"], saved_at=time.time())
    if tok.get("refresh_token"):
        snap["refresh_token"] = tok["refresh_token"]   # Snap may rotate it; keep the newest
    tokens["snapchat"] = snap
    tmp = DATA / "tokens.json.tmp"
    tmp.write_text(json.dumps(tokens))
    os.replace(tmp, DATA / "tokens.json")
    out["signed_in"] = True

    h = {"Authorization": "Bearer " + tok["access_token"], "Content-Type": "application/json"}
    status, body = _call(API + f"organizations/{ORG}/public_profiles", headers=h)
    profiles = [p.get("public_profile", {}) for p in body.get("public_profiles", [])]
    if not profiles:
        out["detail"] = f"could not read the Public Profile ({status})"
        print(json.dumps(out))
        return 0
    prof = profiles[0]
    out["profile"] = {"id": prof.get("id"), "name": prof.get("display_name")}
    payload = {"type": "VIDEO", "name": "permission-check",
               "key": base64.b64encode(os.urandom(32)).decode(),
               "iv": base64.b64encode(os.urandom(16)).decode()}
    status, _ = _call(API + f"public_profiles/{prof['id']}/media",
                      data=json.dumps(payload).encode(), headers=h, method="POST")
    out["posting_allowed"] = status in (200, 201)
    out["detail"] = "Snap allows uploads" if out["posting_allowed"] else f"upload refused ({status}): waiting on Snap's allowlist"
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
