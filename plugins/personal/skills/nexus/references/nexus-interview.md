# NEXUS Interview Protocol
*Load this file at startup. Run every question in sequence. Do not skip phases.*

---

## Pre-Interview Announcement

Print this exactly:

```
╔══════════════════════════════════════════════════════════╗
║          NEXUS — Neural Exchange & Unified               ║
║              Coordination System v2.0                    ║
╠══════════════════════════════════════════════════════════╣
║  Starting session interview.                             ║
║  I will ask you a series of setup questions.             ║
║  This takes about 3 minutes and only happens once.       ║
║  Answers are saved — future sessions can reuse the map.  ║
╚══════════════════════════════════════════════════════════╝
```

---

## PHASE 1 — Project Identity & Rules

**Q1.1** — What is the name of this project?
*(Used to label all session files, logs, and reports)*

**Q1.2** — Give this NEXUS session a short ID (e.g. NEXUS-01, PM-Alpha).
*(Used in log entries and status files)*

**Q1.3** — What is the Google Drive path to your project folder?
*(e.g. Projects/CareerNav/ — NEXUS will store everything inside
this project, not in a generic location)*

**Q1.4** — Where does your project store documentation?
*(e.g. Projects/CareerNav/docs/ — NEXUS writes all reports,
backlogs, decisions logs, and sprint boards here)*

**Q1.5** — What are your project's folder rules?
*(NEXUS will automatically read your project's CLAUDE.md or
README.md if one exists and extract the rules from it.
Or describe them here — e.g. "code in /code, docs in /docs,
no loose files at root, outputs only in designated folders")*

**Q1.6** — What is today's date and approximate time?
*(Or confirm the system date if known)*

> After Q1.3 is answered: NEXUS immediately reads the project's
> CLAUDE.md and README.md from Google Drive to extract any
> existing folder rules before continuing. These rules take
> precedence over NEXUS defaults for all file placement.

---

## PHASE 2 — Claude Project Context

**Q2.1** — Which Claude project are we working in?
*(The Claude.ai project name that contains your Chat and Cowork
sessions — e.g. "CareerNav Platform". This helps NEXUS understand
the session context and reference the right project memory)*

**Q2.2** — Do your Chat sessions have specific skills loaded?
*(e.g. "Chat-Arch has the devops + ai-architect skills",
"Chat-Backend has the devops skill". This helps NEXUS understand
what each Chat is capable of and route work appropriately)*

**Q2.3** — Is there any existing project documentation NEXUS
should read before the intake session?
*(e.g. an architecture doc, a feature list, a previous sprint
board — paste the Drive path and NEXUS will read it during intake)*

---

## PHASE 3 — Dispatch Configuration

**Q3.1** — What is your mobile email address for decision dispatches?
*(NEXUS will email you here when a critical decision fires
or you have been away from the console for 5+ minutes)*

**Q3.2** — Confirm the inactivity dispatch rule:
If no console input is detected for 5 minutes AND decisions
are pending, NEXUS sends a summary dispatch email to your phone.
Type YES to confirm, or specify a different timeout
*(e.g. "10 minutes")*

---

## PHASE 4 — Active Session Discovery

**Before registering any sessions, do this first.**

Print this exactly:

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS — SESSION DISCOVERY                               ║
╠══════════════════════════════════════════════════════════╣
║  Please look at your Claude Desktop sidebar RIGHT NOW.   ║
║                                                          ║
║  List every session you can see:                         ║
║                                                          ║
║  For each CHAT session:                                  ║
║    - Its name or topic                                   ║
║    - Is it part of this project? YES / NO                ║
║                                                          ║
║  For each COWORK session:                                ║
║    - Its name or topic                                   ║
║    - Is it part of this project? YES / NO                ║
║                                                          ║
║  Take your time — scroll through the sidebar fully.      ║
║  Include sessions that are open but not active.          ║
╚══════════════════════════════════════════════════════════╝
```

Wait for the user to list all sessions before continuing.

**Do not proceed to Phase 5 until the user has explicitly listed
at least one Cowork session. If none are listed:**

Print:
```
⚠️  No Cowork sessions listed yet.
    NEXUS needs at least one Cowork session to route work to.

    Please check your Claude Desktop sidebar again:
    - Cowork sessions appear with a terminal/code icon
    - They may be named by project or topic
    - Open a new Cowork session now if none exist yet

    Once you have at least one Cowork session open,
    list its name and what it is used for.
```

Wait again. Do not proceed without at least one Cowork registered.

**Once all sessions are listed**, confirm the full inventory:

```
✅ Session inventory captured:

CHAT sessions (part of this project):
  [list each one]

COWORK sessions (part of this project):
  [list each one]

EXCLUDED (not part of this project):
  [list any excluded sessions]

Is this correct? Type YES to continue registration,
or correct anything I missed.
```

---

## PHASE 5 — Chat Session Registration

**Q5.1** — For each Chat session identified in Phase 4, answer the following:

*For each Chat session, answer Q5.2 through Q5.6:*

**Q5.2** — What is this Chat's name or ID?
*(e.g. Chat-Arch, Chat-Backend, Chat-UX — keep it short)*

**Q5.3** — What is its role or specialty?
*(e.g. "System architecture consultant", "Backend API design")*

**Q5.4** — What skills does it have loaded?
*(e.g. "devops + ai-architect" or "unknown" — helps NEXUS
understand its capability and route appropriately)*

**Q5.5** — What types of tasks does it produce?
*(e.g. "Design decisions, ADRs, technology choices")*

**Q5.6** — What is its inbox folder name under $ORCH/inbox/?
*(NEXUS creates this — confirm or customize the folder name)*

---

## PHASE 6 — Cowork Session Registration

> ⚠️ VALIDATION: If the user did not list any Cowork sessions
> during Phase 4 discovery, stop here and repeat the discovery
> prompt before continuing. Never skip Cowork registration.

**Q6.1** — How many Cowork sessions will NEXUS coordinate?

*For each Cowork session, answer Q6.2 through Q6.5:*

**Q6.2** — What is this Cowork's name or ID?
*(e.g. Cowork-1, Cowork-Code, Cowork-DB, Cowork-Infra)*

**Q6.3** — What is its primary capability?
*(e.g. "TypeScript + React", "SQL + Supabase migrations",
"Shell + deployment + infra")*

**Q6.4** — What types of tasks should be routed to it?
*(e.g. "All SQL and Supabase tasks", "React component builds")*

**Q6.5** — What is its work folder name under $ORCH/cowork/?
*(NEXUS creates instructions/ and results/ subfolders here)*

---

## PHASE 7 — Relationship Mapping

> Before asking these questions, print the confirmed session list
> from Phase 4 so the user can see exactly what they named.
> Use the actual names — never say "Chat 1" or "Cowork A".

Print:
```
Let's map relationships using your actual session names:

CHATS:   [list every registered Chat name]
COWORKS: [list every registered Cowork name]
```

**Q7.1** — Which Chats route tasks to which Coworks?
*(Use the actual session names from Phase 4.
e.g. "[Chat-Arch] → [Cowork-Code] and [Cowork-DB]")*

For each Chat, ask explicitly:
"[Chat name] — which Cowork sessions does it send work to?"
Do this for every Chat. Do not bundle them into one question.

**Q7.2** — Do any Chats share data or results directly with other Chats?
*(e.g. "[Chat-Arch] output feeds into [Chat-Backend] before going to Cowork"
NEXUS will relay between them automatically)*

**Q7.3** — Are there any sequencing rules across sessions?
*(e.g. "Architecture decisions from [Chat-Arch] must be confirmed
before [Chat-Backend] starts backend tasks"
NEXUS enforces these as hard dependencies)*

**Q7.4** — What is the default Cowork for unassigned tasks?
*(If a task arrives with no clear Cowork owner, which one
should receive it? Pick one from the registered Coworks.)*

> ⚠️ VALIDATION: After answering Q7.1, every registered Cowork
> must have at least one Chat that routes to it.
> If any Cowork has no Chat routing to it, ask:
> "No Chat routes to [Cowork name] — is this correct,
> or did we miss a relationship?"

---

## PHASE 8 — Escalation Rules

**Q8.1** — What decisions always require your input before NEXUS proceeds?

Suggest these defaults — confirm or modify:
- Security decisions (auth, permissions, data exposure)
- Cost-incurring actions (API calls at scale, paid services)
- Architecture changes (changing a chosen technology)
- Permanent deletions (files, database records)
- Anything marked `CRITICAL` or `Requires-approval: true`

**Q8.2** — How long before NEXUS flags a stalled task?
*(Default: 15 minutes — confirm or set a different threshold)*

**Q8.3** — Should NEXUS produce a session summary on `nexus pause`?
*(Default: Yes)*

---

## PHASE 9 — Confirmation

Print a full session map summary:

```
╔══════════════════════════════════════════════════════════╗
║  NEXUS SESSION MAP — [Session ID]                        ║
║  Project: [Project Name]          Date: [Date]           ║
╠══════════════════════════════════════════════════════════╣
║  PROJECT PATHS                                           ║
║  Root:   [Google Drive project path]                     ║
║  Docs:   [documentation path]                            ║
║  Orch:   [orchestrator path]                             ║
║  Rules:  [summary of folder rules]                       ║
╠══════════════════════════════════════════════════════════╣
║  CLAUDE PROJECT                                          ║
║  [Claude project name]                                   ║
╠══════════════════════════════════════════════════════════╣
║  CHAT SESSIONS                                           ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │ [Chat Name] — [Role]                            │    ║
║  │   Skills: [loaded skills]                       │    ║
║  │   Inbox:  $ORCH/inbox/[folder]/                 │    ║
║  │   Routes to: [Cowork names]                     │    ║
║  └─────────────────────────────────────────────────┘    ║
║  (one box per Chat)                                      ║
╠══════════════════════════════════════════════════════════╣
║  COWORK SESSIONS                                         ║
║  ┌─────────────────────────────────────────────────┐    ║
║  │ [Cowork Name] — [Capability]                    │    ║
║  │   Work: $ORCH/cowork/[folder]/instructions/     │    ║
║  │   Results: $ORCH/cowork/[folder]/results/       │    ║
║  └─────────────────────────────────────────────────┘    ║
║  (one box per Cowork)                                    ║
╠══════════════════════════════════════════════════════════╣
║  RELATIONSHIPS                                           ║
║  [Chat → Cowork routing summary]                         ║
║  [Chat ↔ Chat data sharing summary]                      ║
╠══════════════════════════════════════════════════════════╣
║  ESCALATION TRIGGERS                                     ║
║  [confirmed trigger list]                                ║
╠══════════════════════════════════════════════════════════╣
║  STALL THRESHOLD:  [X] minutes                           ║
║  DISPATCH EMAIL:   [email address]                       ║
║  INACTIVITY RULE:  [X] minutes                           ║
╚══════════════════════════════════════════════════════════╝
```

Ask:
> "Does this session map look correct?
> Type YES to save and start NEXUS, or tell me what to change."

---

## Post-Confirmation Actions

Once confirmed:

**1. Set dynamic path variables**
```
$PROJECT = [Q1.3 answer — Google Drive project root]
$DOCS    = [Q1.4 answer — documentation folder]
$ORCH    = $PROJECT/orchestrator/
```

**2. Read project rules**
Read `$PROJECT/CLAUDE.md` and `$PROJECT/README.md` if they exist.
Extract folder rules. Log: "Project rules loaded from CLAUDE.md"
If not found: use rules described in Q1.5.

**3. Create Drive folder structure**
Using run_shell, create:
```
$ORCH/
  inbox/[each chat folder]/
  outbox/[each chat folder]/
  cowork/[each cowork folder]/instructions/
  cowork/[each cowork folder]/results/
  decisions/
  decisions/resolved/
  log/
  sessions/
  archive/
```

**4. Create project management files in $DOCS**
Following project folder rules, create if not existing:
```
$DOCS/backlog.md
$DOCS/sprint-board.md
$DOCS/decisions-log.md
$DOCS/risk-register.md
$DOCS/project-plan.md
```

**5. Write session files to $ORCH**
```
$ORCH/routing-table.md      ← session routing map
$ORCH/status.md             ← NEXUS live status
$ORCH/sessions/nexus-session-[YYYY-MM-DD-HHMM].md
```

**6. Initialize task counter**
Write `1` to `$ORCH/log/task-counter.txt`
Write header to `$ORCH/log/processed.log`
Write header to `$ORCH/log/active-tasks.md`

**7. Print ready message**
```
╔══════════════════════════════════════════════════════════╗
║  ✅ NEXUS is RUNNING                                     ║
╠══════════════════════════════════════════════════════════╣
║  Project:  [name]                                        ║
║  Docs:     [docs path]                                   ║
║  Inbox:    $ORCH/inbox/[chat-name]/                      ║
║  Dispatch: [email]                                       ║
╠══════════════════════════════════════════════════════════╣
║  Type 'nexus plan' to start sprint planning, or          ║
║  drop task files into any inbox folder to begin.         ║
║  Type 'nexus status' anytime to check state.             ║
╚══════════════════════════════════════════════════════════╝
```

**8. Proceed to intake**
Load `references/nexus-intake.md` and begin project knowledge capture.
