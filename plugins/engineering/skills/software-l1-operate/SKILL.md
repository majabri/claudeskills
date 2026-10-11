---
name: software-l1-operate
description: Use this skill whenever the user is dealing with a live system in trouble, an active or past production incident, performance issues under load, on-call duties, observability gaps, or any "the running system is misbehaving" situation. Triggers on phrases like "production is down," "the service is slow," "we're getting paged," "incident response," "postmortem," "elevated error rate," "high latency," "the alert fired," "memory is climbing," "the queue is backing up," "we have a customer reporting," "P99 spiked," and on mentions of logs/metrics/traces/alerts/dashboards/SLO/SLA in a problem-solving context. Use this even when the user is asking calmly — the operate-mindset is different from the build-mindset and applies wherever live systems are involved. This is L1 of a four-tier set; for a bug in a single function or test, use L0 (software-l0-debug); for designing the system in the first place, use L3 (software-l3-architect).
---

# L1 — Operate & diagnose

This skill covers production operations: keeping a running system healthy and recovering it when it isn't. The work is at the altitude of a live system you don't fully control: you can't pause it, your changes have blast radius, and what's happening *right now* matters more than what would be elegant.

Mindset shift from L0: in L0 you have time and the surface is small, so deep hypothesis-testing pays off. In L1 the surface is large, the clock is running, and stabilizing the system often takes precedence over understanding it. You will diagnose, but mitigation comes first.

## The 8 bedrock principles (universal across tiers)

1. **Read before you write.** Before changing anything in a running system, understand what's there: the code, the configuration, the recent deploys, the active alerts, the dependencies' status. The cost of "I'll just try X" in production is much higher than at L0.

2. **Verify, don't guess.** Especially in incidents, the temptation to act on a theory is enormous. Confirm before acting when you can. Look at the actual graph, the actual log, the actual response — not what you assume they say.

3. **Distinguish what you know from what you assume.** During an incident, label your beliefs out loud — "confirmed: errors started at 14:32; assumed: caused by the deploy at 14:30; unknown: whether it's correlated with the DB upgrade yesterday." Premature certainty causes wrong mitigations.

4. **Small, reversible changes.** Doubly true in production. Roll out a config change to one host before all hosts. Use feature flags. Prefer rollback over forward-fix when in doubt.

5. **Think about failure modes.** Especially second-order: what happens when your fix interacts with the still-broken parts? With autoscaling? With retries? With the cache?

6. **Address root causes, not symptoms** — eventually. During an active incident, addressing the symptom (mitigate first) is correct. After the incident, the postmortem must reach root cause or you'll see this again.

7. **Optimize for the reader** — including the next on-call. Document your incident actions in the timeline as you go. Future-you, at 3 a.m., is one of the readers.

8. **Match the codebase / environment.** Use the team's existing runbooks, dashboards, alert routes, deploy tooling. Inventing your own under pressure makes things worse.

## The L1-specific principle: blast radius before everything

Before any action in a production-affecting context, ask: **if this is wrong, what breaks, for how many users, and how do I undo it?** A safe action with a tiny blast radius taken now beats a "perfect" action with a large blast radius taken in five minutes. This principle dominates during incidents and shapes good ops work even outside them.

## Incident response

The standard order, and the reason for each step:

```
1. Declare         — name the incident; assign roles
2. Mitigate        — make the symptom stop, even if you don't yet know why
3. Diagnose        — find the cause
4. Fix             — apply the durable fix
5. Postmortem      — learn from it; close the loop on action items
```

People skip "mitigate" because they want to understand first. This is wrong. The user-visible bleed should stop before deep diagnosis. Then diagnose at a less-frantic pace.

### Declare

- Name the incident. Even if it might be small. Naming creates a shared object everyone can refer to.
- Assign roles: incident commander (decision-maker), comms (updates stakeholders), diagnoser/operator (does technical work). On a small team one person wears multiple hats — but make it explicit who is wearing which.
- Open a single channel/doc for the incident. All info goes there. Sidebar conversations lose context.
- Start a running timeline: what alert fired when, what was tried, what was observed. Write it as it happens, not from memory afterward.

### Mitigate

The mitigation toolkit, in rough preference order:

- **Rollback** the last change. If errors started after a deploy, revert. This is the highest-success-rate mitigation in practice.
- **Failover** to a healthy region/instance/replica.
- **Disable the bad path** with a feature flag, kill switch, or config.
- **Shed load** — rate limit, drop low-priority traffic, return cached/degraded responses.
- **Scale up** capacity if the symptom is saturation (carefully — scaling can mask a leak that's actually getting worse).
- **Restart** specific components if they're stuck (last resort; it loses diagnostic state).

You do not need to know the root cause to mitigate. You need to know *what's being affected* and *what change reduces the bleed*. "We deployed at 14:30 and errors started at 14:32" is enough information to roll back even if you don't yet know which line broke.

If you mitigate by rolling back, the diagnosis can happen at human pace. Note: mitigation is not fix — the rolled-back change still has to be understood, fixed, and re-deployed safely.

### Diagnose

Once the bleeding has stopped (or while it's being mitigated by someone else), find the cause. Use the observability hierarchy — start broad, narrow down:

```
Alerts        — what's firing? Often points roughly at the area.
Dashboards    — the four golden signals. Where are the anomalies?
Logs          — for the affected service, in the affected window. What changed?
Traces        — for slow or failing requests, where's the time/error?
Code/state    — only after the above narrows down where to look.
```

Do not start by reading code. Start by looking at the system's own answers to "what's wrong with me." Code-reading is the *last* step of diagnosis at L1, not the first.

### Fix

Once root cause is understood and the system is stable, design the durable fix. The fix is normal engineering work (often L0 or L2) — but the path back to production should respect blast radius. Roll out gradually. Verify each stage.

If the cause was a deploy that broke things: the fixed deploy should be more conservative than the original (more canary, more soak time) since trust is reduced.

### Postmortem

Blameless. The point is to learn, not to assign fault. A good postmortem has:

- **Timeline** with timestamps: what happened, when, who knew, what they did.
- **Root cause** (with the proper humility — sometimes there's a tree of contributing factors, not a single root). Use techniques like "5 whys" but don't stop at the first satisfying answer.
- **Impact** quantified: users affected, duration, revenue, SLO impact.
- **What went well** alongside what went wrong. Mitigation worked? Alerts caught it? Note these so they're preserved.
- **Action items**: concrete, owned, time-bound. Distinguish "prevent this exact bug" from "improve our ability to handle this *category* of incident." The second is usually more valuable.
- **No naming and shaming.** "The on-call engineer ran a destructive command" is fine; "Alice ran a destructive command" is counterproductive. Systems should make destructive actions hard to do by accident.

## Performance investigation under load

Different mode from L0 debugging. You're asking "why is the system slow under conditions X" rather than "why does this function return wrong output."

### Order of operations

1. **Define the question precisely.** "Slow" is not actionable. "P99 latency on `/checkout` is >2s under traffic of >500 RPS, baseline is 300ms" is. Get specific numbers.
2. **Reproduce the load condition** if possible. Either in production (during natural high traffic), in staging (with load test), or by examining a recent natural occurrence.
3. **Look at the four golden signals** for the affected component:
   - **Latency** (and its distribution — P50, P99, P99.9; look at the tail, not the average)
   - **Traffic** (RPS — is something unusually high?)
   - **Errors** (even ones that are "expected")
   - **Saturation** (CPU, memory, file descriptors, thread pools, connection pools, queue depths)
4. **Find the bottleneck.** Saturation usually points clearly. If CPU is pegged, it's CPU-bound. If a thread pool is full, it's likely waiting on something downstream. If GC time is high, it's allocation pressure. If queue depth is climbing, downstream is slower than upstream.
5. **Profile the bottleneck.** Use a real profiler (CPU profiler for CPU, allocation profiler for GC, query profiler for DB, flame graph for "where is time going"). Don't optimize blind.
6. **Hypothesize and verify** like L0 — but at the system level.

### Common production performance patterns to recognize

- **Cascading failures**: one slow dependency causes upstream pools to fill, which makes upstream slow, which causes its upstream to fill, etc. Mitigate with timeouts, circuit breakers, bulkheads.
- **Retry storms**: a transient failure triggers retries; retries amplify the load on the failing dependency; it gets worse. Mitigate by reducing or removing retries during incidents, retry budgets, and exponential backoff with jitter.
- **Thundering herd**: many clients waiting for the same resource (cache miss, lock release, deploy) all hit it simultaneously. Mitigate with jittered backoff, request coalescing, locked single-flight.
- **Queue buildup**: producer faster than consumer. Backpressure failure. Look for: unbounded buffers, missing flow control. Mitigate by shedding, scaling consumers, or rejecting new work.
- **Memory pressure / GC death spiral**: heap fills, GC takes longer, less time for actual work, latency rises, requests pile up, more allocation, GC takes longer still. Often a leak. Restart buys time; fix the leak.
- **Slow queries**: a query that worked at small scale degrades at large scale. Missing index, full table scan, lock contention. Read the query plan, don't guess.
- **Connection exhaustion**: pool size too small, or connections leaked (not returned). Symptoms look like timeouts and queue buildup. Check pool stats.
- **Clock skew / TLS issues / DNS issues** at boundaries between systems. Less common than the above but recurrent.
- **Cold caches** after deploy or restart: latency spikes that resolve as caches warm. Pre-warming strategies, gradual rollout.
- **Noisy neighbor**: shared infrastructure has another tenant consuming resources. Often visible only as unexplained variance.

## Observability: what to look at, what to add

The observability hierarchy is `metrics → logs → traces`, in roughly increasing detail and decreasing volume.

- **Metrics** answer "is the system healthy" at a glance. Use them for alerts. Should always include the four golden signals per service. Cardinality matters — avoid metrics with unbounded label values (user IDs, URLs with parameters), which break time-series databases.
- **Logs** answer "what happened in this specific request/event." Structured (JSON) beats free-form. Always include trace/request ID, key entity IDs, and actor identity. Don't log secrets, PII, or sensitive payloads. Watch volume — logs at the wrong rate are expensive and hide the signal.
- **Traces** answer "where did the time go in this request." Indispensable for systems with more than a couple of components. Sample appropriately; head-based sampling for cost, tail-based for catching the slow tail.
- **Alerts**: based on user-visible symptoms (error rate, latency, missing data) more than causes (CPU high). Symptom-based catches what matters; cause-based cries wolf. Every alert should be actionable — if it fires and the on-call's correct response is "ignore it," delete it.

If during diagnosis you notice you can't see something you need, that's a finding. After the incident, add the missing observability. Most "we don't know why" incidents are observability gaps in disguise.

## Reviewing operationally-affecting changes

The L1 slice of code review focuses on changes that affect the running system: configs, alerts, dashboards, runbooks, deploy specs, capacity, feature flags, infrastructure-as-code. The risk profile differs from a normal code change — a misconfigured alert can be invisible until it matters.

Specific checks:

- **Does this change affect production safety?** A config change that "looks small" can take a service down (TLS settings, feature flag defaults, timeout values). Treat these with care.
- **Is the change reversible?** Schema changes, irreversible migrations, destructive operations need explicit attention to rollback. "What if we need to undo this in 10 minutes" should have an answer.
- **Does the alert change preserve coverage?** Changing thresholds, suppressing alerts, or removing alerts during cleanup is a common way to lose operational insight.
- **Can the dashboard change mislead?** Dashboards drive on-call decisions at 3 a.m. A misleading panel costs more than a missing one.
- **Capacity changes**: have we modeled load? Especially for changes that affect a shared resource (DB connections, thread pools).
- **Feature flag changes**: who can set this, what's the blast radius if flipped wrong, is there a rate-limit on changes?
- **Deploy spec changes**: changing rollout strategies, health checks, readiness probes — these affect every future deploy. Test in a non-prod environment.
- **Runbook changes**: are they tested? A runbook nobody has run is a guess. Periodic game days catch this.

## On-call discipline

- **Acknowledge fast, even if you don't have a fix yet.** "I see it, investigating" is information.
- **Ask for help early, not late.** Heroism in incidents is anti-pattern. Two engineers diagnose faster than one.
- **Take notes as you go.** You will not remember timing accurately afterward.
- **Hand off cleanly.** A page at the end of your shift gets a real handoff with current state, hypotheses, and what's been tried — not "good luck."
- **Sustainable pace.** Sleep is part of operating. After a major incident, take recovery time. Tired on-call makes worse decisions.

## AI failure modes specific to L1 work

When Claude is helping with operational work, these are especially common:

- **Confidently asserting a cause without observability data.** "It's probably a memory leak" sounds expert but is a guess if you haven't seen memory growth in the actual graph. Push for data, label theories as theories.
- **Recommending complex fixes during an active incident.** Mid-incident is the wrong time for "let me redesign your retry logic." The right answer is usually "roll back" or "flip the flag." Save the redesign for after.
- **Skipping mitigation in favor of explaining the cause.** The user pages you because their site is on fire; lecturing about the bug while it burns is unhelpful. Mitigation first, explanation second.
- **Generic advice ungrounded in the user's actual stack.** Real ops debugging is in the specifics. Ask for the relevant graphs, log lines, error messages, recent deploys. Generic incident-response checklists without tying to actual data are noise.
- **Underestimating second-order effects.** "Just disable retries" — but downstream depends on the retry behavior. "Just bump the connection pool" — but the DB has a limit. Always ask: what does this change interact with?
- **Recommending fixes that can't be safely rolled back.** Especially with infrastructure or data. Default to reversible. If irreversibility is unavoidable, name it explicitly.

If the user is in an active incident, your tone shifts: shorter messages, clearer prioritization, fewer caveats, more "do this then check that." The luxury of nuance comes back after stabilization.
