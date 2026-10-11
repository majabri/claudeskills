---
name: short-form-video-package
description: Use this skill whenever the user wants to create, make, or produce a video of any kind — short film, explainer, social media post (TikTok, Reels, Shorts), ad, family scene, message-driven video, storyboard, or anything cinematic. Also trigger when turning an article, message, or written content into a video. Produces a complete production package — illustrated storyboard PDF, ready-to-paste AI video prompts (Sora, Veo, Runway, Kling, Pika, HeyGen), shot list, voiceover script, and direction notes — because Claude cannot render video files directly but CAN deliver everything needed to make one quickly with AI tools or a freelancer. Do NOT skip this skill just because the user asked for "a video" Claude can't render — that's exactly when it's needed.
---

# Short-Form Video Package

## What this skill does

When a user asks to "create a video," Claude cannot actually render an MP4. But the user almost always doesn't care *who* renders it — they want a video to exist. This skill closes that gap by producing a complete production package the user can hand to an AI video tool (Sora, Veo, Runway, Kling, Pika, HeyGen) or a human editor and have a finished video within minutes to hours.

The package includes:
1. **A clear, honest framing** of what Claude can and can't do — set this expectation up front, before producing anything.
2. **A storyboard PDF** with illustrated scenes, dialogue, shot direction, and production notes.
3. **AI video tool prompts** — one block per scene, optimized for the user's chosen tool.
4. **A voiceover/narration script** — ready for tools like ElevenLabs, HeyGen, or human voice talent.
5. **A shot list and direction sheet** — for if the user is filming with humans or hiring a freelancer.

## Step 1: Set expectations honestly

Before doing anything else, tell the user clearly:

> "I can't render a video file directly — no AI video model is available in this environment. What I *can* do is produce a complete production package: a storyboard PDF, scene-by-scene AI video prompts you can paste into Sora/Veo/Runway, a voiceover script, and shot direction. With that, you can have a finished video in 15–60 minutes using an AI tool, or hand it to a freelancer."

Don't bury this. Users get frustrated when they think they're getting a video and instead get a script. Be upfront, then move on confidently.

## Step 2: Gather the minimum you need

Before producing anything, make sure you have:
- **The message or topic** (what's the video about?)
- **Length** — typically 30s, 60s, 90s, 2min, 3min. Default to 60–90s if unspecified for social media content.
- **Tone** — warm, serious, funny, dramatic, documentary, energetic. Default to "warm and natural" if unspecified.
- **Cast/setting** — who's in it, where? Family at home? Single narrator? Two friends? Animated characters?
- **Target platform** — TikTok/Reels/Shorts (vertical 9:16), YouTube (16:9), LinkedIn (1:1 or 16:9). This affects framing.
- **Production path** — does the user want to use an AI video tool, film it themselves, or hand it to a freelancer? This determines which deliverables to emphasize.

If the user gave you a substantial brief already, don't re-ask everything. Use the `ask_user_input_v0` tool sparingly — pick 2–3 questions max, only on what you genuinely can't infer. Common defaults are fine.

## Step 3: Choose what to produce

Match deliverables to the user's path:

| User's path | Primary deliverable | Secondary |
|---|---|---|
| AI video tool (Sora/Veo/Runway) | Scene-by-scene prompts + voiceover script | Storyboard PDF |
| Filming with people | Storyboard PDF + shot list | Voiceover script (if narrated) |
| Hiring a freelancer | Storyboard PDF (this is the "brief") | Prompts as backup |
| Slideshow-style video | PPTX with timed slides + narration | (Use the `pptx` skill in parallel) |
| User unsure | Storyboard PDF + AI prompts (covers most paths) | Voiceover script |

**Default if unspecified:** Storyboard PDF + AI video prompt sheet. Covers ~80% of cases.

## Step 4: Produce the storyboard PDF

Use the `build_storyboard.py` script in `scripts/` as the foundation. The script:
- Generates one page per scene with a flat-illustration thumbnail, dialogue, shot direction, and visual notes
- Adds a cover page with metadata (length, tone, cast, scene count)
- Adds a production notes page (visual style, camera, wardrobe, performance, music, pacing)
- Uses a warm earth-tone palette by default; can be swapped via the `PALETTE` constant

**Don't run the script as-is.** Open it, replace the `SCENES` list with scenes for the user's specific topic, and adjust `PALETTE` if the tone calls for it (e.g., dark/dramatic → cool blue-gray; energetic → bright primary colors).

### Scene structure (each scene needs these fields)

```python
{
    "num": 1,
    "title": "OPENING — A Family Together",
    "duration": "0:00 – 0:10",
    "shot": "Wide establishing shot. Living room, soft afternoon light.",
    "visual": "Warm tones. Slow push-in toward the couch.",
    "dialogue": [
        ("DAD", "Hey kids — we want to talk about something."),
        ("DAUGHTER", "Are we in trouble?"),
    ],
    "direction": "Set a calm, inviting tone. No tension.",
}
```

### Scene count by length

| Video length | Scenes | Seconds per scene |
|---|---|---|
| 30s | 4–5 | 6–8s |
| 60s | 6–8 | 8–10s |
| 90s | 8–10 | 9–11s |
| 2 min | 10–12 | 10–12s |
| 3 min | 12–16 | 11–15s |

### Illustration approach

The script includes basic flat-illustration drawers using ReportLab shapes (rectangles, circles, ellipses) — see `draw_living_room_wide`, `draw_close_dad`, etc. in the example. They're intentionally minimal because storyboards aren't meant to be art — they're meant to communicate framing and blocking. **Don't waste time making the illustrations elaborate.** Stick figures with shirt colors and basic backgrounds are enough.

For each new project, write small drawer functions that match each scene's framing (wide / medium / close-up / two-shot / over-the-shoulder). The pattern is:
- Background color block
- 1–2 environmental elements (window, table, lamp glow)
- Figure(s) as shirt-rectangle + skin-circle + hair shape
- Optional prop (book, plate, phone)

### Output location

Save the PDF to `/mnt/user-data/outputs/<topic>_Storyboard.pdf` and use `present_files` to share it. Use a slug-cased filename like `Responsible_Parenting_Storyboard.pdf`.

## Step 5: Produce AI video tool prompts

If the user is going to use an AI video tool, prompts are the most valuable deliverable. Each prompt should be one self-contained paragraph per scene that includes:

1. **Shot type** (wide, medium, close-up, two-shot)
2. **Subject** with concrete physical detail (age, hair, clothing — keep consistent across scenes)
3. **Action/expression** (what's happening, what emotion)
4. **Setting** with lighting and time of day
5. **Camera movement** (static, slow push-in, handheld, dolly)
6. **Style/mood keywords** (cinematic, warm, documentary, golden hour)
7. **Aspect ratio** if relevant (9:16 for TikTok/Reels, 16:9 for YouTube)

### Example prompt format (Sora / Veo / Runway)

> "Medium close-up of a father in his late 30s, short dark hair, wearing a terracotta sweater, sitting on a navy couch in a warm-lit living room during late afternoon. He speaks gently with a thoughtful expression, making eye contact with someone off-camera. Slow push-in. Cinematic, warm color grade, golden hour lighting through a window behind him. 9:16 vertical, photorealistic, shallow depth of field."

### Tool-specific notes

See `references/ai_video_tools.md` for prompt formatting differences between tools (Sora, Veo 3, Runway Gen-3, Kling, Pika, HeyGen). Read it when the user names a specific tool.

### Character consistency

This is the #1 problem with AI video. Keep one detailed character description and **paste it into every scene's prompt**. Example:

> "Father (consistent across all scenes): late 30s, 5'10", short dark brown hair, light beard, warm brown eyes, wearing a terracotta knit sweater and dark jeans."

Tell the user explicitly: "Paste the character description block at the start of every scene prompt — AI video tools won't remember characters across separate generations."

## Step 6: Produce the voiceover script

Even videos with on-screen dialogue often layer voiceover for narration, intro, or closing. Format:

```
[SCENE 1 — 0:00–0:10] Voiceover (warm, conversational male voice):
"There's something happening with how kids are being raised today…"

[SCENE 8 — 1:14–1:25] Voiceover (closing, slightly slower):
"Parenting isn't about convenience. It's about preparing them for life."
```

Save as a separate `.txt` or `.md` so the user can paste straight into ElevenLabs or HeyGen.

## Step 7: Hand off cleanly

After producing the package, tell the user:

1. **Where each file is** and what it's for
2. **Recommended next step** based on their production path
3. **One specific tool you'd suggest** (don't list 8 — pick the best fit and mention 1 alternative)
4. **An offer to iterate** — refine a specific scene, change tone, generate prompts for a different tool

Don't end with "Let me know if you have questions!" — end with a concrete suggestion.

## File-saving rule

If the user has specified a save destination earlier in the conversation (e.g., "always save to this Drive folder"), still save to `/mnt/user-data/outputs/` first — Claude can't write to user filesystems directly. Tell the user explicitly: "I've saved the files here. To put them in your specified folder, drag them in after download." This avoids confusion.

## Common failure modes to avoid

- **Don't pretend you generated a video.** Don't say "Here's your video!" when you produced a PDF. Say "Here's the storyboard for your video."
- **Don't skip the honest framing in Step 1.** Users feel misled when they expect MP4 and get PDF.
- **Don't over-decorate the storyboard illustrations.** They're functional, not art.
- **Don't produce all five deliverables every time.** Match deliverables to the user's actual path (Step 3).
- **Don't ask the user 7 clarifying questions.** Pick 2–3 that genuinely matter; default the rest.
- **Don't forget character consistency** in AI prompts. This is the single biggest cause of bad AI video output.
- **Don't use the example "Responsible Parenting" content** as a default. It's just a sample. Replace SCENES with content for the user's actual topic.

## Reference files

- `references/ai_video_tools.md` — Prompt formatting tips for Sora, Veo, Runway, Kling, Pika, HeyGen
- `references/scene_archetypes.md` — Common scene types (opening, problem, turn, resolution, CTA) for short-form video structure
- `scripts/build_storyboard.py` — Storyboard PDF generator. Edit SCENES and PALETTE; run with python.
- `scripts/build_prompt_sheet.py` — AI video prompt sheet generator. Outputs a clean PDF or markdown.
