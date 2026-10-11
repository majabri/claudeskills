# AI Video Tool Prompt Reference

Each AI video tool has its own quirks. Read the relevant section when the user names a specific tool. If they haven't picked one, default to **Sora** or **Veo 3** for realistic content with people, **Runway** for stylized/abstract, **HeyGen** for talking-head/avatar work.

## Sora (OpenAI)

**Strengths:** Photorealistic, strong character coherence within a single generation, good with complex scenes, handles dialogue lip-sync reasonably.

**Prompt style:** Long-form, descriptive, comma-separated clauses. Reads almost like a screenplay shot description.

**Format:**
```
[Shot type] of [subject with detailed physical description], [action/expression], in [setting with lighting], [camera movement], [style descriptors], [aspect ratio if 9:16].
```

**Tips:**
- 100–250 words per scene works well; longer can confuse it
- Be explicit about lighting time of day ("golden hour late afternoon")
- For realistic people, name camera lens equivalents ("shot on 35mm, shallow depth of field")
- Avoid telling it "the same person as before" — it doesn't work. Repeat the full character description every scene.
- Vertical: append "9:16 vertical aspect ratio"

**Length limits:** Currently up to 20 seconds per generation in most tiers. Plan one Sora generation per scene.

## Veo 3 (Google)

**Strengths:** Excellent for realistic dialogue with native audio generation, strong physics, good handling of complex scenes.

**Prompt style:** Similar to Sora but responds especially well to explicit dialogue lines in quotes.

**Format:**
```
[Shot type] of [character description]. [Setting + lighting]. [Action]. The character says: "[dialogue line]". [Camera and style].
```

**Tips:**
- For dialogue scenes, put the line in quotes inside the prompt — Veo handles voice generation
- Specify accent/tone ("warm American male voice, late 30s")
- Native audio means you may not need a separate voiceover step
- Strong with realistic interiors and outdoor scenes

## Runway (Gen-3 Alpha / Gen-4)

**Strengths:** Stylized output, motion graphics, abstract concepts. Less reliable for photorealistic humans.

**Prompt style:** Shorter, more cinematic. Image-to-video with a reference frame works better than text-only.

**Format:**
```
[Visual description, ~50–80 words]. Camera: [movement]. Style: [aesthetic keywords].
```

**Tips:**
- Generate a still image first (Midjourney, DALL-E, or Runway's image tool), then use image-to-video
- Best for B-roll, transitions, abstract sequences, atmospheric shots
- Less good at: dialogue scenes, character consistency across multiple clips
- Length: 5–10s per generation typically

## Kling

**Strengths:** Strong physics, good motion realism, handles Asian faces especially well. Good free tier.

**Prompt style:** Concise, action-focused. Less is more.

**Format:**
```
[Subject + action], [setting], [camera movement], [style].
```

**Tips:**
- Keep prompts under 100 words
- Focus on what's *happening* (motion) more than appearance
- Strong with image-to-video; weaker with text-only
- Good for action sequences and dynamic shots

## Pika

**Strengths:** Stylized, anime-friendly, fast iteration, good motion controls.

**Prompt style:** Short and punchy. Use motion brushes and camera controls in the UI rather than describing in prompt.

**Format:**
```
[Brief subject + action], [style keywords].
```

**Tips:**
- Best for: stylized content, animation, social media-friendly motion
- Use camera controls in the UI rather than describing motion in text
- Good for music videos, abstract content, lifestyle B-roll

## HeyGen / Synthesia (avatar-based)

**Strengths:** Fastest path to a "talking head" video. Pick an avatar, paste a script, get a video in minutes. Good for explainer content, training, marketing.

**Prompt style:** N/A — these aren't prompt-driven. Provide:
1. Avatar selection (built-in or custom)
2. Script with exact words to be spoken
3. Background (stock or upload)
4. Voice selection

**Tips:**
- For our skill output: skip prompts entirely. Provide a clean script formatted as `[Avatar 1]: line. [Avatar 2]: line.`
- Best for: educational, corporate, explainer videos with one or two speakers
- Weak for: scenes with action, multiple characters interacting physically, anything cinematic
- Background music is added in their UI

## Cross-tool: character consistency

The hardest problem in AI video. Strategies:

1. **Repeat the full character description in every prompt.** Don't say "the same father" — re-paste the whole thing.
2. **Use a reference image.** Generate a character portrait first (Midjourney, DALL-E), then use image-to-video so the character locks in.
3. **Lock seed/style** where possible (Runway, Pika support this).
4. **Accept some drift** for ambitious projects. Plan tight cuts so small inconsistencies between shots are less visible.

## Cross-tool: aspect ratio cheat sheet

| Platform | Aspect ratio | How to specify |
|---|---|---|
| TikTok / Reels / Shorts | 9:16 vertical | "9:16 vertical aspect ratio" |
| YouTube standard | 16:9 horizontal | "16:9 widescreen" or default |
| Instagram feed | 1:1 square or 4:5 portrait | "1:1 square" or "4:5 portrait" |
| LinkedIn | 1:1 or 16:9 | Either; 1:1 plays better in feed |
| Twitter/X | 16:9 | "16:9 widescreen" |

## Cross-tool: things that consistently fail

Avoid in prompts — these cause artifacts or hallucinations:
- Hands doing complex things (typing, holding small objects, sign language)
- Reading text on screens or signs (text generation is unreliable)
- Specific recognizable people, brands, or logos
- Long uncut conversations between multiple people
- Complex group choreography (dancing, sports)
- Mirrors, reflections, glass that should reflect the room

If the storyboard calls for any of these, plan workarounds (cut away, suggest the action, use B-roll).
