# Kanban Reference

## When to Load This
Load for Kanban boards, WIP limits, flow optimization, cycle time, cumulative flow diagrams, or continuous delivery without fixed sprints.

## The Four Core Practices
1. Visualize the workflow
2. Limit WIP
3. Manage flow
4. Make policies explicit

## Board Design
Backlog | Ready (3) | In Progress (2) | Review (2) | Done

WIP limit guide: team size × 1.5 for "In Progress"

## Key Metrics
| Metric | Definition |
|---|---|
| Cycle Time | "Started" to "done" — delivery speed baseline |
| Lead Time | "Requested" to "done" — customer-facing time |
| Throughput | Items completed per time period |
| Flow Efficiency | Active work ÷ total elapsed time (typically 15–40%) |

**Little's Law**: Cycle Time = WIP ÷ Throughput. Double WIP = double cycle time.

## Classes of Service
- Expedite: urgent; max 1 in system; bypass queue
- Fixed Date: hard deadline; track explicitly
- Standard: default WIP limits apply
- Intangible: tech debt; explicit % of capacity (e.g. 20%)

## Kanban vs. Scrum
Use Kanban: continuous/variable work (support, ops, BAU), no predictable intake
Use Scrum: feature dev, stakeholders benefit from fixed cadence
Scrumban: sprint cadence for planning + Kanban WIP limits for execution

## Anti-Patterns
- WIP limits ignored → enforce hard; have capacity conversation
- No classes of service → expedite starves standard work
- Metrics never discussed → integrate into monthly ops review
