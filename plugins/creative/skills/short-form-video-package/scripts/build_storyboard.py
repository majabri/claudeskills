"""
Storyboard PDF generator for short-form video projects.

USAGE:
    1. Copy this script to your working area (e.g., /home/claude/build_storyboard.py)
    2. Replace the SCENES list, PROJECT metadata, and PALETTE if needed
    3. Optionally write/customize the scene drawer functions in SCENE_DRAWERS
    4. Run: python build_storyboard.py
    5. Output goes to OUTPUT_PATH (default: /mnt/user-data/outputs/)

The illustrations are intentionally minimal — flat shapes, clear blocking.
Storyboards are functional, not art. Don't over-decorate.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable
)
from reportlab.lib import colors

# =============================================================================
# CUSTOMIZE THESE FOR EACH PROJECT
# =============================================================================

OUTPUT_PATH = "/mnt/user-data/outputs/Storyboard.pdf"

PROJECT = {
    "title": "PROJECT TITLE",
    "subtitle": "A Video Storyboard",
    "format": "Short-form video (60–90 seconds)",
    "tone": "Warm and educational",
    "cast": "Describe cast",
    "setting": "Describe setting",
    "music": "Soft acoustic, warm and grounded",
    "premise": (
        "<b>Core message:</b> Replace this with the project's premise — "
        "what is the video about, what is the takeaway, why does it matter."
    ),
}

# Palette presets — pick one or define your own
PALETTES = {
    "warm": {
        "bg": "#FFF8F0", "accent": "#C97B4A", "accent_dark": "#8C4A24",
        "soft": "#4A6B8C", "text": "#2B2B2B", "panel": "#FBEFE2", "border": "#D4B59E",
    },
    "cool": {
        "bg": "#F0F4F8", "accent": "#3A5A7C", "accent_dark": "#1F3A5C",
        "soft": "#7A8FA8", "text": "#1F2B3A", "panel": "#E0EAF3", "border": "#B0C2D6",
    },
    "energetic": {
        "bg": "#FFFAF0", "accent": "#E8533F", "accent_dark": "#A8311F",
        "soft": "#F2A736", "text": "#2B2B2B", "panel": "#FFEEDC", "border": "#F0C8A0",
    },
    "dramatic": {
        "bg": "#1F2228", "accent": "#D4A85A", "accent_dark": "#A87E2E",
        "soft": "#7A6F58", "text": "#E8E4DC", "panel": "#2D3138", "border": "#4A4F5A",
    },
}
PALETTE = PALETTES["warm"]   # change this per project

# =============================================================================
# SCENES — replace this list for each project
# =============================================================================

SCENES = [
    {
        "num": 1,
        "title": "OPENING — Scene title here",
        "duration": "0:00 – 0:10",
        "shot": "Wide / medium / close-up — describe the framing.",
        "visual": "Lighting, mood, camera movement.",
        "dialogue": [
            ("CHARACTER A", "Their line."),
            ("CHARACTER B", "Their line."),
        ],
        "direction": "Performance and tone notes for the actor or AI tool.",
    },
    # Add more scenes...
]

# =============================================================================
# SCENE DRAWERS — each scene needs a drawer function. Build minimal flat illustrations.
# Pattern: background -> environment elements -> figure(s) -> optional prop
# Use rectangles for bodies, circles for heads, simple shapes for everything else.
# =============================================================================

def draw_default_scene(c, x, y, w, h, palette):
    """Fallback drawer if no scene-specific one is provided."""
    c.setFillColor(HexColor(palette["panel"]))
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(HexColor(palette["accent"]))
    c.rect(x + w*0.30, y + h*0.20, w*0.40, h*0.40, fill=1, stroke=0)
    c.setFillColor(HexColor(palette["accent_dark"]))
    c.circle(x + w*0.50, y + h*0.65, w*0.10, fill=1, stroke=0)


# Map scene number -> drawer function. Override per project.
# def draw_scene_1(c, x, y, w, h, palette): ...
# SCENE_DRAWERS = {1: draw_scene_1, 2: draw_scene_2, ...}

SCENE_DRAWERS = {}   # populate this in the project-specific copy

# =============================================================================
# PDF building (usually no changes needed below this line)
# =============================================================================

def get_styles(palette):
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title", parent=styles["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=26, textColor=HexColor(palette["accent_dark"]),
            alignment=TA_CENTER, spaceAfter=4
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=styles["Normal"], fontName="Helvetica",
            fontSize=11, leading=14, textColor=HexColor(palette["text"]),
            alignment=TA_CENTER, spaceAfter=14
        ),
        "scene_header": ParagraphStyle(
            "sceneHeader", parent=styles["Heading2"], fontName="Helvetica-Bold",
            fontSize=14, leading=18, textColor=white, alignment=TA_LEFT,
            leftIndent=8, spaceAfter=0, spaceBefore=0
        ),
        "label": ParagraphStyle(
            "label", parent=styles["Normal"], fontName="Helvetica-Bold",
            fontSize=9, leading=12, textColor=HexColor(palette["accent_dark"]),
            spaceAfter=2
        ),
        "body": ParagraphStyle(
            "body", parent=styles["Normal"], fontName="Helvetica",
            fontSize=10, leading=13, textColor=HexColor(palette["text"]),
            spaceAfter=6
        ),
        "dialogue": ParagraphStyle(
            "dialogue", parent=styles["Normal"], fontName="Helvetica",
            fontSize=10, leading=13, textColor=HexColor(palette["text"]),
            leftIndent=10, spaceAfter=4
        ),
        "note": ParagraphStyle(
            "note", parent=styles["Normal"], fontName="Helvetica-Oblique",
            fontSize=9, leading=12, textColor=HexColor("#6B5544"), spaceAfter=2
        ),
    }


class SceneIllustration(Flowable):
    def __init__(self, scene_num, width, height, palette):
        super().__init__()
        self.scene_num = scene_num
        self.width = width
        self.height = height
        self.palette = palette

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(HexColor(self.palette["accent_dark"]))
        c.setLineWidth(2)
        c.rect(0, 0, self.width, self.height, fill=0, stroke=1)
        inset = 4
        drawer = SCENE_DRAWERS.get(self.scene_num, draw_default_scene)
        drawer(c, inset, inset, self.width - 2*inset, self.height - 2*inset, self.palette)
        c.setFillColor(HexColor(self.palette["accent_dark"]))
        c.rect(0, self.height - 22, 80, 22, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(8, self.height - 16, f"SCENE {self.scene_num}")
        c.restoreState()


def build_scene_page(scene, palette, st):
    elements = []

    header_table = Table(
        [[Paragraph(f"SCENE {scene['num']} — {scene['title']}", st["scene_header"]),
          Paragraph(f"<font color='white'>{scene['duration']}</font>",
                    ParagraphStyle("dur", fontName="Helvetica-Bold", fontSize=11,
                                   textColor=white, alignment=2))]],
        colWidths=[5.0*inch, 2.5*inch]
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(palette["accent_dark"])),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (1, 0), (1, 0), 12),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.12*inch))

    illustration = SceneIllustration(scene["num"], 3.6*inch, 2.5*inch, palette)
    right_col = [
        Paragraph("SHOT", st["label"]),
        Paragraph(scene["shot"], st["body"]),
        Paragraph("VISUAL", st["label"]),
        Paragraph(scene["visual"], st["body"]),
    ]
    side_table = Table([[illustration, right_col]], colWidths=[3.7*inch, 3.7*inch])
    side_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(side_table)
    elements.append(Spacer(1, 0.18*inch))

    dialogue_block = [Paragraph("DIALOGUE", st["label"])]
    for character, line in scene["dialogue"]:
        dialogue_block.append(Paragraph(f"<b>{character}:</b> &ldquo;{line}&rdquo;", st["dialogue"]))

    dialogue_table = Table([[dialogue_block]], colWidths=[7.4*inch])
    dialogue_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(palette["panel"])),
        ("BOX", (0, 0), (-1, -1), 0.75, HexColor(palette["border"])),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(dialogue_table)
    elements.append(Spacer(1, 0.12*inch))

    direction_block = [
        Paragraph("DIRECTION", st["label"]),
        Paragraph(scene["direction"], st["note"]),
    ]
    direction_table = Table([[direction_block]], colWidths=[7.4*inch])
    direction_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(palette["panel"])),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor(palette["border"])),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(direction_table)

    return KeepTogether(elements)


def draw_cover_bg_factory(palette):
    def draw(c, doc):
        width, height = letter
        c.setFillColor(HexColor(palette["bg"]))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        c.setFillColor(HexColor(palette["accent"]))
        c.rect(0, height - 0.3*inch, width, 0.3*inch, fill=1, stroke=0)
        c.setFillColor(HexColor(palette["accent_dark"]))
        c.rect(0, 0, width, 0.2*inch, fill=1, stroke=0)
    return draw


def draw_page_bg_factory(palette, project_title):
    def draw(c, doc):
        width, height = letter
        c.setFillColor(HexColor(palette["bg"]))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        c.setFillColor(HexColor(palette["accent_dark"]))
        c.setFont("Helvetica", 8)
        c.drawString(0.5*inch, 0.3*inch, project_title)
        c.drawRightString(width - 0.5*inch, 0.3*inch, f"Page {doc.page}")
    return draw


def build_pdf(scenes=None, project=None, palette=None, output_path=None,
              production_notes=None):
    """
    Main entry point. All args optional — will fall back to module-level
    constants. Pass arguments to use this as a library function.
    """
    scenes = scenes or SCENES
    project = project or PROJECT
    palette = palette or PALETTE
    output_path = output_path or OUTPUT_PATH
    st = get_styles(palette)

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch,
        title=project["title"],
    )
    story = []

    # Cover
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph(project["title"], st["title"]))
    story.append(Paragraph(project["subtitle"], st["subtitle"]))
    story.append(Spacer(1, 0.4*inch))

    cover_info = [
        ["Format:", project["format"]],
        ["Tone:", project["tone"]],
        ["Cast:", project["cast"]],
        ["Setting:", project["setting"]],
        ["Scenes:", f"{len(scenes)} scenes total"],
        ["Music:", project["music"]],
    ]
    t = Table(cover_info, colWidths=[1.4*inch, 4.6*inch])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), HexColor(palette["accent_dark"])),
        ("TEXTCOLOR", (1, 0), (1, -1), HexColor(palette["text"])),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(palette["panel"])),
        ("BOX", (0, 0), (-1, -1), 1, HexColor(palette["border"])),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, HexColor(palette["border"])),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(project["premise"], st["body"]))
    story.append(PageBreak())

    # Scenes
    for scene in scenes:
        story.append(build_scene_page(scene, palette, st))
        story.append(PageBreak())

    # Production notes (use defaults if none provided)
    notes = production_notes or [
        ("Visual style", "Warm, natural lighting throughout. Soft contrast. Lean into golden-hour interiors."),
        ("Camera", "Mostly handheld but stable. Slow push-ins on emotional beats. Static medium shots elsewhere."),
        ("Wardrobe", "Comfortable, real clothes. Earth tones. Nothing branded or distracting."),
        ("Performance direction", "Nothing should feel staged. Real eye contact, real pauses. Let people improvise small reactions."),
        ("Music", f"{project.get('music', 'Soft acoustic')}. Gentle swell at the emotional pivot. Resolves warmly at the end."),
        ("Pacing", "Roughly 10 seconds per scene. If trimming for length, shorten the opener and the warmest beat first."),
    ]

    story.append(Paragraph("PRODUCTION NOTES", st["title"]))
    story.append(Spacer(1, 0.3*inch))
    for label, content in notes:
        story.append(Paragraph(f"<b>{label}</b>", st["label"]))
        story.append(Paragraph(content, st["body"]))
        story.append(Spacer(1, 0.1*inch))

    doc.build(
        story,
        onFirstPage=draw_cover_bg_factory(palette),
        onLaterPages=draw_page_bg_factory(palette, project["title"]),
    )
    print(f"PDF created: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
