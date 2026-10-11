# Refactoring

Refactoring is changing the structure of code without changing its behavior. The two halves of that definition are equally important: if behavior changes, it isn't refactoring; if structure doesn't change, nothing was refactored.

For architecture-scale restructuring (extracting a service from a monolith, migrating a database, breaking up a platform), use L3. This reference covers code-level refactoring within a service or codebase.

## The hard rule

> Refactoring and behavior change do not share a commit.

This rule is non-negotiable, and it's the single most important thing in this document. The reason is reviewability: when behavior and structure change together, the reader cannot tell which differences are intentional. Refactor in one commit (only mechanical or supporting changes); change behavior in the next.

If you find yourself wanting to "fix this thing while I'm in here" mid-refactor: stop, finish the refactor, commit, then do the fix as a separate change.

## Prerequisite: tests

You cannot safely refactor code that isn't covered by tests, because you have no way to know whether you preserved behavior. Options, in order of preference:

1. **The tests already exist and pass.** Run them. Make sure they actually exercise the code you're about to change — high coverage is not the same as relevant coverage.
2. **Write characterization tests** before refactoring. These are tests that pin down the *current* behavior, including any quirks. They aren't "the right behavior" — they're "the behavior we have." Their job is to scream if you accidentally change something.
3. **Use a strong type system + a small change** to provide some safety. This is a degraded option, only acceptable for very mechanical changes (rename, extract, inline) in well-typed languages, and only when you control the only callers.
4. **Don't refactor.** If you can't test it and can't safely change it, document the limitation and leave it alone, or invest in testability first as its own piece of work.

The temptation to skip this step is enormous. Resist it. Most "the refactor broke production" stories are this step skipped.

## When to refactor

Reasonable triggers:

- **A specific change is hard to make.** The refactor exists to enable the change. (Don't refactor speculatively for changes you might want.)
- **Reading the code is taking disproportionate effort** and that's about to be paid by many future readers.
- **A clear duplication or abstraction violation is causing repeated bugs.**
- **A name is actively wrong** — not just imperfect, but misleading.

Bad triggers:

- "It's not how I would have written it."
- "I read about a pattern I want to apply."
- "The metrics tool flagged it."
- "It's old."

Code being old is not a reason to change it. Code being old and *blocking something* is.

## Common safe refactorings

These are the workhorses. They're mechanical enough that a tool can do them, and they compose into larger structural changes.

- **Rename**: variable, function, class, file. Use the IDE/tool's rename, not find-replace, so you only change semantically intended occurrences.
- **Extract function/method**: lift a coherent block into its own named function. The new function's name pays for the change.
- **Inline**: the inverse. When a function is only called once and its name doesn't add clarity, inline it.
- **Extract variable**: give a complex expression a name. Often the cheapest readability win.
- **Move**: relocate a function/class to a more fitting module.
- **Change signature**: add/remove/reorder parameters. Update all callers in the same commit.
- **Replace conditional with polymorphism** (or the reverse): when type-based switches recur across the codebase, classes earn their keep; when there's exactly one switch, polymorphism is overkill.
- **Introduce parameter object**: when several parameters are passed together repeatedly.

## The disciplined sequence for larger refactors

When the refactor is bigger than a single mechanical step:

1. **Make the change easy.** First, refactor the surrounding code so the change you actually want becomes a simple insertion or replacement. Then make the easy change. Kent Beck: "Make the change easy, then make the easy change."
2. **Sequence steps so each leaves the system working.** Never have a "broken in the middle" state on the main branch. Use feature flags, parallel implementations, or staged rollouts to keep both old and new viable until the cutover.
3. **One commit per step.** Resist combining. The reviewer (and bisect, when it bites you in 6 months) will thank you.
4. **Run tests after every step.** If a step breaks tests, you know which step. Batch ten steps and you don't.

## Specific patterns for risky transformations

### Replacing one implementation with another

Don't rip out and replace. Run them in parallel:

1. Introduce the new implementation alongside the old, behind a flag.
2. Route a small percentage of traffic / calls to the new one.
3. Compare outputs (shadow mode) when feasible.
4. Increase percentage as confidence grows.
5. Remove the old implementation only after the new one has handled 100% for long enough that you trust it.

### Changing a widely-used interface

Don't change the signature in place — that breaks every caller at once. Instead:

1. Add the new interface.
2. Make the old one delegate to the new (preserving exact behavior).
3. Migrate callers one at a time.
4. Remove the old when no callers remain.

### Renaming across a large codebase

If the rename is in a public API, you need a deprecation period:

1. Add the new name as an alias for the old.
2. Mark the old as deprecated with a clear pointer to the new.
3. Migrate internal usage to the new.
4. Wait at least one release cycle (longer if external).
5. Remove the old.

## Things that look like refactoring but aren't

These are valuable, but call them what they are and treat them with the rigor due to behavior changes:

- **Performance optimization** changes observable behavior (timing) and often correctness if done carelessly. Benchmark before and after.
- **Bug fix during refactor** — even a "small obvious one" — is a behavior change. Pull it out into its own commit.
- **Adding logging or metrics** is a behavior change if the logs are observable (and they are, e.g., to log volume / cost).
- **Updating dependencies** is a behavior change. The new version's behavior may differ in ways you haven't checked.
- **Reformatting** is fine as a refactor, but should be its own commit and ideally automated by a formatter.

## When to stop

Refactors expand. Set a budget at the start ("two days," "this PR only") and be ruthless about scope. Adjacent code can almost always wait. The point of refactoring is to enable specific work; once it's enabled, the refactor is done. Resisting "while I'm here" is its own engineering skill.

## When not to refactor

- **Code that's about to be deleted.**
- **Code in a system you don't own**, unless you're prepared to also own the breakage.
- **Code right before a release**, unless the refactor is required for the release.
- **Code that's working and not currently blocking anything.** It will probably keep working. The opportunity cost of refactoring it is real.
