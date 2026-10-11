# NEXUS File Formats
*All task, result, data, and decision files follow these schemas.*

---

## Overview

Every file that flows through NEXUS has:
1. A **NEXUS header** (metadata block at the top)
2. A **body** (the actual content)

Headers use simple `Key: Value` format — one per line, no YAML fences needed.

---

## 1. Task File (Chat → NEXUS → Cowork)

**Written by:** A Chat session or Amir directly
**Dropped in:** `$ORCH/inbox/[chat-name]/`
**Filename:** `[TASK-ID]-[short-slug].md` *(NEXUS assigns the ID; the Chat can use any name — NEXUS renames on pickup)*

```markdown
From: Chat-Arch
To: Cowork-1
Priority: high
Type: task
Subject: Design Supabase auth schema
Requires-approval: false
Depends-on: none
Return-to: Chat-Arch

---

## Context
We have decided to use Supabase for authentication.
The platform has three user roles: admin, member, guest.

## Instructions
Design the full auth schema including:
- User profiles table
- RLS policies for each role
- SQL migration file

## Expected Output
1. A SQL migration file: `001_auth_schema.sql`
2. A plain-English explanation of the RLS logic

## Acceptance Criteria
- All three roles can only access their own data
- Admin can read all records
- Guest is read-only on public content
```

**Required header fields:**
| Field | Values | Notes |
|-------|--------|-------|
| `From` | Chat or Cowork name | Must match routing table |
| `To` | Chat, Cowork name, or `NEXUS` | NEXUS resolves ambiguity |
| `Priority` | `critical`, `high`, `normal`, `low` | Default: `normal` |
| `Type` | `task`, `result`, `data`, `decision-request` | Required |
| `Subject` | Short description | Used in logs and status |

**Optional header fields:**
| Field | Values | Notes |
|-------|--------|-------|
| `Requires-approval` | `true`, `false` | Forces escalation if true |
| `Depends-on` | Task ID or `none` | NEXUS holds until dependency delivered |
| `Return-to` | Chat name | Override return destination |
| `Deadline` | datetime or `none` | NEXUS flags if approaching |
| `ESCALATE` | Reason text | Immediately triggers escalation |

---

## 2. Result File (Cowork → NEXUS → Chat)

**Written by:** A Cowork session
**Dropped in:** `$ORCH/cowork/[cowork-name]/results/`
**Filename:** `[TASK-ID]-result.md`

```markdown
From: Cowork-1
Task-ID: TASK-0042
For: Chat-Arch
Type: result
Status: complete
Subject: Supabase auth schema — complete

---

## Result Summary
Auth schema designed and ready. Two files produced.

## Output
### File 1: 001_auth_schema.sql
[SQL content here or reference to where file was saved in Drive]

### File 2: Explanation
The RLS policies work as follows:
- `admin` role: unrestricted SELECT on all tables
- `member` role: SELECT/UPDATE own rows via `auth.uid() = user_id`
- `guest` role: SELECT only on `public_content` table

## Notes
Recommend adding an index on `user_id` for performance.
Consider enabling `pgcrypto` extension for future token hashing.

## Files Saved To
/Projects/Random/[project]/code/supabase/001_auth_schema.sql
```

**Required header fields:**
| Field | Notes |
|-------|-------|
| `From` | Cowork name |
| `Task-ID` | Must match the original task ID |
| `For` | Chat name — NEXUS routes result here |
| `Type` | Always `result` |
| `Status` | `complete`, `partial`, `blocked`, `failed` |

---

## 3. Data Relay File (Chat → Chat via NEXUS)

**Written by:** A Chat session
**Dropped in:** `$ORCH/inbox/[source-chat]/`
**Filename:** `DATA-[slug].md`

```markdown
From: Chat-Arch
To: Chat-Backend
Type: data
Subject: API contract for auth endpoints
Priority: normal

---

## Data Being Shared
The following API contracts have been finalized and Chat-Backend
should use these as the source of truth for implementation:

### POST /auth/login
Request: `{ email: string, password: string }`
Response: `{ token: string, user: UserProfile }`

### GET /auth/me
Headers: `Authorization: Bearer [token]`
Response: `{ id: uuid, role: admin|member|guest, ... }`

## Action Required
No action needed — this is reference data only.
Use these contracts when designing the backend implementation.
```

---

## 4. Decision Request File (Any → NEXUS)

**Written by:** A Chat or Cowork session when they need Amir's input
**Dropped in:** `$ORCH/inbox/[source-name]/`

```markdown
From: Chat-Backend
To: NEXUS
Type: decision-request
Subject: Should we use Supabase Edge Functions or a separate API?
Priority: high
ESCALATE: Architecture decision required before proceeding

---

## The Decision
We are at a fork:

Option A — Supabase Edge Functions
Pros: simpler infra, already in Supabase
Cons: limited runtime, harder to test locally

Option B — Separate Node.js API (e.g. on Railway or Vercel)
Pros: full control, easier testing
Cons: additional service to manage

## Impact
This decision affects Chat-Arch (system design),
Cowork-1 (implementation), and Cowork-2 (deployment).

## Recommendation
Option A for MVP, migrate to Option B post-launch if needed.

## Your Decision
[Amir fills this in]
```

---

## 5. Acknowledgement File (NEXUS → Chat outbox)

NEXUS writes a lightweight ACK when it picks up a task,
so the Chat knows their task was received:

**Written to:** `$ORCH/outbox/[source-chat]/ACK-[TASK-ID].md`

```markdown
From: NEXUS
Type: acknowledgement
Task-ID: TASK-0042
Received-at: 2025-05-23 14:02:11
Routed-to: Cowork-1
Estimated: no ETA available

NEXUS has received your task and routed it to Cowork-1.
You will receive the result in this outbox folder when complete.
```

---

## Naming Conventions

| File type | Pattern | Example |
|-----------|---------|---------|
| Task (new, unnamed) | `[any name].md` | `auth-schema-task.md` |
| Task (NEXUS renamed) | `TASK-[NNNN]-[slug].md` | `TASK-0042-auth-schema.md` |
| Result | `TASK-[NNNN]-result.md` | `TASK-0042-result.md` |
| Data relay | `DATA-[slug]-[date].md` | `DATA-api-contracts-20250523.md` |
| Decision request | `DECISION-REQ-[slug].md` | `DECISION-REQ-edge-vs-api.md` |
| NEXUS decision file | `DECISION-[TASK-ID]-[datetime].md` | `DECISION-TASK-0043-20250523-1405.md` |
| ACK | `ACK-[TASK-ID].md` | `ACK-TASK-0042.md` |
