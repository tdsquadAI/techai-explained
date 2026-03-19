#!/usr/bin/env python3
"""
TechAI Explained — Daily Tech Brief Generator

Usage:
    python generate_daily_brief.py <news.json> [--output <path.mp4>]

Takes a JSON file with 3 news items and generates a 60-90 second video.
"""

import argparse, asyncio, json, os, sys, tempfile, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    VOICE_NAME, VOICE_RATE, VOICE_PITCH,
    FPS, VIDEO_BITRATE, AUDIO_BITRATE,
    INTRO_DURATION, OUTRO_DURATION,
)
from slide_templates import (
    render_title_slide, render_bullet_slide, render_cta_slide, render_intro_slide,
)


async def generate_tts(text: str, output_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=VOICE_NAME, rate=VOICE_RATE, pitch=VOICE_PITCH)
    await communicate.save(output_path)


def assemble_video(slide_data: list[dict], output_path: str, video_title: str):
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

    clips = []

    # Intro
    intro_img = render_intro_slide(video_title)
    intro_path = os.path.join(tempfile.gettempdir(), "_daily_intro.png")
    intro_img.save(intro_path)
    clips.append(ImageClip(intro_path, duration=INTRO_DURATION))

    # Content slides
    for sd in slide_data:
        audio = AudioFileClip(sd["audio_path"])
        img_clip = ImageClip(sd["image_path"], duration=audio.duration).with_audio(audio)
        clips.append(img_clip)

    # Outro
    outro_img = render_cta_slide("Subscribe for Daily Updates!")
    outro_path = os.path.join(tempfile.gettempdir(), "_daily_outro.png")
    outro_img.save(outro_path)
    clips.append(ImageClip(outro_path, duration=4))

    final = concatenate_videoclips(clips, method="compose")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac",
                          bitrate=VIDEO_BITRATE, audio_bitrate=AUDIO_BITRATE, logger="bar")
    print(f"\n✅ Daily brief saved to: {output_path}")


async def run_daily_brief(json_path: str, output_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    date = data.get("date", "Today")
    items = data.get("items", [])
    video_title = f"TechAI Daily Brief — {date}"

    print(f"🎬 Generating: {video_title}")
    print(f"📰 {len(items)} news items")

    work_dir = tempfile.mkdtemp(prefix="techai_daily_")
    slide_data = []

    # Opening narration
    opening = f"Welcome to the TechAI Daily Brief for {date}. Here are today's top 3 tech stories."
    open_img = render_title_slide(f"Daily Brief", date)
    open_img_path = os.path.join(work_dir, "slide_open.png")
    open_img.save(open_img_path)
    open_audio = os.path.join(work_dir, "audio_open.mp3")
    await generate_tts(opening, open_audio)
    slide_data.append({"image_path": open_img_path, "audio_path": open_audio})

    # Each news item
    for i, item in enumerate(items[:3]):
        headline = item.get("headline", f"Story {i+1}")
        bullets = item.get("bullets", [])
        narration = f"Story {i+1}: {headline}. " + ". ".join(bullets)

        img = render_bullet_slide(headline, bullets)
        img_path = os.path.join(work_dir, f"slide_{i}.png")
        img.save(img_path)
        audio_path = os.path.join(work_dir, f"audio_{i}.mp3")
        await generate_tts(narration, audio_path)
        slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Closing
    closing = "That's your daily brief. Subscribe and hit the bell for daily updates. See you tomorrow!"
    close_img = render_bullet_slide("That's a Wrap!", ["Subscribe for daily updates", "New brief every weekday"])
    close_img_path = os.path.join(work_dir, "slide_close.png")
    close_img.save(close_img_path)
    close_audio = os.path.join(work_dir, "audio_close.mp3")
    await generate_tts(closing, close_audio)
    slide_data.append({"image_path": close_img_path, "audio_path": close_audio})

    assemble_video(slide_data, output_path, video_title)
    shutil.rmtree(work_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="TechAI Daily Brief Generator")
    parser.add_argument("json_file", help="Path to news JSON file")
    parser.add_argument("--output", "-o", default=None, help="Output MP4 path")
    args = parser.parse_args()

    if args.output is None:
        args.output = os.path.join("pipeline", "output", "daily-brief.mp4")

    asyncio.run(run_daily_brief(args.json_file, args.output))


if __name__ == "__main__":
    main()
