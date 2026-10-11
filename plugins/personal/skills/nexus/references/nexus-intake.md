# NEXUS Intake Module
*Load during startup Phase 2 — extracting all existing project state into the backlog.*

---

## Purpose

Before NEXUS can manage a project, it needs to understand what already exists.
Intake converts raw project knowledge from Chats, documents, and the user's brain
into structured backlog items that NEXUS can track, prioritize, and assign.

Run intake once at first startup. Re-run with `nexus intake` when major new work is scoped.

---

## Intake Sources (in order of priority)

### Source 1 — Existing Drive documents
Scan these locations for existing project artifacts:
```
$ORCH/../               ← parent project folder
$ORCH/../docs/          ← documentation
$ORCH/../code/          ← code files (signals what exists)
$ORCH/sessions/         ← previous NEXUS sessions
```

Look for: existing task lists, architecture docs, README files,
previous sprint boards, decision logs, and any `.md` files describing work.

### Source 2 — User brain dump
Ask the user directly:

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS INTAKE — Project Knowledge Capture                ║
╠══════════════════════════════════════════════════════════╣
║  I need to understand your project to build the backlog. ║
║  Please answer as much or as little as you know.         ║
╚══════════════════════════════════════════════════════════╝

1. What is this platform/product? (1-3 sentences)

2. What has already been built or decided?
   (paste any notes, list features, whatever you have)

3. What is currently in progress?
   (things being worked on right now)

4. What is next on the agenda?
   (what you planned to do this week/sprint)

5. What is blocked or waiting?
   (anything stuck waiting for a decision or dependency)

6. What are the biggest open questions?
   (things not yet decided that affect direction)

7. Who (which Chat) owns which area?
   (e.g. Chat-Arch owns system design, Chat-Backend owns API)
```

### Source 3 — Chat session summaries
Ask the user to paste any key outputs from existing Chat sessions:
- Architecture decisions
- API designs
- Data models
- Feature lists
- Outstanding questions

---

## Extraction Rules

When processing any input, extract every item that is:

| Type | Signal words | Backlog status |
|------|-------------|----------------|
| **Feature** | "need to build", "should have", "the app does X" | `BACKLOG` |
| **Task** | "working on", "in progress", "doing X" | `IN PROGRESS` |
| **Decision** | "decided to", "agreed that", "using X for Y" | Log to `decisions-log.md` |
| **Blocker** | "blocked on", "waiting for", "can't proceed until" | `BLOCKED` |
| **Question** | "not sure", "TBD", "need to decide" | `OPEN QUESTION` |
| **Done** | "already built", "completed", "finished" | `DONE` |

---

## Backlog Item Format

Every extracted item becomes a backlog entry:

```markdown
## TASK-[NNNN] — [Short Title]
Status: BACKLOG | IN PROGRESS | BLOCKED | DONE | OPEN QUESTION
Type: feature | task | bug | decision | question
Priority: critical | high | normal | low
Area: [which Chat owns this domain]
Assigned-to: [Cowork name, or UNASSIGNED]
Depends-on: [TASK-IDs or NONE]
Blocks: [TASK-IDs or NONE]
Source: intake | [chat name] | manual
Created: [datetime]
Updated: [datetime]

### Description
[What needs to be done — plain English]

### Acceptance Criteria
[How we know this is done — if known]

### Notes
[Any context, decisions, constraints]
```

---

## Post-Intake Actions

After extracting all items:

**1. Write backlog.md**
Write all extracted tasks to `$ORCH/backlog.md` using the full backlog format
(see `nexus-backlog.md` for the complete file structure).

**2. Write decisions-log.md**
Write all extracted decisions to `$ORCH/decisions-log.md`.

**3. Write risk-register.md**
Write all extracted blockers and open questions to `$ORCH/risk-register.md`.

**4. Print intake summary:**
```
╔══════════════════════════════════════════════════════════╗
║  NEXUS INTAKE COMPLETE                                   ║
╠══════════════════════════════════════════════════════════╣
║  Tasks extracted:      [n]                               ║
║    In Progress:        [n]                               ║
║    Backlog:            [n]                               ║
║    Blocked:            [n]                               ║
║    Done:               [n]                               ║
║  Decisions logged:     [n]                               ║
║  Open questions:       [n]                               ║
║  Risks identified:     [n]                               ║
╠══════════════════════════════════════════════════════════╣
║  Backlog saved to: $ORCH/backlog.md                      ║
║  Ready for sprint planning. Type: nexus plan             ║
╚══════════════════════════════════════════════════════════╝
```

**5. Ask if sprint planning should run now:**
```
Would you like to run sprint planning now to assign
the highest priority tasks to your Cowork sessions?
Type YES or 'nexus plan' when ready.
```
