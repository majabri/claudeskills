# One-time setup

About an hour of clicking. Everything private lives in `<skill>/.data/` (git-ignored):
`.env` (settings and keys), `tokens.json` (sign-ins), `state.json` (what was posted), `videos/`.

Never paste a key or token into a chat. Copy it, then run one of the helpers in Terminal on your Mac:

```bash
bash scripts/save-token.sh                       # Instagram token on the clipboard -> IG_ACCESS_TOKEN
bash scripts/save-token.sh YT_CLIENT_SECRET      # Google client secret (starts GOCSPX-)
bash scripts/save-token.sh TIKTOK_CLIENT_SECRET  # TikTok client secret
bash scripts/save-signin.sh                      # the address you landed on after approving a sign-in
```

## 0. Install
```bash
mkdir -p .data && cp assets/.env.example .data/.env
pip install --target .pylib -r requirements.txt   # scripts find .pylib automatically
```

## 1. Instagram (source)
The account must be Professional (Business or Creator).

1. developers.facebook.com → register as a developer → **Create app** → use case
   **"Manage messaging & content on Instagram"** → skip the business portfolio for now.
2. Newer apps only offer **API setup with Unified login**, which needs a business portfolio:
   connect or create one.
3. **App roles → Add people → Instagram Tester →** your Instagram username.
   Accept it at instagram.com → Settings → Apps and websites → **Tester Invites**
   (the tab only appears while an invite is pending, and only for the invited account).
4. Back in API setup: **Create new configuration** (system-user token, never expires),
   then **Generate token** (click it yourself; it opens a popup) and pick the portfolio that
   owns the Instagram account.
5. Click **Copy**, run `bash scripts/save-token.sh`, and set `IG_USER_ID` in `.env` to the
   number shown under the account name.

## 2. YouTube
1. console.cloud.google.com → new project → enable **YouTube Data API v3**.
2. Google Auth Platform → **Get started**: app name, support email, **External**, contact email,
   agree to the policy.
3. **Clients → Create client → Desktop app.** Save the Client ID in `YT_CLIENT_ID`; copy the
   secret and run `bash scripts/save-token.sh YT_CLIENT_SECRET` before closing the dialog.
4. **Branding:** home page, privacy policy and terms links, plus that domain under Authorized
   domains. **Audience → Publish app** (in Testing, sign-ins expire after 7 days).
5. Sign in:
   ```bash
   python3 scripts/auth.py start youtube     # prints a link
   ```
   Open it in your normal browser, approve (Advanced → Go to app for the unverified notice).
   On the "can't be reached" page, copy the address, then:
   ```bash
   bash scripts/save-signin.sh && python3 scripts/auth.py finish "$(cat .data/landed_url.txt)"
   ```

## 3. TikTok
1. developers.tiktok.com → sign up (email) → **Connect an app** → Individual → type Other.
2. Switch to **Sandbox → Create Sandbox.** Fill icon (1024×1024), category, description,
   terms and privacy URLs, platform **Web** and its URL.
3. **Add products:** Login Kit (redirect URI = `TIKTOK_REDIRECT_URI`, must be https on a domain
   you control; a 404 page is fine) and Content Posting API (Direct Post on).
   Scopes user.info.basic, video.upload, video.publish are added automatically. **Apply changes.**
4. Save the client key in `TIKTOK_CLIENT_KEY`. Reveal the secret, **double-click** the code, Cmd+C,
   run `bash scripts/save-token.sh TIKTOK_CLIENT_SECRET`.
5. **Target users → Add account** → log in as the TikTok account to post to.
6. `python3 scripts/auth.py start tiktok`, open the link **in a browser logged into that same
   TikTok account** (otherwise: `non_sandbox_target`), approve, copy the landing address,
   `bash scripts/save-signin.sh`, then `auth.py finish` as above.
   Sandbox: inbox drafts work; direct posts are forced to "Only me". Apply for TikTok's
   Content Posting audit to post publicly.

## 4. X (optional, paid)
console.x.com → app → OAuth 2.0 (callback `X_REDIRECT_URI`, read+write) → buy credits →
`auth.py start x` / `finish`. Add `x` to `CROSSPOST_PLATFORMS`.

## 5. Test
```bash
python3 scripts/crosspost.py doctor          # every platform "ready": true
python3 scripts/crosspost.py baseline        # older videos count as already handled
python3 scripts/crosspost.py list
python3 scripts/crosspost.py run --limit 1             # dry run
python3 scripts/crosspost.py run --limit 1 --publish   # real (set YT_PRIVACY=unlisted first)
```

## 6. Automatic runs (cloud, no computer needed)
`.github/workflows/crosspost.yml` in this repo runs every hour on GitHub Actions:
- backlog left (reels older than 3 days not yet posted): YouTube up to 6 and TikTok up to 5 per
  run, each stopping at the platform's daily cap;
- caught up: only at 08:30, 16:30 and 19:30 America/Detroit.

It needs these repository secrets: IG_ACCESS_TOKEN, IG_USER_ID, YT_CLIENT_ID, YT_CLIENT_SECRET,
YT_REFRESH_TOKEN, TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN. Upload them from
the Mac in one step with `bash scripts/push-secrets.sh` (needs the GitHub CLI, `gh auth login`).
Posting history (no secrets) lives on the `crosspost-state` branch; the run refuses to start
without it so nothing is ever posted twice. Run it by hand from the Actions tab (Run workflow,
"force") to test.

To backfill an older catalog: `python3 scripts/crosspost.py include-old`, then let the hourly
runs work through it; `crosspost.py backlog` shows what's left.
