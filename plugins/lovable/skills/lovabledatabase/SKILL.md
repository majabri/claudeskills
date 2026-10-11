---
name: lovabledatabase
description: Do database work on a Lovable Cloud project through the Lovable MCP server — read-backs, live reads and diagnostics directly via query_database, and every schema change as a committed migration file that Lovable applies. Use this whenever work touches a Lovable app's database: adding or changing tables, columns, RLS policies, grants, functions, triggers, indexes or scheduled jobs, investigating a query that returns nothing or everything, or deciding which channel a change belongs in. The governing rule is replay — the repo must rebuild from supabase/migrations/ alone, so DDL never goes through query_database under a ledger rule, however convenient that would be. Use it even when the request sounds like plain SQL ("add a status column", "why can users see each other's rows").
---

# Lovable Cloud: database work

## The three channels, and what each one actually does

Lovable Cloud is managed Postgres on Supabase's open-source stack. It exposes
**no connection string and no retrievable password**, so `psql`, an ORM, a
Supabase MCP server, or anything else expecting a DSN cannot reach it. That
limit is real and permanent.

What *can* reach it:

| Channel | Cost | Writes migration file | Regenerates `types.ts` | Driven by |
|---|---|---|---|---|
| **MCP `query_database`** | free per Lovable's FAQ (verify — see below) | **no** | **no** | an agent, directly |
| **SQL editor** (More → Cloud → SQL editor) | free | **no** | **no** | a human, by paste |
| **Lovable chat** | **billed per Build-mode request** | yes | yes | Lovable's agent |

The whole shape of this skill follows from that table. The MCP server removes
the cost and the copy-paste, but it does **not** remove the bookkeeping: only
the chat produces a Drizzle migration copy, a journal entry, and regenerated
types. Treating `query_database` as a full replacement for the chat is the
central mistake to avoid, and most of this skill is about the gap it leaves.

### Connecting (one-time)

```bash
claude mcp add --transport http lovable "https://mcp.lovable.dev"
```

OAuth only — no API keys. A browser window opens the first time a Lovable tool
runs. Verify with `/mcp`. On an Enterprise workspace an admin must first enable
"Third-party MCP clients."

The three database tools, with their real parameters:

- `get_database_status(project_id)` — is Cloud provisioned
- `enable_database(project_id)` — provision it, 30–60 seconds, one-time
- `query_database(project_id, sql)` — "Execute SQL (SELECT, INSERT, UPDATE,
  DELETE, DDL)"

### What the docs do not promise, and you must not assume

Be skeptical here; the absence of documentation is itself the finding:

- **Credits.** The FAQ says "Standard Lovable credits apply to `create_project`
  and `send_message` calls. Other tools are free." But the pre-connection
  warning says "Tool calls use real credits and edit real projects." These
  conflict. Treat `query_database` as free *provisionally*, and check **More →
  Cloud → Usage** after the first real session rather than trusting either line.
- **No safety rails are documented.** No confirmation prompt, no destructive-
  statement gating, no transaction wrapping. The SQL editor at least prompts on
  `DELETE`/`DROP`/`TRUNCATE`/`ALTER`/`UPDATE`; `query_database` is documented to
  run "with your full database permissions" and nothing more. Assume a `DROP`
  executes immediately and silently.
- **No limits are documented** — not query size, timeout, or row count, and
  nothing about result truncation. So chunk large work rather than discovering a
  limit mid-statement, and never assume a long result came back whole.
- **Scope is the whole account.** A connected client can reach **every project
  the account can access**, not just one. `project_id` is the only thing
  separating a change to the right database from a change to the wrong one.

## Rules for driving `query_database`

These exist because the tool has no guardrails of its own.

1. **Pin `project_id` explicitly on every call**, resolved once at the start of
   the session via `list_projects` and then reused verbatim. Never infer it from
   context or carry it across sessions from memory. One wrong id is a change
   applied to a different app.
2. **Read before you write.** Confirm the object exists and has the shape you
   think it does before altering it. The cost of a `SELECT` is nothing; the cost
   of an `ALTER` against a mistaken assumption is a broken published app.
3. **One logical change per call**, so a failure is attributable. Batching four
   statements and getting one error tells you little about the other three.
4. **Wrap multi-statement changes in an explicit transaction** so a partial
   failure doesn't leave half a change applied:

   ```sql
   begin;
     alter table public.invoices add column if not exists currency text;
     update public.invoices set currency = 'USD' where currency is null;
   commit;
   ```

   DDL is transactional in Postgres, which makes this genuinely useful rather
   than cosmetic — though note `create index concurrently` cannot run inside a
   transaction.
5. **State the rollback before running anything destructive**, in the response,
   as a statement that can be pasted. If you cannot write one — a dropped column
   with data in it, a `TRUNCATE` — say so and stop: Cloud backups are daily
   snapshots retained roughly 14 days, restoring reverts the schema too and
   discards everything after the snapshot. That is not a rollback.
6. **Verify from the database, not from the call returning cleanly.** The
   verification queries below are part of the change, not an optional extra.
7. **Never read or write `auth.users` directly**, and never move secrets through
   SQL. Secrets belong in More → Cloud → Secrets.

## The repo's own rules outrank everything above

A direct SQL channel makes it *easier* to desync a repo, not harder. Before any
change, find out whether the repo has a migration discipline — if it does, that
discipline wins. Check, in this order:

1. `CLAUDE.md` and any `docs/` or ADR file describing database process.
2. Tests that read the migration directory. A file like `appliedOrder.test.ts`
   or `appliedLedger.ts` means the committed migration copy is being treated as
   the **authoritative ledger of what has been applied**.
3. Any queue or hand-off convention — an "Awaiting Lovable" section, a paste
   block, a migration checklist.

A repo with no such convention falls through to the plain guidance below.

### The source-first ledger pattern

Some repos run a stricter discipline than Lovable requires, because Lovable's
own behaviour isn't trustworthy enough alone. **Re-read `CLAUDE.md` for the
authoritative wording** — the following is the pattern, and the repo's copy wins:

- **Two directories, two jobs.** `supabase/migrations/`
  (`<14-digit-timestamp>_<name>.sql`) holds the **source of truth**, authored and
  committed by hand. `drizzle/migrations/` (`NNNN_<name>.sql`) plus
  `drizzle/migrations/meta/_journal.json` is **Lovable's ledger of what it
  actually applied**, written only by Lovable. Never hand-edit the ledger.
- **Matching is normalized, not byte-for-byte.** Don't call it byte-for-byte.
  The comparison strips `--` line comments and collapses whitespace to single
  spaces. Two consequences people get wrong:
  - `/* … */` block comments are **not** stripped, so a copy differing only in a
    block comment **fails**. Keep block comments out of migration SQL.
  - A `--` inside a string literal is cut too. Harmless for matching, but it
    means comment text is never trustworthy as content.
- **Copies match by content, not filename.** The Drizzle copy
  `0065_stock_intel_signed.sql` is recognised as the source
  `20261011100000_stock_intel_signed.sql` because the normalized text matches.
  Each copy must map to exactly one committed source.
- **A copy with no committed source fails the build, and the fix is to commit
  the source — never to loosen the test.**
- **Order of operations:** commit the source file → add the queue row → ask
  Lovable to apply → Lovable commits its ledger copy and journal entry →
  `types.ts` is regenerated.
- **The ledger has a floor.** Sources older than the timestamp behind Drizzle
  `0000` predate the ledger and are treated as applied. Don't reconcile them.
- **No gaps.** A committed migration must not sit unapplied while a newer one is
  applied. This fails on the main branch, not only on a PR — and it is the check
  that catches an unapplied migration adding rows or functions.
- **The forward-dependency check is narrower than it sounds.** It catches only an
  applied migration referencing a **table** an unapplied file creates. Everything
  else falls to the gap check.
- **Every new migration needs its queue row**, or the PR fails. **Stale rows are
  fine** — a row for an already-applied migration is allowed so Lovable's own
  commit doesn't redden main. It is removed in the PR that verifies the apply.
- **Audit Lovable's own merge commits.** Lovable should only touch the ledger,
  `types.ts`, and lockfiles. A Lovable merge changing anything else has silently
  reverted someone's work — this has happened. Check the diff.
- **Lovable does not publish.** Applying a migration is not a deploy.

**The pinned journal exception.** The journal may legitimately lack an entry for
one specific copy, pinned by the test as the single allowed discrepancy. In this
repo that is `0012_goals_account.sql` — Lovable's journal skipped it when it was
applied, and the apply was verified at the time. **Do not "fix" the journal by
hand.** Adding the entry breaks the test, and hand-editing the ledger is
forbidden anyway. A careful reader will be tempted; say so before they are.

**The queue table.** Columns are `# | Migration | What it needs | Addendum`. The
parser recognises only `\d{14}_[a-z0-9_]+\.sql` filenames, and only between the
`## Awaiting Lovable` heading and the next `## ` heading — a name written any
other way, or placed outside that block, is invisible to it. The addendum lives
at `docs/implementation/LOVABLE-QUEUE-<date>-<name>.md`.

### Reconciling direct SQL with a ledger rule

This is the hard part, and `query_database` sharpens it rather than solving it.
A ledger test compares committed sources against Lovable's applied copies.
Direct SQL produces **no** applied copy. So:

- **Do not** commit a source file into the ledger directory for a change applied
  directly. A committed source with no applied copy is an unapplied migration,
  and the gap check fails — typically on main, not just a PR.
- **Do** record the SQL where the ledger parser does not read, so the change
  stays reproducible. A sibling directory and a short index is enough. What must
  not happen is the change existing only in the live database: then
  `supabase/migrations/` quietly stops describing the schema, a rebuild from
  scratch produces something different, and the next person to trust the
  migration history is misled.

**Where that sibling directory lives, and whether the repo wants one, is a
convention decision — not this skill's to make.** Propose it, name the test it
has to stay clear of, and get it into `CLAUDE.md` before relying on it.

## Routing: what goes where

The deciding question is **replay**, not convenience and not types. A repo under
a ledger rule must be able to rebuild its database from
`supabase/migrations/` alone, and both the replay and the ledger test read
**only those files**. Anything that exists solely in the live database is absent
from the rebuild — so a reconstructed database has different constraints,
different functions, and *different security posture* than production. A policy
that exists in production but not in the replay is the worst version of this,
because nothing fails loudly; the rebuilt database is simply more open.

That is a stronger constraint than the `types.ts` concern, and it covers more:

> **Under a ledger rule, every schema change is a committed
> `supabase/migrations/` file that Lovable applies. Never `query_database`.**

"Schema change" here means **all DDL** — not just tables and columns, but
policies, grants, functions, triggers, indexes, and enum values. The earlier
instinct that policies and functions are safe to apply directly because they
don't appear in `types.ts` is wrong: they don't desync the types, they desync
the replay, which matters more.

### What `query_database` is for

Everything that changes no schema and leaves nothing to reproduce:

- **Read-backs and verification** — the queries in this skill, run after an
  apply to confirm what actually landed
- **Live reads and diagnostics** — investigating a query that returns nothing,
  checking row counts, inspecting `pg_policies` or `information_schema`
- **Hand-fired runs** — invoking a job or endpoint once, on purpose, the way a
  scheduled run would have
- **Data-only corrections**, where the repo's convention allows them and no
  structure changes

This is the free, direct, no-transcription-error path, and it covers most of the
day-to-day work. It simply does not cover DDL.

### How a schema change gets applied

1. Author the SQL as a new `supabase/migrations/<timestamp>_<name>.sql` file and
   commit it. The file is the proposal.
2. Add its queue row.
3. Deliver the paste block. `send_message` can send it to Lovable directly
   rather than routing it through a human — which is the real convenience the MCP
   server buys here. **`send_message` is a billed Build-mode request**, unlike
   the read tools, so it is the one call worth being deliberate about.
4. Lovable applies it, commits its ledger copy and journal entry, and
   regenerates `types.ts`.
5. Read back with `query_database` and confirm.

### Never `deploy_project`

Publishing is the owner's decision, not an agent's, and applying a migration is
not a deploy. Don't call it, and don't offer to. Better than remembering: make
it unreachable with a permission rule — see `lovable-mcp-setup`.

### A repo with no ledger rule

Then the replay argument doesn't apply and the looser routing does: direct SQL
for anything outside the type surface, chat for tables, columns, enums and
column types, because only Lovable regenerates `types.ts`. Hand-editing that
file is possible via Git but it is a divergence waiting to happen, since Lovable
overwrites it on its next apply — if you do it anyway, say plainly that you did.
**Backward-incompatible changes still go through the chat either way** — see the
next section.

**The SQL editor is the human fallback**, not a third strategy: use it when the
MCP server isn't connected, or when someone wants to see the statement before it
runs. Under a ledger rule it is subject to exactly the same prohibition as
`query_database`, for the same reason.

## The backward-incompatible trap

`Execute backward incompatible database migrations` is a Cloud permission that
**defaults to Never allow**. While it is set that way, asking Lovable in chat to
drop or rename something does not fail loudly — Lovable quietly adds a new column
or table, copies the data, and **leaves the old one in place**. The user believes
`full_name` became `display_name`; in fact both exist, different code paths write
each, and one is going stale.

`query_database` bypasses this gate entirely — it has your full permissions and
no gating is documented. That is convenient and dangerous in equal measure, and
it is a second reason DDL doesn't belong there: the gate exists to make someone
look at a destructive migration first, and a direct call removes the only place
that happens. Before any destructive change:

1. Say what will be irreversibly lost, and give the rollback statement. If there
   isn't one, stop and ask.
2. For a rename, prefer the three-step additive path (below) over a bare
   `ALTER ... RENAME` when anything is reading the old name.
3. After any rename or drop requested earlier through the chat, **verify the old
   object is actually gone** rather than trusting it happened.

Drafts share the shape of this limitation: a draft can add tables and columns but
cannot remove or rename them.

## Files Lovable owns

Never hand-edit: `drizzle/`, `drizzle.config.ts`, `drizzle/schema.ts`,
`drizzle/migrations/`. The generated types file is also Lovable's output — its
path isn't documented, so **locate it in the repo** rather than guessing, and
edit the code that consumes it, not the file.

## Writing SQL for this database

Cloud runs Supabase's open-source stack, so `auth.uid()`, `auth.role()`, RLS and
the `authenticated` / `anon` roles behave as on Supabase. Verify anything exotic
rather than assuming — extension availability is a query, not a guess:

```sql
select extname, extversion from pg_extension order by extname;
```

### Make every statement re-runnable

There is no migration history behind direct SQL, so a half-run statement leaves
no record. Write SQL that survives being run twice:

```sql
alter table public.invoices
  add column if not exists status text not null default 'draft';

create index if not exists invoices_status_idx on public.invoices (status);

-- policies have no "if not exists" — drop first
drop policy if exists "invoices_select_own" on public.invoices;
create policy "invoices_select_own"
  on public.invoices for select
  to authenticated
  using (user_id = auth.uid());
```

### Adding a required column without breaking the app

Never `add column ... not null` with no default on a table with rows or a live
writer. Three steps, each safe alone:

```sql
alter table public.invoices add column if not exists currency text;
update public.invoices set currency = 'USD' where currency is null;
alter table public.invoices alter column currency set not null;
alter table public.invoices alter column currency set default 'USD';
```

The third step is backward incompatible — read that section first.

## RLS policies

Cloud enables RLS automatically for tables holding user data and writes starter
policies. Two failure modes matter more than any other, and both are invisible
until someone looks.

**RLS enabled with no policy** denies everything to normal users — the app reads
empty arrays and it looks like missing data:

```sql
select c.relname as table_name
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'r' and c.relrowsecurity
  and not exists (select 1 from pg_policy p where p.polrelid = c.oid)
order by 1;
```

**A policy granted to `anon`** means unauthenticated visitors can read or write
it. Sometimes intended, usually not — audit the roles, not just the `using`:

```sql
select schemaname, tablename, policyname, cmd, roles, qual, with_check
from pg_policies where schemaname = 'public' order by tablename, policyname;
```

Rules worth holding to:

- **Name policies for what they allow**: `invoices_select_own`. A policy called
  `Enable read access for all users` tells a reader nothing and is usually wrong.
- **One policy per command.** A single `for all` policy makes "read but not
  delete" impossible, and that distinction is always wanted eventually.
- **`to authenticated` explicitly** — no role clause means every role, `anon`
  included.
- **`insert` needs `with_check`, not `using`.** `using` on an insert policy
  silently permits nothing, or everything, depending on the rest.
- **Match the owning column to reality.** `user_id = auth.uid()` only works if
  that column holds the auth user's id. Confirm before writing it.

Lovable's RLS view (More → Cloud → Database → RLS policies) is **read-only** —
for review, never for changes.

## Functions, triggers, and jobs

**Functions.** Pin `search_path` on every function. An unpinned `security
definer` function is a privilege-escalation path:

```sql
create or replace function public.touch_updated_at()
returns trigger language plpgsql security invoker set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;
```

Prefer `security invoker`; reach for `security definer` only when the function
must bypass RLS, and when it does, say in the response what it bypasses and why.
With `search_path = ''`, every reference inside must be schema-qualified.

**Triggers.** No `create trigger if not exists`; drop first.

```sql
drop trigger if exists invoices_touch_updated_at on public.invoices;
create trigger invoices_touch_updated_at
  before update on public.invoices
  for each row execute function public.touch_updated_at();
```

**Scheduled jobs.** Lovable surfaces these at More → Cloud → Jobs, which is
review-only — creating, rescheduling and deleting happen through SQL or the chat.
The docs do **not** confirm the scheduler is `pg_cron`, so check:

```sql
select extname from pg_extension where extname = 'pg_cron';
select jobid, schedule, jobname, active from cron.job order by jobid;
```

If `pg_cron` is present, schedule through it and name every job so it can be
found and replaced. If it isn't, the chat is the only route — don't invent a
scheduling API. Jobs consume Cloud run credits per execution, so state roughly
what a proposed frequency costs; hourly when daily would do is a real bill. A
scheduled job also keeps a project from auto-pausing.

## Verify, don't assume

Lovable's database views do not update live — the Refresh button is load-bearing,
and a user reporting "it didn't work" may be looking at a stale page. Confirm
from the database itself:

```sql
select column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_schema = 'public' and table_name = 'invoices'
order by ordinal_position;

select policyname, cmd, roles, qual, with_check
from pg_policies where schemaname = 'public' and tablename = 'invoices';
```

For column-level grants use `has_column_privilege(...)` rather than inspecting
catalogs by hand — it answers the question actually being asked. For a rename or
drop, verify the **absence** of the old object.

## Keeping the app in step

A schema change isn't finished when the SQL succeeds:

1. **Types.** A chat-driven change regenerates them; a direct one does not. If a
   direct change touched the type surface, that was probably the wrong channel —
   say so, and either route it through the chat or state plainly that `types.ts`
   is now hand-maintained.
2. **Queries.** New column, new select. Find every call site, not the first.
3. **Writers.** A `not null` column with no default needs every insert path
   updated, edge functions and seeds included.
4. **Edge functions.** Code edits sync through Git but **are not deployed** by the
   sync. Deployment is a chat request. Say so rather than letting someone think
   their pushed fix is live.

Never put a secret in a `VITE_`-prefixed variable — those are compiled into the
browser bundle.

## Writing the chat prompt

When the chat is genuinely required, the prompt is the deliverable. State the
table, exact column names and types, nullability, defaults, RLS intent, and what
happens to existing rows.

Weak: *"add a status to invoices"*

Strong:

```text
Add a column `status` to the `invoices` table: text, not null, default 'draft',
constrained to one of 'draft', 'sent', 'paid', 'void'. Backfill existing rows to
'draft'. Keep the existing RLS policies unchanged — users should still only see
invoices where user_id = auth.uid(). Regenerate the types and update the invoice
list and detail components to display the status.
```

Under a ledger rule the paste block has five parts, in this order: the file to
apply, named exactly as the queue table names it, and where it goes in the order
(after which Drizzle index); one sentence on what it does and whether `types.ts`
changes; the read-backs from the addendum verbatim, each with its expected answer
in a comment; the rollback line at one-day recovery granularity; and the one
request — report the answers verbatim and the Drizzle index the copy received.

Three rules govern the block: **nothing else goes in it** (no history, no
"publish", no filename from memory — the queue table and addendum are the only
sources); **one block per queue row, in apply order**, leaving out any row whose
PR hasn't merged, since its source isn't on main for Lovable to copy; and **the
block ends the report** and is forwarded unedited.

## Response shape

Lead with the channel and why, in one line — naming the repo rule that decided
it when there is one, and when the answer is the chat, saying it will cost
credits and what forced it there. Then the SQL or the prompt. Then the
verification query. Then anything the app needs.

For a destructive change, the irreversible loss and the rollback go **first**,
not last.

If a request can't be done at all — a direct connection string, sharing one
database between projects, restoring to an arbitrary point in time, retrieving
the password — say so immediately and give the closest real option.
