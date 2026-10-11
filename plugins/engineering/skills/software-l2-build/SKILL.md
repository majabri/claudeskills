---
name: software-l2-build
description: Use this skill whenever the user is doing code-level engineering at the module, feature, or class scale — designing new functions/modules/APIs, refactoring existing code, writing tests, or reviewing PRs at this level. Triggers on phrases like "implement this feature," "refactor this," "design this class/module/API," "write tests for," "review this PR," "clean up this code," "split this function," "add unit tests," "this needs to be testable," and on requests to build, modify, or improve units of code that are larger than a single bug fix but smaller than a full system. Use this even when the user is asking informally; the build-and-maintain mindset benefits from explicit discipline. This is L2 of a four-tier set; for fixing a specific bug use L0 (software-l0-debug); for production incidents use L1 (software-l1-operate); for system architecture use L3 (software-l3-architect).
---

# L2 — Build & maintain

This skill covers code-level engineering: designing modules and features, refactoring, writing tests, and reviewing PRs at this scale. The work is at the altitude of a codebase — larger than a single bug, smaller than an architectural choice.

This is the tier where most day-to-day engineering happens. The texture is different from L0 (debugging individual bugs) and L1 (running production), and from L3 (designing whole systems): you have time, but you also have to live with what you build for a long time. Decisions compound.

For an active bug or test failure, use L0 (`software-l0-debug`). For production incidents or perf-under-load, use L1 (`software-l1-operate`). For cross-service or system-level architecture, use L3 (`software-l3-architect`).

## The 8 bedrock principles (universal across tiers)

1. **Read before you write.** Before changing any code, understand what's already there. Read the function being called, the function calling it, the tests that touch it, the comments explaining why it exists. Most "AI-generated diff that doesn't match the codebase" failures are this principle skipped.

2. **Verify, don't guess.** When you don't know something — what a function returns, what's in a config, what an API actually does — find out. The cost of checking is almost always lower than the cost of being wrong.

3. **Distinguish what you know from what you assume.** Confirmed (read it / ran it), inferred (probably works this way), unknown. Most disasters come from inferred treated as confirmed.

4. **Small, reversible changes.** Each step should leave the system in a working state. Never combine refactoring with behavior change in the same commit — this rule is non-negotiable in L2 work; the reader can't tell what's intentional otherwise.

5. **Think about failure modes.** Empty input, null, very large input, concurrent access, partial writes. Decide which you handle and which you don't, and make that decision explicit.

6. **Address root causes, not symptoms.** A test that's flaky has a real reason. A confusing API has a design problem. A repeated pattern of bugs has a structural cause. Don't paper over.

7. **Optimize for the reader.** Names should describe what something *is*. Comments explain *why*, not *what*. Functions do one thing. The runtime sees your code once; humans read it many times.

8. **Match the codebase.** Existing conventions almost always win over your aesthetic preferences. Consistency lets the next reader predict where things are. Deviate only with explicit reason.

## Routing: which reference to load

Match the task and read the corresponding file fully before starting work. Compound tasks (e.g., "refactor this and add tests") read multiple, in the listed order.

| If the task is about... | Read |
|---|---|
| Designing a new module, class, function, or feature-scale API | `references/design.md` |
| Restructuring code without changing behavior | `references/refactoring.md` |
| Writing or improving tests | `references/testing.md` |
| Reviewing a PR or someone else's diff | `references/code-review.md` |

If the task is "implement this feature from scratch": design → testing → (debug as you go using L0) → review before merging. Read design first, then testing.

## L2 sub-areas at a glance

The references go deep; this is the on-ramp.

**Design (module/feature scale).** Start from the data and the access patterns. Decide what the unit's responsibility is in one sentence — if you need "and" you have two responsibilities. Make interfaces narrow; hide what callers don't need. Prefer fewer parameters, fewer states, fewer edge cases over fewer lines. Boring, predictable code is a feature.

**Refactoring.** The hard rule: *refactoring and behavior change do not share a commit*. Tests must exist (or write characterization tests first) before refactoring; without them you have no way to know you preserved behavior. Each step should be small enough to revert independently.

**Testing.** Test observable behavior, not implementation. The right unit of test is a behavior, not a function. Tests should fail for one reason, fast, deterministically, and informatively. Coverage is a floor, not a target — the goal is confidence to change the code.

**Code review.** Review in passes — intent, correctness, security, design, tests, style. Lead with questions, not verdicts. Distinguish blocking issues from preferences. The point is to make the codebase better and the author better, not to demonstrate that you read it.

## AI failure modes specific to L2 work

- **Pattern-matching past the actual problem.** Producing code that *looks like* the right kind of solution without engaging with the codebase's specific constraints. Counter by reading the surrounding code and existing similar patterns first.
- **Confabulating APIs.** Inventing function signatures, library methods, or config keys that look plausible but don't exist. Counter by checking the actual library/source. If you can't, label the call as "unverified — please confirm."
- **Over-engineering.** Adding configuration knobs, abstractions, or "future-proofing" that aren't justified by the current need. Default to the simplest thing that works; abstraction earns its keep.
- **Tests that don't fail on broken implementations.** "Test passes" optimizes for the wrong target. Verify a test would fail if you broke the code it covers — break the code (locally, mentally, or actually) and confirm the test catches it.
- **Style drift.** Writing code that doesn't match the codebase's conventions because the model defaulted to its training-distribution average. Read existing code in the same module first; mimic its idioms.
- **Mixing refactor with behavior change.** "While I'm here" edits embedded in a refactor. Always pull these out into a separate commit, even if it costs an extra step.
