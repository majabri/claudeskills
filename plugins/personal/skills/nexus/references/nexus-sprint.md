# NEXUS Sprint Module
*Load for sprint planning, board management, and capacity decisions.*

---

## Sprint Philosophy

A sprint is a focused window of work — typically 3-7 days for an AI-assisted build.
NEXUS runs lightweight sprints: enough structure to stay focused, not so much it slows things down.

---

## Sprint Board Structure

`$ORCH/sprint-board.md`:

```markdown
# Sprint Board
Sprint: [number] — [name]
Started: [date]  |  Target end: [date]
Goal: [one sentence describing what this sprint delivers]

Last updated: [datetime]

---

## 🔵 TODO (committed to this sprint)
| Task ID | Title | Assigned To | Priority | Est. |
|---------|-------|-------------|----------|------|
| TASK-0010 | Design auth schema | Cowork-DB | HIGH | S |

---

## 🟡 IN PROGRESS
| Task ID | Title | Assigned To | Started | Elapsed |
|---------|-------|-------------|---------|---------|
| TASK-0008 | Build nav component | Cowork-Code | 09:00 | 2h |

---

## 🔴 BLOCKED
| Task ID | Title | Blocked By | Since |
|---------|-------|-----------|-------|
| TASK-0011 | Write RLS policies | Waiting: TASK-0010 | 10:00 |

---

## ✅ DONE THIS SPRINT
| Task ID | Title | Completed | Cowork |
|---------|-------|-----------|--------|
| TASK-0007 | DB schema v1 | 08:45 | Cowork-DB |

---

## 📊 Sprint Health
Committed: [n] tasks
Done: [n] | In Progress: [n] | Blocked: [n] | Not Started: [n]
Completion rate: [n]%
On track: YES / AT RISK / OFF TRACK
```

---

## Sprint Planning Protocol

Run when user types `nexus plan` or NEXUS suggests it after intake.

### Step 1 — Review current backlog health
Load `nexus-backlog.md` → run grooming check first.

### Step 2 — Set sprint goal
Ask: *"What is the primary goal for this sprint? What should be working/done at the end?"*

### Step 3 — Determine capacity
For each registered Cowork session, ask:
- Is this Cowork available this sprint?
- Any known constraints (partial availability, specific focus area)?

Default capacity assumption: each Cowork can handle 3-5 NORMAL tasks per sprint.

### Step 4 — Select sprint tasks

Pull from backlog in this order:
1. CRITICAL priority (all of them, regardless of capacity)
2. HIGH priority with no unmet dependencies
3. IN PROGRESS tasks that carry over from previous sprint
4. NORMAL priority — fill remaining capacity

For each candidate task:
- Check dependencies — only select if dependencies are DONE or also in this sprint
- Check Cowork assignment — balance load across Coworks
- Check task size — decompose EPICs before selecting

### Step 5 — Assign to Coworks

Use the routing table to assign each sprint task to the right Cowork.
Print the assignment plan for confirmation:

```
╔══════════════════════════════════════════════════════════╗
║  SPRINT [n] PLAN — [goal]                                ║
╠══════════════════════════════════════════════════════════╣
║  Cowork-DB (capacity: 4 tasks)                           ║
║    TASK-0010  Design auth schema           [HIGH]        ║
║    TASK-0011  Write RLS policies           [HIGH]        ║
║    TASK-0016  Add indexes to users table   [NORMAL]      ║
║                                                          ║
║  Cowork-Code (capacity: 5 tasks)                         ║
║    TASK-0012  Build /auth/login endpoint   [HIGH]        ║
║    TASK-0013  Build /auth/me endpoint      [HIGH]        ║
║    TASK-0014  Build JWT middleware         [HIGH]        ║
║    TASK-0015  Write auth tests             [NORMAL]      ║
║    TASK-0008  Build nav component  [CARRY OVER]          ║
║                                                          ║
║  Cowork-Infra (capacity: 3 tasks)                        ║
║    TASK-0017  Set up CI pipeline           [NORMAL]      ║
║                                                          ║
║  Total committed: 9 tasks                                ║
║  Held in backlog: 14 tasks                               ║
╚══════════════════════════════════════════════════════════╝

Confirm this sprint plan? YES to start routing, or tell me what to change.
```

### Step 6 — Start the sprint

Once confirmed:
1. Write sprint-board.md with all committed tasks in TODO column
2. Write sprint metadata to `$ORCH/sessions/sprint-[n].md`
3. Begin routing TODO tasks to Coworks in dependency order
4. Log sprint start

---

## Mid-Sprint Management

During the sprint, NEXUS automatically:

- Moves tasks between columns as status changes
- Detects when blocked tasks become unblocked (dependency completed)
- Routes newly unblocked tasks to their Cowork
- Flags tasks approaching stall threshold
- Updates sprint health metrics on every cycle

---

## Sprint Completion

When all sprint tasks are DONE or the sprint end date arrives:

1. Generate sprint summary (see `nexus-reports.md`)
2. Move completed tasks to DONE section in backlog
3. Return incomplete tasks to backlog with priority elevated
4. Archive sprint board to `$ORCH/archive/sprint-[n]-board.md`
5. Ask: *"Ready to plan the next sprint?"*
