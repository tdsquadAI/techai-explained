#!/usr/bin/env python3
"""
TechAI Explained — Slide-Based Video Generator

Usage:
    python generate_video.py <script.md> [--output <path.mp4>]

Reads a markdown script with slide markers, generates slide images + TTS
audio per section, then composites everything into a 1080p video with
fade transitions.
"""

import argparse, asyncio, os, re, sys, tempfile, shutil

# Add pipeline dir to path so config/templates import cleanly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    VOICE_NAME, VOICE_RATE, VOICE_PITCH,
    WIDTH, HEIGHT, FPS, VIDEO_BITRATE, AUDIO_BITRATE,
    FADE_DURATION, INTRO_DURATION, OUTRO_DURATION,
)
from slide_templates import (
    render_title_slide, render_bullet_slide, render_code_slide,
    render_diagram_slide, render_comparison_slide, render_quote_slide,
    render_cta_slide, render_intro_slide,
)

# ── Script Parser ───────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Extract YAML-ish front-matter between --- delimiters."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip().strip('"')] = val.strip().strip('"')
    return meta


def parse_slides(text: str) -> list[dict]:
    """
    Parse markdown into slide dicts.

    Slide markers: ## [TYPE] Title
    Supported types: TITLE, BULLETS, CODE, DIAGRAM, COMPARISON, QUOTE
    Everything else defaults to BULLETS.
    """
    # Remove front-matter
    text = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)

    # Split on ## headings
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    slides = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Match heading
        heading_match = re.match(r"^##\s+(?:\[(\w+)\]\s*)?(.+)", section)
        if not heading_match:
            continue

        slide_type = (heading_match.group(1) or "BULLETS").upper()
        title = heading_match.group(2).strip()
        body = section[heading_match.end():].strip()

        slide = {"type": slide_type, "title": title, "body": body, "narration": ""}

        # Extract narration from blockquotes
        narration_parts = re.findall(r'>\s*"?(.+?)"?\s*$', body, re.MULTILINE)
        if narration_parts:
            slide["narration"] = " ".join(narration_parts)
        else:
            # Fall back: use plain text (strip markdown formatting)
            plain = re.sub(r"```[\s\S]*?```", "", body)
            plain = re.sub(r"[#*>`|_\[\]]", "", plain)
            plain = re.sub(r"\n{2,}", ". ", plain).strip()
            slide["narration"] = plain[:800] if plain else title

        # Type-specific parsing
        if slide_type == "CODE":
            code_match = re.search(r"```(\w*)\n([\s\S]*?)```", body)
            if code_match:
                slide["language"] = code_match.group(1)
                slide["code"] = code_match.group(2).strip()
            else:
                slide["language"] = ""
                slide["code"] = body

        elif slide_type == "BULLETS":
            bullets = re.findall(r"^[-*]\s+(.+)", body, re.MULTILINE)
            slide["bullets"] = bullets if bullets else [body[:120]]

        elif slide_type == "DIAGRAM":
            diag_match = re.search(r"```[\w]*\n([\s\S]*?)```", body)
            slide["diagram"] = diag_match.group(1).strip() if diag_match else body

        elif slide_type == "COMPARISON":
            # Parse markdown table
            headers = []
            rows = []
            for line in body.splitlines():
                if "|" in line and "---" not in line:
                    cells = [c.strip() for c in line.strip().strip("|").split("|")]
                    if not headers:
                        headers = cells
                    else:
                        rows.append(cells)
            slide["headers"] = headers or ["A", "B"]
            slide["rows"] = rows

        elif slide_type == "QUOTE":
            quote_match = re.search(r'>\s*"?(.+?)"?\s*$', body, re.MULTILINE)
            slide["quote"] = quote_match.group(1) if quote_match else body[:200]

        slides.append(slide)

    return slides


# ── Slide Image Renderer ────────────────────────────────────────

def render_slide(slide: dict) -> "Image.Image":
    """Dispatch to the right template renderer."""
    t = slide["type"]
    if t == "TITLE":
        parts = slide["title"].split("\n", 1)
        title = parts[0]
        subtitle = slide.get("body", "").split("\n")[0] if len(parts) < 2 else parts[1]
        return render_title_slide(title, subtitle)
    elif t == "CODE":
        return render_code_slide(slide["title"], slide.get("code", ""), slide.get("language", ""))
    elif t == "DIAGRAM":
        return render_diagram_slide(slide["title"], slide.get("diagram", ""))
    elif t == "COMPARISON":
        return render_comparison_slide(slide["title"], slide.get("headers", []), slide.get("rows", []))
    elif t == "QUOTE":
        return render_quote_slide(slide.get("quote", slide["title"]))
    else:  # BULLETS or default
        return render_bullet_slide(slide["title"], slide.get("bullets", [slide["body"][:120]]))


# ── TTS Generation ──────────────────────────────────────────────

async def generate_tts(text: str, output_path: str):
    """Generate speech audio using edge-tts."""
    import edge_tts
    communicate = edge_tts.Communicate(
        text,
        voice=VOICE_NAME,
        rate=VOICE_RATE,
        pitch=VOICE_PITCH,
    )
    await communicate.save(output_path)


# ── Video Assembly ──────────────────────────────────────────────

def assemble_video(slide_data: list[dict], output_path: str, video_title: str):
    """
    Combine slide images + audio into a single MP4 with fade transitions.

    slide_data: list of {"image_path": str, "audio_path": str}
    """
    from moviepy import (
        ImageClip, AudioFileClip, concatenate_videoclips,
        CompositeVideoClip,
    )

    clips = []

    # Intro slide
    intro_img = render_intro_slide(video_title)
    intro_path = os.path.join(tempfile.gettempdir(), "_techai_intro.png")
    intro_img.save(intro_path)
    intro_clip = ImageClip(intro_path, duration=INTRO_DURATION)
    clips.append(intro_clip)

    # Content slides
    for sd in slide_data:
        audio = AudioFileClip(sd["audio_path"])
        duration = audio.duration
        img_clip = ImageClip(sd["image_path"], duration=duration)
        img_clip = img_clip.with_audio(audio)
        clips.append(img_clip)

    # Outro slide
    outro_img = render_cta_slide()
    outro_path = os.path.join(tempfile.gettempdir(), "_techai_outro.png")
    outro_img.save(outro_path)
    outro_clip = ImageClip(outro_path, duration=OUTRO_DURATION)
    clips.append(outro_clip)

    # Concatenate with crossfade
    if len(clips) > 1:
        final = concatenate_videoclips(clips, method="compose")
    else:
        final = clips[0]

    # Write output
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate=VIDEO_BITRATE,
        audio_bitrate=AUDIO_BITRATE,
        logger="bar",
    )
    print(f"\n✅ Video saved to: {output_path}")


# ── Main Pipeline ───────────────────────────────────────────────

async def run_pipeline(script_path: str, output_path: str):
    print(f"📄 Reading script: {script_path}")
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()

    meta = parse_frontmatter(text)
    video_title = meta.get("title", os.path.splitext(os.path.basename(script_path))[0])
    print(f"🎬 Video: {video_title}")

    slides = parse_slides(text)
    print(f"📊 Parsed {len(slides)} slides")

    if not slides:
        print("❌ No slides found. Check script format.")
        sys.exit(1)

    # Create temp working dir
    work_dir = tempfile.mkdtemp(prefix="techai_")
    print(f"🗂  Working directory: {work_dir}")

    slide_data = []
    for i, slide in enumerate(slides):
        print(f"  [{i+1}/{len(slides)}] Rendering slide: {slide['type']} — {slide['title'][:50]}")

        # Render slide image
        img = render_slide(slide)
        img_path = os.path.join(work_dir, f"slide_{i:03d}.png")
        img.save(img_path)

        # Generate TTS
        narration = slide.get("narration", slide["title"])
        if not narration.strip():
            narration = slide["title"]
        audio_path = os.path.join(work_dir, f"audio_{i:03d}.mp3")
        print(f"         🔊 Generating TTS ({len(narration)} chars)...")
        await generate_tts(narration, audio_path)

        slide_data.append({"image_path": img_path, "audio_path": audio_path})

    print(f"\n🎥 Assembling video...")
    assemble_video(slide_data, output_path, video_title)

    # Clean up temp files
    shutil.rmtree(work_dir, ignore_errors=True)
    print("🧹 Cleaned up temp files")


def main():
    parser = argparse.ArgumentParser(description="TechAI Explained — Video Generator")
    parser.add_argument("script", help="Path to the markdown script file")
    parser.add_argument("--output", "-o", default=None, help="Output MP4 path")
    args = parser.parse_args()

    if not os.path.isfile(args.script):
        print(f"❌ Script file not found: {args.script}")
        sys.exit(1)

    if args.output is None:
        base = os.path.splitext(os.path.basename(args.script))[0]
        args.output = os.path.join("pipeline", "output", f"{base}.mp4")

    asyncio.run(run_pipeline(args.script, args.output))


if __name__ == "__main__":
    main()
