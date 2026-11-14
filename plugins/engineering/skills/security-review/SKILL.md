---
name: security-review
description: Security review for web apps built on Next.js, Supabase and Vercel — auth flows, Row Level Security, secrets and env vars, edge functions, user input, file uploads, AI/LLM features, dependencies, and pre-launch audits. Use whenever code touches authentication, authorization, RLS policies, API routes, server actions, edge functions, user-supplied input, uploads, payments, webhooks, secrets, or model prompts; when the user says "is this secure", "security review", "audit", "pen test", "check for vulnerabilities", "before we launch"; or before merging any change to auth or data access. Load alongside the engineering tier (software-l2-build / l3-architect), not instead of it.
---

# Security review

The job is to find what an attacker would find, before they do, and to say exactly how to fix it. Report only what you verified in the code, config or database. Label anything inferred as inferred.

## Order of work

1. **Scope.** List what changed or what is in scope: routes, server actions, edge functions, migrations/policies, env vars, dependencies. Security review of "everything" with no scope finds nothing; pick the trust boundaries.
2. **Data access first.** In a Supabase app, most real breaches are authorization bugs, not injection. Check RLS before anything else (below).
3. **Secrets and keys.** Then input handling, then the rest of the checklist.
4. **Report** in the format at the end. Severity reflects exploitability and impact, not how bad the code looks.

## Supabase and RLS (check first)

- Every table in an exposed schema has RLS **enabled**. A table without RLS is readable and writable by anyone with the anon key, which ships to every browser.
- Every policy is scoped to the owner or role: `using ((select auth.uid()) = user_id)`. Watch for `using (true)`, policies on `authenticated` that should be per-user, and missing `with check` on insert/update (users writing rows they don't own).
- Policies that join to other tables (team membership, org roles): confirm the joined table is itself protected and that a user can't add themselves to a team.
- `security definer` functions bypass RLS. Each one needs an explicit authorization check inside and `set search_path = ''`.
- The **service-role key** never reaches the browser, a `NEXT_PUBLIC_*` var, client bundles, logs or the repo. Use it only in edge functions or server code that has already authorized the caller.
- Storage buckets: public vs private is deliberate, and bucket policies match table policies.
- Run Supabase's security advisor (Supabase MCP `get_advisors` type `security`) and treat every finding as at least MEDIUM until explained.
- Test it, don't just read it: as user A, try to select, update and delete user B's rows through the anon client.

## Next.js and Vercel

- Server Actions and Route Handlers authenticate **and** authorize inside the handler. Middleware alone is not authorization.
- Validate all input at the boundary with a schema (zod or similar). Never trust `params`, `searchParams`, form data or headers.
- No secrets in `NEXT_PUBLIC_*`. Check Vercel env vars for Production and Preview separately; previews are often public URLs.
- `dangerouslySetInnerHTML` only with sanitized content. Redirects only to an allow-list (open-redirect).
- Server-side fetches of user-supplied URLs are SSRF; block internal addresses or use an allow-list.

## Edge functions

- Verify the caller's JWT and derive the user from it; never accept a `user_id` from the request body as identity.
- Webhooks verify the provider signature before doing anything.
- Secrets come from `supabase secrets`, never from code. CORS is not an auth control.
- Rate-limit anything that costs money (LLM calls, email, SMS) per user.

## AI / LLM features

- Treat resumes, job descriptions and any fetched content as untrusted input that can contain prompt injection. Model output that triggers actions (writes, emails, tool calls) needs validation or a human confirmation step.
- Never put secrets or other users' data in a prompt. Scope retrieval to the requesting user.
- Log prompts and outputs with PII handling in mind; check what your model provider retains.

## Everything else

Work through the general checklists when the scope calls for them:
- `references/checklist.md` — secrets, input validation, SQL injection, authn/authz, XSS, CSRF, rate limiting, data exposure, dependencies, pre-deploy checklist.
- `references/cloud-infra.md` — IAM, secrets managers, network exposure, logging, CI/CD pipeline security (GitHub Actions).
- `references/reviewer-procedure.md` — step-by-step review procedure, common false positives, emergency response for a leaked secret.

## Report format

For each finding:

```
[SEVERITY] Title
Where: file:line (or table/policy/function name)
What: one sentence on the flaw
Exploit: how an attacker uses it, concretely
Fix: the exact change
Verified: yes (how) / inferred
```

Severities: **CRITICAL** (data of other users exposed or writable, secret leaked, auth bypass), **HIGH** (exploitable with some effort or limited scope), **MEDIUM** (defense-in-depth gap, hard to exploit), **LOW** (hygiene). End with a one-line verdict: ship / ship after fixes / don't ship.

## Failure modes to avoid

- Listing generic OWASP items without checking whether they apply to this code.
- Calling RLS "fine" after reading policies without testing cross-user access.
- Inflating severity to look thorough, or deflating it to be agreeable.
- Fixing issues silently in a review; report first, then fix if asked.

<!-- References adapted from Everything Claude Code (MIT, (c) Affaan Mustafa). See NOTICE. -->
