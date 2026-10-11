# NEXUS Decomposition Module
*Load when a task is too large to route directly — break it into assignable subtasks.*

---

## When to Decompose

NEXUS decomposes a task when ANY of these are true:

| Signal | Example |
|--------|---------|
| Task description spans multiple domains | "Build the auth system" (schema + API + UI + tests) |
| Task would take a Cowork more than one work session | "Implement the entire dashboard" |
| Task contains the word "system", "module", "full", "complete", "entire" | "Build the full notifications system" |
| Task has no clear single Cowork owner | Routes to both Cowork-DB and Cowork-Code |
| Task has implicit sequential steps | "Design then build then test X" |
| Estimated complexity: EPIC | Chat marks it as an epic |

When in doubt — decompose. Small tasks are always better than large ones.

---

## Decomposition Protocol

### Step 1 — Classify the task

```
EPIC     — 5+ subtasks, spans multiple Coworks, multi-day
STORY    — 2-4 subtasks, one primary Cowork, single day
TASK     — single unit of work, one Cowork, few hours
SUBTASK  — smallest unit, part of a Story
```

Route TASKS and SUBTASKS directly.
Decompose EPICS and STORIES before routing.

### Step 2 — Identify domains

For each epic/story, identify which capability domains it touches:
- **Schema/Data** → Cowork-DB
- **API/Backend** → Cowork-Code (backend)
- **UI/Frontend** → Cowork-Code (frontend)
- **Infrastructure** → Cowork-Infra
- **Testing** → assigned to same Cowork as implementation
- **Documentation** → assigned to source Chat

### Step 3 — Identify sequence

Map the order tasks must happen:

```
Example: "Build user authentication"

TASK-0010  Design auth schema          (Cowork-DB)
    ↓ depends on nothing
TASK-0011  Write RLS policies          (Cowork-DB)    depends-on: TASK-0010
    ↓
TASK-0012  Build /auth/login endpoint  (Cowork-Code)  depends-on: TASK-0011
TASK-0013  Build /auth/me endpoint     (Cowork-Code)  depends-on: TASK-0011
    ↓
TASK-0014  Build JWT middleware        (Cowork-Code)  depends-on: TASK-0012
    ↓
TASK-0015  Write auth tests            (Cowork-Code)  depends-on: TASK-0014, TASK-0013
```

### Step 4 — Write decomposed tasks to backlog

For each subtask, create a full backlog entry.
Set the parent epic as `Parent: TASK-[epic-id]` in each subtask.
Set the epic status to `IN PROGRESS — decomposed into [n] subtasks`.

### Step 5 — Route the first available task(s)

Route all tasks with no unmet dependencies immediately.
Hold tasks with dependencies — they will be auto-released when predecessors complete.

---

## Decomposition Output Format

When NEXUS decomposes a task, print the breakdown:

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS DECOMPOSITION — TASK-0009                         ║
║  "Build user authentication"                             ║
╠══════════════════════════════════════════════════════════╣
║  Decomposed into 6 subtasks:                             ║
║                                                          ║
║  TASK-0010  Design auth schema          → Cowork-DB      ║
║  TASK-0011  Write RLS policies          → Cowork-DB      ║
║             (depends on: TASK-0010)                      ║
║  TASK-0012  Build /auth/login endpoint  → Cowork-Code    ║
║             (depends on: TASK-0011)                      ║
║  TASK-0013  Build /auth/me endpoint     → Cowork-Code    ║
║             (depends on: TASK-0011)                      ║
║  TASK-0014  Build JWT middleware        → Cowork-Code    ║
║             (depends on: TASK-0012)                      ║
║  TASK-0015  Write auth tests            → Cowork-Code    ║
║             (depends on: TASK-0013, TASK-0014)           ║
║                                                          ║
║  Routing now: TASK-0010 (no dependencies)                ║
║  Holding:     TASK-0011 through TASK-0015                ║
╚══════════════════════════════════════════════════════════╝
```

---

## Decomposition Questions to Ask the Chat

If the epic is ambiguous, NEXUS asks the source Chat (via their outbox):

```
From: NEXUS
To: [source chat]
Type: clarification-request
Subject: Decomposition questions for TASK-[id]

Before I break down "[task title]", I need to clarify:

1. [specific question about scope]
2. [specific question about technology choice if relevant]
3. [specific question about acceptance criteria]

Please reply in your inbox folder.
```

Do not decompose without enough information to get it right.
An ambiguous decomposition creates cascading problems downstream.

---

## Parent-Child Tracking

Epic entry in backlog.md:
```markdown
## TASK-0009 — Build User Authentication [EPIC]
Status: IN PROGRESS — decomposed
Type: epic
Subtasks: TASK-0010, TASK-0011, TASK-0012, TASK-0013, TASK-0014, TASK-0015
Progress: 0/6 complete
```

NEXUS updates the epic progress count each time a subtask moves to DONE.
When all subtasks are DONE, the epic automatically moves to DONE.
