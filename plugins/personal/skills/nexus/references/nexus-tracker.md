# NEXUS Tracker Module
*Load for progress monitoring, status updates, velocity tracking, and completion detection.*

---

## What NEXUS Tracks

On every monitoring cycle, NEXUS checks:

1. **New task files** in all Chat inboxes → add to backlog, route
2. **New result files** in all Cowork result folders → deliver to Chat outbox, mark DONE
3. **Stalled tasks** → flag in risk register
4. **Newly unblocked tasks** → auto-route
5. **Sprint health** → update sprint-board.md
6. **Email replies** → check Gmail for decision responses

---

## Monitoring Cycle Frequency

| Condition | Cycle frequency |
|-----------|----------------|
| Active tasks in progress | Every 30 seconds |
| Sprint running, no active tasks | Every 60 seconds |
| Idle (no sprint, no tasks) | Every 120 seconds |
| WAITING mode (decision pending) | Every 60 seconds (Gmail check) |

---

## Result Detection Protocol

When a result file appears in `$ORCH/cowork/[name]/results/`:

**Step 1 — Read result file**
Extract: Task-ID, For (destination Chat), Status, content

**Step 2 — Validate**
- Task-ID exists in backlog → proceed
- Task-ID not found → log WARN, write to decisions/ for Amir

**Step 3 — Quality check**
Check result Status field:
- `complete` → proceed to delivery
- `partial` → deliver with a note, keep task IN PROGRESS, notify source Chat
- `blocked` → update backlog to BLOCKED, write to risk register, notify source Chat
- `failed` → escalate to decisions/, notify Amir

**Step 4 — Deliver to Chat**
Write result to `$ORCH/outbox/[chat-name]/TASK-[id]-result.md`

**Step 5 — Update backlog**
- Move task from IN PROGRESS → DONE (if complete)
- Update sprint board
- Check if this task unblocks other tasks
- Auto-route any newly unblocked tasks

**Step 6 — Update epic progress**
If task has a Parent epic, increment the epic's progress counter.
If all subtasks done, mark epic as DONE.

**Step 7 — Log and update status.md**

---

## Stall Detection

On every cycle, for each IN PROGRESS task:

```python
elapsed = now - task.routed_at
threshold = stall_threshold  # from interview, default 15 min

if elapsed > threshold:
    if task not in risk_register:
        add_to_risk_register(task, reason="STALLED")
        send_stall_alert(task)
    elif elapsed > threshold * 2:
        escalate_to_decisions(task, reason="LONG STALL")
```

Stall alert (written to Chat outbox AND printed in console):
```
⚠️  STALL DETECTED — TASK-[id]
    Title: [task title]
    Assigned to: [Cowork]
    Elapsed: [time]
    Threshold: [stall threshold]

    This task has been with [Cowork] for [elapsed].
    If the Cowork is stuck, ask it to either:
    - Return a partial result with Status: partial
    - Return Status: blocked with the reason
```

---

## Velocity Tracking

At the end of each day (when `nexus eod` runs):

```
Today's velocity:
  Tasks completed: [n]
  Story points equivalent: [n]  (S=1, M=2, L=3, XL=5)
  
7-day rolling average: [n] tasks/day
Sprint burndown:
  Day [n] of [total]: [n] tasks done of [sprint total]
  Projected finish: [on track / n days behind / n days ahead]
```

Velocity is saved to `$ORCH/log/velocity.md` and used to calibrate
future sprint capacity recommendations.

---

## Status Summary (nexus status output)

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS STATUS — [project name]                           ║
║  Session: [ID]  |  [datetime]                            ║
╠══════════════════════════════════════════════════════════╣
║  SPRINT [n] — [goal]                                     ║
║  Day [n] of [n]  |  Health: [ON TRACK / AT RISK]         ║
║                                                          ║
║  Done today:    [n] tasks                                ║
║  In progress:   [n] tasks                                ║
║  Blocked:       [n] tasks                                ║
║  Todo (sprint): [n] tasks                                ║
║  Backlog total: [n] tasks                                ║
╠══════════════════════════════════════════════════════════╣
║  ACTIVE TASKS                                            ║
║  TASK-0012  /auth/login endpoint    → Cowork-Code  [45m] ║
║  TASK-0016  Add user indexes        → Cowork-DB    [12m] ║
╠══════════════════════════════════════════════════════════╣
║  BLOCKERS                                                ║
║  TASK-0011  RLS policies waiting on TASK-0010            ║
╠══════════════════════════════════════════════════════════╣
║  PENDING DECISIONS: [n]                                  ║
║  NEXUS MODE: RUNNING                                     ║
╚══════════════════════════════════════════════════════════╝
```
