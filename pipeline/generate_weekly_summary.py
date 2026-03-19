#!/usr/bin/env python3
"""
TechAI Explained — Weekly Summary Video Generator

Usage:
    python generate_weekly_summary.py <weekly.json> [--output <path.mp4>]

Takes a JSON file with the week's top stories and generates a 5-8 minute video.
"""

import argparse, asyncio, json, os, sys, tempfile, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    VOICE_NAME, VOICE_RATE, VOICE_PITCH,
    FPS, VIDEO_BITRATE, AUDIO_BITRATE,
    INTRO_DURATION, OUTRO_DURATION,
)
from slide_templates import (
    render_title_slide, render_bullet_slide, render_code_slide,
    render_diagram_slide, render_cta_slide, render_intro_slide,
)


async def generate_tts(text: str, output_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=VOICE_NAME, rate=VOICE_RATE, pitch=VOICE_PITCH)
    await communicate.save(output_path)


def assemble_video(slide_data: list[dict], output_path: str, video_title: str):
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

    clips = []
    intro_img = render_intro_slide(video_title)
    intro_path = os.path.join(tempfile.gettempdir(), "_weekly_intro.png")
    intro_img.save(intro_path)
    clips.append(ImageClip(intro_path, duration=INTRO_DURATION))

    for sd in slide_data:
        audio = AudioFileClip(sd["audio_path"])
        img_clip = ImageClip(sd["image_path"], duration=audio.duration).with_audio(audio)
        clips.append(img_clip)

    outro_img = render_cta_slide("See You Next Week!")
    outro_path = os.path.join(tempfile.gettempdir(), "_weekly_outro.png")
    outro_img.save(outro_path)
    clips.append(ImageClip(outro_path, duration=OUTRO_DURATION))

    final = concatenate_videoclips(clips, method="compose")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac",
                          bitrate=VIDEO_BITRATE, audio_bitrate=AUDIO_BITRATE, logger="bar")
    print(f"\n✅ Weekly summary saved to: {output_path}")


async def run_weekly(json_path: str, output_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    week_of = data.get("week_of", "this week")
    stories = data.get("stories", [])
    deep_dive = data.get("deep_dive", None)
    video_title = f"TechAI Weekly — Week of {week_of}"

    print(f"🎬 Generating: {video_title}")
    work_dir = tempfile.mkdtemp(prefix="techai_weekly_")
    slide_data = []

    # Opening
    opening = (f"Welcome to TechAI Weekly for the week of {week_of}. "
               f"We have {len(stories)} top stories and one deep dive. Let's get into it.")
    img = render_title_slide("TechAI Weekly", f"Week of {week_of}")
    img_path = os.path.join(work_dir, "slide_open.png")
    img.save(img_path)
    audio_path = os.path.join(work_dir, "audio_open.mp3")
    await generate_tts(opening, audio_path)
    slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Top stories
    for i, story in enumerate(stories[:5]):
        headline = story.get("headline", f"Story {i+1}")
        bullets = story.get("bullets", [])
        narration = story.get("narration", f"Story {i+1}: {headline}. " + ". ".join(bullets))

        img = render_bullet_slide(f"#{i+1}: {headline}", bullets)
        img_path = os.path.join(work_dir, f"slide_story_{i}.png")
        img.save(img_path)
        audio_path = os.path.join(work_dir, f"audio_story_{i}.mp3")
        await generate_tts(narration, audio_path)
        slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Deep dive
    if deep_dive:
        dd_title = deep_dive.get("title", "Deep Dive")
        dd_sections = deep_dive.get("sections", [])
        for j, sec in enumerate(dd_sections):
            sec_title = sec.get("title", f"Deep Dive Part {j+1}")
            sec_bullets = sec.get("bullets", [])
            sec_narration = sec.get("narration", ". ".join(sec_bullets))

            img = render_bullet_slide(sec_title, sec_bullets)
            img_path = os.path.join(work_dir, f"slide_dd_{j}.png")
            img.save(img_path)
            audio_path = os.path.join(work_dir, f"audio_dd_{j}.mp3")
            await generate_tts(sec_narration, audio_path)
            slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Closing
    closing = "That wraps up this week in tech. If you found this useful, subscribe and share with your team. See you next week!"
    img = render_bullet_slide("This Week's Takeaways", ["Stay curious", "Ship code", "Subscribe for next week"])
    img_path = os.path.join(work_dir, "slide_close.png")
    img.save(img_path)
    audio_path = os.path.join(work_dir, "audio_close.mp3")
    await generate_tts(closing, audio_path)
    slide_data.append({"image_path": img_path, "audio_path": audio_path})

    assemble_video(slide_data, output_path, video_title)
    shutil.rmtree(work_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="TechAI Weekly Summary Generator")
    parser.add_argument("json_file", help="Path to weekly summary JSON file")
    parser.add_argument("--output", "-o", default=None, help="Output MP4 path")
    args = parser.parse_args()

    if args.output is None:
        args.output = os.path.join("pipeline", "output", "weekly-summary.mp4")

    asyncio.run(run_weekly(args.json_file, args.output))


if __name__ == "__main__":
    main()
