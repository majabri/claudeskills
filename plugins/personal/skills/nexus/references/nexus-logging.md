# NEXUS Logging Standard
*Every action NEXUS takes must produce a log entry. No silent operations.*

---

## Log File Locations

| Log | Path | Purpose |
|-----|------|---------|
| Main log | `$ORCH/log/nexus-[date].log` | All actions, one per line |
| Processed files | `$ORCH/log/processed.log` | Prevents double-processing |
| Active tasks | `$ORCH/log/active-tasks.md` | Live task tracker |
| Session summary | `$ORCH/log/session-[ID]-summary.md` | End-of-session report |

---

## Main Log Format

One entry per line, append-only:

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [ACTION] [details]
```

**Levels:**
- `INFO` — normal operations
- `WARN` — something unusual but handled
- `ESCALATE` — decision required, task held
- `RESOLVE` — decision resolved, task resumed
- `ERROR` — something failed, needs attention

**Example entries:**
```
[2025-05-23 14:02:11] INFO  CYCLE      Scan complete. Inbox files: 2. Cowork results: 0.
[2025-05-23 14:02:11] INFO  DETECT     New task: TASK-0042 from Chat-Arch → Cowork-1
[2025-05-23 14:02:12] INFO  ROUTE      TASK-0042 written to cowork/cowork-1/instructions/
[2025-05-23 14:03:45] INFO  RESULT     Cowork-1 result for TASK-0042 detected
[2025-05-23 14:03:46] INFO  DELIVER    TASK-0042 result → outbox/chat-arch/
[2025-05-23 14:05:00] ESCALATE HOLD   TASK-0043 held — trigger: SECURITY (RLS policy change)
[2025-05-23 14:07:22] RESOLVE PROCEED TASK-0043 resumed — user chose: Option A
[2025-05-23 14:15:00] WARN  STALL      TASK-0041 stalled — 15min elapsed, no result from Cowork-2
```

---

## Processed Files Log

`$ORCH/log/processed.log` — simple list, append-only:

```
inbox/chat-arch/TASK-0042.md
cowork/cowork-1/results/TASK-0042-result.md
inbox/chat-backend/TASK-0043.md
```

Before processing any file, check this log. If the file path is listed → skip it.
After processing any file, append its path here immediately.

---

## Active Tasks Tracker

`$ORCH/log/active-tasks.md` — updated at every routing and delivery event:

```markdown
# Active Tasks
Last updated: [datetime]

| Task ID | From | Routed To | Routed At | Elapsed | Status |
|---------|------|-----------|-----------|---------|--------|
| TASK-0041 | Chat-Backend | Cowork-2 | 14:00:00 | 15m | ⚠️ STALLED |
| TASK-0042 | Chat-Arch | Cowork-1 | 14:02:12 | 2m | ✅ DELIVERED |
| TASK-0043 | Chat-Arch | Cowork-1 | 14:07:22 | 0m | 🔄 IN PROGRESS |
```

Status values:
- `🔄 IN PROGRESS` — routed, waiting for result
- `✅ DELIVERED` — result returned to source Chat
- `⚠️ STALLED` — elapsed > stall threshold
- `🔴 HELD` — escalated, waiting for decision
- `❌ CANCELLED` — user cancelled via decision

---

## Task ID Generation

Format: `TASK-[NNNN]` where NNNN is a zero-padded incrementing counter.

Read the highest existing task ID from `active-tasks.md` and increment.
If no tasks exist yet, start at `TASK-0001`.

Store the current counter in `$ORCH/log/task-counter.txt`.

---

## Session Summary Format

Written when user types `nexus pause`, `nexus stop`, or at session end:

`$ORCH/log/session-[ID]-summary.md`

```markdown
# NEXUS Session Summary
Session ID: [ID]
Project: [name]
Started: [datetime]
Ended: [datetime]
Duration: [HH:MM]

## Sessions Coordinated
- Chats: [list]
- Coworks: [list]

## Task Statistics
- Total tasks received: [n]
- Successfully delivered: [n]
- Stalled: [n]
- Cancelled: [n]
- Decisions escalated: [n]
- Decisions resolved: [n]

## Task Log
| Task ID | From | To | Received | Delivered | Duration | Status |
|---------|------|----|----------|-----------|----------|--------|

## Decisions Made
| Task ID | Trigger | Decision | Time |
|---------|---------|----------|------|

## Issues Encountered
[Any errors, warnings, or anomalies]

## Recommendations
[NEXUS observations — e.g. "Cowork-2 was consistently slow — consider reassigning SQL tasks to Cowork-1"]
```

---

## Logging Rules

1. **Always append** — never overwrite a log file mid-session
2. **Log before acting** — write the log entry, then perform the action
3. **Log failures** — if a file write fails, log the failure in the main log
4. **Timestamps always** — every entry has a full datetime stamp
5. **Human readable** — logs are for Amir, not just machines
