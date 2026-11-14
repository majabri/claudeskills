---
description: Security review of the current changes or a given path, Supabase RLS first. Reports findings by severity with exact fixes; does not change code unless asked.
argument-hint: "[path | pr-number | blank for uncommitted changes]"
---

# Security Scan

Load the `security-review` skill and follow it.

Scope: $ARGUMENTS
- Blank → uncommitted changes plus anything they call into.
- A path → that directory or file.
- A PR number or URL → that PR's diff (`gh pr diff`).

Steps:
1. List the trust boundaries in scope (routes, server actions, edge functions, migrations/policies, env vars, dependencies).
2. Check RLS and the service-role key first. If the Supabase MCP is connected, run the security advisor and, where safe, test cross-user access against a non-production project or branch.
3. Run the rest of the skill's checks that apply to the scope.
4. If the project has a package manager lockfile, run its audit (`npm audit --omit=dev`, `pnpm audit --prod`, …) and include HIGH/CRITICAL results.
5. Report in the skill's format and end with: ship / ship after fixes / don't ship.

Do not edit code during the scan. Offer the fixes; apply them only when the user says so.
