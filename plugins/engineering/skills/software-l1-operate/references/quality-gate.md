# Pre-deploy quality gate (iCareerOS)

Run before merging to main or promoting a Vercel deployment. Each step is pass/fail; any fail blocks the release unless the owner explicitly accepts the risk in writing.

## 1. Code
- `tsc --noEmit` clean
- Lint clean (project's configured linter)
- Unit/integration tests pass
- `next build` succeeds locally with the Vercel Node version

## 2. Database
- New migrations applied cleanly to a Supabase branch or local stack (`supabase db reset`)
- Supabase security and performance advisors show no new warnings
- Every new table has RLS enabled and policies; no policy uses the service role as a shortcut
- Generated types regenerated and committed

## 3. Edge functions
- Changed functions deployed to the branch / staging project first and invoked once with a real payload
- Required secrets exist in the target project (`supabase secrets list`)

## 4. Deployment
- Env vars present for Production and Preview on Vercel
- Vercel preview smoke-tested: sign-in, the changed feature, one RLS check
- Rollback known: previous Vercel deployment to promote, and a forward-fix migration plan if a migration is involved

## 5. Report
List each step with PASS / FAIL / SKIPPED (with reason). Do not report PASS for anything you did not actually run.
