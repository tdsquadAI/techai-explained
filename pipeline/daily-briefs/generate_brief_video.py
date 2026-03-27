"""
Generates a short video (60-120s) from a daily brief JSON file.
Creates slide images with Pillow, generates TTS with edge-tts,
and composites everything with ffmpeg.
"""
import asyncio
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

try:
    import edge_tts
except ImportError:
    print("edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

# ── Constants ────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1920, 1080
BG_COLORS = [(15, 12, 41), (48, 43, 99), (36, 36, 62)]
TTS_VOICE = "en-US-GuyNeural"
TTS_VOICE_HE = "he-IL-AvriNeural"

TOPIC_COLORS = {
    "dotnet": (138, 43, 226),
    "ai": (0, 200, 255),
    "cloud": (0, 180, 120),
    "dev": (255, 165, 0),
    "security": (220, 20, 60),
    "gamedev": (50, 205, 50),
}


def _get_font(size):
    """Return a TrueType font, falling back to default if needed."""
    candidates = [
        # Windows fonts
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        # Linux fonts (ubuntu-latest runner)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _get_bold_font(size):
    candidates = [
        # Windows fonts
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        # Linux fonts (ubuntu-latest runner)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return _get_font(size)


def _gradient_bg():
    """Create a 1920x1080 dark gradient background image."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    c1, c2, c3 = BG_COLORS
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        if ratio < 0.5:
            r2 = ratio * 2
            r = int(c1[0] + (c2[0] - c1[0]) * r2)
            g = int(c1[1] + (c2[1] - c1[1]) * r2)
            b = int(c1[2] + (c2[2] - c1[2]) * r2)
        else:
            r2 = (ratio - 0.5) * 2
            r = int(c2[0] + (c3[0] - c2[0]) * r2)
            g = int(c2[1] + (c3[1] - c2[1]) * r2)
            b = int(c2[2] + (c3[2] - c2[2]) * r2)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def _draw_topic_badge(draw, topic_id, topic_name, y=40):
    """Draw a colored badge in the top-right corner."""
    color = TOPIC_COLORS.get(topic_id, (100, 100, 255))
    font = _get_bold_font(28)
    bbox = draw.textbbox((0, 0), topic_name, font=font)
    tw = bbox[2] - bbox[0]
    pad = 20
    x = WIDTH - tw - pad * 2 - 40
    draw.rounded_rectangle([x, y, WIDTH - 40, y + 50], radius=12, fill=color)
    draw.text((x + pad, y + 8), topic_name, fill="white", font=font)


def make_title_slide(brief, output_path):
    """Create the title/intro slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    topic_id = brief["topic_id"]
    topic_name = brief["topic_name"]

    _draw_topic_badge(draw, topic_id, topic_name)

    # Title
    title_font = _get_bold_font(72)
    draw.text((120, 300), topic_name, fill="white", font=title_font)

    # Date
    date_font = _get_font(36)
    draw.text((120, 400), brief["date"], fill=(180, 180, 220), font=date_font)

    # Story count
    count_font = _get_font(32)
    n = len(brief["items"])
    draw.text(
        (120, 480),
        f"{n} stories today",
        fill=(140, 140, 180),
        font=count_font,
    )

    # Brand
    brand_font = _get_bold_font(28)
    draw.text(
        (120, HEIGHT - 80),
        "TechAI Explained",
        fill=(100, 100, 140),
        font=brand_font,
    )

    img.save(output_path)


def make_item_slide(brief, index, item, output_path):
    """Create a slide for a single news item."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    topic_id = brief["topic_id"]
    topic_name = brief["topic_name"]
    total = len(brief["items"])

    _draw_topic_badge(draw, topic_id, topic_name)

    # Slide number
    num_font = _get_bold_font(28)
    draw.text(
        (120, 40),
        f"Story {index + 1} of {total}",
        fill=(140, 140, 180),
        font=num_font,
    )

    # Headline (wrap to fit)
    headline_font = _get_bold_font(52)
    wrapped = textwrap.fill(item["headline"], width=40)
    draw.text((120, 160), wrapped, fill="white", font=headline_font)

    # Summary
    summary_font = _get_font(32)
    summary_wrapped = textwrap.fill(item["summary"], width=65)
    draw.text((120, 480), summary_wrapped, fill=(200, 200, 230), font=summary_font)

    # Source URL
    src_font = _get_font(22)
    url = item.get("source_url", "")
    if len(url) > 80:
        url = url[:80] + "…"
    draw.text((120, HEIGHT - 80), url, fill=(100, 100, 140), font=src_font)

    img.save(output_path)


def make_outro_slide(brief, output_path):
    """Create the outro/CTA slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)

    title_font = _get_bold_font(56)
    draw.text(
        (120, 340),
        "Thanks for watching!",
        fill="white",
        font=title_font,
    )

    sub_font = _get_font(36)
    draw.text(
        (120, 440),
        "Subscribe for daily tech briefs",
        fill=(180, 180, 220),
        font=sub_font,
    )

    brand_font = _get_bold_font(28)
    draw.text(
        (120, HEIGHT - 80),
        "TechAI Explained",
        fill=(100, 100, 140),
        font=brand_font,
    )

    img.save(output_path)


async def generate_tts(text, output_path, voice=None):
    """Generate TTS audio using edge-tts."""
    if voice is None:
        voice = TTS_VOICE
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def build_tts_script(brief):
    """Build the narration script from the brief."""
    parts = [brief["intro"]]
    for i, item in enumerate(brief["items"], 1):
        parts.append(f"Story {i}. {item['headline']}. {item['summary']}")
    parts.append(brief["outro"])
    return parts


def compose_video_ffmpeg(slides, audio_files, output_path, per_slide_secs=None):
    """Use ffmpeg to combine slides and audio into an MP4."""
    tmp_dir = Path(output_path).parent / "_tmp_ffmpeg"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Build a concat list: each slide shown for its audio duration
    concat_entries = []
    for idx, (slide_path, audio_path) in enumerate(zip(slides, audio_files)):
        # Probe audio duration
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    audio_path,
                ],
                capture_output=True, text=True, timeout=10,
            )
            duration = float(result.stdout.strip())
        except Exception:
            duration = per_slide_secs[idx] if per_slide_secs else 8.0

        # Create a short video clip from the still image + audio
        clip_path = str(tmp_dir / f"clip_{idx:03d}.mp4")
        clip_result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-loop", "1", "-i", slide_path,
                "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-t", str(duration + 0.5),
                "-shortest",
                clip_path,
            ],
            capture_output=True, text=True, timeout=120,
        )
        if clip_result.returncode != 0:
            print(f"ffmpeg clip {idx} error: {clip_result.stderr[:200]}", file=sys.stderr)
        else:
            concat_entries.append(clip_path)

    if not concat_entries:
        print(f"ERROR: No valid clips generated for {output_path}", file=sys.stderr)
        return

    # Write concat file (use just filenames since clips are in same directory)
    concat_file = str(tmp_dir / "concat.txt")
    with open(concat_file, "w") as f:
        for entry in concat_entries:
            filename = os.path.basename(entry)
            f.write(f"file '{filename}'\n")

    # Concatenate all clips
    concat_result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            str(output_path),
        ],
        capture_output=True, text=True, timeout=300,
    )
    if concat_result.returncode != 0:
        print(f"ffmpeg concat error (rc={concat_result.returncode}): {concat_result.stderr[-500:]}", file=sys.stderr)

    # Cleanup temp files
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"Video saved: {output_path}")


async def generate_video(brief_json_path, language="en"):
    """Main entry: read brief JSON, create slides, TTS, compose video."""
    with open(brief_json_path, encoding="utf-8") as f:
        brief = json.load(f)

    is_hebrew = language == "he"
    voice = TTS_VOICE_HE if is_hebrew else TTS_VOICE

    base_dir = Path(brief_json_path).parent
    slides_dir = base_dir / "_slides"
    audio_dir = base_dir / "_audio"
    slides_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    topic_id = brief["topic_id"]
    narration_parts = build_tts_script(brief)

    slides = []
    audio_files = []

    # Title slide
    title_slide = str(slides_dir / f"{topic_id}_title.png")
    make_title_slide(brief, title_slide)
    slides.append(title_slide)

    title_audio = str(audio_dir / f"{topic_id}_title.mp3")
    await generate_tts(narration_parts[0], title_audio, voice=voice)
    audio_files.append(title_audio)

    # Item slides
    for i, item in enumerate(brief["items"]):
        slide_path = str(slides_dir / f"{topic_id}_item_{i:02d}.png")
        make_item_slide(brief, i, item, slide_path)
        slides.append(slide_path)

        audio_path = str(audio_dir / f"{topic_id}_item_{i:02d}.mp3")
        await generate_tts(narration_parts[i + 1], audio_path, voice=voice)
        audio_files.append(audio_path)

    # Outro slide
    outro_slide = str(slides_dir / f"{topic_id}_outro.png")
    make_outro_slide(brief, outro_slide)
    slides.append(outro_slide)

    outro_audio = str(audio_dir / f"{topic_id}_outro.mp3")
    await generate_tts(narration_parts[-1], outro_audio, voice=voice)
    audio_files.append(outro_audio)

    # Compose final video — use -he suffix for Hebrew
    suffix = "-he" if is_hebrew else ""
    output_path = base_dir / f"{topic_id}{suffix}-brief.mp4"
    compose_video_ffmpeg(slides, audio_files, str(output_path))

    # Clean up slide/audio dirs
    import shutil
    shutil.rmtree(slides_dir, ignore_errors=True)
    shutil.rmtree(audio_dir, ignore_errors=True)

    return str(output_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate daily brief video")
    parser.add_argument("brief_json", help="Path to the brief JSON file")
    parser.add_argument("--language", default="en", choices=["en", "he"],
                        help="Language: 'en' (default) or 'he' for Hebrew")
    args = parser.parse_args()
    asyncio.run(generate_video(args.brief_json, language=args.language))
