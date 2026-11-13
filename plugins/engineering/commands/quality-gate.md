---
description: Run the iCareerOS pre-deploy quality gate (types, lint, tests, build, migrations/RLS, edge functions, Vercel env, rollback) and report PASS/FAIL per step.
argument-hint: "[blank | --skip-db | --skip-e2e]"
---

# Quality Gate

Read `software-l1-operate/references/quality-gate.md` and run every step that applies. Options: $ARGUMENTS

- Use the project's own scripts from `package.json` (`typecheck`, `lint`, `test`, `build`) when they exist; otherwise `tsc --noEmit`, the configured linter, the test runner, and `next build`.
- `--skip-db`: skip section 2 (say so in the report).
- `--skip-e2e`: skip the preview smoke test (say so in the report).
- Never run migrations or deploy edge functions against production as part of the gate.

Report a table: step, PASS / FAIL / SKIPPED, evidence (command and the relevant output line). Finish with "Gate: PASS" only if nothing failed. Do not mark a step PASS that you did not run.
