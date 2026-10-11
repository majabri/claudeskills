# Agile Scrum Reference

## When to Load This
Load when working with Scrum ceremonies, sprint operations, Scrum roles, velocity, backlog, retrospectives, sprint planning, or team-level Agile.

---

## Scrum in Brief

Scrum is an iterative framework for delivering value in time-boxed sprints (1–4 weeks, most commonly 2 weeks). Three roles, five events, three artifacts.

### The Three Roles

| Role | Responsibility |
|---|---|
| **Product Owner (PO)** | Owns the Product Backlog; prioritizes work by value; represents the customer; accountable for ROI |
| **Scrum Master (SM)** | Servant-leader; facilitates events; removes impediments; coaches team on Scrum; protects team from outside interference |
| **Developers (the team)** | Cross-functional; self-organizing; responsible for delivering a potentially shippable increment each sprint |

### The Five Events

| Event | Purpose | Timebox (2-week sprint) |
|---|---|---|
| **Sprint** | The container for all other events | 2 weeks |
| **Sprint Planning** | Team selects backlog items and creates Sprint Goal | ≤4 hours |
| **Daily Scrum** | 15-min sync; inspect progress toward Sprint Goal; adapt the plan | 15 min |
| **Sprint Review** | Inspect the increment with stakeholders; update backlog | ≤2 hours |
| **Sprint Retrospective** | Inspect the process; identify 1–3 improvements | ≤1.5 hours |

### The Three Artifacts

| Artifact | Purpose | Commitment |
|---|---|---|
| **Product Backlog** | Ordered list of all desired work | Product Goal |
| **Sprint Backlog** | Selected PB items + plan for the sprint | Sprint Goal |
| **Increment** | Sum of all completed work this sprint + previous | Definition of Done |

---

## The Sprint Goal

The most underused element of Scrum. The Sprint Goal:
- Is a single sentence (not a list of stories)
- Describes why the team is doing this sprint (business/user value)
- Gives the team flexibility in how they achieve it
- Good: "Customers can complete checkout without calling support"
- Bad: "Complete 8 stories from the backlog"

---

## Definition of Done (DoD)

A shared, explicit checklist that every increment must meet before being called "done." Typical items:
- Code reviewed and approved
- Unit tests written and passing
- Integration tests passing
- Acceptance criteria met
- Deployed to staging/test environment
- Documentation updated

---

## Estimation in Scrum

**Story Points** (relative sizing, not hours):
- Use Fibonacci sequence: 1, 2, 3, 5, 8, 13, 21
- Reference stories: agree on a "medium" story, estimate relative to it

**Velocity**: Average story points completed per sprint over last 3–5 sprints. Use for capacity planning, not as a performance metric.

---

## Common Scrum Anti-Patterns

| Anti-Pattern | Diagnosis | Fix |
|---|---|---|
| No real PO | PM owns backlog by default | Designate a PO with authority to prioritize |
| Stories not meeting DoD | Incomplete work carried over | Hard stop at sprint end; improve estimation |
| Daily Scrum is a status report | SM managing, not coaching | Team members speak to each other |
| No Sprint Goal | Stories without coherent purpose | Start with "why this sprint?" |
| Retro actions never happen | No follow-through | Review previous actions first; assign owners |
| Velocity used as pressure | Management pushing for more | Focus on predictability not raw numbers |

---

## Scrum vs. Kanban at a Glance

| | Scrum | Kanban |
|---|---|---|
| Cadence | Fixed-length sprints | Continuous flow |
| Roles | PO, SM, Developers | No prescribed roles |
| Planning | Sprint planning | On-demand |
| Metric | Velocity | Cycle time, throughput |
| Best for | Feature development | Support, ops, maintenance |
