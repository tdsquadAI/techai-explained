"""
TechAI Explained — Video Pipeline Configuration
"""

# ── Voice Settings ──────────────────────────────────────────────
VOICE_NAME = "en-US-GuyNeural"
VOICE_RATE = "+0%"
VOICE_PITCH = "+0Hz"

# ── Color Scheme (dark tech theme) ──────────────────────────────
BG_GRADIENT_TOP = (26, 26, 46)       # #1a1a2e
BG_GRADIENT_BOTTOM = (22, 33, 62)    # #16213e

TEXT_COLOR = (255, 255, 255)          # white
SUBTITLE_COLOR = (180, 200, 220)     # light blue-grey
ACCENT_COLOR = (0, 180, 216)         # cyan accent
CODE_BG_COLOR = (15, 15, 30)         # near-black for code blocks
CODE_BORDER_COLOR = (0, 180, 216)    # cyan border
BULLET_COLOR = (0, 210, 180)         # teal for bullet dots
COMPARISON_HEADER_BG = (40, 40, 80)  # purple-ish header
HIGHLIGHT_COLOR = (255, 200, 50)     # gold highlight

# ── Font Settings ───────────────────────────────────────────────
# We use Pillow's default font as fallback; system fonts used when available.
TITLE_FONT_SIZE = 64
SUBTITLE_FONT_SIZE = 36
BODY_FONT_SIZE = 32
CODE_FONT_SIZE = 26
BULLET_FONT_SIZE = 34
SMALL_FONT_SIZE = 24

# ── Output Settings ────────────────────────────────────────────
WIDTH = 1920
HEIGHT = 1080
FPS = 30
VIDEO_BITRATE = "5000k"
AUDIO_BITRATE = "192k"
FADE_DURATION = 0.5          # seconds for cross-fade transitions
INTRO_DURATION = 3           # seconds for intro slide
OUTRO_DURATION = 5           # seconds for outro slide

# ── Channel Branding ───────────────────────────────────────────
CHANNEL_NAME = "TechAI Explained"
CHANNEL_TAGLINE = "AI & DevOps — Explained Simply"
SUBSCRIBE_CTA = "Subscribe for more deep dives"
WEBSITE_URL = "techai-explained.dev"
