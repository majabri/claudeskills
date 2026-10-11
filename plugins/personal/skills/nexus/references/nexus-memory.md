# NEXUS Memory Module
*Load when accessing cross-session context, the decisions log, or project institutional memory.*

---

## Why Memory Matters

Every Claude session starts fresh — it has no memory of previous conversations.
NEXUS solves this by writing all important context to Drive files that any session can read.

The memory system ensures:
- No decision is ever made twice
- No context is ever lost between sessions
- Any new Chat or Cowork can get up to speed instantly
- NEXUS can reconstruct full project state after a restart

---

## Memory Files

### decisions-log.md — Every decision ever made

`$ORCH/decisions-log.md`:

```markdown
# Decisions Log
Project: [name]
Total decisions: [n]
Last updated: [datetime]

---

## [YYYY-MM-DD] — [Decision Title]
Decision ID: DEC-[NNNN]
Made by: [Amir / Chat-Arch / NEXUS / etc.]
Area: [architecture / security / UX / data / infra / product]
Status: ACTIVE | SUPERSEDED | REVERSED

### Context
[Why this decision was needed]

### Decision
[Exactly what was decided]

### Rationale
[Why this option over alternatives]

### Implications
[What this decision affects — other tasks, constraints, dependencies]

### Supersedes
[DEC-ID if this replaces a previous decision, or NONE]
```

### project-plan.md — Work breakdown structure

`$ORCH/project-plan.md`:

```markdown
# Project Plan
Project: [name]
Last updated: [datetime]

## Vision
[1-3 sentence description of what is being built]

## Milestones
| Milestone | Description | Target | Status |
|-----------|------------|--------|--------|
| M1 | Auth working end-to-end | Sprint 2 | IN PROGRESS |

## Work Breakdown Structure

### AREA: Authentication
- TASK-0009 [EPIC] Build user authentication
  - TASK-0010 Design auth schema
  - TASK-0011 Write RLS policies
  - ...

### AREA: Dashboard
- TASK-0020 [EPIC] Build main dashboard
  - ...

## Technology Decisions
[Key technology choices — extracted from decisions-log.md]

## Architecture Summary
[High-level architecture — extracted from Chat-Arch sessions]

## Open Questions
[From risk register — things not yet decided]
```

---

## Session Context Files

Every NEXUS session writes a context file that future sessions can load:

`$ORCH/sessions/nexus-session-[datetime].md`:

```markdown
# NEXUS Session — [ID]
Project: [name]
Date: [datetime]
Duration: [HH:MM]

## What Happened This Session
[Summary of work routed and completed]

## Decisions Made
[DEC-IDs logged this session]

## Tasks Completed
[TASK-IDs moved to DONE]

## Tasks Started
[TASK-IDs routed to Coworks]

## Outstanding Issues
[Anything carried over or unresolved]

## State at Session End
[backlog count, sprint status, pending decisions]
```

---

## Session Onboarding Packet

When a Chat or Cowork session is new or restarted, NEXUS can generate
an onboarding packet — a summary of everything they need to know:

Command: `nexus brief [session-name]`

Output written to their outbox:

```markdown
# NEXUS Project Brief — for [session name]
Generated: [datetime]

## Project Summary
[Vision, what's built, what's in progress]

## Your Role
[What this session is responsible for]

## Decisions That Affect You
[Relevant DEC-IDs from decisions-log.md]

## Your Active Tasks
[Any tasks currently assigned or waiting]

## Key Constraints
[Technology choices, architecture rules, things not to change]

## Current Sprint Goal
[What this sprint is trying to deliver]

## Questions Open in Your Area
[From risk register]
```

---

## Memory Maintenance Rules

1. **Write decisions immediately** — when any session makes a decision,
   NEXUS logs it to decisions-log.md in the same monitoring cycle.

2. **Update project-plan.md weekly** — or when a milestone is reached
   or an epic is completed.

3. **Never delete decisions** — mark as SUPERSEDED with a reference
   to the new decision. History is always preserved.

4. **Cross-reference** — every backlog task that relates to a decision
   includes the DEC-ID in its Notes field.

5. **Rebuild from memory** — if NEXUS restarts and finds existing files,
   it reads memory files before running the interview.
   It asks: *"I found a previous session for [project]. Resume from there?"*
