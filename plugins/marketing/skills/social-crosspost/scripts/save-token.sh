#!/bin/bash
# Saves a value currently on your clipboard into the private settings file.
#   bash scripts/save-token.sh                -> Instagram token (IG_ACCESS_TOKEN)
#   bash scripts/save-token.sh YT_CLIENT_SECRET
ENV="$(cd "$(dirname "$0")/.." && pwd)/.data/.env"
KEY="${1:-IG_ACCESS_TOKEN}"
VAL="$(pbpaste | tr -d '[:space:]')"
if [ -z "$VAL" ] || [ ${#VAL} -lt 10 ]; then
  echo "Your clipboard looks empty. Click Copy on the value first, then run this again."; exit 1
fi
case "$KEY" in IG_ACCESS_TOKEN) case "$VAL" in EAA*|IG*) ;; *) echo "That isn't the Instagram token (it starts with IG or EAA). Click Copy next to the token first."; exit 1;; esac;; esac
case "$KEY" in YT_CLIENT_SECRET) case "$VAL" in GOCSPX-*) ;; *) echo "That isn't the Google client secret (it starts with GOCSPX-). Click Copy next to it first."; exit 1;; esac;; esac
case "$KEY" in TIKTOK_CLIENT_SECRET) [[ "$VAL" =~ ^[A-Za-z0-9]{24,64}$ ]] || { echo "That is not the TikTok client secret (it is one word of letters and numbers). Double-click the revealed secret, press Cmd+C, and run this again."; exit 1; };; esac
# replace any existing line for this key, then add the new one
grep -v "^${KEY}=" "$ENV" > "$ENV.tmp"; cat "$ENV.tmp" > "$ENV"; : > "$ENV.tmp"
printf '%s=%s\n' "$KEY" "$VAL" >> "$ENV"
pbcopy < /dev/null
echo "saved $KEY"
