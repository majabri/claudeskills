---
name: devops
description: Use this skill as the entry point for substantial software engineering work — building features, fixing bugs, reviewing PRs, designing systems, handling production incidents, refactoring, or writing tests — especially when the altitude isn't clear from the request alone. Triggers on phrases like "help me with this codebase," "engineering review," "make this better," "do this properly," "be a good engineer about this," "what would a senior engineer do," "engineering practice," "code quality," and on any compound task that spans multiple altitudes (debug + refactor, design + test, ops + redesign). Use this whenever the user wants engineering rigor across the spectrum, or when the right tier isn't obvious yet — this skill assesses altitude and points to the appropriate specialized tier (L0 debug, L1 operate, L2 build, L3 architect). Use even for casually-phrased requests where the underlying work is substantial.
---

# DevOps

The umbrella entry point for a four-tier software engineering skill set. This skill holds the shared principles, dispatches to the right tier based on the altitude of the work, and serves as the canonical source for the system as it evolves.

> **Note on the name.** This skill is named `devops` because that's what its owner calls it. The scope is broader than the industry-standard meaning of DevOps (CI/CD, deployment automation, infrastructure-as-code) — it covers the full software engineering practice across four altitudes. If you're a future collaborator and the name throws you, the scope is what matters; the name is a label.

## What this skill is for

This is the place to start when a software engineering request comes in and either (a) the altitude isn't obvious or (b) the work spans multiple altitudes. It does three things:

1. **Holds the bedrock principles** that apply at every altitude — the canonical source for these.
2. **Dispatches to the right tier** by helping assess the altitude of the work.
3. **Documents the system itself** — what's intentional, what's open to revision, how to extend it.

When a request clearly fires one tier (a specific bug → L0, an active incident → L1, a PR review → L2, an architecture proposal → L3), the tier triggers directly and you don't need this umbrella. The umbrella matters most for the in-between cases.

## The 8 bedrock principles

These apply at every altitude. **The umbrella is the canonical source.** Each tier mirrors them inline so it works standalone, but if there's ever a discrepancy, this version wins.

1. **Read before you write.** Before changing any code, understand what's already there. Read the function being called, the function calling it, the tests that touch it. The most common failure mode for AI-assisted coding is producing plausible code that doesn't match the codebase's conventions, types, or invariants.

2. **Verify, don't guess.** When you don't know something — what a function returns, what's in a config, what an API actually does — find out. Run the code. Read the file. Print the value. The cost of checking is almost always lower than the cost of being wrong.

3. **Distinguish what you know from what you assume.** Separate three categories explicitly: confirmed (read it / ran it / tested it), inferred (probably works this way based on similar patterns, unverified), unknown. Most engineering disasters come from inferred treated as confirmed. Label your beliefs honestly to the user — "I'm confident X, fairly sure Y, would need to check Z."

4. **Small, reversible changes.** Each step should leave the system in a working state. Never combine refactoring with behavior change in the same commit — the reader can't tell what's intentional. The bigger the change, the more important reversibility becomes.

5. **Think about failure modes.** For any code you write or change, ask: what happens at the boundaries? Empty input, null, very large input, concurrent access, partial writes, a clock that goes backward. You don't have to handle all of them, but you have to know which ones you're handling and which you aren't.

6. **Address root causes, not symptoms.** If a test is flaky, find out why before adding a retry. If a function is slow, profile it before adding a cache. A workaround is fine when you've decided it's a workaround — not when you've mistaken it for a fix.

7. **Optimize for the reader.** The runtime sees your code once; humans read it many times. Names should describe what something *is*, not how it's used. Comments should explain *why*, not *what*. Functions should do one thing, and their signature should say what that thing is.

8. **Match the codebase.** Existing conventions — naming, structure, error handling, logging, test style — almost always win over your aesthetic preferences. Consistency lets the next reader predict where things are. Deviate only with explicit reason.

## Altitude assessment: which tier to load

The four tiers correspond to altitudes of engineering work. Match the request to one (or more) and load the corresponding skill.

| Tier | Altitude | Load when the request is about... |
|---|---|---|
| **L0 — Debug & troubleshoot** (`software-l0-debug`) | A single bug, function, or piece of code | A failing test, an exception, "why doesn't this work," a stack trace, unexpected output, a small surface where you can hold the code in your head |
| **L1 — Operate & diagnose** (`software-l1-operate`) | A live system | Production incidents, on-call work, perf under load, observability gaps, "we got paged," "service is slow," reading logs/metrics/traces, postmortems |
| **L2 — Build & maintain** (`software-l2-build`) | Module / feature scale | Designing a new module/class/function/API, refactoring, writing tests, reviewing a PR, "implement this feature," "clean up this code" |
| **L3 — Architect** (`software-l3-architect`) | System / multi-service scale | System design, scaling decisions, migrations, technology choices for foundational pieces, ADRs, cross-service boundaries, designing for non-functional requirements |

### Compound tasks: load multiple tiers

When the work spans altitudes, load tiers in the order they apply:

- "Implement this feature": L2 (design) → L2 (testing) → L0 (debug as you go) → L2 (review before merging)
- "Production is slow, and the fix needs a refactor": L1 first (mitigate, diagnose), then L2 (refactor) when stable
- "Migrate from monolith to two services": L3 (design + migration plan) → L2 (per-service refactoring) → L1 (operationalize)
- "Refactor this and add tests": L2 (refactoring + testing references)

### Cues for assessing altitude

When the request doesn't obviously fire one tier, these cues help:

- **Time pressure** ("on fire," "we're paged," "P99 spiked," "customers complaining") → L1.
- **Specific error or stack trace pasted** → L0.
- **Words like "design," "architect," "scale," "migrate," "service boundaries"** → L3 (or L2 if module-scale).
- **Words like "implement," "feature," "refactor," "test," "review"** → L2.
- **Multiple of the above in one request** → start with the highest altitude implied; the lower-altitude work usually nests inside.

If you genuinely can't tell, ask the user one clarifying question rather than guessing — but lean toward dispatching with the bedrock principles in hand even if the tier is uncertain. The bedrock alone covers most engineering hygiene.

## Dispatching examples

A few worked examples of how to route real requests:

> **"My pytest fixture is seeing stale data on the second test."**
> → L0. Specific failure, single test surface, debugging methodology applies.

> **"P99 jumped from 200ms to 4s eight minutes ago."**
> → L1. Live system, time pressure, observability-first diagnosis.

> **"How do I split this 400-line OrderProcessor?"**
> → L2. Module-scale refactor; load `refactoring.md` and `design.md` references.

> **"50k DAU on Rails monolith, projecting 500k in 18 months — where do we start?"**
> → L3. Systems-level scaling and possibly migration.

> **"Help me write a clean implementation of a rate limiter."**
> → L2 (primary, design + testing). Possibly L3 if it's a service-scale rate limiter affecting multiple consumers.

> **"This is a senior engineer interview prep — how would you approach designing Twitter?"**
> → L3 (primary). The prompt is asking for systems design.

> **"I want this codebase to be better."**
> → Umbrella alone is fine; the bedrock principles are most of what's actionable. If specifics surface, dispatch to the relevant tier.

## Design notes (what's intentional, what's open to revision)

This section names the choices made in the current version, so future improvers can change them with eyes open rather than by accident.

**Intentional and load-bearing — change with care:**

- **Slicing by altitude, not by activity.** An earlier version sliced by activity (debug, review, design, refactor, test). The altitude framing is more useful because real requests come in by altitude — "production is broken" and "I'm building a feature" want different texture, not just different content.
- **Code review split across all tiers.** Each tier carries its own scope-specific review section (reviewing fixes is different from reviewing PRs is different from reviewing ADRs). The duplication is intentional for precision.
- **L1 = SRE / production ops.** Not systems programming. If you want kernel/driver/low-level perf content, that's a different skill (a hypothetical L1b).
- **Tone: opinionated, direct, principle-based.** Not encyclopedic. The goal is to make Claude make better engineering decisions, not to be a textbook.
- **The 8 bedrock principles.** These are the load-bearing element; the tiers apply them at different altitudes. Adding or removing a principle is a major-version change.

**Reasonable to revise:**

- The exact list of references in L2 (currently: design, refactoring, testing, code-review). New references can be added (e.g., concurrency, dependency hygiene, error-handling patterns) without restructuring.
- The wording and order of the dispatching examples — these should evolve with experience.
- The L3 architecture content — system design is a deep topic and the current treatment is solid but not exhaustive.
- The AI-failure-mode lists at the end of each tier — these should grow as patterns are observed in practice.

**Open questions (genuinely uncertain):**

- Whether security review deserves its own dedicated tier or stays distributed across L2 and L3 as it currently is.
- Whether "concurrency" deserves a dedicated reference somewhere or stays as a recurring sub-theme.
- Whether to add an L4 for org/team-level engineering (tech strategy, technical leadership) or to keep that out of scope.

## How to extend

Adding a new sub-area to L2:
1. Create a new reference file under `software-l2-build/references/`.
2. Add a row to L2's routing table in `SKILL.md`.
3. Add a brief mention in L2's "sub-areas at a glance" section.
4. Bump version in this file's changelog with what was added and why.

Adding a new tier:
1. Create a new skill directory following the `software-lN-name/` naming.
2. Inline the bedrock principles (mirror from this umbrella).
3. Tier-specific guidance, code-review section for that altitude, and AI-failure-mode list.
4. Update the routing table here.
5. Update the cross-references in adjacent tiers.

Modifying the bedrock:
1. Edit here first — this is the canonical source.
2. Propagate to each tier's inline copy.
3. Bump major version in the changelog.

Modifying a tier:
1. Edit the tier directly.
2. Note the change in the changelog here.

## AI failure modes umbrella-wide

When Claude is doing engineering work using these skills, two failure modes apply across all tiers and are worth keeping in mind:

- **Confabulating APIs / behavior / facts.** Inventing function signatures, library defaults, error messages, or system behavior that look plausible. Counter by checking the actual library, source, or docs before claiming. When you can't check, label the claim as inferred.

- **Pattern-matching past the actual problem.** Producing output that looks like the right kind of solution without engaging with the specific constraints of this case. Counter by reading the surrounding context first — the codebase, the symptom, the actual numbers.

Both are versions of skipping bedrock principles 1, 2, and 3.

## Version

**1.0.0** (initial release)

### Changelog

- **1.0.0** — Initial release. Four tiers (L0 debug, L1 operate, L2 build, L3 architect) plus this umbrella. Bedrock principles canonical here, mirrored in each tier for standalone use. L2 uses references for its four sub-areas (design, refactoring, testing, code-review); other tiers self-contained.
