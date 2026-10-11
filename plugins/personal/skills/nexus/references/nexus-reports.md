# NEXUS Reports Module
*Load when generating standup, EOD summary, sprint report, or full project status.*

---

## Report Types

| Command | Report | When |
|---------|--------|------|
| `nexus standup` | Morning standup | Start of work session |
| `nexus eod` | End-of-day summary | End of work session |
| `nexus report` | Full project status | On demand |
| `nexus sprint` | Sprint board view | On demand |
| `nexus risk` | Risk register view | On demand |
| Auto | Sprint completion report | When sprint ends |

---

## Morning Standup (`nexus standup`)

Generated from: backlog.md, sprint-board.md, risk-register.md, decisions-log.md

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS STANDUP — [project name]                          ║
║  [Day of week], [Date]  |  Sprint [n] — Day [n] of [n]  ║
╠══════════════════════════════════════════════════════════╣
║  SPRINT GOAL: [goal]                                     ║
╠══════════════════════════════════════════════════════════╣
║  ✅ COMPLETED SINCE LAST STANDUP                         ║
║                                                          ║
║  TASK-0010  Design auth schema          (Cowork-DB)      ║
║  TASK-0008  Build nav component         (Cowork-Code)    ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  🔄 IN PROGRESS TODAY                                    ║
║                                                          ║
║  TASK-0011  Write RLS policies          → Cowork-DB      ║
║  TASK-0012  Build /auth/login endpoint  → Cowork-Code    ║
║  TASK-0017  Set up CI pipeline          → Cowork-Infra   ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  🔴 BLOCKERS                                             ║
║                                                          ║
║  TASK-0013  /auth/me endpoint — waiting on TASK-0011     ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  ⚠️  RISKS & FLAGS                                       ║
║                                                          ║
║  Sprint is AT RISK — 3 tasks not yet started             ║
║  TASK-0015 (auth tests) may not fit in sprint            ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  📊 SPRINT HEALTH                                        ║
║  Done: 4/9  In Progress: 3  Blocked: 1  Todo: 1          ║
║  Completion: 44%  |  Target for today: 55%               ║
╚══════════════════════════════════════════════════════════╝
```

After standup, NEXUS automatically:
- Routes any TODO tasks that have no unmet dependencies
- Sends standup summary to all registered Chat outboxes

---

## End-of-Day Summary (`nexus eod`)

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS EOD SUMMARY — [project name]                      ║
║  [Date]  |  Sprint [n] — Day [n] of [n]                  ║
╠══════════════════════════════════════════════════════════╣
║  TODAY'S COMPLETED TASKS                                 ║
║                                                          ║
║  ✅ TASK-0011  Write RLS policies          (Cowork-DB)   ║
║  ✅ TASK-0017  Set up CI pipeline          (Cowork-Infra)║
║                                                          ║
║  TODAY'S VELOCITY: 4 tasks completed                     ║
║  7-day average: 3.2 tasks/day  ↑ above average           ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  CARRYING OVER TO TOMORROW                               ║
║                                                          ║
║  🔄 TASK-0012  /auth/login endpoint  (started, 60% done) ║
║  🔴 TASK-0013  /auth/me endpoint     (blocked on 0011)   ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  UNRESOLVED DECISIONS                                    ║
║                                                          ║
║  DECISION-0043  Edge Functions vs. API layer             ║
║  → Emailed to you at [time]. Reply needed to unblock     ║
║    TASK-0018 and TASK-0019.                              ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  TOMORROW'S PRIORITY                                     ║
║                                                          ║
║  1. Resolve DECISION-0043 (unblocks 2 tasks)             ║
║  2. Complete TASK-0012 (/auth/login)                     ║
║  3. Start TASK-0014 (JWT middleware) once 0012 done      ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  SPRINT PROJECTION                                       ║
║  At current velocity, sprint completes on time ✅        ║
╚══════════════════════════════════════════════════════════╝
```

After EOD, NEXUS:
- Archives any DONE tasks older than 7 days from backlog
- Updates velocity log
- Sends EOD summary email to Amir's mobile email

---

## Full Project Status Report (`nexus report`)

A comprehensive report covering everything:

```markdown
# NEXUS Project Status Report
Project: [name]
Generated: [datetime]
Session: [ID]

---

## Executive Summary
[2-3 sentence overall status — what's working, what's at risk, what needs attention]

## Sprint Status
Sprint [n] — [goal]
[n] of [total] days complete
[n]% of tasks done
Health: ON TRACK / AT RISK / OFF TRACK

## Work Breakdown
[Table of all areas with % complete]

| Area | Total Tasks | Done | In Progress | Blocked | Backlog |
|------|------------|------|-------------|---------|---------|
| Authentication | 6 | 2 | 2 | 1 | 1 |
| Dashboard | 8 | 0 | 1 | 0 | 7 |
...

## Active Risks
[From risk register — active items only]

## Key Decisions Made This Sprint
[From decisions-log.md — this sprint only]

## Open Questions Needing Resolution
[From risk register — open questions]

## Upcoming (Next Sprint Preview)
[Top 5 backlog items likely in next sprint]

## Session Activity
[Summary of which Chats and Coworks have been active]
```

---

## Sprint Completion Report (auto-generated)

When all sprint tasks are DONE or sprint end date reached:

```markdown
# Sprint [n] Completion Report
Goal: [goal]
Duration: [n] days
Completed: [date]

## Outcome
ACHIEVED / PARTIALLY ACHIEVED / NOT ACHIEVED

## Completed Tasks ([n])
[List of all DONE tasks]

## Incomplete Tasks ([n])
[List with reasons — carried to next sprint]

## Velocity
Planned: [n] tasks
Completed: [n] tasks
Completion rate: [n]%

## Decisions Made This Sprint ([n])
[DEC-IDs]

## Retrospective Notes
[Any patterns NEXUS detected — e.g. which Cowork was fastest, what caused delays]

## Next Sprint Recommendation
Based on velocity and remaining backlog, next sprint should target [n] tasks.
Suggested focus: [top 3 areas with most backlog]
```
