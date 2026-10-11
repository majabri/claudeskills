# NEXUS Backlog Module
*Load when managing the master task list, prioritizing work, or reading backlog state.*

---

## The Backlog is Sacred

`$ORCH/backlog.md` is the single source of truth for all work in the project.

Rules:
- Every task that exists must be in the backlog
- Every task in the backlog has a unique TASK-ID
- No task is routed to a Cowork unless it exists in the backlog first
- When a Chat drops a new task file, NEXUS adds it to the backlog before routing
- The backlog is never deleted — completed tasks are archived, not removed

---

## Backlog File Structure

`$ORCH/backlog.md`:

```markdown
# Project Backlog
Project: [name]
Last updated: [datetime]
Total tasks: [n]
Open: [n] | In Progress: [n] | Blocked: [n] | Done: [n]

---

## 🔴 CRITICAL

[TASK entries with Priority: critical]

---

## 🟠 HIGH

[TASK entries with Priority: high]

---

## 🟡 NORMAL

[TASK entries with Priority: normal]

---

## 🟢 LOW

[TASK entries with Priority: low]

---

## ✅ DONE (last 7 days)

[Recently completed tasks — older tasks move to archive/]

---

## ❓ OPEN QUESTIONS

[Items that are blockers pending a decision]
```

---

## Task Status Lifecycle

```
BACKLOG → IN PROGRESS → DONE
              │
              ├── BLOCKED (waiting on dependency or decision)
              │       └── → IN PROGRESS (when unblocked)
              │
              └── CANCELLED (user decision)
```

Status values:
- `BACKLOG` — not yet started, queued
- `IN PROGRESS` — assigned to a Cowork, work underway
- `BLOCKED` — cannot proceed (dependency or decision needed)
- `REVIEW` — Cowork returned result, Chat needs to review
- `DONE` — accepted and complete
- `CANCELLED` — deliberately removed from scope

---

## Priority Rules

NEXUS uses these rules to set and adjust priority:

| Rule | Priority set to |
|------|----------------|
| Explicitly marked `Priority: critical` by a Chat | CRITICAL |
| Blocks 3 or more other tasks | HIGH |
| In current sprint and not started | HIGH |
| Dependency of an IN PROGRESS task | HIGH (auto-elevated) |
| Normal backlog item | NORMAL |
| Nice-to-have, no dependencies | LOW |
| Stalled > stall threshold | Elevated one level automatically |

NEXUS may auto-elevate priority but always logs the reason.
NEXUS never auto-reduces priority — only Amir or a Chat can lower priority.

---

## Adding a Task to the Backlog

Triggered when:
- A Chat drops a new file in `$ORCH/inbox/[chat-name]/`
- User types `nexus add task`
- Intake process extracts a task

Steps:
1. Read the task file or user input
2. Assign next TASK-ID (read from `$ORCH/log/task-counter.txt`, increment, write back)
3. Create backlog entry using the task format (see `nexus-formats.md`)
4. Insert into backlog.md under the correct priority section
5. Update the counts in the backlog header
6. Log: `[datetime] INFO BACKLOG-ADD TASK-[id] — [title] — Priority: [p]`
7. Write ACK to `$ORCH/outbox/[source-chat]/ACK-[TASK-ID].md`

---

## Updating a Task in the Backlog

When status changes (routed, result received, blocked, done):
1. Find the task entry in backlog.md by TASK-ID
2. Update the Status field
3. Update the Updated field
4. If moving to DONE: move entry to the DONE section
5. Update header counts
6. Log the status change

---

## Dependency Management

Before routing any task, check its `Depends-on:` field.

```
Task has Depends-on: TASK-0001
          │
          ▼
Look up TASK-0001 in backlog.md
          │
          ├── Status: DONE → proceed, route this task
          │
          ├── Status: IN PROGRESS → hold this task
          │       Write to BLOCKED status
          │       Log: "TASK-[id] blocked — waiting for TASK-0001"
          │
          └── Status: BACKLOG → hold this task
                  Elevate TASK-0001 priority to HIGH
                  Log: "TASK-0001 elevated — blocks TASK-[id]"
```

When a task moves to DONE, NEXUS checks `Blocks:` field
and automatically un-blocks all dependent tasks, elevating them to HIGH priority.

---

## Backlog Grooming (run during `nexus plan`)

Before sprint planning, NEXUS does a quick backlog health check:

1. **Orphan check** — tasks with no description or acceptance criteria → flag for Chat
2. **Stale check** — tasks IN PROGRESS for > 2× stall threshold → flag as stalled
3. **Dependency check** — tasks whose dependencies are CANCELLED → flag for re-scoping
4. **Priority check** — tasks blocking others but still LOW priority → auto-elevate
5. **Unassigned check** — IN PROGRESS tasks with no Cowork assigned → flag

Print grooming report before sprint planning begins.

---

## Archiving

Completed tasks older than 7 days move from backlog.md to `$ORCH/archive/backlog-archive-[month].md`.

This keeps backlog.md readable without losing history.
Archive on: `nexus eod` if DONE section has items older than 7 days.
