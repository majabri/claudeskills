# Creative Rights

The legal layer that sits underneath every other creative skill. Brand-identity, digital-design, copywriting, and marketing-strategy all produce things that get *used in commerce* — and the moment something is used in commerce, IP law starts mattering. Most creative-rights problems are cheap to avoid upfront and expensive to fix afterward. The job of this skill is to spot the avoidable problems early and route the unavoidable ones to a real attorney.

> **This is not legal advice.** Claude is not a lawyer; this skill is a sophisticated checklist informed by current US IP practice and recent rulings. For any specific decision involving real money, real launch dates, or real legal exposure, the answer always includes "have an actual IP attorney review this." This skill tells you *when* that's the answer and *how to think about the problem* in the meantime.

## The four IP regimes

Most creative work brushes against four separate bodies of law. They protect different things, in different ways, with different durations. Confusing them is the #1 source of bad assumptions.

| Regime | Protects | Source of right | Duration | Triggered by |
|---|---|---|---|---|
| **Copyright** | Original creative *expression* fixed in tangible form (text, images, music, code, video) | Automatic on creation; registration adds enforcement teeth | Life + 70 years (individual) / 95 years (corporate work-for-hire) | Reproducing, distributing, displaying, performing, or making derivatives of someone else's expression |
| **Trademark** | *Source-identifiers* (names, logos, slogans, sometimes colors / sounds / shapes) used in commerce | Common-law from use; federal registration adds nationwide rights | Indefinite — as long as you keep using it and renew (every 10 years federally in the US) | Using a name / logo / mark that's confusingly similar to an existing one in the same category |
| **Right of publicity** | A person's *name, likeness, voice, persona* | State law (varies by state — California is broadest); some states recognize for celebrities only, some for everyone | Varies; some states extend post-mortem (CA: 70 years) | Using a real person's image/voice/name in a way that implies endorsement or commercial value extraction |
| **Trade dress** | Distinctive *visual look-and-feel* of a product, packaging, or interface that signals brand source | Common-law from use; can register | Indefinite while distinctive and in use | Cloning a competitor's distinctive packaging / store layout / app UI in a way that confuses customers |

The most common confusion is between copyright and trademark. They overlap on logos but answer different questions:

- **Copyright on a logo** = "do I own the artistic expression of this drawing?"
- **Trademark on a logo** = "do I have exclusive rights to use this mark to identify *my* business in this category?"

You can have one without the other. (Crucially: an AI-generated logo can be trademarked even though, under current US law, it can't be copyrighted as a creative work — see the AI section below.)

## The four-factor fair use test

When the question is "can I use this copyrighted thing without permission?" the answer in the US runs through 17 USC § 107 — the four-factor fair-use analysis. Apply it honestly; don't decide your conclusion first.

1. **Purpose and character of the use.** Commercial vs. non-commercial. *Transformative* vs. *substitutive*. Transformative use (commentary, criticism, parody, news reporting, scholarship, or use that adds new expression / meaning / message) leans toward fair use. Pure commercial reproduction leans away. Note: the Supreme Court's 2023 *Warhol v. Goldsmith* decision tightened this — "transformative" requires more than aesthetic difference, it requires a meaningfully different *purpose*.
2. **Nature of the copyrighted work.** Factual / published works → more likely fair use. Highly creative / unpublished works → less likely.
3. **Amount and substantiality used.** Less is better; using the *heart* of the work counts more than raw word/pixel count. Quoting two sentences can fail factor 3 if those two sentences are the punchline.
4. **Effect on the market for the original.** The most important factor in modern doctrine. Does your use *substitute* for the original or harm a licensing market for it? If a rights-holder could plausibly have licensed this use, factor 4 leans against fair use.

Fair use is decided case-by-case. The doctrine is **a defense**, not a permission — meaning even if you're probably right, being sued is itself the cost. For commercial work where the cost of being wrong matters (most launches, most ad campaigns), license rather than rely on fair use. Reserve fair use for genuinely transformative commentary / criticism / parody / education and document your reasoning before publishing.

### Things that are *not* fair use, no matter how the user frames it

- "I gave them credit." Attribution doesn't create permission.
- "I changed it 30%." There is no percentage rule.
- "It's for a non-profit." Helps factor 1 but doesn't decide.
- "It's only for inspiration." If your output is substantially similar, the inspiration framing doesn't matter.
- "It was on the internet." Internet content is generally copyrighted by default.
- "I bought a copy." Buying a copy gives you the copy; not the right to reproduce or display publicly.

## Licensing — what the labels actually mean

Most commercial creative work runs on licensed assets, not fair use. The licensing landscape has specific terms with specific meanings. Get the term right; the difference matters.

### Stock photos / images / video

- **Royalty-Free (RF).** You pay once and can use under the license terms forever, often across multiple projects. *Royalty-free does not mean free.* Most RF licenses limit print run, redistribution, "sensitive use" (alcohol, politics, dating, adult), and commercial vs. editorial use. Read the exact license, especially for high-print-run uses, merchandise, and template / theme use. Standard RF on Shutterstock, Getty's iStock, Adobe Stock, etc., generally covers most commercial use up to a print/impression cap (often 500K).
- **Rights-Managed (RM).** Licensed for a specific use, in a specific medium, region, and time window. More expensive, more controlled, more exclusive. Use when you need exclusivity or for high-stakes campaigns (a billboard, a national TV spot).
- **Editorial-only.** Permission to use in news / commentary contexts. *Cannot be used in advertising or to suggest endorsement.* Common gotcha: a celebrity stock photo licensed editorially used in a marketing email is a clear violation.
- **Extended / enhanced licenses.** Required for merchandise (the photo on a t-shirt for sale), templates resold to others, or unlimited print runs.
- **Model release / property release.** Even after licensing, if a recognizable person is in the image and there's no model release on file, you can't use the image in advertising or in any way that implies endorsement. Same for recognizable private property and many distinctive buildings (e.g., the Hollywood sign, the Eiffel Tower at night, certain stadiums).

### Creative Commons (CC) — read the suffix

CC isn't one license, it's a family. The suffix tells you what's permitted.

- **CC0 / Public Domain.** Use freely, even commercially, no attribution required.
- **CC BY.** Use freely, even commercially, *with attribution*.
- **CC BY-SA** ("ShareAlike"). Same, but derivative works must be released under the same license. Risky for proprietary commercial use.
- **CC BY-NC** ("NonCommercial"). *Cannot be used commercially.* "Commercial" includes most marketing, ads, products. (Note: free-tier Midjourney historically licensed outputs under CC BY-NC — meaning free-tier outputs can't be used commercially.)
- **CC BY-ND** ("NoDerivatives"). Can use as-is, but cannot modify and distribute.
- **CC BY-NC-SA / CC BY-NC-ND.** Combinations of the above.

The two failure modes: (1) using CC BY content commercially without attributing properly (it's a license violation, even though the asset is "free"), and (2) using CC BY-NC content commercially because the user assumed "free" meant "any use."

### Fonts — a category-specific minefield

Font licensing is *the* most commonly violated IP category in creative work because the rules are confusing and the enforcement is increasingly aggressive (Monotype, MyFonts, and others actively scan for unlicensed use).

- **Desktop license.** Use the font in static design files (logos, prints, exports). *Does not* cover web embedding, app embedding, server use, or e-book embedding.
- **Web license** (often pageview-capped). Embed via @font-face on a website. Usually capped by monthly pageviews; exceeding the cap requires a tier upgrade.
- **App license.** Embed in mobile / desktop applications.
- **Server license.** For dynamically rendering text into images on a server (e.g., generated social media cards). Often the most expensive and most-skipped tier.
- **Logo license / extended.** Some foundries require an extra license to use the font *in a logo*, especially a registered trademark. This is a real category — Adobe Fonts and Google Fonts allow it, many premium foundries don't without a buyout.
- **Free for personal use only.** Common on sites like DaFont. Most fonts there cannot be used commercially. Always check the original foundry license, not the download site's blurb.
- **Google Fonts / Open Font License (OFL).** Free for any use, including commercial and embedding. Safe default for most projects.

When in doubt, screenshot the license terms when you download the font and store them with the project assets. If a font is later involved in a dispute, that's the documentation you need.

### Music

The most-licensed asset in marketing. Music has *two* copyrights, both of which need clearance:

- **Composition / publishing rights.** The song itself (notes, lyrics). Held by composer / publisher.
- **Sound recording / master rights.** The specific recording of the song. Held by the recording artist / label.

For most uses you also need:

- **Sync license.** To synchronize music with visuals (video, ads, social). From the publisher.
- **Master use license.** To use a specific recording. From the label.
- **Mechanical license.** To reproduce the composition in audio products.
- **Performance rights.** Public performance — usually handled via PROs (ASCAP, BMI, SESAC, GMR).

For a TikTok ad with a popular song, you generally need both a sync license (publisher) and a master use license (label). Posting a popular song under a brand video without these = textbook infringement, no matter how short the clip. Use **production music libraries** (Artlist, Musicbed, Epidemic Sound, AudioJungle, Soundstripe) for safe royalty-free music with bundled sync rights, or commission original composition. "I only used 7 seconds" is not a defense.

### Software / code

- **MIT / BSD / Apache 2.0** — permissive, generally safe for commercial use; check attribution requirements.
- **GPL / AGPL** — copyleft. Using GPL code in proprietary software can require open-sourcing your derivative work. Read carefully before pulling GPL components into a commercial product.
- **Proprietary / "free for personal use" / source-available.** Read the actual license; don't assume.

## Trademark clearance

Before launching a name (company, product, feature), run a clearance process. The cost is low; the cost of launching a name that gets a cease-and-desist three months later is large.

The clearance ladder, in order:

1. **Knockout search.** Search USPTO TESS (now also accessible via search.uspto.gov), EUIPO eSearch, and the relevant national registries. Check the exact mark and obvious phonetic / visual variants in the same Nice classes (categories) as your goods/services. Search Google for the name + your category. Search domain availability and key social handles. Most disqualifying conflicts surface in this pass.
2. **Common-law search.** A mark doesn't have to be federally registered to bind you. Look for unregistered (common-law) use of similar marks in your industry. Industry directories, Crunchbase, app stores, GitHub, and AngelList are good sources.
3. **Likelihood-of-confusion analysis.** A formal trademark conflict isn't "same word"; it's "likely to confuse a reasonable consumer in the same market." Factors include similarity of the marks (sound, sight, meaning), similarity of goods/services, channels of trade, sophistication of buyers, evidence of actual confusion, intent. *"Different industry"* often saves you (Apple Records vs. Apple Computer co-existed for decades) — but tech and consumer brands are increasingly broad in scope.
4. **Full clearance opinion from a trademark attorney.** For any name with material commercial value (you're putting a logo on it, building a website around it, spending on marketing), pay a trademark attorney for a real clearance opinion before launch. The cost is usually a few thousand dollars; it can save you a forced rebrand later.

### The five categories of distinctiveness

Mark strength varies by how distinctive the mark is. Stronger marks get stronger protection.

- **Fanciful** — invented words (Kodak, Xerox, Verizon). Strongest.
- **Arbitrary** — real word with no relation to product (Apple for computers, Amazon for e-commerce). Very strong.
- **Suggestive** — hints at the product without describing it (Netflix, Greyhound, Coppertone). Strong, common middle ground.
- **Descriptive** — describes the product or feature ("Cold and Creamy" ice cream). Weak; not registrable on the Principal Register without proven secondary meaning.
- **Generic** — the common name for the product itself ("Bicycle" for bicycles). *Never* registrable; even strong marks can become generic and lose protection (escalator, thermos, aspirin in some jurisdictions, dumpster).

Practical implication: when naming, push for fanciful / arbitrary / suggestive. Resist descriptive names — they feel intuitive but produce a weaker, harder-to-defend trademark.

## Right of publicity and persona use

Using a real person's name, likeness, voice, persona, or identifiable characteristics in commercial work without permission is a separate liability from copyright. Right of publicity:

- Applies to celebrities and (in many states) ordinary people.
- Is governed by *state* law in the US — California, New York, and Indiana are the most aggressive.
- Survives death in some states (CA: 70 years post-mortem).
- Includes voice. Bette Midler v. Ford and Tom Waits v. Frito-Lay established that a "soundalike" of a recognizable artist used in advertising can violate right of publicity even when the actual recording isn't used.
- Applies to AI-generated soundalikes / lookalikes / "deepfakes" used commercially. Tennessee's ELVIS Act (2024) and several other state laws now explicitly cover AI-generated voice clones and digital replicas.

Practical rules:

- Never use a celebrity's image, name, or voice in advertising without a signed endorsement / appearance deal.
- Never use a soundalike intended to evoke a specific artist without legal review.
- For ordinary people in user-generated content / case studies / testimonials, get a signed model release covering the specific use.

## Comparative advertising and competitor references

Mentioning a competitor by name in marketing is legal in the US (and is sometimes excellent strategy), but it has guardrails:

- Statements must be **truthful, substantiated, and not deceptive.** False or misleading comparative claims expose you to Lanham Act false-advertising claims.
- Use the competitor's mark only **as needed** to make the comparison (nominative fair use). Don't use their logo gratuitously, and don't imply endorsement or affiliation.
- Don't disparage in ways that imply false facts. "Faster" needs proof; "the worst" without specifics is a problem.

UK / EU jurisdictions are more restrictive on comparative advertising. If launching in those markets, get jurisdiction-specific review.

## AI authorship and rights — the current (2026) landscape

The AI/IP landscape shifted significantly between 2023 and 2026 and is still moving. Current US doctrine, accurate as of April 2026:

### Copyright in AI-generated work

- **Pure AI output is not copyrightable in the US.** *Thaler v. Perlmutter* — affirmed by D.C. Circuit (March 2025), Supreme Court denied cert (March 2, 2026) — confirms that the Copyright Act requires human authorship. A work autonomously generated by an AI from a prompt has no copyright in the US.
- **AI-assisted output *with sufficient human creative contribution* can be registered.** The US Copyright Office's "Copyright and AI" Part 2 report (January 2025) reaffirmed this. Selecting, arranging, modifying, or substantially editing AI output can produce copyrightable human-authored elements; the registration covers only those elements, not the underlying AI-generated material.
- **Prompts alone don't qualify.** The Copyright Office's current position is that a text prompt — even an elaborate one — does not, by itself, give the prompter authorship over the resulting image. Iterative editing, compositing, painting over, or substantial human modification of the output strengthens the case.
- **Allen v. Perlmutter** (still pending in federal court as of early 2026) is testing whether iterative prompting with significant human curation crosses the threshold. Watch this case — the outcome may move the line.

### Trademark in AI-generated work

This is where many users get the wrong answer. **Trademark protects source-identifying use in commerce, regardless of who or what authored the underlying design.** The USPTO trademark application has no field for "was this made by AI."

- An AI-generated logo *can* be federally registered as a trademark if (a) you use it in commerce as a source identifier, (b) it's distinctive (not generic / merely descriptive), and (c) it doesn't conflict with existing marks.
- The trademark protects the mark's *commercial role*. It doesn't grant copyright in the artwork itself.
- Practical implication: you can prevent competitors from using a confusingly similar mark, but you may not be able to prevent random third parties from copying the underlying *image* (because the image itself isn't copyrighted).
- Recommendation for high-value logos: have a human designer substantially modify or rework the AI output. This adds copyrightable human-authored elements and strengthens both copyright and trademark posture.

### Training data and AI outputs — the rulings to know

- **Bartz v. Anthropic** (N.D. Cal., 2025): Judge Alsup ruled that training LLMs on legally acquired books was "quintessentially transformative" and fair use, but downloading from pirate libraries was not. Anthropic settled the piracy class for ~$1.5B (final approval hearing scheduled May 14, 2026). Establishes: training on lawfully sourced material has a strong fair-use case; piracy doesn't.
- **Kadrey v. Meta** (N.D. Cal., 2025): Judge Chhabria found training fair use on the facts before him but emphasized the ruling was narrow and fact-specific, particularly on factor 4 (market harm). Plaintiffs' failure to show market harm was decisive.
- **Disney/Universal v. Midjourney** (filed June 2025, trial late 2026): Major studios allege Midjourney trained on copyrighted character images and that outputs reproduce protected IP. Outcome could materially change AI image-tool commercial-use posture. Until resolved, treat AI-generated outputs *that resemble identifiable copyrighted characters* (Marvel, Disney, Studio Ghibli, branded characters, named celebrities) as high-risk regardless of the platform's terms.

### Tool-specific terms

Each AI tool has its own ToS that allocates rights. Read the actual terms — they change. As of early 2026:

- **Midjourney (paid tiers):** "You own all Assets You create with the Services to the fullest extent possible under applicable law." Translation: Midjourney assigns you whatever rights they have, but US law may not grant copyright over the unmodified output. **Midjourney free tier:** outputs licensed CC BY-NC — *not commercial-use-safe*.
- **OpenAI (DALL-E, GPT image):** Outputs assigned to user; commercial use permitted under enterprise / API terms with content moderation.
- **Adobe Firefly:** Trained on Adobe Stock + licensed / public-domain content. Adobe offers IP indemnification for enterprise customers — meaningful commercial assurance.
- **Stable Diffusion / open models:** Output rights generally with the user, but the underlying model's training data (especially LAION-derived) carries unsettled risk.

### Practical AI-rights checklist

Before deploying AI-generated creative output commercially:

1. Confirm the platform terms grant commercial rights for your tier.
2. If the output resembles known IP (characters, celebrities, branded designs), *don't ship*. Re-prompt or hire a human.
3. For high-value brand assets (logos, primary brand imagery), have a human designer substantially modify the AI output — for both legal and quality reasons.
4. Document the prompt, the iterations, and the human modifications. If you ever need to register or defend the work, that record is your evidence of human authorship.
5. Disclose AI involvement when registering with the Copyright Office (it's required); don't disclose unprompted to USPTO for trademarks (their forms don't ask).
6. For enterprise-scale commercial use, prefer tools that offer IP indemnification (currently: Adobe Firefly enterprise, some Microsoft Copilot tiers, some Getty Images AI products).

## Asset clearance — a workflow

For any commercial project that uses outside assets, run this checklist before launch:

1. **Inventory.** List every external asset: images, fonts, music, code, video, illustrations, icons, voiceover, names mentioned.
2. **Source.** For each asset, where did it come from? Stock site / commissioned / licensed from owner / AI-generated / "found online" (red flag).
3. **License.** What license covers it, and what's the exact scope (commercial, region, duration, print run, derivative work, sublicense)?
4. **Releases.** Any recognizable people in the asset? Any recognizable property? Have you got signed releases?
5. **Trademark proximity.** Any names / logos used? Any uncomfortably close to existing marks in your category?
6. **AI assets.** For any AI-generated content used commercially: is the platform's commercial license clear, and does the output resemble protected IP?
7. **Documentation.** Save licenses, releases, and source links with the project. If a dispute surfaces three years later, the documentation is what protects you.

## Common failure modes

- **"It's on the internet, so it's free."** The single most common and most expensive misunderstanding. Internet content is copyrighted by default.
- **"I'll just blur the logo."** Blurring identifiable trademarks doesn't cure use of the underlying image; it sometimes makes things worse by signaling consciousness of the issue.
- **Using a stock photo with a recognizable person in advertising without checking the model release.** Standard stock licenses generally don't cover endorsement-implying use without releases.
- **Using "free for personal use" fonts in commercial work.** A massive class of font-licensing violations.
- **Using popular music in social media ads.** Platform-provided "commercial-safe" libraries are safe; popular tracks generally aren't, even briefly.
- **Mistaking a domain registration for a trademark right.** They're independent — you can hold the domain and still infringe a trademark by using the name commercially.
- **Choosing a descriptive name for a product because it's "clear."** Descriptive marks are weak and often unregistrable. Push toward suggestive / arbitrary / fanciful.
- **Comparison ad with unsubstantiated claims about a competitor.** "Twice as fast" without data is a Lanham Act problem.
- **Treating AI outputs as fully owned.** AI ownership is a *trademark / contract* posture in the US, not a copyright one; design accordingly.
- **Assuming the AI tool's "you own it" language means US copyright.** It generally means "we assign whatever we have"; what they have under US law may be nothing.
- **Using AI output that closely resembles a recognizable existing character or style.** Even if the platform allows it, the rights-holder's position is not bound by the platform's ToS.
- **Skipping clearance because "we're small."** Small-company brand disputes are common precisely because small companies skip clearance. The cost of a forced rebrand at the wrong moment is far higher than the cost of clearance.

## Working with the user

Most users don't ask the IP question explicitly — they ask a creative question that has IP implications underneath. Surface the rights issues proactively when they're material. The diagnostic moves:

1. **What's the asset, and where does it come from?** "Use this photo" / "this song" / "this name" / "this AI-generated logo." Each has a different rights regime.
2. **Is it being used commercially?** Editorial / educational / parody is a different regime than ads / marketing / merchandise / products.
3. **Is the use proximate to someone else's IP?** Real brands, real people, real characters, real songs — even adjacent — raise the risk profile.
4. **What's the cost of being wrong?** A small blog post is one risk; a Super Bowl ad is another. Calibrate the rigor.

When the work is high-stakes and the question is non-trivial, the right answer almost always includes: "this needs an actual IP attorney to bless before launch." Saying so isn't a copout — it's the right answer. The skill's job is to set up that attorney conversation well, not to substitute for it.

When the user pushes for a definitive yes/no on a fact-specific legal question ("can I use this song"), don't manufacture certainty you can't have. Lay out the considerations, identify the risk vectors, and recommend the next actionable step (a license inquiry, a clearance search, a call with counsel). Confident-sounding wrong answers in IP are very costly.

## When to hand off to other skills (or to a real lawyer)

Hand back to other creative skills:

- The rights question is resolved; now the user needs to actually make / write / design something → return to `brand-identity`, `digital-design`, `copywriting`, or `marketing-strategy`.
- The user is choosing between names from a marketing standpoint, not just a legal one → `marketing-strategy` (positioning) and `brand-identity` (naming craft) take the lead with creative-rights as input.

Hand off to a real attorney (not just "consider a lawyer," but specifically recommend one) when:

- The user is launching a product / company / brand commercially and the name / mark hasn't been cleared.
- The user is pursuing federal trademark registration (do not file pro se for marks with material commercial value).
- The user is using a real person's name / likeness / voice in commercial work.
- The user is using third-party copyrighted material (music, images, video, code) and relying on fair use rather than a license.
- The user has received a cease-and-desist, takedown notice, or DMCA notice.
- The user is making comparative claims about competitors involving substantiable facts.
- The work involves AI-generated output for high-value commercial use and the user wants to register or defend rights in it.
- The user is operating internationally (IP regimes vary substantially across jurisdictions; UK, EU, China, Japan all have meaningful differences from US doctrine).
- The user is acquiring, assigning, or licensing IP — contracts here are not a place to wing it.

For these, the skill's job is to make the case crisply, name the regime that's relevant, and frame the conversation so the user goes to counsel with a clear question rather than a blank slate. That's faster, cheaper, and produces better legal outcomes than handing the lawyer an unscoped problem.
