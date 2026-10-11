---
name: project-management
description: Use this skill as the entry point for ANY project management work — planning projects, running sprints, managing stakeholders, handling risk, writing charters, status reports, retrospectives, choosing a methodology, or leading delivery at any scale. Triggers on: sprint planning, risk register, project charter, status update, stakeholder management, agile transformation, PMO, OKRs, program management, portfolio management, change management, and any delivery challenge. Use even for casual requests like "our project is a mess" or "help me get this shipped." Covers Agile (Scrum, Kanban, SAFe, LeSS, Scrum@Scale), Waterfall, PMBOK/PMP, PRINCE2, Hybrid, Lean, Six Sigma, and OKRs. Also use when the user needs to adapt, blend, or choose between frameworks.
---

# Project Management Skill

Umbrella entry point for a four-tier PM skill. Holds 8 bedrock principles, dispatches to the right tier by altitude, and loads framework references on demand.

## The 8 Bedrock Principles

1. **Understand why before you plan how.**
2. **Scope is a contract, not a wish list.**
3. **Risk is managed, not ignored.**
4. **Stakeholders are people, not roles.**
5. **Delivery happens in small, visible increments.**
6. **Change is inevitable; control it explicitly.**
7. **The plan is wrong; the planning is priceless.**
8. **Teams deliver; PMs enable.**

## Altitude Assessment

| Tier | Altitude | Load when... |
|---|---|---|
| **L0 — Execute** (`pm-l0-execute`) | Day-to-day | Standups, sprints, blockers, status reports, retros |
| **L1 — Plan** (`pm-l1-plan`) | Project scope | Charters, WBS, risk register, RACI, backlog, kickoff |
| **L2 — Lead** (`pm-l2-lead`) | Program/PMO | Portfolio, governance, OKRs, steering committee |
| **L3 — Strategy** (`pm-l3-strategy`) | Org transformation | Framework selection, agile transformation, PM practice |

## Framework References

| Reference | Load when... |
|---|---|
| `references/agile-scrum.md` | Scrum ceremonies, velocity, backlog, retrospectives |
| `references/agile-kanban.md` | Flow, WIP limits, cycle time, Kanban boards |
| `references/safe-scaled.md` | SAFe, LeSS, Scrum@Scale, PI Planning, ARTs |
| `references/pmbok-waterfall.md` | PMBOK 7, PMP, Waterfall, EVM, CPM |
| `references/prince2.md` | PRINCE2 7, stage management, formal governance |
| `references/hybrid.md` | Blending waterfall + agile, PRINCE2 Agile |
| `references/lean-sixsigma.md` | DMAIC, waste reduction, value stream mapping |
| `references/okr-strategy.md` | OKRs, strategic alignment, portfolio prioritization |

## Cues for Assessing Altitude

- "blocked / behind / standup / sprint / daily" → L0
- "charter / kickoff / plan / milestones / RACI" → L1
- "PMO / portfolio / program / steering / OKR / budget" → L2
- "transformation / methodology / scaling / operating model" → L3

## Version
**1.0.0** — Initial release.
