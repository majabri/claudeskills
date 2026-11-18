#!/bin/bash
# Saves the sign-in address you copied (from the "can't be reached" page) for Claude to finish.
OUT="$(cd "$(dirname "$0")/.." && pwd)/.data/landed_url.txt"
URL="$(pbpaste | tr -d '[:space:]')"
case "$URL" in
  *code=*state=*|*state=*code=*) printf '%s\n' "$URL" > "$OUT"; pbcopy < /dev/null; echo "saved sign-in" ;;
  *) echo "That doesn't look like the sign-in address. In the browser, click the address bar, press Cmd+A then Cmd+C, and run this again." ;;
esac
