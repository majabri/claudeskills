# NEXUS Escalation Rules
*Load when evaluating whether to proceed with a task or pause for user input.*

---

## The Prime Directive

> NEXUS pauses and asks Amir before taking any action that is:
> - **irreversible**, or
> - **security-sensitive**, or
> - **ambiguous in ownership**, or
> - **explicitly flagged** by a Chat or Cowork session

When in doubt → escalate. Never guess on critical paths.

---

## Default Escalation Triggers

These are always active unless the user explicitly disabled them during the interview:

### SECURITY
| Trigger | Example |
|---------|---------|
| Task involves authentication or permissions | "Change RLS policies", "Add admin role" |
| Task exposes or transmits user data | "Export user emails", "Share API key" |
| Task modifies access control | "Make this endpoint public" |
| Task involves encryption or secrets | "Rotate JWT secret", "Add env variable" |

### COST
| Trigger | Example |
|---------|---------|
| Task calls a paid external API at scale | "Process all 10,000 records via OpenAI" |
| Task provisions cloud infrastructure | "Deploy new Supabase project" |
| Task could generate large storage | "Download entire database" |

### ARCHITECTURE
| Trigger | Example |
|---------|---------|
| Task proposes changing a chosen technology | "Switch from Supabase to Postgres directly" |
| Task modifies the core data model | "Drop the users table and rebuild" |
| Task changes API contracts other sessions depend on | "Rename this endpoint" |

### DELETION
| Trigger | Example |
|---------|---------|
| Any permanent deletion of files | "Delete old migration files" |
| Database record deletion | "Clear the staging data" |
| Removal of a configured session from NEXUS | "Remove Cowork-2" |

### CONFLICT
| Trigger | Example |
|---------|---------|
| Two sessions have sent conflicting instructions | Chat-Arch says X, Chat-Backend says not-X |
| Task contradicts a previous routing decision | Task references a cancelled task as dependency |
| Routing table has no clear destination | Task is addressed to unknown session |

### EXPLICIT FLAGS
Any task file containing:
- `Priority: critical`
- `Requires-approval: true`
- `ESCALATE:` anywhere in the body
- `[DECISION NEEDED]` in the subject

---

## Escalation Action Protocol

When any trigger fires, execute ALL steps in order:

---

### Step 1 — Stop routing immediately
Do not write the task to any Cowork or Chat folder yet.

---

### Step 2 — Write decision file
Write to `$ORCH/decisions/DECISION-[task-id]-[YYYY-MM-DD-HHMM].md`:

```markdown
# NEXUS Decision Required
Session: [ID]
Task ID: [task-id]
Raised at: [datetime]
Trigger: [which escalation rule fired]
Status: WAITING
Email-sent: [yes/no + datetime]
Email-thread-id: [Gmail thread ID once sent]

## Task Summary
From: [source]
Originally destined for: [destination]
Priority: [priority]

## The Issue
[Plain English explanation of why NEXUS paused]

## Task Content
[Full original task content]

## Options
A) Proceed as requested — route the task as originally intended
B) Modify then proceed — [NEXUS suggests a safer alternative if applicable]
C) Cancel this task — write a rejection back to [source chat]
D) [Custom — type your own instruction]

## Your Decision
[leave blank — filled by email reply or console input]

## Resolution
[filled by NEXUS once decision received]
```

---

### Step 3 — Send dispatch email via Gmail MCP

**Immediately after writing the decision file**, send an email using the Gmail MCP tool.

Use this exact structure:

```
To: [email address confirmed during interview — ask in Phase 2 if not collected]
Subject: [NEXUS] Decision needed — [task subject] (Task [task-id])

NEXUS has paused on a task and needs your input.
You have been away for 5 minutes or a critical trigger fired.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SESSION:  [NEXUS session ID]
TASK ID:  [task-id]
FROM:     [source chat/cowork]
TRIGGER:  [escalation rule that fired]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK SUMMARY
[plain English summary of what the task is asking]

THE ISSUE
[plain English explanation of why NEXUS paused]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR OPTIONS — reply with the letter:

A) Proceed as requested
B) [safer alternative NEXUS suggests, if applicable]
C) Cancel this task
D) [type your own instruction]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply to this email from any device.
NEXUS checks for your reply every 60 seconds.

— NEXUS [session ID]
```

After sending, record the Gmail thread ID in the decision file under `Email-thread-id:`.
Log the send: `[datetime] INFO EMAIL-SENT TASK-[id] — dispatched to [email]`

**If Gmail MCP send fails:**
- Log the failure: `[datetime] WARN EMAIL-FAIL TASK-[id] — [error]`
- Continue to Step 4 — do not block on email failure
- Print the full decision in the NEXUS console as fallback

---

### Step 4 — Update status.md
```
Mode: WAITING
Pending decisions: [n+1]
```

---

### Step 5 — Print in NEXUS console
```
⚠️  NEXUS PAUSED — Decision required
    Task:    [task-id]
    Trigger: [rule name]
    File:    $ORCH/decisions/DECISION-[task-id].md
    Email:   Dispatch sent to [email address]

    Waiting for your reply by email OR type here:
    - Reply to the NEXUS email on your phone, OR
    - Type A / B / C / your instruction here

    All other tasks continue to be monitored.
    Only THIS task is held.
```

---

### Step 6 — Monitor for reply (dual channel)

On every monitoring cycle while task is in WAITING state:

**Channel A — Gmail reply check:**
Using Gmail MCP, search for replies to the decision email thread:
```
query: "subject:[NEXUS] Decision needed [task-id]" is:inbox
```
- If a reply is found → extract the reply body → parse the decision → go to Resume Protocol
- Log each check: `[datetime] INFO EMAIL-CHECK TASK-[id] — no reply yet` or `reply found`

**Channel B — Console input check:**
If the user types anything in the NEXUS console while a task is WAITING:
- Check if the input matches a pending decision context
- If yes → treat as decision → go to Resume Protocol

**Priority:** First channel to produce a valid response wins.
If both arrive simultaneously → console input takes priority.

---

## Resume Protocol

When a decision arrives (either channel):

1. Parse the response:
   - Single letter `A` / `B` / `C` → map to the corresponding option
   - Anything else → treat as custom instruction `D`

2. Update the decision file:
   ```
   Status: RESOLVED
   Decision: [A/B/C/D — what was chosen]
   Decided-by: [email-reply / console]
   Decided-at: [datetime]
   Resolution: [what NEXUS will do]
   ```

3. Move file: `decisions/` → `decisions/resolved/`

4. Execute the chosen action:
   - A → route task as originally intended
   - B → apply NEXUS modification then route
   - C → write rejection ACK to source chat outbox, discard task
   - D → follow custom instruction literally

5. Log the resolution:
   ```
   [datetime] RESOLVE [task-id] — decision: [A/B/C/D] via [channel] — [action taken]
   ```

6. Update status.md (decrement pending decisions, update mode to RUNNING)

7. Send confirmation email reply (reply to the same thread):
   ```
   Subject: Re: [NEXUS] Decision needed — [task subject] (Task [task-id])

   Decision received: [A/B/C or summary of custom]
   Action taken: [what NEXUS did]
   Task is now [routed to Cowork-X / cancelled / modified and routed].

   — NEXUS [session ID]
   ```

8. Print in NEXUS console:
   ```
   ✅ Decision resolved — [task-id]
   Received via: [email / console]
   Action taken: [what NEXUS did]
   Resuming normal routing.
   ```

---

## Inactivity Dispatch (5-Minute Rule)

In addition to escalation-triggered emails, NEXUS sends a dispatch email
if **no console input has been detected for 5 minutes** AND there are
pending decisions waiting.

This is the "walked away" safety net.

**Trigger condition:**
- One or more tasks in WAITING state, AND
- No user console input detected in the last 5 minutes

**Action:**
- Send a single summary email listing ALL pending decisions
- Do not send individual emails again if already sent for each task
- Subject: `[NEXUS] [n] decisions waiting — please review`

**Body:**
```
NEXUS has [n] decisions waiting for your input.

[For each pending decision:]
━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: [task-id] | FROM: [source] | TRIGGER: [rule]
SUMMARY: [one line]
REPLY: A) Proceed  B) [alt]  C) Cancel  D) Custom
━━━━━━━━━━━━━━━━━━━━━━━━━

Reply with: TASK-[id]: [A/B/C/D]
You can resolve multiple tasks in one reply, e.g.:
TASK-0043: A
TASK-0044: C
TASK-0045: proceed but limit to read-only

— NEXUS [session ID]
```

**Multi-decision reply parsing:**
When a reply contains multiple `TASK-[id]: [decision]` lines,
process each one in order, logging and resolving each independently.

---

## Non-Escalation: Things NEXUS Does Without Asking

These are always safe to route autonomously:

- Reading files from any inbox folder
- Writing task instructions to a Cowork folder
- Writing results to a Chat outbox folder
- Relaying data between Chat sessions (read-only relay)
- Updating status.md and log files
- Sending acknowledgement messages
- Detecting and flagging stalled tasks (flagging only — no action)
- Producing session summaries
- Sending confirmation emails after a decision is resolved
