---
name: software-l3-architect
description: Use this skill for system-level or architecture engineering work — designing new systems/services, planning migrations, choosing foundational technologies, designing for non-functional requirements (scale, availability, latency, cost), cross-service boundaries, or writing/reviewing ADRs. Triggers on phrases like "design a system," "system architecture," "how would you architect," "scale this to," "migrate from X to Y," "decompose this monolith," "service boundaries," "platform design," "ADR," "architecture review," and requests spanning multiple services or involving foundational technology choices. Use whenever the question is how-the-pieces-fit rather than what's-inside-one-piece. L3 of a four-tier set; for module-scale design use L2 (software-l2-build); for live operations use L1 (software-l1-operate); for individual bugs use L0 (software-l0-debug).
---

# L3 — Architect

This skill covers system-level engineering: how multiple services, components, and data stores fit together, how systems evolve at scale, and how to make foundational technology choices that will be paid for over years. The work is at the altitude of a system or platform — decisions here shape what's possible at L0–L2 below.

For module/feature design within a service, use L2 (`software-l2-build`). For live operations, use L1 (`software-l1-operate`). The principles overlap; the texture is different. At L3, decisions are slow to make and slower to undo.

## The 8 bedrock principles (universal across tiers)

1. **Read before you write.** At system scale, "read before you write" means understanding the existing system's actual behavior under load, the existing data model, the existing dependencies, and the constraints the team actually operates under. Designing without this context produces architectures that look elegant on a whiteboard and fail on contact with the real org.

2. **Verify, don't guess.** Especially for non-functional claims. "We need to handle 10k QPS" deserves to be checked: do we currently handle that? What's the projection based on? "We have a database bottleneck" — is that measured, or assumed?

3. **Distinguish what you know from what you assume.** Architecture documents that don't separate evidence from conjecture mislead the readers who will rely on them for years. Be explicit about which numbers are measured, which are projected, which are estimated.

4. **Small, reversible changes.** At architectural scale this means migrations in stages, parallel implementations before cutover, the ability to roll back at each step. The bigger the change, the more important reversibility becomes — because the cost of unwinding a year-long migration is enormous.

5. **Think about failure modes.** What happens when a service is slow, not just down? When a region fails? When a third-party dependency degrades? When the queue backs up? At system scale, partial failure is the common case, not the edge case.

6. **Address root causes, not symptoms.** Adding a service to work around a database limitation is sometimes correct and often the architectural equivalent of a try/catch. Ask whether the architecture is solving the actual problem or routing around it.

7. **Optimize for the reader.** The reader of an architecture decision is, often, an engineer 18 months from now trying to understand why things are the way they are. Document the *reasoning*, not just the conclusion. ADRs exist for this.

8. **Match the codebase / org.** The most beautiful architecture for someone else's team can be wrong for yours. Existing skills, existing infrastructure, existing tooling, and the team's operational maturity all constrain the right answer. Architecture choices that don't match the org's capacity get half-built and rotted.

## The L3-specific principle: constraints are the design

A system design is, fundamentally, a choice of which constraints to honor and which trade-offs to accept. Functional requirements (what does it do?) shape what the system must accomplish. Non-functional requirements (how well, how reliably, how cheaply, under what load?) shape how it must accomplish it — and those, more than anything else, determine the architecture.

Most "design problems" at this scale are problems of having not pinned down the constraints clearly enough before drawing boxes. If you find yourself debating Postgres vs. DynamoDB without numbers, stop: you don't yet know the problem.

## The order of operations

Always work top-down. Resist the urge to start with technology choices.

```
1. Requirements (functional + non-functional)
2. Data model and access patterns
3. Component decomposition
4. Interfaces between components
5. Failure modes and trade-offs
6. Observability and operations
7. Technology choices (last)
```

Many engineers go straight to step 7. The result is a stack assembled from current taste rather than current need.

## Step 1: Requirements

### Functional requirements

What does the system *do*? Express as user-visible behaviors, not internal mechanisms. "Users can upload images and tag friends" is functional. "Uses S3" is not — that's a mechanism.

A useful exercise: write 3–5 concrete user stories or API examples *before* designing anything. They expose ambiguities better than abstract requirements lists.

### Non-functional requirements

These determine the shape of the architecture far more than the functional ones.

- **Scale**: how many users, requests/sec, data volume — and on what time horizon? Design for current scale + a realistic growth target, not for hypothetical future planet-scale.
- **Latency**: P50 and P99 targets. P99 is usually the one that constrains the design.
- **Availability**: 99%, 99.9%, 99.99%? Each "9" is roughly an order of magnitude more cost.
- **Consistency**: does every reader need to see the most recent write immediately, or is some staleness OK?
- **Durability**: if we lose this, what's the cost? (For a draft, low. For a payment record, high.)
- **Security and compliance**: who can see what; what regulations apply.
- **Cost**: budget, in dollars and in engineering time.

Ask the user for these explicitly. If they don't know, propose reasonable defaults and label them as assumptions. A design without numbers is a design without constraints.

## Step 2: Data model

The data model is the longest-lived artifact in any system. Code can be rewritten; schemas accumulate downstream consumers and become hard to change. Spend disproportionate care here.

- **Identify the core entities** and their relationships before thinking about storage.
- **List the access patterns**: how is each entity read, written, queried? Which queries need to be fast? Which need to be transactional?
- **Choose storage to match access patterns**, not the other way around. A document store, relational DB, or wide-column store each makes different access patterns fast or slow. The data model should drive the choice.
- **Design indexes from access patterns**, not by guessing.
- **Think about size and growth** of each table/collection. Tables that grow without bound need an archival or partitioning story.
- **Be precise about uniqueness, nullability, and ownership.** "Email is unique" — across what scope? Globally, per-tenant? Forever, or only among active users?

A useful test: can you write down the SQL (or equivalent) for the top 5 access patterns? If not, the model isn't yet concrete enough.

## Step 3: Component decomposition

Now draw boxes — but each box should justify its existence.

- **A component should have a clear single responsibility** expressible in a sentence without "and."
- **Boundaries should follow the seams of change.** Things that change together belong together; things that change for different reasons should be separable.
- **Default to fewer components, not more.** Each network boundary you introduce buys you isolation but costs you latency, partial failure, debuggability, and operational complexity. Microservices are not free.
- **Stateless before stateful.** Stateless components scale and fail more gracefully. Push state to the edges (database, cache, queue) when possible.
- **Synchronous before asynchronous.** Async (queues, events) decouples but makes flow harder to reason about. Use it when you need it (long jobs, fan-out, smoothing load), not by default.

## Step 4: Interfaces

The contract between components matters more than what's inside them. Get the contract wrong and you'll be paying for it for years.

- **Make interfaces narrow.** Expose what callers need; hide what they don't.
- **Prefer explicit over implicit.** A function with named, typed arguments is easier to evolve than one with a generic options bag.
- **Versioning story upfront**, especially for any interface that will have external consumers.
- **Backward compatibility**: how do you add a field, deprecate a field, change semantics? If you don't have an answer before launch, you'll have a hard answer later.
- **Idempotency keys** for any write operation that might be retried.
- **Pagination, filtering, and sorting** for any list endpoint that could grow.

## Step 5: Failure modes and trade-offs

For every component and every interaction, ask: what happens when it fails?

- **What does each component do when its dependencies are down or slow?** "Crashes" is an answer; so is "returns cached," "queues for retry," "fails fast with a clear error." Pick on purpose.
- **Timeouts on every external call.** Without them, one slow downstream takes everything down.
- **Retries with backoff and a budget.** Infinite retries amplify outages.
- **Circuit breakers** for high-volume calls to external services.
- **Bulkheads**: separate resource pools so one slow path doesn't starve everything else.
- **Backpressure**: when downstream can't keep up, upstream needs to slow down or shed load — not silently buffer until OOM.

Make trade-offs explicit. CAP-style choices (during a partition, prefer consistency or availability), latency vs. cost, complexity vs. scalability, build vs. buy — these are choices, not technical inevitabilities. Document the chosen trade-offs and the reasoning so the next reader knows what's intentional.

## Step 6: Observability and operations

If you can't see what the system is doing, you can't keep it running. Treat this as part of the design, not an afterthought. (For deeper ops content, see L1.)

- **Logs**: structured, with enough context (request ID, user ID, key entity IDs) to trace a request through the system. Sensitive data redacted.
- **Metrics**: the four golden signals — latency, traffic, errors, saturation. Per service, per endpoint.
- **Traces**: for any system with more than a couple of components, distributed tracing is the difference between "we know what's happening" and "we have theories."
- **Alerts**: based on user-visible symptoms (error rate, latency) more than on causes (CPU high). Cause-based alerts cry wolf; symptom-based alerts catch what matters.
- **Runbooks**: for each likely operational scenario, who responds and how.
- **Deployability**: how does this get to production, how does it get rolled back, can it be deployed during business hours.

## Step 7: Technology choices

Now — and only now — pick the database, the queue, the language, the framework. The earlier work has constrained the choice space dramatically.

Heuristics:

- **Boring beats novel** for foundational pieces. Postgres, Redis, Nginx, a major cloud provider — these are boring because they work, and "works" is what you want load-bearing.
- **Match the team's existing skills** unless there's a strong reason not to. The cost of one new technology is large; the cost of three at once is enormous.
- **Buy before build** for anything that isn't your core differentiation.
- **One way to do each thing.** Don't introduce a second message queue, a second cache, a second deploy tool unless the first really won't do.

## Architecture-scale migrations

Migrations at this scale are where good designs go to die. The principles:

### Extracting a service from a monolith

A genre that goes wrong constantly. Heuristics:

- **Don't extract until the seam is clearly visible** in the code itself. If the service boundary doesn't map cleanly to existing module boundaries, you're not ready — invest in modularization first.
- **Carve out the data first, or last** — never simultaneously with the code. Splitting code and data at the same time is two hard problems multiplied.
- **The first version should be a literal in-process port** — same code, just behind a network boundary. Optimize later.
- **Shadow before switch.** Run the new service alongside the old code path, comparing outputs, before cutting over.
- **Cutover happens behind a flag**, in stages, with the ability to revert.

### Replacing one system with another

Strangler pattern, generally:

1. Stand up the new system alongside the old.
2. Migrate the easiest, lowest-risk slice of traffic first.
3. Verify behavior matches. Compare outputs in shadow mode where feasible.
4. Increase percentage as confidence grows.
5. Remove the old system only after the new has carried 100% for long enough that you trust it.
6. *Actually delete the old code*, or it becomes load-bearing through inattention.

### Database migrations

Schema changes at scale need expand/contract:

1. **Expand**: add the new column/table/index, alongside the old, both populated.
2. **Migrate writers**: have application code write to both old and new.
3. **Backfill**: populate the new schema for existing data.
4. **Migrate readers**: have application code read from new instead of old.
5. **Contract**: stop writing to old, then drop old.

Each step is independently deployable. Skipping steps causes outages.

### When the migration is going to take a year

Plan for the steady state of "during the migration." The intermediate state can last longer than expected; designs that assume a quick cutover often have ugly transitional states that turn into permanent debt. Make the intermediate state itself livable.

## Reviewing architecture docs and ADRs

The L3 slice of code review focuses on architecture decision records, design docs, and proposed system changes. Different muscles than reviewing a PR.

What to look for in an architecture document:

- **Is the problem stated clearly?** Many designs solve adjacent problems; many solve no specific problem and are speculative. The doc should make the problem unambiguous before proposing a solution.
- **Are the requirements specific?** Look especially for non-functional requirements with numbers. "Highly scalable" is not a requirement. "10k QPS at <300ms P99" is.
- **Are alternatives considered?** A design doc that proposes one solution without comparing alternatives is incomplete. The reasoning for choosing A over B is the most useful content for future readers.
- **Are the trade-offs explicit?** Every architectural choice has a downside. If the doc reads as if the proposed design has no costs, the costs are hidden, not absent.
- **Is the data model laid out?** If not, push for it before approving anything.
- **What are the failure modes?** What happens when each component is down/slow/wrong?
- **What's the migration plan?** Especially for replacing existing systems.
- **What's reversible if we're wrong?** The most important question on big bets.
- **Who's accountable for it operationally?** Architecture doesn't deploy or page itself.

When you (or Claude) write an ADR, structure it minimally as: **Context** (what's the situation), **Decision** (what we're doing), **Alternatives considered** (what we're not doing and why), **Consequences** (what we're accepting in exchange). Short ADRs read; long ones get skimmed.

## Special considerations

### When the user gives you a vague design prompt

Push back productively. Ask for the missing constraints. A good designer's first deliverable is often *the questions*, not the answers.

A useful template:

> "Here's how I'd think about this, but to actually design it I need to know: [3–5 specific constraint questions]. With reasonable defaults [state them], a sketch would look like [sketch]."

This shows the work, names the assumptions, and gives the user something concrete to react to.

### When the user has already chosen the technology

Sometimes the decision is locked in (org standard, existing infrastructure, team expertise). Work within it gracefully. But if the choice forces a poor fit, name it: "given Postgres, this access pattern will be slow at scale; the options are X, Y, or accepting the slowness up to N RPS."

### Designing for AI consumers as well as humans

If the system has an API or interface that AI agents will consume, design accordingly: clear and stable schemas, explicit error messages, predictable pagination, idempotency. AI is sometimes a more demanding consumer than a human SDK user, not less.

## AI failure modes specific to L3 work

When Claude is helping with architecture, watch for:

- **Designing for hypothetical scale.** Producing an architecture for the planet-scale version of a system that currently has 50 users. Boring works for 50 users; the planet-scale version causes years of operational pain. Design for current scale + a realistic horizon.
- **Picking fashionable technologies.** Defaulting to whatever was prominent in the training distribution (microservices, Kubernetes, NoSQL, event sourcing) regardless of whether the problem calls for it. The boring choice is usually right.
- **Proposing solutions without numbers.** "Add caching" / "use a queue" / "go to Kafka" — without the numbers that would justify them. Push for measurements before architectural changes.
- **Skipping the alternatives section.** A design that doesn't compare itself to alternatives is incomplete; the reasoning is the artifact's most valuable part.
- **Hand-waving the data model.** Going straight to box-and-arrow service diagrams without writing down what data lives where. The data model is the design.
- **Underestimating migration cost.** Architectural changes that are easy to draw are often hard to execute, especially with running production. Treat the migration plan as part of the design, not an afterthought.
- **Confidently asserting non-functional behavior.** "This will handle 10k QPS easily" is a hypothesis, not a fact. Distinguish modeled/measured claims from estimates.
- **Reaching for complexity to demonstrate sophistication.** Architecture is judged by results over years, not by how clever the diagram is. Simpler designs that work are better than complex ones that might.

If you're being asked to architect something significant: ask the requirements questions first, propose alternatives, name the trade-offs, document what's reversible. Resist the urge to deliver the answer before the question is clear.
