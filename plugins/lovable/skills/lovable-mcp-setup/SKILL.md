---
name: lovable-mcp-setup
description: Connect Claude Code (or another agent) to the Lovable MCP server so it can work on Lovable projects directly — reading files and diffs, checking analytics, and running SQL against a Lovable Cloud database via query_database. Use when setting up the Lovable connection for the first time, when a Lovable tool call fails with an auth or permission error, when /mcp shows lovable as disconnected, when deciding whether a Lovable action costs credits, or when you need the project_id for a Lovable project. Also use before any first use of query_database, since the safety rules live here.
---

# Lovable MCP server: setup and safe use

Lovable runs an MCP server at `https://mcp.lovable.dev`, available on all plans.
It is what lets an agent act on Lovable projects without going through the
Lovable chat — which matters because chat messages are billed Build-mode
requests and most tool calls are not.

For database work specifically, read `lovabledatabase` as well. This skill is
the connection, the identifiers, and the guardrails; that one is the SQL.

## Connect

```bash
claude mcp add --transport http lovable "https://mcp.lovable.dev"
```

Or, for slash commands alongside the tools:

```bash
/plugin install lovable@claude-plugins-official
```

**Auth is OAuth only** — there are no API keys. A browser window opens the first
time a Lovable tool runs. Verify with `/mcp`.

On an **Enterprise workspace**, an admin or owner must first enable
"Third-party MCP clients," and on SSO workspaces with session limits the client
must re-authenticate when the session expires. If a call fails with an auth or
permission error, check those two before assuming the server is down.

## Two front doors, and they are configured separately

Where the session runs decides how Lovable gets connected, and the wrong
instruction wastes real time:

- **Terminal Claude Code** — `claude mcp add --transport http lovable
  "https://mcp.lovable.dev"`, or `/plugin install lovable@claude-plugins-official`.
- **A cloud session (claude.ai / Cowork)** — the CLI commands do nothing here.
  Add it as a **custom connector** at `claude.ai/customize/connectors` with the
  URL `https://mcp.lovable.dev`, and approve the sign-in in the browser window
  that opens.

Either way: **a session loads connectors when it starts.** Adding the connector
mid-session does not give the running session the tools, and no amount of
retrying changes that — the correct next step is always to start a fresh session.
Say that plainly rather than attempting a workaround.

The same split applies to the skills themselves. A cloud session gets skills
from the claude.ai account, not from a repo — so a repo that has been updated can
sit alongside a stale account copy, and the session will follow the stale one. If
a session's behaviour doesn't match the current `SKILL.md`, suspect that before
suspecting the file. The fix is either to update the account copy or to have the
session read the file from the repo directly.

## Know which project you are touching

**A connected client can reach every project the account can access**, not just
the one in front of you. The `project_id` parameter is the only thing standing
between a change to the right database and a change to someone else's app.

So: resolve it **once**, explicitly, at the start of a session —

```
list_projects           → find the project, note its id
get_project(project_id) → confirm name, editor URL, preview URL
```

— then reuse that id verbatim. Never infer it from conversation, and never carry
one across sessions from memory. If the id in hand doesn't match the project the
user just named, stop and re-resolve.

## What the tools cover

- **Identity / workspaces:** `get_me`, `list_workspaces`, `get_workspace`
- **Projects:** `list_projects`, `get_project`, `create_project`,
  `deploy_project`, `remix_project`, `set_project_visibility`,
  `set_folder_visibility`, `move_projects_to_folder`, `list_template_projects`,
  `list_design_systems`
- **Agent:** `send_message`, `get_message`, `list_messages`
- **Knowledge / skills:** `get_workspace_knowledge`, `set_workspace_knowledge`,
  `get_project_knowledge`, `set_project_knowledge`, `list_workspace_skills`,
  `get_workspace_skill`, `create_workspace_skill`, `update_workspace_skill`,
  `delete_workspace_skill`
- **Code inspection:** `get_diff`, `list_files`, `read_file`, `list_edits`
- **Cloud database:** `get_database_status(project_id)`,
  `enable_database(project_id)`, `query_database(project_id, sql)`
- **Connectors:** `list_connectors`, `list_connections`,
  `list_custom_connectors`, `list_available_connectors`, `add_connector`,
  `remove_connector`
- **Analytics:** `get_project_analytics`, `get_project_analytics_trend`
- **Uploads:** `get_file_upload_url`

`mcp.lovable.dev/skill.md` is the authoritative parameter reference — consult it
rather than guessing a signature.

## Cost

The FAQ says: "Standard Lovable credits apply to `create_project` and
`send_message` calls. Other tools are free." The warning shown before connecting
says: "Tool calls use real credits and edit real projects."

**These conflict, so don't state either as fact.** Work on the assumption that
`query_database` and the read tools are free and that `send_message` and
`create_project` are not — then confirm against **More → Cloud → Usage** after
the first real session. If a user is managing credit spend, that check is worth
doing before a long run of tool calls, not after.

Note that `send_message` is the chat — using it through MCP is still a billed
Build-mode request. MCP changes the interface, not the pricing.

## Make the dangerous tools unreachable

Several tools act irreversibly on live projects, and a rule written in a skill
is guidance a future session can reason around. A permission rule is not. Prefer
the rule.

MCP tools are addressed as `mcp__<server>__<tool>` — and **`<server>` is whatever
*this client* named the connection, which is not the same everywhere:**

| How it was connected | Server segment | Example |
|---|---|---|
| `claude mcp add … lovable …` | `lovable` | `mcp__lovable__query_database` |
| claude.ai custom connector | `Lovable_MCP` | `mcp__Lovable_MCP__query_database` |

A rule written for the wrong segment **matches nothing and silently protects
nothing** — the only symptom is a startup warning that is easy to miss. So read
the real names out of the session with `/permissions` or `/mcp` and write the
rules from those. Never copy the example below without checking the prefix; it
uses the terminal spelling.

```json
{
  "permissions": {
    "deny": [
      "mcp__lovable__deploy_project",
      "mcp__lovable__remix_project",
      "mcp__lovable__set_project_visibility",
      "mcp__lovable__delete_workspace_skill"
    ],
    "ask": [
      "mcp__lovable__query_database",
      "mcp__lovable__send_message"
    ]
  }
}
```

Why these:

- **`deploy_project` denied.** Publishing is the owner's decision. A bare tool
  name in `deny` removes the tool from the model's context entirely, so it isn't
  declined — it is never considered.
- **`remix_project`, `set_project_visibility`, `delete_workspace_skill` denied.**
  Each is irreversible or externally visible, and none belongs in a database
  workflow.
- **`query_database` on `ask`.** It runs with full database permissions and no
  documented gating, so a prompt is the only thing standing between a generated
  `DROP` and an executed one.
- **`send_message` on `ask`.** It is the one database-workflow call that costs
  credits; a prompt makes the spend deliberate.

Rules are evaluated **deny → ask → allow**, first match wins, and specificity
does not change that order — so a `deny` cannot be carved out by a later
`allow`. Wildcards work: `mcp__<server>__*` covers the whole server, `mcp__*`
every MCP tool. A rule naming a tool that doesn't exist produces a startup
warning, which is how typos surface — so confirm the real names with
`/permissions` or `/mcp` before writing them, rather than trusting this list.

Parameter-level matching is not available for MCP tools in settings files; a rule
written with parentheses is skipped when the file loads. There is also no
documented per-tool *allowlist* for a locally added server — to expose only a few
tools you must deny the rest explicitly, or run in a mode that denies anything
not pre-approved.

## Rules that keep this safe

Several tools act irreversibly on live projects, and the documentation describes
no confirmation prompts, no destructive-statement gating, and no limits on
anything. The caution has to come from here.

- **`query_database` runs with full database permissions.** A `DROP` executes
  immediately and silently. Read before writing, one logical change per call,
  wrap multi-statement changes in `begin; … commit;`, and state the rollback
  before running anything destructive. If there is no rollback, stop and ask —
  Cloud backups are daily snapshots kept roughly 14 days, and restoring reverts
  the schema and discards everything since.
- **No documented limits.** Nothing on query size, timeout, row count, or result
  truncation. Chunk large work; never assume a long result came back whole.
- **`deploy_project` publishes to a real URL.** It is refused while a project has
  unresolved critical security findings — treat that refusal as information, not
  an obstacle to route around. Free and Pro published apps are reachable by
  anyone with the link.
- **`set_workspace_knowledge` and `set_project_knowledge` replace content
  entirely.** Read the current value first, or you will silently delete someone
  else's context.
- **`delete_workspace_skill` cannot be undone** except by recreating the skill.
- **`add_connector` only returns a dashboard URL** — connectors are actually
  added in the Lovable UI, so don't report one as connected.
- **Analytics tools only work for published projects.**
- **`enable_database` takes 30–60 seconds** and is one-time; check
  `get_database_status` first rather than calling it speculatively.

## When something fails

Work through this in order rather than retrying:

1. `/mcp` — is `lovable` connected at all?
2. Auth error → the OAuth session expired, or Enterprise hasn't enabled
   third-party MCP clients.
3. Permission error → the server inherits the user's Lovable permissions and adds
   nothing; the account may simply lack access to that project.
4. Wrong or empty results → re-resolve `project_id` with `list_projects`. An id
   that belongs to a different project returns plausible-looking nonsense.
5. `query_database` error → read the Postgres error literally before rewriting
   the SQL; it usually names the real problem.

If two or three attempts don't resolve it, say what was tried and what the error
was, and ask — rather than escalating to broader or more destructive calls.
