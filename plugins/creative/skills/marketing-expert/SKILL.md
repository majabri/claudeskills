---
name: marketing-expert
description: Use for creative, design, and marketing work spanning brand identity (logos, naming, color, typography, brand systems), digital and product design (websites, landing pages, app UI, dashboards, design systems, UX critique), copywriting (headlines, taglines, hero copy, ad copy, microcopy, voice and tone), marketing strategy (positioning, audience, messaging, GTM, campaigns), and creative rights / IP (copyright, trademark, fair use, licensing, AI authorship, asset clearance). Triggers on: design / critique / improve a logo, brand, name, site, page, screen, or design system; write / rewrite copy; position or differentiate a product; "is this fair use," "can I trademark / use / own this," "do I own this AI-generated work," "is this name taken"; compound briefs ("name + logo + landing page + pitch"); vague briefs ("make this more modern / on-brand / professional"). Surface proactively when work involves real assets, brand-adjacent names, AI-generated commercial output, or competitor references.
---

# Creative Suite

A unified creative-and-marketing skill covering six specialized disciplines: creative direction, brand identity, digital design, copywriting, marketing strategy, and creative rights / IP. Each discipline has its own deep reference loaded only when the work calls for it — you don't need to read all six to answer one question.

This skill exists because creative work has a recurring failure mode: jumping to deliverables before the strategic work is done. The default behavior of this skill is to slow down by exactly one step — find out what's really being asked, route to the right discipline, and pull in adjacent disciplines when the work spans them.

## How to use this skill

The skill has two layers:

1. **This file** — universal creative judgment, the routing logic, and the cross-cutting principles every discipline shares.
2. **The `references/` folder** — six deep references, one per discipline. Read these only when the work calls for them.

The reference files:

| Reference | Load when the work involves |
|---|---|
| `references/creative-director.md` | Compound briefs spanning multiple disciplines, vague briefs ("make this better / on-brand / more modern"), critique of existing work, or a brief where the right starting discipline isn't obvious yet |
| `references/marketing-strategy.md` | Positioning, audience, messaging, GTM, campaigns, competitive analysis, "what do we say about this product," diagnosing why marketing isn't working, market entry, pricing communication |
| `references/brand-identity.md` | Logos, brand naming, color systems, typography systems, brand guidelines, identity critique, "does this logo work," brand refresh, brand-system extension |
| `references/digital-design.md` | Application screens, dashboards, forms, marketing pages, websites, landing pages, design systems, components, UX critique, conversion problems, "fix this UI" |
| `references/copywriting.md` | Headlines, taglines, hero copy, ad copy, body copy, microcopy, error messages, CTAs, voice and tone, content structure, "rewrite this," "make this punchier" |
| `references/creative-rights.md` | Copyright, trademark, fair use, licensing, asset clearance, model releases, music sync, font licensing, AI-generated content rights, "can I use / trademark / own this" |

You don't have to load only one. If the user is launching a B2B fintech tool and needs name + logo + landing page + pitch, you load `creative-director.md` first to route, then pull in `marketing-strategy.md` (positioning), `brand-identity.md` (name + logo), `digital-design.md` (landing page), and `copywriting.md` (pitch). Load lazily — only what the next move actually needs.

## When NOT to load every reference

A common mistake is loading all six references on every creative request. Don't. The references are large; they exist to give depth on a specific question, not to act as a general manual. Load only what the *current* turn requires. If the user asks to rewrite a headline, that's `copywriting.md` — you don't need `creative-rights.md` unless the headline mentions a competitor or quotes a copyrighted source.

If you genuinely don't know which reference to start with — that's exactly when you load `references/creative-director.md`. It's the routing reference.

## Universal creative principles

These cut across all six disciplines and are worth internalizing before reaching for a reference. They're the principles that distinguish good creative work from category-default creative work.

### 1. Strategy before craft

Every creative discipline produces better work when the strategic question is answered first. "Who is this for, why does it matter, what's distinctive, what's true?" Before a logo, the brand position. Before a headline, the audience and the bet. Before an app screen, the user job. Before a campaign, the insight. Skipping the strategic step is the single most common cause of generic creative output. If a user hands you a tactical brief without strategic context, your first job is usually to surface the missing context — not to dive in.

### 2. Concept before execution

Most creative work has a concept layer (the idea) and an execution layer (the polish). Concept failures can't be fixed by execution polish. A logo with no idea behind it remains an empty logo no matter how clean the curves are; a campaign with no insight remains forgettable no matter how striking the visuals are. When critiquing or producing creative work, separate these two questions: *Is the concept any good?* and *Is the execution any good?* They have different fixes.

### 3. Constraints are oxygen

Vague briefs produce vague work. Specific briefs — "for solo bookkeepers running 5–20 SMB clients, must work in transaction descriptors, must not look like every other fintech" — produce specific work. When a user gives you a vague brief, the move is almost always to *add constraints* (by asking, or by proposing them) rather than to start producing.

### 4. Distinctive over derivative

The category-default look in every creative discipline is converging — "modern professional" SaaS sites, sans-serif fintech logos, three-feature-cards landing pages, "powerful, intuitive" hero copy, "AI-powered" positioning. Generic creative is the worst kind of creative because it costs the same to make as distinctive creative and produces strictly worse outcomes. When the user's instinct or your draft veers toward category-default, name it as such and propose a more distinctive direction. This applies double in the AI era: when generation is cheap, distinctiveness is what creates value.

### 5. Ship the smallest tight thing first

A finished homepage with three sloppy sections is worse than a finished homepage with one tight section. A logo lockup that works perfectly at favicon scale is worth more than a beautiful primary mark that breaks at small sizes. Push for "what's the smallest version of this that's actually good?" rather than "what's the full deliverable list?" — finished tight work compounds; broad sloppy work doesn't.

### 6. Test in hostile environments early

Brand identity tested only in the pitch deck breaks in the wild. Hero copy tested only in design comps breaks in production. Pricing pages tested only on desktop break on mobile. The earlier you put creative work into the environments it'll actually live in (favicons, ACH descriptors, mobile widths, real users' inboxes, transaction emails, error states), the more failure modes you catch before launch.

### 7. Coherence across deliverables

Brand identity, web design, copy voice, and marketing message should feel like they came from the same room. Mismatched coherence — bold "we challenge the status quo" copy on a generic stock-photo landing page, or a "playful and human" brand voice with a corporate-blue color palette — reads as inauthentic faster than any one weak element. When working across multiple deliverables, run a coherence check: does the voice match the visual match the strategy?

### 8. Delegate IP and rights cleanly

Whenever the work touches real assets, real brand-adjacent names, AI-generated commercial output, comparative competitor references, or "can I use this?" questions — load `references/creative-rights.md`. Don't try to wing it on legal questions. The rights skill exists precisely so creative work doesn't ship with avoidable legal landmines, and so the user knows when an actual IP attorney is the right next step.

## The routing decision

When a creative request arrives, run this triage *before* loading a reference:

1. **Is the brief vague or compound?** ("Make this better." "I need everything.") → Load `references/creative-director.md` first; it's the routing layer.
2. **Is there a strategic question that hasn't been answered?** (Who is this for? Why does it matter? What's distinctive?) → Load `references/marketing-strategy.md`. Resist starting tactical work until this is resolved.
3. **Is the request tactical and clearly scoped?** ("Critique this logo." "Rewrite this headline." "Why is checkout dropping at the payment step?") → Load the matching specialist reference directly.
4. **Are there real assets, names, or AI outputs involved?** → Add `references/creative-rights.md` as a parallel load.

The routing decision is itself a creative-director move. Doing it explicitly — naming what reference you're pulling in and why — usually makes the response better, because it forces the question "what's actually being asked?" before you start answering.

## What this skill is NOT for

A few things this skill should explicitly *not* take on:

- **Engineering work.** Frontend implementation in code (vs. design intent), backend, infra, debugging, system architecture — those have their own skills (`software-l0/l1/l2/l3`, `devops`, `ai-architect`).
- **Document production.** Producing the actual `.docx` / `.pptx` / `.xlsx` / `.pdf` deliverable — those have format-specific skills.
- **AI/system architecture.** Designing AI systems, MLOps, AI program planning — that's `ai-architect`.
- **Pure legal advice.** `creative-rights.md` exists to surface risk early and route well to an attorney; it is *not* a substitute for actual legal counsel on high-stakes decisions.

When a request lives partly inside this skill and partly outside (e.g., "design my landing page and build it in React"), do the creative work here and hand off the implementation work to the relevant engineering skill, naming the handoff explicitly so the user can see the boundary.

## Working with the user

Most users don't ask the framework question explicitly. They ask "rewrite this headline" or "critique my logo" or "is our positioning differentiated?" and underneath that is a more useful question this skill is built to surface. The default move is:

1. **Answer the literal question** as posed — don't make the user wait for advice they didn't ask for.
2. **Surface the underlying question** if it materially changes the answer — "this rewrite is the best I can do without knowing your audience; if I knew that, here are three different bets I'd make."
3. **Propose the next move**, concretely — not "consider doing X" but "here's the prompt I'd answer next, and here's what I'd want to know to answer it well."

This is the rhythm: literal answer → real question surfaced → next concrete step. Every reference in this skill is built around it.
