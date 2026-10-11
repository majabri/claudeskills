---
name: lovabledatabase
description: Make database changes to a Lovable Cloud project correctly on the first attempt — schema, RLS policies, functions, triggers, scheduled jobs, and the TypeScript/app-code sync that has to follow. Use this whenever the work touches a Lovable app's database: adding or changing tables and columns, writing or auditing RLS policies, creating RPCs, triggers or cron jobs, fixing a query that returns nothing or everything, or deciding whether a change belongs in the SQL editor or the Lovable chat. It defers to the repo's own migration ledger and queue conventions where those exist. Use it even when the request sounds like plain SQL ("add a status column", "why can users see each other's rows") — Lovable Cloud has constraints that make ordinary SQL advice wrong.
---

# Lovable Cloud: database changes

## What is actually possible — read this before promising anything

Lovable Cloud is a managed Postgres instance built on Supabase's open-source
stack. It exposes **no connection string, no database URL, and no retrievable
password**. Nothing outside Lovable can connect to it: not psql, not a Supabase
MCP server, not an ORM running locally. Any plan that assumes direct access is
wrong, and saying otherwise wastes the user's time.

There are exactly **two channels** that can change a Cloud database:

| Channel | Where | What it's for |
|---|---|---|
| **SQL editor** | More → Cloud → SQL editor | Statements you author precisely and the user runs. Destructive statements (DELETE, DROP, TRUNCATE, ALTER, UPDATE) prompt for confirmation. |
| **Project chat** | The Lovable project chat | Structural changes you want Lovable to own: migration file, generated types, and app wiring together. |

**Git is not a third channel — but it may still be where the change starts.**
Lovable's docs are explicit that migration files added through Git are never
run: pushing a `.sql` file applies nothing. What Git *can* be is the **source of
record** that a change is authored into before Lovable applies it, and some
repos require exactly that (see the ledger section below). The distinction
matters: committing the SQL is not applying it, and treating a committed file as
applied is the error. Edge-function code is likewise editable through Git but
not deployed until someone asks Lovable in chat to deploy it.

Git is also where app code, queries, components, and type files live, and those
you can edit directly.

## The repo's own rules outrank everything below

Before choosing a channel, find out whether this repo already has a migration
discipline, because if it does, that discipline wins and the generic guidance in
this skill is subordinate to it. Check, in this order:

1. `CLAUDE.md` and any `docs/` or ADR file describing database or migration
   process.
2. Tests that read the migration directory — a file like
   `appliedOrder.test.ts` is a strong signal that the committed migration copy
   is being treated as the **authoritative ledger of what has been applied**.
3. Any queue or hand-off convention in the repo or its issue templates — an
   "Awaiting Lovable" column, a paste block, a migration checklist.

**When the committed migration copy is the ledger, every structural change must
go through the chat**, so that Lovable writes the migration and it lands on the
synced branch. The SQL editor produces no migration file, so a change made there
is invisible to the ledger: the test that reads it will disagree with the live
database, the next PR goes red, and — worse than the red build — the repo now
contains a migration history that lies about the schema. That is the exact
failure this skill exists to prevent, so do not trade it for the convenience of
pasting SQL.

Under a ledger rule, the SQL editor narrows to **read-only use**: the diagnostic
and verification queries in this skill, which change nothing and leave no gap.
If a change genuinely cannot be expressed through the chat, say so, name the
ledger rule it would break, and let the user decide — never pick silently.

A repo with no such convention falls through to the guidance below.

### The source-first ledger pattern

Some repos run a stricter discipline than Lovable requires, because Lovable's
own behaviour isn't trustworthy enough on its own. The markers are a test over
the migration directory, a journal file, and a queue section in `CLAUDE.md`.
Where you find them, this is the shape — but **re-read `CLAUDE.md` for the
authoritative wording**, since the details below are a pattern, not a spec, and
the repo's copy wins:

- **Two directories, two jobs.** `supabase/migrations/`
  (`<14-digit-timestamp>_<name>.sql`) holds the **source of truth**, authored and
  committed by hand. `drizzle/migrations/` (`NNNN_<name>.sql`) plus
  `drizzle/migrations/meta/_journal.json` is **Lovable's ledger of what it
  actually applied**, written only by Lovable. Never hand-edit the ledger.
- **Matching is normalized, not byte-for-byte.** Don't describe it as byte-for-
  byte; that overstates it in one direction and understates it in another. The
  comparison strips `--` line comments and collapses all whitespace to single
  spaces before comparing. Two consequences people get wrong:
  - `/* … */` block comments are **not** stripped, so a copy differing only in a
    block comment **fails**. Keep block comments out of migration SQL.
  - A `--` inside a string literal is cut too. Harmless for matching, but it
    means comment text is never trustworthy as content — never put meaning in a
    comment and expect it to survive.
- **Copies are matched by content, not by filename.** The Drizzle copy
  `0065_stock_intel_signed.sql` is recognised as the source
  `20261011100000_stock_intel_signed.sql` because the normalized text matches.
  Each copy must map to exactly one committed source file.
- **A copy with no committed source fails the build, and the fix is to commit the
  source — never to loosen the test.** This has happened in practice and was
  resolved by back-filling the source file afterwards.
- **Order of operations, every time:** commit the source file → add the queue row
  → ask Lovable to apply → Lovable commits its ledger copy and journal entry →
  `types.ts` is regenerated.
- **Never author schema SQL that doesn't exist as a committed source file
  first.** This is the inversion of normal practice and it's the whole point: the
  file is the proposal, the ledger is the receipt.
- **The ledger has a floor.** Source files with a timestamp older than the one
  behind Drizzle `0000` predate the ledger and are treated as already applied.
  Don't try to reconcile them.
- **No gaps.** A committed migration must not sit unapplied while a newer one is
  applied. This check fails on the main branch, not only on a PR, so an
  out-of-order apply breaks everyone — and it is the check that catches an
  unapplied migration adding rows or functions.
- **The forward-dependency check is narrower than it sounds.** It catches only an
  applied migration referencing a **table** that an unapplied file creates.
  Anything else out of order is caught by the gap check above, not this one.
- **Every new migration needs its queue row**, or the PR fails regardless of
  whether the SQL is correct. **Stale rows are fine**: a row for an
  already-applied migration is allowed, so that Lovable's own commit doesn't turn
  the main branch red. It is removed in the PR that verifies the apply.
- **Audit Lovable's own merge commits.** Lovable should only ever touch the
  ledger, `types.ts`, and the lockfiles. A Lovable merge that changes anything
  else has silently reverted someone's work — this has actually happened. Check
  the diff rather than assuming.
- **Lovable does not publish.** Applying a migration is not a deploy.

**The pinned journal exception.** The journal may legitimately be missing an
entry for one specific copy, pinned by the test as the single allowed
discrepancy: every journal entry must have a copy, and exactly one copy is
allowed without a journal entry. In this repo that is
`0012_goals_account.sql` — Lovable's journal skipped it when it was applied, and
the apply was verified at the time. **Do not "fix" the journal by hand.** Adding
the missing entry breaks the test, and hand-editing the ledger is forbidden
anyway. A careful reader will be tempted; say so before they are.

**The queue table.** Columns are `# | Migration | What it needs | Addendum`. The
parser recognises only `\d{14}_[a-z0-9_]+\.sql` filenames, and only between the
`## Awaiting Lovable` heading and the next `## ` heading — so a name written any
other way, or placed outside that block, is invisible to it. The matching
addendum lives at `docs/implementation/LOVABLE-QUEUE-<date>-<name>.md`.

**What stays outside the migration flow.** Not everything Lovable does is a
schema change, and treating it as one creates busywork: secrets, scheduled-job
rows, hand-fired runs, and live read-only queries are legitimate non-migration
work. Don't manufacture a migration file for them, and don't block them behind
the queue.

### The paste block

Under this pattern the deliverable handed to Lovable is a block with five parts,
in this order:

1. **The file to apply**, named exactly as the queue table names it, and where it
   goes in the order — after which Drizzle index.
2. **One sentence** on what it does, and whether `types.ts` changes.
3. **The read-backs from the addendum, verbatim**, each with its expected answer
   in a comment.
4. **The rollback line**, at one-day recovery granularity.
5. **The one request**: report the answers verbatim, and the Drizzle index the
   copy received.

Three rules govern the block itself, and each exists because of a specific way it
has gone wrong:

- **Nothing else goes in it.** No history, no "publish", and no filename from
  memory. The queue table and the addendum are the only sources for what goes in
  the block — a filename recalled rather than copied is how the wrong migration
  gets applied.
- **One block per queue row, in apply order.** A row whose PR hasn't merged is
  left out entirely, because its source file isn't on the main branch for Lovable
  to copy from.
- **The block ends the report**, and is forwarded unedited. Anything written
  after it tends to get pasted along with it.

For column-level grants, write the read-backs with `has_column_privilege(...)`
rather than inspecting catalogs by hand — it answers the question actually being
asked. Keep it to the one request: a paste containing two asks is how the second
one gets silently dropped.

## Choosing the channel

This is the decision that determines whether a change lands cleanly, so make it
deliberately rather than defaulting to whichever is faster to type.

**Use the chat when the change should be owned end to end** — a new table, a new
feature's worth of columns, anything the app's TypeScript needs to know about.
Lovable writes the Drizzle migration, regenerates the types, and updates the
calling code in one pass. Hand-running the equivalent SQL gets you the schema
and leaves the migration history and types stale.

**Use the SQL editor when the change is invisible to the app's type surface**
*and the repo has no ledger rule* — adding an index, writing or replacing an RLS
policy, creating or altering a function or trigger, scheduling a job, backfilling
data, or running diagnostics. These don't change the generated types, so there's
nothing to desync, and authoring them precisely beats describing them in prose.
Re-read the section above before using this branch: under a ledger rule these
all belong in the chat instead, because each one is a schema change that must
produce a migration file.

**Use the chat even when you could use SQL** if the change is backward
incompatible: dropping or renaming a table or column, changing a column's type,
or adding a required column without a default. See the next section for why.

Whichever channel applies, the SQL in this skill is still the deliverable — a
chat-routed change is better served by handing Lovable the exact statements and
intent than by describing them loosely. Authoring precisely and routing
correctly are separate decisions.

## The backward-incompatible trap

`Execute backward incompatible database migrations` is a Cloud permission that
**defaults to Never allow**. While it's set that way, asking Lovable in chat to
drop or rename something does not fail loudly — Lovable quietly does something
else instead: it adds a new column or table, copies the data across, and
**leaves the old one in place**.

This is the single most common way a Lovable schema rots. The user believes
`full_name` was renamed to `display_name`; in fact both exist, both are being
written by different code paths, and one of them is slowly going stale.

So before any destructive change:

1. Say plainly that the permission gates it, and where it lives — Connectors →
   Cloud → "Manage my agent's permissions", or Account settings → Preferences →
   Agent permissions.
2. Recommend **Ask each time** over **Always allow**. Ask-each-time shows the
   SQL for review before it runs, which is the right amount of friction for an
   operation that can break a published app.
3. After any rename or drop that was requested earlier, **verify** the old
   object is actually gone rather than trusting that it happened.

Drafts have the same shape of limitation: a draft can add tables and columns but
cannot remove or rename them.

## Files Lovable owns

Do not hand-edit these. Lovable maintains them, and edits get overwritten or
desync the migration state:

- `drizzle/` — the whole directory
- `drizzle.config.ts`
- `drizzle/schema.ts`
- `drizzle/migrations/` (and `supabase/migrations/` on older projects)

The generated TypeScript types are also Lovable's output. Lovable's docs don't
name the file, so **locate it in the repo rather than guessing a path** — look
for a generated types file imported by the database client, and read its header
comment. Edit the code that *consumes* the types, never the generated file.

## Writing SQL for this database

Cloud runs Supabase's open-source stack, so the Postgres-side primitives behave
the way they do on Supabase: `auth.uid()`, `auth.role()`, RLS, and the
`authenticated` / `anon` roles. Treat that as the working assumption but
**verify before relying on anything exotic** — Lovable doesn't document its
Postgres surface, so extension availability (`pg_cron`, `pgvector`, `pg_net`) is
a question to answer with a query, not an assumption:

```sql
select extname, extversion from pg_extension order by extname;
```

### Make every statement re-runnable

The SQL editor has no migration history behind it, so a statement that half-ran
leaves no record. Write SQL that can be run twice without error:

```sql
-- additive, safe to re-run
alter table public.invoices
  add column if not exists status text not null default 'draft';

create index if not exists invoices_status_idx
  on public.invoices (status);

-- policies have no "if not exists" — drop first
drop policy if exists "invoices_select_own" on public.invoices;
create policy "invoices_select_own"
  on public.invoices for select
  to authenticated
  using (user_id = auth.uid());
```

### Adding a required column without breaking the app

Never `add column ... not null` with no default on a table that has rows or a
live writer. Three steps, each safe on its own:

```sql
-- 1. add nullable
alter table public.invoices add column if not exists currency text;
-- 2. backfill
update public.invoices set currency = 'USD' where currency is null;
-- 3. constrain, once the app writes it
alter table public.invoices alter column currency set not null;
alter table public.invoices alter column currency set default 'USD';
```

Step 3 is backward incompatible. It belongs in the chat, or behind the permission.

## RLS policies

Cloud turns RLS on automatically for tables holding user data and writes
starter policies. Two failure modes matter more than any other, and both are
invisible until someone looks:

**RLS enabled with no policy** means the table denies everything to normal
users — the app reads empty arrays and the bug looks like missing data. Find it:

```sql
select c.relname as table_name
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind = 'r'
  and c.relrowsecurity
  and not exists (
    select 1 from pg_policy p where p.polrelid = c.oid
  )
order by 1;
```

**A policy granted to `anon`** means unauthenticated visitors can read or write
it. Sometimes intended (a public listings table); usually not. Audit the roles
a policy applies to, not just its `using` clause:

```sql
select schemaname, tablename, policyname, cmd, roles, qual, with_check
from pg_policies
where schemaname = 'public'
order by tablename, policyname;
```

Rules worth holding to:

- **Name policies for what they allow**: `invoices_select_own`,
  `invoices_insert_own`. A policy called `Enable read access for all users` tells
  a future reader nothing and is usually wrong anyway.
- **One policy per command.** A single `for all` policy makes it impossible to
  let users read a row but not delete it, and that distinction is almost always
  wanted eventually.
- **`to authenticated` explicitly.** A policy with no role clause applies to
  every role including `anon`.
- **`insert` needs `with_check`, not `using`.** Writing `using` on an insert
  policy silently permits nothing — or everything, depending on the rest.
- **Match the owning column to reality.** `user_id = auth.uid()` only works if
  that column holds the auth user's id. Confirm the column before writing it.

Lovable's RLS view (More → Cloud → Database → RLS policies) is **read-only** —
useful for review, never for changes.

## Functions, triggers, and jobs

**Functions.** Pin `search_path` on every function you create. An unpinned
`security definer` function is a privilege-escalation path, because a caller can
manipulate the schema resolution order:

```sql
create or replace function public.touch_updated_at()
returns trigger
language plpgsql
security invoker
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;
```

Prefer `security invoker` and reach for `security definer` only when the
function genuinely must bypass RLS — and when it does, state in the response
what it bypasses and why. With `search_path = ''`, every reference inside the
body must be schema-qualified (`public.invoices`, not `invoices`).

**Triggers.** No `create trigger if not exists` exists; drop first:

```sql
drop trigger if exists invoices_touch_updated_at on public.invoices;
create trigger invoices_touch_updated_at
  before update on public.invoices
  for each row execute function public.touch_updated_at();
```

**Scheduled jobs.** Lovable surfaces these at More → Cloud → Jobs, which is
review-only: creating, rescheduling, and deleting happen through the chat or
SQL. The docs do **not** confirm the scheduler is `pg_cron`, so check before
writing cron SQL:

```sql
select extname from pg_extension where extname = 'pg_cron';
select jobid, schedule, jobname, active from cron.job order by jobid;
```

If `pg_cron` is present, schedule through it and give every job a name so it can
be found and replaced later. If it isn't, the chat is the only route — don't
invent a scheduling API.

Jobs consume Cloud run credits per execution, so when proposing a schedule, say
what the frequency costs in rough terms. Hourly when daily would do is a real
bill. Note also that a scheduled job keeps a project from auto-pausing.

## Verify, don't assume

Lovable's database views do not update live — the Refresh button is load-bearing,
and a user reporting "it didn't work" may be looking at a stale page. After any
change, confirm the state from the database itself rather than from the UI:

```sql
-- columns actually present
select column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_schema = 'public' and table_name = 'invoices'
order by ordinal_position;

-- policies actually present
select policyname, cmd, roles, qual, with_check
from pg_policies
where schemaname = 'public' and tablename = 'invoices';
```

For a rename or drop requested through the chat, verify the **absence** of the
old object. That's where the backward-incompatible default bites, and the only
way to catch it is to look.

## Keeping the app in step

A schema change isn't finished when the SQL succeeds. In order:

1. **Types.** A chat-driven change regenerates them. A SQL-editor change does
   not — so if a SQL-editor change did alter the type surface (it usually
   shouldn't; if it did, consider whether it belonged in the chat), ask Lovable
   in chat to regenerate.
2. **Queries.** New column, new select. Find every call site rather than the
   first one — a column added for one screen is usually wanted on two.
3. **Writers.** A column that is `not null` with no default needs every insert
   path updated, including edge functions and seed scripts.
4. **Edge functions.** Code edits sync through Git but **are not deployed** by
   the sync. Deployment is a chat request. Say so rather than leaving the user
   to discover that their pushed fix isn't live.

Never put a secret in a `VITE_`-prefixed variable — those are compiled into the
browser bundle. Service-role keys and API secrets belong in the project's
secrets store (More → Cloud → Secrets).

## Writing the chat prompt

When the chat is the right channel, the prompt is the deliverable, so make it
precise enough that Lovable can't interpret it loosely. State the table, the
exact column names and types, nullability, defaults, the RLS intent, and what
should happen to existing rows.

Weak: *"add a status to invoices"*

Strong:

```text
Add a column `status` to the `invoices` table: text, not null, default 'draft',
constrained to one of 'draft', 'sent', 'paid', 'void'. Backfill existing rows to
'draft'. Keep the existing RLS policies unchanged — users should still only see
invoices where user_id = auth.uid(). Regenerate the types and update the invoice
list and detail components to display the status.
```

For a destructive change, name it as such and say what you expect:

```text
Rename `invoices.full_name` to `customer_name`. This is a backward incompatible
migration — I have set "Execute backward incompatible database migrations" to
Ask each time, so show me the SQL. I want an actual rename, not a new column
alongside the old one. Update all code references and regenerate the types.
```

## Response shape

Lead with which channel the change belongs in and why, in one line — naming the
repo rule that decided it when there is one. Then the SQL or the prompt. Then
the verification query. Then anything the app needs.
Don't bury a backward-incompatible warning at the end — if the change is gated
by that permission, that's the first thing said.

If a request can't be done on Cloud at all — direct connections, sharing a
database between projects, restoring to an arbitrary point in time, retrieving
the password — say so immediately and give the closest real option. Backups are
daily snapshots retained roughly 14 days; restoring reverts the schema too and
discards everything created after the snapshot, so it's a last resort, not a
tool.
