# Code review (at the PR / module level)

The job of a code review is to make the codebase better as a result of the change, and to make the author better as a result of the review. It is not to demonstrate that you read it.

This reference covers PR-scale review — the everyday review of a feature, refactor, or fix at the module/feature level. For reviewing fix correctness specifically, also see L0. For reviewing operational changes (configs, alerts, runbooks), see L1. For reviewing architectural docs and ADRs, see L3.

Two reviewer mindsets to hold simultaneously:
- **What the change is trying to do** — is the goal clear, and does the diff actually accomplish it?
- **What the change might unintentionally do** — what breaks, what regresses, what surprises a future reader.

## Pass 1: Understand the intent

Before reading any code: read the description, ticket, or PR title. What problem is this solving? What's the success criterion? If you can't tell, that's your first comment — and it's a *real* comment, not a nitpick. A change whose purpose isn't legible is hard to review and harder to maintain.

Then look at the diff scope. Is it doing one thing, or several? Multi-purpose PRs are a review smell — they make every later step harder.

## Pass 2: Correctness

This is the only level that's truly non-negotiable. Style can be argued; correctness can't.

For each non-trivial change, ask:

- **Does it do what the description says?** Diff/description mismatches are surprisingly common.
- **Edge cases**: empty inputs, zero, negative, very large, unicode, null/None/undefined, missing fields, duplicate items.
- **Error handling**: are errors caught at the right layer, surfaced usefully, logged with enough context, distinguished from expected outcomes? Is anything silently swallowed?
- **Concurrency**: shared state, race conditions, ordering assumptions, locks held during I/O, deadlocks.
- **Resource lifecycle**: are files/connections/handles closed, in all paths including errors? (`with`/`defer`/`using`/try-finally.)
- **Off-by-one**: loop bounds, slice indices, pagination, time windows.
- **Numerical**: integer overflow, float comparison, currency in floats (don't), unit confusion, time zones, leap seconds and DST when relevant.
- **State transitions**: can the new code put the system into a state that other code doesn't expect?
- **Idempotency**: if this runs twice, does it do the right thing? (Especially important for retries, webhooks, queue consumers.)

## Pass 3: Security

Adopt a hostile mindset, even on internal code. Every input is potentially malicious until validated.

- **Injection**: SQL, shell, template, log, header. Are inputs parameterized?
- **Authentication / authorization**: is the right check happening? At the right layer? Is the user identity coming from a trusted source (server-derived) rather than a client claim?
- **Secrets**: are credentials in the diff? In logs? In error messages? In responses?
- **Path traversal**: file paths constructed from user input.
- **Server-side request forgery**: URLs constructed from user input that the server then fetches.
- **Deserialization** of untrusted input.
- **PII / sensitive data**: is it being logged, sent to a third party, stored unencrypted, included in responses to users who shouldn't see it?
- **Rate limiting / abuse**: any new public endpoint should have a story for who can hit it how often.

You don't have to find every issue. You do have to scan deliberately.

## Pass 4: Design

- **Single responsibility**: does each function/class have one reason to change? When you describe what it does, do you have to use "and"?
- **Coupling**: does this change reach across module boundaries it shouldn't? Are abstractions leaking implementation?
- **Abstraction level**: is the same function operating at multiple levels of detail? (Calling `db.execute` next to high-level business logic is a smell.)
- **Premature abstraction**: a parameter, base class, or strategy pattern introduced "in case we need it." If there's only one caller / one implementation, push back.
- **Dead code**: unused parameters, unreachable branches, commented-out blocks.
- **Naming**: does the name describe what the thing *is*? Would a new reader understand it without context?
- **Comments**: present where they explain *why*; absent where the code already says *what*. Lying or stale comments are worse than no comments.

## Pass 5: Tests

- **Is there a test for the new behavior?** If not, why not? "Hard to test" usually means "designed in a way that resists testing" — sometimes that's acceptable, often it isn't.
- **Does the test actually verify the behavior**, or just exercise the code? Tests that pass with the implementation gutted are not tests.
- **Does the test fail for the right reason** when it fails? One test, one reason.
- **Edge cases tested**: not just the happy path.
- **Test names**: do they describe the scenario and expected outcome?

## Pass 6: Style and consistency

Last, and lightest. Most style issues should be handled by a linter/formatter, not a human reviewer. When you do raise them:

- Match the codebase's existing conventions, even when you'd choose differently in a vacuum.
- Distinguish "this is wrong" from "I'd prefer." Mark preferences as preferences (some teams use a "nit:" prefix for this).
- Don't rewrite the author's style in your voice.

## How to write the comments

- **Lead with the question, not the verdict.** "Is there a reason X?" invites discussion; "X is wrong" invites defense.
- **Distinguish severity.** Blocking issues, suggestions, and nits are not the same. Mix them and the author can't tell what to act on.
- **Explain the why, not just the what.** "Move this to the service layer" is less useful than "this couples the controller to the DB schema, which we've been trying to avoid because of X."
- **Suggest concretely** when you can. "Maybe extract this into `validateOrder()`?" beats "this is messy."
- **Praise specific things**, not generic ("nice diff"). "I like that you used a generator here — keeps memory bounded for large inputs" — that's useful both as feedback and as documentation of the design choice.
- **Resist scope creep.** If you find a pre-existing issue, note it but don't demand it be fixed in this PR.

## When you're the reviewer of an AI-generated diff

Some failure modes are more common in AI-generated code; scan for these explicitly:

- **Invented APIs** — function calls, methods, or imports that look plausible but don't exist in the version being used.
- **Plausible-looking but wrong logic** — the code follows the right shape (filter, then map, then reduce) but the predicates or transformations are subtly off.
- **Tests that don't fail on broken implementations** — "test passes" is the success criterion the AI optimizes; test *quality* needs human judgment.
- **Style drift** — code that doesn't match the codebase's conventions (different naming, different error pattern, different structure) because the model defaulted to its training-distribution average.
- **Over-engineering** — extra abstractions, configuration knobs, or "future-proofing" that aren't justified by the task.

## When you're the author receiving a review

- Read all comments before responding to any.
- Assume good faith. The reviewer is trying to help.
- "I disagree" is a fine response, with a reason. So is "you're right, fixing."
- If a comment reveals that the *code* was unclear, update the code, not just the explanation in the thread. The next reader won't have the thread.
- Don't merge over unresolved blocking comments.
