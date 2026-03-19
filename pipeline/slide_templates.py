"""
TechAI Explained — Slide Template Renderers

Each function receives a Pillow ImageDraw, the slide data, and config,
and draws the appropriate layout onto a 1920×1080 image.
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap, os, platform

from config import (
    WIDTH, HEIGHT,
    BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM,
    TEXT_COLOR, SUBTITLE_COLOR, ACCENT_COLOR,
    CODE_BG_COLOR, CODE_BORDER_COLOR,
    BULLET_COLOR, COMPARISON_HEADER_BG, HIGHLIGHT_COLOR,
    TITLE_FONT_SIZE, SUBTITLE_FONT_SIZE, BODY_FONT_SIZE,
    CODE_FONT_SIZE, BULLET_FONT_SIZE, SMALL_FONT_SIZE,
    CHANNEL_NAME, CHANNEL_TAGLINE, SUBSCRIBE_CTA, WEBSITE_URL,
)

# ── Font helpers ────────────────────────────────────────────────

def _find_system_font(name_hints: list[str], bold: bool = False) -> str | None:
    """Return first font path found on this system."""
    if platform.system() == "Windows":
        font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    else:
        font_dir = "/usr/share/fonts/truetype"
    for hint in name_hints:
        path = os.path.join(font_dir, hint)
        if os.path.isfile(path):
            return path
    return None


def _title_font(size: int | None = None):
    size = size or TITLE_FONT_SIZE
    path = _find_system_font(["segoeuib.ttf", "segoeui.ttf", "arialbd.ttf", "Arial Bold.ttf"])
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _body_font(size: int | None = None):
    size = size or BODY_FONT_SIZE
    path = _find_system_font(["segoeui.ttf", "arial.ttf", "Arial.ttf"])
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _code_font(size: int | None = None):
    size = size or CODE_FONT_SIZE
    path = _find_system_font(["consola.ttf", "consolab.ttf", "cour.ttf", "Courier New.ttf"])
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ── Background gradient ────────────────────────────────────────

def _gradient_bg() -> Image.Image:
    """Create a vertical gradient background image."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_GRADIENT_TOP[0] + (BG_GRADIENT_BOTTOM[0] - BG_GRADIENT_TOP[0]) * ratio)
        g = int(BG_GRADIENT_TOP[1] + (BG_GRADIENT_BOTTOM[1] - BG_GRADIENT_TOP[1]) * ratio)
        b = int(BG_GRADIENT_TOP[2] + (BG_GRADIENT_BOTTOM[2] - BG_GRADIENT_TOP[2]) * ratio)
        ImageDraw.Draw(img).line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def _draw_accent_line(draw: ImageDraw.ImageDraw, y: int, width: int = 200):
    """Draw a short accent line."""
    x_start = (WIDTH - width) // 2
    draw.rectangle([x_start, y, x_start + width, y + 4], fill=ACCENT_COLOR)


def _wrapped_text(draw, text, font, x, y, max_width, fill=TEXT_COLOR, line_spacing=8):
    """Draw word-wrapped text and return the y after the last line."""
    # Estimate chars per line
    avg_char_w = font.getlength("M") if hasattr(font, "getlength") else 16
    chars_per_line = max(20, int(max_width / avg_char_w))
    lines = textwrap.wrap(text, width=chars_per_line)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_h = bbox[3] - bbox[1]
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h + line_spacing
    return y


# ── Slide Renderers ─────────────────────────────────────────────

def render_title_slide(title: str, subtitle: str = "") -> Image.Image:
    """Big centered title + subtitle."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_t = _title_font(72)
    font_s = _body_font(SUBTITLE_FONT_SIZE)

    # Title — center
    bbox = draw.textbbox((0, 0), title, font=font_t)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (WIDTH - tw) // 2
    ty = HEIGHT // 2 - th - 40
    # wrap if too wide
    if tw > WIDTH - 200:
        lines = textwrap.wrap(title, width=30)
        ty = HEIGHT // 2 - (th + 10) * len(lines) // 2 - 40
        for line in lines:
            lbbox = draw.textbbox((0, 0), line, font=font_t)
            lw = lbbox[2] - lbbox[0]
            draw.text(((WIDTH - lw) // 2, ty), line, font=font_t, fill=TEXT_COLOR)
            ty += th + 10
    else:
        draw.text((tx, ty), title, font=font_t, fill=TEXT_COLOR)
        ty += th + 10

    # Accent line
    _draw_accent_line(draw, ty + 10, 300)

    # Subtitle
    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_s)
        sw = bbox2[2] - bbox2[0]
        draw.text(((WIDTH - sw) // 2, ty + 40), subtitle, font=font_s, fill=SUBTITLE_COLOR)

    return img


def render_bullet_slide(title: str, bullets: list[str]) -> Image.Image:
    """Title + bullet points."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_t = _title_font(52)
    font_b = _body_font(BULLET_FONT_SIZE)

    # Title
    draw.text((120, 80), title, font=font_t, fill=TEXT_COLOR)
    _draw_accent_line(draw, 155, 160)
    # Move accent to be left-aligned under the title
    draw.rectangle([120, 155, 280, 159], fill=ACCENT_COLOR)

    y = 200
    for bullet in bullets[:7]:
        # Bullet dot
        draw.ellipse([140, y + 12, 156, y + 28], fill=BULLET_COLOR)
        # Text
        y = _wrapped_text(draw, bullet, font_b, 180, y + 4, WIDTH - 320, fill=TEXT_COLOR, line_spacing=6)
        y += 18
    return img


def render_code_slide(title: str, code: str, language: str = "") -> Image.Image:
    """Title + syntax-highlighted code block."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_t = _title_font(48)
    font_c = _code_font(CODE_FONT_SIZE)
    font_lang = _body_font(SMALL_FONT_SIZE)

    # Title
    draw.text((120, 60), title, font=font_t, fill=TEXT_COLOR)

    # Code box
    box_x, box_y = 100, 150
    box_w, box_h = WIDTH - 200, HEIGHT - 220
    # Background
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                            radius=16, fill=CODE_BG_COLOR)
    # Border
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                            radius=16, outline=CODE_BORDER_COLOR, width=2)
    # Language badge
    if language:
        draw.text((box_x + 20, box_y + 12), language.upper(), font=font_lang, fill=ACCENT_COLOR)

    # Code text
    code_y = box_y + 50
    for line in code.split("\n")[:24]:  # max 24 lines visible
        # Simple keyword colouring
        colored = line
        draw.text((box_x + 30, code_y), colored, font=font_c, fill=(200, 220, 240))
        code_y += 34

    return img


def render_diagram_slide(title: str, diagram: str) -> Image.Image:
    """Title + ASCII/text diagram rendered in monospace."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_t = _title_font(48)
    font_d = _code_font(22)

    draw.text((120, 60), title, font=font_t, fill=TEXT_COLOR)

    # Diagram box
    box_x, box_y = 100, 150
    box_w, box_h = WIDTH - 200, HEIGHT - 220
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                            radius=16, fill=(20, 20, 40))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                            radius=16, outline=ACCENT_COLOR, width=1)

    dy = box_y + 30
    for line in diagram.split("\n")[:32]:
        draw.text((box_x + 40, dy), line, font=font_d, fill=ACCENT_COLOR)
        dy += 26

    return img


def render_comparison_slide(title: str, headers: list[str], rows: list[list[str]]) -> Image.Image:
    """Two-or-more column comparison table."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_t = _title_font(48)
    font_h = _title_font(30)
    font_b = _body_font(28)

    draw.text((120, 50), title, font=font_t, fill=TEXT_COLOR)

    num_cols = len(headers)
    col_w = (WIDTH - 240) // num_cols
    table_x = 120
    table_y = 150

    # Header row
    for i, header in enumerate(headers):
        hx = table_x + i * col_w
        draw.rectangle([hx, table_y, hx + col_w - 4, table_y + 56], fill=COMPARISON_HEADER_BG)
        draw.text((hx + 16, table_y + 12), header, font=font_h, fill=ACCENT_COLOR)

    # Data rows
    ry = table_y + 64
    for row in rows[:12]:
        for i, cell in enumerate(row[:num_cols]):
            cx = table_x + i * col_w
            # alternating row bg
            bg = (30, 30, 55) if rows.index(row) % 2 == 0 else (25, 25, 45)
            draw.rectangle([cx, ry, cx + col_w - 4, ry + 50], fill=bg)
            _wrapped_text(draw, cell, font_b, cx + 16, ry + 10, col_w - 32, fill=TEXT_COLOR)
        ry += 54

    return img


def render_quote_slide(quote: str, attribution: str = "") -> Image.Image:
    """Large centred quote."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_q = _body_font(42)
    font_a = _body_font(SMALL_FONT_SIZE)

    # Big quotation mark
    qm_font = _title_font(120)
    draw.text((140, 160), "\u201C", font=qm_font, fill=ACCENT_COLOR)

    _wrapped_text(draw, quote, font_q, 200, 320, WIDTH - 400, fill=TEXT_COLOR, line_spacing=14)

    if attribution:
        bbox = draw.textbbox((0, 0), f"\u2014 {attribution}", font=font_a)
        aw = bbox[2] - bbox[0]
        draw.text((WIDTH - aw - 200, HEIGHT - 160), f"\u2014 {attribution}", font=font_a, fill=SUBTITLE_COLOR)

    return img


def render_cta_slide(heading: str = "Thanks for Watching!") -> Image.Image:
    """Call-to-action / outro slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_h = _title_font(60)
    font_b = _body_font(36)
    font_s = _body_font(28)

    # Heading
    bbox = draw.textbbox((0, 0), heading, font=font_h)
    hw = bbox[2] - bbox[0]
    draw.text(((WIDTH - hw) // 2, 260), heading, font=font_h, fill=TEXT_COLOR)

    # Accent line
    _draw_accent_line(draw, 360, 400)

    # Subscribe CTA
    cta_text = f"\U0001F514  {SUBSCRIBE_CTA}"
    bbox2 = draw.textbbox((0, 0), cta_text, font=font_b)
    cw = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - cw) // 2, 420), cta_text, font=font_b, fill=ACCENT_COLOR)

    # Channel info
    info = f"{CHANNEL_NAME}  |  {WEBSITE_URL}"
    bbox3 = draw.textbbox((0, 0), info, font=font_s)
    iw = bbox3[2] - bbox3[0]
    draw.text(((WIDTH - iw) // 2, 520), info, font=font_s, fill=SUBTITLE_COLOR)

    return img


def render_intro_slide(video_title: str) -> Image.Image:
    """Channel branding intro slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    font_channel = _title_font(56)
    font_tag = _body_font(30)
    font_vtitle = _body_font(40)

    # Channel name
    bbox = draw.textbbox((0, 0), CHANNEL_NAME, font=font_channel)
    cw = bbox[2] - bbox[0]
    draw.text(((WIDTH - cw) // 2, 280), CHANNEL_NAME, font=font_channel, fill=ACCENT_COLOR)

    # Tagline
    bbox2 = draw.textbbox((0, 0), CHANNEL_TAGLINE, font=font_tag)
    tw = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - tw) // 2, 360), CHANNEL_TAGLINE, font=font_tag, fill=SUBTITLE_COLOR)

    _draw_accent_line(draw, 420, 300)

    # Video title
    _wrapped_text(draw, video_title, font_vtitle, 200, 470, WIDTH - 400, fill=TEXT_COLOR, line_spacing=10)

    return img
