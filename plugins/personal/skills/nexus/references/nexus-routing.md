# NEXUS Routing Engine
*Load when a task arrives or needs to be routed.*

---

## Monitoring Loop

NEXUS runs a continuous monitoring cycle using `jabri-mcp: run_shell`:

```bash
# Check all inbox folders for new task files
ls "$ORCH/inbox/[chat-name]/" 2>/dev/null
```

**Cycle frequency:**
- Default: every 60 seconds
- When active tasks exist: every 30 seconds
- When idle (no tasks for 10+ minutes): every 120 seconds

At each cycle:
1. Scan all registered Chat inbox folders
2. Scan all registered Cowork outbox folders (for completed results)
3. Process any new files found (oldest first)
4. Update `status.md`
5. Log the cycle

---

## Task File Detection

A file is a **new task** if:
- It exists in `$ORCH/inbox/[chat-name]/`
- Its filename ends in `.md` or `.txt`
- It has NOT been logged as processed in `$ORCH/log/processed.log`

A file is a **completed result** if:
- It exists in `$ORCH/cowork/[cowork-name]/results/`
- Its filename ends in `.md` or `.txt`
- It has NOT been logged as processed

---

## Task File Format

Read `references/nexus-formats.md` for the full schema.

Minimum required fields NEXUS reads from every task file:
```
From: [Chat or Cowork name]
To: [destination — can be a Chat, Cowork, or "NEXUS"]
Priority: [critical | high | normal | low]
Type: [task | result | data | decision-request]
```

If any required field is missing → write `$ORCH/decisions/MALFORMED-[filename].md` and pause.

---

## Routing Decision Tree

```
New file detected
       │
       ▼
Read header fields
       │
       ├── Type: task ──────────────────────────────────────────┐
       │                                                         │
       │   Check escalation rules (nexus-escalation.md)         │
       │          │                                              │
       │          ├── ESCALATE → write decisions/ file, PAUSE   │
       │          │                                              │
       │          └── PROCEED                                    │
       │                  │                                      │
       │           Look up routing-table.md                      │
       │                  │                                      │
       │          ┌───────┴────────┐                             │
       │          │                │                             │
       │     To: Cowork       To: Chat                          │
       │          │                │                             │
       │   Write to            Write to                         │
       │   cowork/[name]/      outbox/[chat-name]/              │
       │   instructions/       [file]                           │
       │                                                         │
       ├── Type: result ─────────────────────────────────────────┤
       │                                                         │
       │   Read "For:" field → find destination Chat             │
       │   Write result to outbox/[chat-name]/                   │
       │   Log delivery                                          │
       │                                                         │
       ├── Type: data ───────────────────────────────────────────┤
       │                                                         │
       │   Read "To:" field → could be Chat or Cowork            │
       │   Write to their inbox or cowork folder                 │
       │   Log relay                                             │
       │                                                         │
       └── Type: decision-request ──────────────────────────────┘
                                                         │
                                               Write to decisions/
                                               Update status.md
                                               PAUSE + notify user
```

---

## Routing Table Format

`$ORCH/routing-table.md` structure:

```markdown
# NEXUS Routing Table
Session: [ID]
Last updated: [datetime]

## Chat Sessions
| Name | Role | Inbox Path | Routes To |
|------|------|------------|-----------|
| Chat-Arch | Architecture | inbox/chat-arch/ | Cowork-1, Cowork-2 |
| Chat-Backend | Backend API | inbox/chat-backend/ | Cowork-1 |

## Cowork Sessions
| Name | Capability | Work Path | Results Path |
|------|------------|-----------|--------------|
| Cowork-1 | Code + SQL | cowork/cowork-1/instructions/ | cowork/cowork-1/results/ |
| Cowork-2 | Infra + Shell | cowork/cowork-2/instructions/ | cowork/cowork-2/results/ |

## Chat-to-Chat Routes
| From | To | Trigger |
|------|----|---------|
| Chat-Arch | Chat-Backend | When output tagged: needs-backend-review |

## Default Cowork
Cowork-1

## Escalation Triggers
[copied from interview answers]
```

---

## Writing Instructions to Cowork

When routing a task to a Cowork session, NEXUS writes a file to:
`$ORCH/cowork/[cowork-name]/instructions/[task-id].md`

NEXUS adds a routing header to the original task:
```markdown
---
NEXUS-ROUTED: true
Routed-by: [NEXUS session ID]
Routed-at: [datetime]
From-chat: [source chat name]
Return-to: [destination chat name for results]
Task-ID: [unique ID]
---
[original task content below]
```

---

## Delivering Results to Chat

When a Cowork result arrives, NEXUS:
1. Reads the `Return-to:` field from the result file header
2. Writes the result to `$ORCH/outbox/[chat-name]/[task-id]-result.md`
3. Logs the delivery
4. Updates `status.md` (decrements active task count)

---

## Stall Detection

At every cycle, check: `$ORCH/log/active-tasks.md`

For each active task:
- Calculate: `now - routed_at`
- If elapsed > stall threshold (from interview) → write `$ORCH/decisions/STALLED-[task-id].md`
- Print alert in NEXUS console
- Do NOT cancel the task — wait for user instruction

---

## Status File Format

`$ORCH/status.md` updated every cycle:

```markdown
# NEXUS Status
Session: [ID]
Mode: RUNNING | WAITING | IDLE | PAUSED
Last cycle: [datetime]
Next cycle: [datetime]

Active tasks: [n]
Completed today: [n]
Pending decisions: [n]
Stalled tasks: [n]

## Active Tasks
| Task ID | From | To | Routed At | Elapsed |
|---------|------|----|-----------|---------|

## Pending Decisions
| File | Reason | Since |
|------|--------|-------|
```
