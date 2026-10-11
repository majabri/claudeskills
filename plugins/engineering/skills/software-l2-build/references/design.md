# Design (module / feature scale)

This is design at the unit you can hold in your head: a module, a class, a feature, an API endpoint, a job. For multi-service or system-wide design, use L3.

The job is to choose constraints. Most "design problems" at this scale are problems of having not pinned down what the unit is responsible for and what shape its inputs and outputs are.

## Order of operations

```
1. Pin down what this thing must do (and explicitly, not do)
2. Decide its inputs, outputs, and boundary
3. Sketch the data shapes
4. Sketch the failure modes
5. Code (the easy part once 1–4 are real)
```

If you skip 1–4 and start at 5, you're guessing at all the prior steps and will likely re-do the work. Resist the pull.

## Step 1: What does this thing do?

Write a single sentence. If you need "and" to describe its responsibility, you probably have two responsibilities.

Examples:
- ✓ "Validates an order's items against current inventory and reserves them for 10 minutes."
- ✗ "Handles orders." (Too vague.)
- ✗ "Validates orders, reserves inventory, and notifies the warehouse." (Three responsibilities; split.)

Also write what it explicitly does *not* do. This is often more clarifying than the positive statement. "Does not charge the card. Does not handle partial inventory. Does not retry on failure — the caller decides."

The negative scope is gold for the reader: it tells them what they're allowed to assume the unit isn't doing.

## Step 2: Inputs, outputs, boundary

The unit's interface is its single most important design decision. Once published, changing it is expensive.

- **Inputs**: what comes in, what types, what invariants are required. Are inputs validated inside, or is validation the caller's job? Pick one and document it.
- **Outputs**: what comes out, what types. What does success look like? What does failure look like — exception, error value, partial result?
- **Side effects**: what does this thing change in the world (DB writes, network calls, file writes, log emissions)? List them. Functions whose side effects are surprises to the caller cause the worst bugs.
- **Errors**: what can go wrong, how is it surfaced, and is each kind distinguishable? "Throws on any failure" is rarely the right answer at non-trivial scale.

Keep interfaces **narrow**. The fewer things the unit lets callers do, the fewer ways callers can use it wrongly, the easier it is to evolve later. Adding to a public interface is cheap; removing is expensive.

A useful question: of the parameters this function takes, which are required for the core behavior, and which are knobs that callers might one day want? Knobs that don't have a real caller right now are usually premature. Let the second caller motivate the parameter.

## Step 3: Data shapes

The data model lives longer than the code that processes it. Spend disproportionate care here.

- Use precise types. "string" is rarely the right type — `EmailAddress`, `OrderId`, `ISO8601Timestamp` carry meaning the caller and reader will appreciate.
- Make invalid states unrepresentable when the language allows. A field that's only valid in some states should not exist as a generic optional — model the states explicitly.
- Decide nullability deliberately. `Maybe<X>` / `Option<X>` / `X | null` are different choices than `X`; pick on purpose, not by default.
- For collections: expected size, ordering, uniqueness, mutability. These details are part of the contract.

A practical test: can you write down concrete examples (3–5) of what valid input and valid output look like, with all fields filled? If not, the data model is not yet concrete enough.

## Step 4: Failure modes

For each thing the unit depends on or assumes, ask: what if this isn't true?

- Network calls fail or are slow.
- Inputs are at the boundaries (empty, null, very large, malformed).
- The store the unit reads from has stale or missing data.
- The unit is called concurrently for the same key.
- The unit is called twice for the same input (idempotency).
- A partial write left things inconsistent — what's the recovery?

You don't have to handle all cases. You do have to know which you're handling, which you're not, and why. The "won't fix" cases should be explicit, not accidental.

This step often surfaces missing requirements. "What if inventory changes between check and reserve?" — if the answer is "we don't know," go back to step 1.

## Step 5: Code

Now write it. With 1–4 real, the code itself is usually the easy part — most decisions have been made.

While coding, watch for:

- **The thing you avoided thinking about** in step 4 quietly returning. If you find yourself adding error handling that wasn't part of the design, ask whether the design was wrong.
- **Sprawl**. If the unit is getting bigger than your one-sentence responsibility, either the responsibility is wrong, or you're folding in something that should be separate.
- **Coupling creeping in**. Reaching across module boundaries you didn't intend, importing internals you didn't intend to depend on. Each one is a future migration cost.

## Heuristics worth carrying

- **Boring beats clever.** Clever code is expensive to read. Cleverness should pay for itself with a measurable benefit.
- **Easier to add than to remove.** Default to less: fewer parameters, fewer abstractions, fewer modes. Add when the second caller actually shows up.
- **Symmetry is a smell-detector.** If a method has `enable` and `disable` but `enable` takes 3 arguments and `disable` takes 0, look hard at the asymmetry. There's usually something being papered over.
- **Pure functions where possible.** Code that doesn't reach into the world is easier to test and easier to reason about. Push side effects to the edges.
- **Data > behavior** for the long run. A clear data model with simple functions wins over clever object hierarchies most of the time.
- **YAGNI** (You Aren't Gonna Need It) is correct more often than its critics suggest. The future you imagine is rarely the future that arrives.

## Designing for testability

If the unit is hard to test, the design is wrong — or at least suboptimal. Common testability problems and their causes:

- **Hidden dependencies**: the unit reaches for a singleton, a global, the system clock, the random source. Inject these instead of grabbing them.
- **Doing too much**: a unit with five responsibilities needs five-axis test cases. Split.
- **Side effects mixed with logic**: a function that calculates *and* writes is hard to test in isolation. Separate the calculation from the I/O.

Testability is a design property. Adding testability after the fact is much more expensive than designing for it.

## When the design starts to feel wrong

Trust the feeling, but verify. Common mid-design symptoms:

- You can't write the one-sentence responsibility cleanly.
- You keep adding parameters because callers need different behavior.
- The interface keeps changing.
- You're writing tests that mostly mock things out, leaving little real to test.

Each is a hint to step back to step 1, not to push through.
