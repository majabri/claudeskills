# NEXUS Risk Module
*Load when detecting blockers, managing the risk register, or flagging project health issues.*

---

## Risk Register

`$ORCH/risk-register.md` — maintained continuously by NEXUS:

```markdown
# Risk Register
Project: [name]
Last updated: [datetime]

## 🔴 ACTIVE BLOCKERS
| ID | Task | Blocked By | Since | Impact | Action |
|----|------|-----------|-------|--------|--------|

## 🟠 ACTIVE RISKS
| ID | Risk | Likelihood | Impact | Status | Mitigation |
|----|------|-----------|--------|--------|-----------|

## 🟡 OPEN QUESTIONS
| ID | Question | Owner | Raised | Blocks |
|----|----------|-------|--------|--------|

## ✅ RESOLVED
| ID | Issue | Resolution | Resolved |
|----|-------|-----------|---------|
```

---

## Risk Categories

### BLOCKER — Work cannot proceed
Task is IN PROGRESS or BACKLOG but cannot move forward.

Causes:
- Dependency task not yet complete
- Cowork returned `Status: blocked`
- Missing information or decision
- NEXUS holding task pending escalation

Action: Identify root cause → escalate or re-sequence.

### STALL — Work is not moving
Task has been IN PROGRESS longer than the stall threshold.

Causes:
- Cowork session inactive
- Task too large or ambiguous
- Cowork encountered an unexpected problem

Action: Alert Cowork → request partial result or status update.

### DEPENDENCY CHAIN RISK
A task that blocks many others is itself blocked or stalled.

Detected when: a BLOCKED or STALLED task has `Blocks: 3+` entries.

Action: Immediately escalate and prioritize unblocking it above all else.

### CONFLICT RISK
Two sessions have provided contradictory direction on the same area.

Detected when: two task files contain contradictory instructions for the same component.

Action: Hold both tasks → write to decisions/ → notify Amir.

### SCOPE CREEP RISK
New tasks are being added faster than tasks are being completed.

Detected when: backlog is growing 3+ tasks per sprint cycle without proportional completions.

Action: Flag in next standup → recommend backlog grooming session.

### CAPACITY RISK
A Cowork session has more IN PROGRESS tasks than its capacity.

Detected when: a Cowork has more than [capacity] tasks assigned simultaneously.

Action: Hold new assignments for that Cowork → route to next available Cowork.

---

## Proactive Risk Detection

NEXUS scans for risks on every 5th monitoring cycle (not every cycle — avoid noise):

```
Every 5 cycles:
  1. Check all IN PROGRESS tasks for stall
  2. Check all BLOCKED tasks — are any unblocked now?
  3. Check dependency chains for cascade risk
  4. Check backlog growth vs completion rate
  5. Check Cowork capacity balance
  6. Check for conflicting instructions
  7. Update risk-register.md
  8. If new risks found → add to next standup report
```

---

## Risk Severity Matrix

| Likelihood | Low Impact | High Impact |
|-----------|-----------|------------|
| **Likely** | MONITOR | 🔴 ESCALATE |
| **Possible** | MONITOR | 🟠 FLAG |
| **Unlikely** | LOG ONLY | MONITOR |

ESCALATE → write to decisions/, email Amir
FLAG → add to standup report, notify source Chat
MONITOR → log only, review next cycle

---

## Blocker Resolution Tracking

When a blocker is raised:
1. Add to risk-register.md under ACTIVE BLOCKERS
2. Write notification to source Chat outbox
3. If blocker requires Amir's decision → escalate (see nexus-escalation.md)
4. If blocker is a dependency → mark dependent task BLOCKED in backlog

When a blocker is resolved:
1. Move from ACTIVE BLOCKERS to RESOLVED in risk-register.md
2. Update backlog: dependent task → BACKLOG (or IN PROGRESS if Cowork ready)
3. Auto-route the unblocked task
4. Log resolution
5. Include in next standup
