# Digital Design

The job is to design interfaces that:

1. **Communicate hierarchy at a glance.** What matters most is most prominent. The user knows where to look without thinking.
2. **Reduce friction** for the actions users actually take. The next-most-likely action is the most reachable.
3. **Hold up across states and contexts.** Empty, loading, error, dense data, tiny screens, large screens, dark mode, accessibility tools.
4. **Feel like *something specific*** — not the AI/SaaS-default house style of a thousand startups.

Most design failures are not "the colors are wrong." They're either *strategy failures* (designing the wrong thing at the wrong altitude for the wrong user) or *systemic failures* (no consistency across screens, no scale for type, no design tokens, no thought about edge cases).

## Before you open the design tool

### Know what kind of interface this is

The principles overlap but the priorities differ:

| Surface | Primary job | Watch out for |
|---|---|---|
| **Marketing site / landing page** | Persuade in 5 seconds, convert in 30 | Generic hero ("modern", "powerful", "the future of X"), too much text above the fold, no concrete proof |
| **Application UI** (used repeatedly) | Make routine tasks fast and pleasant | Decorative noise, novelty that costs efficiency, hidden states |
| **Dashboard / data UI** | Surface signal, hide noise, support investigation | Charts as decoration, overload, no information density |
| **Forms / checkout / onboarding** | Reduce drop-off at every step | Asking for data you don't need, opaque progress, weak error states |
| **Marketing email / notification** | One specific action | Multiple CTAs, paragraph copy where bullets would do |

If you don't know which kind of surface you're designing for, ask before you start. The same "good design" looks different across these.

### Know the user, the moment, and the action

Before any layout decision, you need:

- **Who** is this for, in plain terms?
- **What state are they in** when they arrive? (Curious / motivated / frustrated / time-pressed / confused)
- **What single thing** do you want them to do or know on this screen?

A common bug: designing the third screen (preferences, settings, advanced features) before the first screen (the moment of arrival) is solid. Design in priority order — the surface most users see most often gets the most attention.

### Steal a specific reference, not a generic vibe

The single most reliable way to avoid generic-looking design is to pick a real, specific reference and steal *intentionally* — the type system from one place, the density philosophy from another, the photography direction from a third. Do this *before* opening Figma.

"Make it look modern" produces nothing. "Make the type feel like Linear's product UI, the marketing density like the New York Times homepage, and the color discipline like Apple HIG" gives every subsequent decision a north star.

## The universal layout principles

These apply to almost every screen you'll design, marketing or product.

### 1. Hierarchy is communicated by contrast, not by adornment

Bigger / heavier / brighter = more important. Smaller / lighter / dimmer = less important. The most common amateur error is making *everything* important — every button is high-contrast, every label is the same size as every value, every section header competes with every other section header.

Working principle: at each scale (page, section, component), there should be exactly one "loudest" thing. Demote everything else. If two things must be equally loud, they're probably one thing.

### 2. Spacing is information

Generous spacing communicates "this is a thing, attend to it." Tight spacing communicates "these belong together." Irregular spacing communicates "this is broken."

Work on a single spacing scale (4, 8, 12, 16, 24, 32, 48, 64 px is standard; pick one and stick to it). Never use ad hoc values like 13 or 27. *Most amateur designs are not "ugly" — they're spaced inconsistently, and the eye reads the inconsistency as broken.*

### 3. Type is the workhorse — get it right first

Most of any interface is type. Get the typography system right and 60% of the design is done:

- One display face for headlines/marketing moments (often), one text face for everything else (often the same family with a different weight/optical size).
- A type scale of 6–8 sizes, paired with line-heights and weights. No ad hoc sizes.
- A clear hierarchy: H1, H2, H3, body, caption, label — each used consistently.
- Body text: 14–16px on web, 17px on iOS, 14sp on Android (with adjustments for accessibility). Line-height 1.5–1.7× for long text, tighter (1.2–1.3) for headlines.
- Measure (line length): 50–75 characters per line for body text. Wider lines fatigue readers; narrower lines feel cramped.

### 4. Color is a system, not a vibe

You should have:

- A **neutral scale** (8–12 steps from near-white to near-black) that does the bulk of the work — backgrounds, text, dividers, surfaces.
- A small **brand color set** (primary + 1–2 accents) used for emphasis and brand moments, not as background workhorses.
- A **semantic set** for product UI (success / warning / danger / info), each with a quiet variant for backgrounds and a loud variant for icons/text.
- **Dark-mode pairs** designed in parallel from the start, not retrofitted.

Saturated brand colors used everywhere produce exhausting interfaces. Use them as accents, not workhorses. See also `brand-identity`.

### 5. Density should match the user, not flatter the designer

Marketing sites tend toward generous whitespace — the user is browsing, persuasion needs breathing room. Productivity tools used 8 hours a day tend toward density — the user wants to fit information on screen and read fast. Linear, Notion, GitHub, Figma, and Stripe's dashboard all reward density when you live in them.

A common failure: applying marketing-page density to a productivity app. Beautiful in a screenshot, miserable to use. Match density to the user's relationship with the surface.

### 6. Design every state, not just the happy state

Every screen has at least these states:

- **Empty** — first-time user, no data yet (the most under-designed state)
- **Loading** — slow connection, partial data
- **Loaded with one item, with many items, with too many**
- **Error** — what went wrong, what to do about it
- **Disabled / read-only**
- **Dark mode**
- **Accessibility states** — focus, screen reader, reduced motion

A screen that's only designed for "loaded with three perfect items" will fall apart in production. Design the empty state and the error state with as much care as the happy path — they're often where users actually live.

### 7. Accessibility is the floor, not a polish task

WCAG 2.1 AA is the practical baseline. Concretely:

- **Contrast:** 4.5:1 for normal text, 3:1 for large text and UI components against their background. Use a contrast checker on every text/background pair.
- **Keyboard navigation:** every interactive element is reachable via Tab, with a visible focus indicator. Modal dialogs trap focus correctly.
- **Screen readers:** images have alt text (or are marked decorative), buttons have meaningful labels, form fields have associated labels, ARIA only where standard semantic HTML can't carry the meaning.
- **Motion:** respect `prefers-reduced-motion`; never use motion as the sole carrier of meaning.
- **Color:** never use color alone to communicate state (red text + an icon, not red text alone).

Accessibility is also commercial — in regulated markets (US ADA, EU Accessibility Act), inaccessible UIs are a litigation risk.

## Marketing pages and landing pages

Marketing pages have one job per page: persuade a specific audience to take a specific next action. Most marketing pages over-promise breadth and under-deliver specificity.

### Above the fold, you have ~5 seconds

The viewer should know in 5 seconds:

- **What this is** (category clarity — "marketing automation tool," not "the future of customer engagement")
- **Who it's for** (specific audience — "for B2B SaaS sales teams of 50+", not "for modern teams")
- **What's different** (one specific point of differentiation, not a generic benefit)
- **What to do next** (one primary CTA, secondary clearly subordinate)

If the hero says "Powerful. Modern. Built for the future." the page has failed before scrolling. That's positioning vacuum-filler. See `marketing-strategy` for how to derive a real hero.

### Page structure that works

A reliable structure for product/SaaS landing pages:

1. **Hero** — clear what + who + why-different + primary CTA. One sentence, one clear visual.
2. **Social proof** — logos, named customers, key metric, *immediately* after the hero. Establishes credibility before more claims.
3. **Problem / status quo** — what is the user dealing with today? Show you understand before you sell.
4. **The new way** — your solution, in concrete terms. Not "platform" — actual screenshots / specific capabilities.
5. **Proof** — testimonials with names + titles + photos, case study summaries, real numbers, demos.
6. **Objection handling** — pricing, security, integrations, common questions answered without being asked.
7. **Final CTA** — one specific next step, friction reduced (no credit card, free tier, sample data).

Resist the urge to put every feature on the page. A landing page is a persuasion tool, not a documentation surface. If users want depth, link to it.

### Marketing-page anti-patterns

- **Hero with a stock-photo abstraction** ("flying through space" / "happy diverse stock people pointing at laptop"). Use a real product screenshot or a specific concept illustration.
- **Three-column "feature trio"** with vague icons and generic benefits. Replace with one specific demonstration.
- **CTA copy that's "Get started"** (vague) or "Submit" (terrible). Use the action: "Try the demo," "Book a call," "Start a free trial."
- **Endless scroll with no narrative arc.** A long page is fine if every section moves the persuasion forward; not if it's just stacked sections of the same shape.
- **Every section the same shape** (full-bleed, image-left/text-right, repeat). Vary rhythm to keep attention.

## Application / product UI

Application UI is judged differently than marketing. The user has *committed* — they've signed up, they have a job to do. Your job is to get out of their way while making the right action obvious.

### The first screen problem

The most-used screen in any product is usually the first screen after login. Treat it as if the user has 60 seconds before deciding the product is worth using:

- The next obvious action is the most prominent.
- The status of their account / data / task is visible without effort.
- Empty states are *helpful* (show what's possible, give a starter), not just blank.
- Loading states show progress, not just spinners.

### Design tokens and design systems

For any product UI bigger than a single screen, work in a token-driven system from day one. Tokens are named design decisions — instead of `#3B82F6`, you use `color.brand.primary` or `color.action.default`. The structure that works:

- **Primitive tokens** — raw values (`color.blue.500 = #3B82F6`, `space.4 = 16px`).
- **Semantic / alias tokens** — use-cases that point to primitives (`color.action.default → color.blue.500`, `text.body → color.gray.900`). This is where dark mode lives — the alias points to a different primitive in dark mode.
- **Component tokens** — specific to a component (`button.primary.background → color.action.default`).

This three-tier model (primitives → aliases → components) is now the de-facto standard at IBM Carbon, Salesforce Lightning, Adobe Spectrum, and most mature systems. It pays off the moment you need to support multiple brands, themes, or accessibility variants.

### Components and atomic design

Brad Frost's atomic design model is still the cleanest way to organize a component library:

- **Atoms** — buttons, inputs, labels, icons, tokens
- **Molecules** — input + label + helper text, search bar, data row
- **Organisms** — header, sidebar, table, form section
- **Templates** — page-level layouts
- **Pages** — concrete templates with real data

Build atoms first, ruthlessly. A weak atom (button without a focus state, input without an error state) will infect everything built on top of it.

### Common product UI failure modes

- **Decoration in places that need clarity.** Animated gradients on dashboards, illustrations crowding data tables, hover effects on every element. Restrain decoration to brand moments.
- **Mystery meat navigation.** Unlabeled icons, hover-only menus, gestures with no discoverability.
- **Confirm-everything dialogs.** Annoying for routine actions, ineffective for actually-destructive ones (users learn to dismiss without reading). Save them for irreversible operations and provide undo for everything else.
- **No information density on data screens.** Spacious dashboards look great in marketing screenshots and feel hollow in daily use.
- **States that pretend to be the happy state.** Loading skeletons that look like real content, empty states that look like loaded states, error states that look like empty states.

## Design system fundamentals

If the user is building or maintaining a design system:

### Start with foundations, not with components

The order that produces a working system:

1. **Voice and design principles** (3–5 statements that arbitrate decisions when reasonable people disagree)
2. **Color system** (primitives → aliases → semantic; light + dark from the start)
3. **Type system** (faces, scale, hierarchy)
4. **Spacing and layout grid** (one scale; one grid)
5. **Iconography** (one set, consistent style and weight)
6. **Foundational atoms** (button, input, link, heading, body) with all states designed
7. **Common molecules and organisms**
8. **Documentation** alongside everything — usage, when-to-use, when-not-to-use, accessibility notes, code reference

Skip foundations and you'll be patching forever. Build foundations carefully and components compound in value.

### Versioning, governance, and sync

Design systems drift fast without governance. Even basic discipline pays off:

- Version the system (semver works fine).
- One source of truth (Figma variables → code via Style Dictionary, Tokens Studio, or similar). Manual hex-typing in code is where drift starts.
- Clear contribution path for new components — who proposes, who reviews, who decides.
- Audit trail for breaking changes; communication channel for adopters.

A small system maintained well beats a large system maintained badly.

## Critique and review

When critiquing a design (yours or someone else's), use this lens in this order:

1. **Strategy** — Is this the right thing to design at all? Is the surface, audience, and primary action right?
2. **Hierarchy** — Can a stranger tell what's most important in 2 seconds?
3. **Information architecture** — Is the right content grouped correctly? Is sequence right (top to bottom for marketing, frequency-of-use for product)?
4. **Type system** — Is the type scale clean and used consistently?
5. **Color system** — Is the palette structured? Contrast adequate? Brand color used as accent or as workhorse (and is that intentional)?
6. **Spacing** — Is the spacing on a scale and consistent? Are related things grouped, unrelated things separated?
7. **States** — Empty, loading, error, edge cases all designed?
8. **Accessibility** — Contrast, keyboard, screen reader, reduced motion?
9. **Distinctiveness** — Could you swap this for three competitors' UI? If yes, the brand is missing.

Spend the most time on 1–3 (strategy / hierarchy / IA). Polish on 4–7 means nothing if 1–3 are wrong.

## When to hand off to other skills

- The brand identity (logo, colors, fonts) needs to be defined or revisited → `brand-identity`.
- The page or UI is structured but the **words** need work (headlines, body copy, CTAs, error messages) → `copywriting`.
- The page is structurally fine but the **strategic story** isn't landing (positioning, audience targeting) → `marketing-strategy`.
- Questions about using fonts, images, illustrations, or icons in commercial UI without licensing risk → `creative-rights`.
