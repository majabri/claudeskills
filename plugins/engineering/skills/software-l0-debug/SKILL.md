---
name: software-l0-debug
description: Use this skill whenever the user is troubleshooting a specific bug, error, exception, traceback, failing test, or any "why is this not working" question at the level of a single function, module, or piece of code. Triggers on phrases like "fix this bug," "this is broken," "why does this fail," "this isn't working," "this throws," pasted error messages or stack traces, mentions of unexpected output, or asking Claude to diagnose a piece of code's misbehavior. Use this even when the request looks simple — debugging discipline matters more on small problems than people assume. This is L0 of a four-tier software engineering skill set; use L1 (software-l1-operate) instead for live production incidents and ops-scale issues.
---

# L0 — Debug & troubleshoot

This skill covers debugging a specific bug, function, test, or piece of code. The work is at the altitude of a single unit: you can hold the relevant code in your head, you can run it, you can step through it.

For live production incidents, performance under load, or anything affecting a running multi-component system, use L1 (`software-l1-operate`) instead. The mindset is different: L0 is patient hypothesis-testing on a small surface; L1 is rapid triage of a moving target.

## The 8 bedrock principles

These apply at every altitude of software engineering work and are worth re-reading even if you've seen them before. They are the load-bearing part of this skill — without them, the methodology below collapses into guessing.

1. **Read before you write.** Before changing any code, understand what's already there. Read the function, its callers, its tests. The most common failure mode for AI-assisted coding is producing plausible code that doesn't match the codebase's conventions, types, or invariants.

2. **Verify, don't guess.** When you don't know something — what a function returns, what's in the config, what the actual error message says — find out. Run the code. Read the file. Print the value. Cost of checking is almost always lower than cost of being wrong.

3. **Distinguish what you know from what you assume.** Separate three categories explicitly: confirmed (I read it / ran it), inferred (probably works this way based on patterns, unverified), unknown. Most engineering disasters come from inferred things being treated as confirmed.

4. **Small, reversible changes.** Each step should leave the system in a working state. Never combine refactoring with behavior change in the same commit — the reader can't tell what's intentional.

5. **Think about failure modes.** For any code you write or change, ask: what happens at the boundaries? Empty input, null, large input, concurrent access, partial writes. You don't have to handle all of them, but you have to know which ones you're handling and which you aren't.

6. **Address root causes, not symptoms.** If a test is flaky, find out *why* before adding a retry. If something throws, understand what invariant was violated before catching the exception. A workaround is fine when you've decided it's a workaround — not when you've mistaken it for a fix.

7. **Optimize for the reader.** Names should describe what something *is*. Comments should explain *why*, not *what*. Functions should do one thing.

8. **Match the codebase.** Existing conventions almost always win over your aesthetic preferences. Consistency lets the next reader predict where things are. Deviate only with explicit reason.

## The debugging loop

Debugging is applied epistemology. The bug is somewhere your model of the system disagrees with reality. The job is to find that disagreement.

```
1. Reproduce reliably
2. Localize (where in the code)
3. Form a hypothesis (why)
4. Test the hypothesis
5. Fix
6. Verify the fix and check for regressions
```

Skip step 1 and every later step is built on sand. Skip step 3 and you're guessing.

### Step 1: Reproduce reliably

Before anything else, get the bug to happen on demand.

- Get the **exact** input — not "something like this," the actual values.
- Get the **exact** environment — versions, OS, container.
- Reduce to the smallest reproduction. Every variable you eliminate is one fewer thing that could be the cause.
- For intermittent bugs: figure out the rate, run the repro until you have at least 5–10 failures to reason about. Truly intermittent almost always means concurrency, ordering, time, randomness, or external state.

If you cannot reproduce the bug, that is itself the most important fact. State it explicitly. Don't pretend to have fixed something you couldn't observe.

### Step 2: Localize

Narrow down where in the code, in roughly this preference order:

- **Read the stack trace top to bottom.** The actual error site is usually obvious; the *interesting* line is usually a few frames up where an assumption was violated.
- **Bisect the history** (`git bisect`) when you have known-good and known-bad commits. Mechanical and devastatingly effective. Underused.
- **Bisect the code** by disabling halves of the suspect region.
- **Print/log/inspect.** Add logging at the boundary between what you're sure of and what you're not. Read the values — don't just check the line was reached.
- **Use the debugger** when state is complex enough that prints would cost more iterations than stepping through.

A discipline that pays off: when you add a print, write down what value you expect to see *before* you run. If actual matches expected, that part of your model is correct. If it doesn't, you've found something.

### Step 3: Form a hypothesis

Articulate, explicitly, a specific theory:

> "The bug happens because `processOrder` is called before `loadInventory` finishes, so `inventory` is undefined and the lookup returns null."

A good hypothesis is **specific** (names actual code paths and values), **testable** (predicts something verifiable), and **mechanistic** (explains *how* the symptom arises from the cause, not just that they correlate). If you cannot articulate this, you don't yet understand the bug — keep observing.

### Step 4: Test the hypothesis

Before fixing: confirm. Cheapest way is usually to add a log/assertion that would only fire if the hypothesis is true, or construct a case that should *not* exhibit the bug under your theory and check it doesn't.

This matters because a fix that "works" can work for the wrong reason. Many fixes accidentally avoid the trigger condition without addressing the cause; six months later the bug returns somewhere else.

### Step 5: Fix

Now — and only now — change the code. Smallest change that addresses the actual cause. Resist "while I'm here" refactoring; that's a separate commit (and often a separate skill — see L2).

If your fix is large, ask whether you actually understood the cause or are rewriting around the problem.

### Step 6: Verify

- Re-run the repro. Confirm it no longer fails.
- Run the tests. Confirm nothing else broke.
- Add a test that would have caught this bug. If you can't write such a test, you've probably not fully understood the bug, or the code isn't testable in its current shape (worth flagging).
- Consider: is this an instance of a *category*? Are there other instances lurking elsewhere?

## Common anti-patterns

- **Shotgun debugging**: changing several things at once. May make it work without learning anything; may make it worse without realizing.
- **Guessing the fix**: skipping hypothesis formation. Even if it works, you've learned nothing.
- **Wrapping in try/catch to make the error go away**: the error was the messenger, not the problem.
- **Adding retries to flaky tests**: turns a deterministic bug into a probabilistic one.
- **"Fixing" tests by changing assertions to match wrong output**: hides the bug.
- **Stopping at the first thing that looks wrong**: confirm it actually explains the observed symptom.

## When you're stuck

- Re-read the error message. Whole thing. Including the parts you skipped because they looked boilerplate.
- Re-check your reproduction. Are you sure you're triggering the same bug?
- Question the load-bearing assumption. What's the one thing you've been *certain* of that, if false, would explain everything? Check it.
- Explain the bug out loud (rubber-duck debugging). Articulating often surfaces the gap.
- Walk away briefly.

## Reviewing a fix (the L0 slice of code review)

When you or someone else has produced a fix, review it specifically as a fix:

- **Does it match a stated hypothesis?** If the author can't articulate why this fix addresses the cause, push back.
- **Is the cause-fix link mechanistic?** "It works now" isn't a review-passing answer. *Why* does it work now?
- **Did the diff change behavior intentionally and only intentionally?** A fix should be a small, scoped change. Watch for "while I was in here" edits that may introduce new bugs.
- **Is there a regression test?** If not, the bug can come back undetected. Acceptable only if the test is genuinely impractical and that's been explained.
- **Does the fix address the symptom or the cause?** A try/catch, a retry, or an extra null-check that "happens to" make the failure go away is suspicious until proven otherwise.
- **Are there related cases?** If `processOrder(null)` was failing, what about `processOrder({items: null})`? Often the fix needs to extend.

## AI failure modes specific to debugging

When Claude is the one debugging, watch for:

- **Jumping to a fix without reproducing the bug.** Tempting because pattern-matching to similar-looking bugs is fast; dangerous because the fix is for a bug that may not be the one the user has.
- **Confabulating a cause that fits the symptom.** A plausible-sounding explanation isn't a verified one. Demand evidence — read the code, run the repro, check the value.
- **Skipping step 4 (hypothesis test).** Going from "I think it's X" straight to "here's the fix" without confirming X is true. The cure is to write down the hypothesis and ask: what observation would confirm or refute this?
- **Inventing API behavior.** Claiming a function returns null when an argument is missing, or that a library has a particular default — without verification. If the bug hinges on the behavior of an external API, read its source or docs. Don't guess.

If you're being asked to debug and you don't have access to run code or read the actual file: say so, give your best hypothesis with explicit caveats, and tell the user what to check to confirm or refute it. Don't pretend to certainty you don't have.
