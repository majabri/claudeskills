"""
AI Video Prompt Sheet generator.

Takes a list of scene prompts + a character description block and writes
a clean PDF or markdown file the user can copy-paste into Sora, Veo, Runway, etc.

USAGE:
    Edit CHARACTERS, SCENE_PROMPTS, and PROJECT below, then run.
    python build_prompt_sheet.py [--format pdf|md] [--output PATH]

Each scene's prompt should already include the character description re-pasted
inside it — character consistency is the #1 problem with AI video, and tools
do not remember characters across separate generations.
"""

import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
)

# =============================================================================
# CUSTOMIZE
# =============================================================================

PROJECT = {
    "title": "Project Title — AI Video Prompts",
    "tool": "Sora",   # Sora / Veo 3 / Runway / Kling / Pika
    "aspect_ratio": "9:16 vertical",
    "style_keywords": "cinematic, warm color grade, golden hour lighting, photorealistic, shallow depth of field",
    "duration_per_clip": "8–10 seconds",
}

CHARACTERS = """\
CHARACTERS — paste this block at the start of every scene prompt.

DAD: Late 30s, 5'10", short dark brown hair, light beard, warm brown eyes, \
wearing a terracotta knit sweater and dark jeans.

MOM: Mid 30s, shoulder-length wavy auburn hair, warm hazel eyes, \
wearing a navy blue cardigan over a cream blouse and dark jeans.

SON: ~10 years old, short dark brown hair, hazel eyes, \
wearing a mustard yellow t-shirt and gray joggers.

DAUGHTER: ~8 years old, long dark brown hair, hazel eyes, \
wearing a sage green long-sleeve and jeans.\
"""

SCENE_PROMPTS = [
    {
        "num": 1,
        "title": "Opening — wide family shot",
        "duration": "0:00 – 0:10",
        "prompt": (
            "Wide shot of a family of four sitting together on a navy couch in a "
            "warmly-lit living room during late afternoon. Father (terracotta sweater) "
            "and mother (navy cardigan) are flanked by their two children — a son in "
            "a mustard t-shirt and a daughter in a sage green top. The parents look "
            "calm and inviting. Slow push-in toward the family. Cinematic, warm color "
            "grade, soft golden light through a window, photorealistic, shallow depth "
            "of field. 9:16 vertical aspect ratio."
        ),
        "notes": "Set the calm tone. Don't show dialogue here — handle that in close-ups.",
    },
    # Add more scene prompts...
]

# =============================================================================
# Builders
# =============================================================================

def build_pdf(output_path):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=20, leading=24, textColor=HexColor("#8C4A24"),
        alignment=TA_CENTER, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "subtitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=11, leading=14, textColor=HexColor("#2B2B2B"),
        alignment=TA_CENTER, spaceAfter=14
    )
    label_style = ParagraphStyle(
        "label", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=HexColor("#8C4A24"), spaceAfter=4
    )
    body_style = ParagraphStyle(
        "body", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, leading=14, textColor=HexColor("#2B2B2B"), spaceAfter=6
    )
    prompt_style = ParagraphStyle(
        "prompt", parent=styles["Normal"], fontName="Courier",
        fontSize=9, leading=12, textColor=HexColor("#2B2B2B"),
        leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4
    )
    note_style = ParagraphStyle(
        "note", parent=styles["Normal"], fontName="Helvetica-Oblique",
        fontSize=9, leading=12, textColor=HexColor("#6B5544"), spaceAfter=4
    )

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch,
        title=PROJECT["title"],
    )
    story = []

    story.append(Paragraph(PROJECT["title"], title_style))
    story.append(Paragraph(
        f"Tool: {PROJECT['tool']}  |  Aspect: {PROJECT['aspect_ratio']}  |  "
        f"Clip length: {PROJECT['duration_per_clip']}", subtitle_style))
    story.append(Spacer(1, 0.2*inch))

    # Instructions
    story.append(Paragraph("HOW TO USE", label_style))
    story.append(Paragraph(
        "1. Open your AI video tool (Sora, Veo, Runway, etc.).<br/>"
        "2. For each scene, paste the CHARACTERS block, then a blank line, then the scene prompt.<br/>"
        "3. Generate. Most tools allow 5–20 second clips. Generate one per scene.<br/>"
        "4. Stitch the clips together in a video editor (CapCut, Descript, iMovie, Premiere).<br/>"
        "5. Add the voiceover, music, and any text overlays in the editor.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("WHY REPEAT THE CHARACTER BLOCK EVERY TIME", label_style))
    story.append(Paragraph(
        "AI video tools do not remember characters across separate generations. "
        "Each clip is generated in isolation. Pasting the full character description "
        "every time is the only way to keep the same person across multiple shots. "
        "Yes, this is tedious. Yes, it's still the best practice.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    # Character block
    story.append(Paragraph("CHARACTER BLOCK (paste at start of every prompt)", label_style))
    char_table = Table([[Paragraph(CHARACTERS.replace("\n", "<br/>"), prompt_style)]],
                       colWidths=[7.4*inch])
    char_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FBEFE2")),
        ("BOX", (0, 0), (-1, -1), 0.75, HexColor("#D4B59E")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(char_table)
    story.append(PageBreak())

    # Scene prompts
    for scene in SCENE_PROMPTS:
        block = []
        block.append(Paragraph(
            f"<b>SCENE {scene['num']} — {scene['title']}</b>  "
            f"<font color='#6B5544'>({scene['duration']})</font>",
            label_style
        ))
        block.append(Paragraph("PROMPT (copy this):", note_style))
        prompt_table = Table([[Paragraph(scene["prompt"], prompt_style)]],
                             colWidths=[7.4*inch])
        prompt_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F4E3CE")),
            ("BOX", (0, 0), (-1, -1), 0.75, HexColor("#D4B59E")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        block.append(prompt_table)
        if scene.get("notes"):
            block.append(Spacer(1, 0.05*inch))
            block.append(Paragraph(f"<b>Notes:</b> {scene['notes']}", note_style))
        block.append(Spacer(1, 0.2*inch))
        story.append(KeepTogether(block))

    doc.build(story)
    print(f"PDF created: {output_path}")


def build_md(output_path):
    lines = []
    lines.append(f"# {PROJECT['title']}\n")
    lines.append(f"**Tool:** {PROJECT['tool']}  |  **Aspect:** {PROJECT['aspect_ratio']}  |  **Clip length:** {PROJECT['duration_per_clip']}\n")
    lines.append("---\n")
    lines.append("## How to use\n")
    lines.append("1. Open your AI video tool (Sora, Veo, Runway, etc.).")
    lines.append("2. For each scene, paste the CHARACTERS block, then a blank line, then the scene prompt.")
    lines.append("3. Generate. Most tools allow 5–20 second clips. Generate one per scene.")
    lines.append("4. Stitch the clips together in a video editor (CapCut, Descript, iMovie, Premiere).")
    lines.append("5. Add voiceover, music, and any text overlays in the editor.\n")
    lines.append("## Character block (paste at start of every prompt)\n")
    lines.append("```")
    lines.append(CHARACTERS)
    lines.append("```\n")
    lines.append("---\n")
    lines.append("## Scene prompts\n")
    for scene in SCENE_PROMPTS:
        lines.append(f"### Scene {scene['num']} — {scene['title']} ({scene['duration']})\n")
        lines.append("```")
        lines.append(scene["prompt"])
        lines.append("```\n")
        if scene.get("notes"):
            lines.append(f"_Notes: {scene['notes']}_\n")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Markdown created: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["pdf", "md"], default="pdf")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.format == "pdf":
        out = args.output or "/mnt/user-data/outputs/Prompt_Sheet.pdf"
        build_pdf(out)
    else:
        out = args.output or "/mnt/user-data/outputs/Prompt_Sheet.md"
        build_md(out)
