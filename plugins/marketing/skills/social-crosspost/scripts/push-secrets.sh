#!/bin/bash
# Upload this skill's keys and sign-ins to the GitHub repo's encrypted Actions secrets,
# so the cloud workflow can run without this computer. Values are never printed.
#   bash scripts/push-secrets.sh [owner/repo]     (default: majabri/claudeskills)
set -euo pipefail
REPO="${1:-majabri/claudeskills}"
DIR="$(cd "$(dirname "$0")/.." && pwd)"
command -v gh >/dev/null || { echo "Install the GitHub CLI first: brew install gh  (then: gh auth login)"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Sign in first: gh auth login"; exit 1; }
TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
python3 - "$DIR" > "$TMP" <<'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1]) / ".data"
env = {}
for line in (d / ".env").read_text().splitlines():
    line = line.split(" #")[0].strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        if v.strip():
            env[k.strip()] = v.strip()
tok = json.loads((d / "tokens.json").read_text()) if (d / "tokens.json").exists() else {}
want = ["IG_ACCESS_TOKEN", "IG_USER_ID", "YT_CLIENT_ID", "YT_CLIENT_SECRET", "TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET"]
out = {k: env[k] for k in want if env.get(k)}
for key, (plat, field) in {"YT_REFRESH_TOKEN": ("youtube", "refresh_token"),
                           "TIKTOK_REFRESH_TOKEN": ("tiktok", "refresh_token")}.items():
    if tok.get(plat, {}).get(field):
        out[key] = tok[plat][field]
    elif env.get(key):
        out[key] = env[key]
missing = [k for k in want + ["YT_REFRESH_TOKEN", "TIKTOK_REFRESH_TOKEN"] if k not in out]
if missing:
    print("MISSING " + " ".join(missing), file=sys.stderr)
for k, v in out.items():
    print(f"{k}={v}")
PY
gh secret set -f "$TMP" -R "$REPO"
echo "Uploaded $(wc -l < "$TMP" | tr -d ' ') secrets to $REPO."
