# Testing

The purpose of tests is to give you confidence to change the code. Everything else — coverage numbers, test counts, the green checkmark — is a means to that end. When the means and the end conflict, side with confidence.

## What to test

The right unit of test is **observable behavior**, not implementation. A test should describe *what* the code is supposed to do for someone who calls it, not *how* it does it. The reason: implementation should be free to change without breaking tests, otherwise the tests obstruct the refactoring they're supposed to enable.

A useful question: if I rewrote the implementation completely while keeping the public interface, would my tests still pass for the right reasons? If yes, you're testing behavior. If no, you're testing internals.

In practice:

- **Test through the public interface** (the function, class, endpoint, CLI) that real callers use.
- **Don't assert on private state, mocked internal calls, or order of internal operations** unless those are part of the contract.
- **Don't write a test per function** out of habit. Write a test per *behavior*. One function may have several behaviors; another may not warrant its own test if it's only called from a tested caller.

## The pyramid (still right, mostly)

```
        /\        end-to-end (slow, brittle, few)
       /  \
      /----\      integration (medium speed, modest number)
     /      \
    /--------\    unit (fast, plentiful)
```

The shape matters because feedback time matters. A test that takes 30 seconds is run rarely; one that takes 30 milliseconds is run constantly. The pyramid distributes coverage where iteration speed is highest.

Anti-patterns:

- **Inverted pyramid** (mostly e2e): every change runs the whole world; failures are slow and unspecific; test maintenance dominates.
- **Hourglass** (lots of unit + lots of e2e, no integration): unit tests pass, e2e tests pass, but the seams between components are uncovered. Bugs live in the seams.
- **No pyramid at all**, just whatever was easy to test: usually means the hard parts are uncovered.

## Anatomy of a good test

```
Arrange — set up the world.
Act     — do the one thing the test is about.
Assert  — verify the result.
```

Properties:

- **One reason to fail.** A test that asserts five different things will, when red, tell you only that one of them broke. Prefer multiple focused tests over one omnibus.
- **Independent.** Tests should not depend on order or shared mutable state. If reordering them breaks them, the framework is hiding a bug.
- **Deterministic.** Same input → same result, every time. Flaky tests train people to ignore failures, which is worse than no tests.
- **Fast.** Slow unit tests get run less, found broken later, and fixed in batches.
- **Readable.** A failing test should make the failure obvious. Names matter: `test_payment_fails_when_card_expired` is useful; `test_2` is not.

## What makes a test fail well

The hardest part of a test is not making it pass. It's making it fail informatively when the code is broken.

- The failure message should name the expected and actual values clearly.
- The failure should localize the bug — ideally a single test fails for a single bug.
- A test that *can't fail for the right reason* is worse than no test. Common version: a test that calls the function but never asserts on its return value, or asserts on something always true.

A practical exercise: after writing the test and watching it pass, deliberately break the implementation and watch the test fail. If it doesn't fail, or fails for the wrong reason, fix the test before moving on.

## Test doubles: mocks, stubs, fakes, spies

Words people use loosely. The distinctions matter:

- **Stub**: returns canned data. ("When asked for the user, return this user.")
- **Fake**: a working but simplified implementation. (An in-memory key-value store standing in for a real database.)
- **Mock**: a stub that *also* asserts on how it was called.
- **Spy**: records calls so you can assert later if needed.

Heuristics:

- **Prefer fakes to mocks.** A fake exercises real behavior — your test verifies you wrote correct code against a working implementation. Mocks tend to verify that you called the things you said you'd call, which is testing your own writing.
- **Mock at architectural seams** (network, filesystem, clock, randomness, third-party APIs), not internal collaborators. Mocking everything turns tests into a description of the implementation.
- **Don't mock what you don't own** when you can avoid it. Mocks of third-party libraries lie when the third party changes; integration tests against the real thing (or a faithful fake) tell you sooner.

## What to test for each kind of code

- **Pure functions / business logic**: dense unit tests, edge cases, property-based tests where applicable.
- **Glue code (controllers, handlers, orchestration)**: integration tests at the next layer up, exercising the glue in context. Unit tests for glue tend to be theater.
- **Boundaries (DB queries, external APIs, file I/O)**: integration tests against a real-ish dependency (test database, recorded fixtures, a fake server).
- **End-to-end critical paths**: e2e tests for the handful of flows that *must* work — sign in, primary user action, payment. Not every flow.
- **UI**: component tests for component logic, e2e for critical user journeys, visual regression where it pays off. Don't try to replicate every interaction in tests.

## Edge cases worth testing on most things

- **Empty input** (empty string, empty list, no fields).
- **Single item** (some bugs only show with N=1).
- **Boundary values** (0, 1, max, max-1, max+1).
- **Negative and zero** for any numeric input.
- **Unicode and weird whitespace** for any string input.
- **Duplicates** in any collection.
- **Concurrent or repeated calls** for stateful operations (idempotency).
- **Failure modes**: what happens when the dependency throws, times out, returns garbage.

You don't write all of these for every test. You scan the list and pick the ones that map to actual risks for this code.

## TDD: when, when not

Test-driven development (write a failing test, make it pass, refactor) is most valuable when:

- The behavior is well-specified before the implementation.
- The interface is more important than the implementation (libraries, APIs).
- The code is at a level of abstraction where unit tests are natural.

It's less helpful when:

- You're in exploratory or spike mode and the design isn't yet known.
- The code is glue or UI where unit tests don't tell you much.
- The right interface only becomes clear after writing some implementation.

Tests-after is also fine. The bar is "tests exist before this is merged," not "tests existed before the implementation."

## Coverage

Coverage is a *floor*, not a target. Low coverage is informative — there's untested code. High coverage is not informative — it could mean tests are thorough or tests just exercise lines without verifying behavior.

If a team imposes a coverage threshold, expect tests to be written specifically to satisfy the threshold. They will pass; they will not be useful. Better to require a test for every behavior change in code review than to enforce a number.

A useful framing: aim for high coverage of *important* code (business rules, state transitions, error handling). Don't burn time covering trivial code (getters, generated code, framework boilerplate).

## Test debugging

When a test is failing and you don't know why:

1. **Read the failure message carefully.** Whole thing.
2. **Run *only* that test.** Test isolation problems disappear; you see only its noise.
3. **Run it twice.** If it's intermittent, that's a fact about the test (or the code) that needs solving — not a fact to ignore.
4. **Bisect**: did the test pass on the previous commit? On main? Where did it start failing?
5. **Add temporary logging** to the test and the code. Pull them out before merging.
6. **Question the test, not just the code.** A test can be wrong. Sometimes the bug is in the test setup or assertions.

## Tests that have outlived their usefulness

Tests are not sacred. Delete tests that:

- Test behavior that no longer exists.
- Test internals so tightly that they break with every refactor without ever catching a real bug.
- Are flaky and not worth fixing.
- Duplicate other tests' coverage.

Removing a test should be a thoughtful decision, but it's a legitimate one.
