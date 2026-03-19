#!/usr/bin/env python3
"""
TechAI Explained — Yearly Recap Video Generator

Usage:
    python generate_yearly_recap.py <yearly.json> [--output <path.mp4>]

Generates a 15-20 minute year-in-review video with month-by-month highlights,
top 10 technologies, and predictions for next year.
"""

import argparse, asyncio, json, os, sys, tempfile, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    VOICE_NAME, VOICE_RATE, VOICE_PITCH,
    FPS, VIDEO_BITRATE, AUDIO_BITRATE,
    INTRO_DURATION, OUTRO_DURATION,
)
from slide_templates import (
    render_title_slide, render_bullet_slide, render_comparison_slide,
    render_quote_slide, render_cta_slide, render_intro_slide,
)


async def generate_tts(text: str, output_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=VOICE_NAME, rate=VOICE_RATE, pitch=VOICE_PITCH)
    await communicate.save(output_path)


def assemble_video(slide_data: list[dict], output_path: str, video_title: str):
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

    clips = []
    intro_img = render_intro_slide(video_title)
    intro_path = os.path.join(tempfile.gettempdir(), "_yearly_intro.png")
    intro_img.save(intro_path)
    clips.append(ImageClip(intro_path, duration=INTRO_DURATION))

    for sd in slide_data:
        audio = AudioFileClip(sd["audio_path"])
        img_clip = ImageClip(sd["image_path"], duration=audio.duration).with_audio(audio)
        clips.append(img_clip)

    outro_img = render_cta_slide("Happy New Year — Keep Building!")
    outro_path = os.path.join(tempfile.gettempdir(), "_yearly_outro.png")
    outro_img.save(outro_path)
    clips.append(ImageClip(outro_path, duration=OUTRO_DURATION))

    final = concatenate_videoclips(clips, method="compose")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac",
                          bitrate=VIDEO_BITRATE, audio_bitrate=AUDIO_BITRATE, logger="bar")
    print(f"\n✅ Yearly recap saved to: {output_path}")


async def run_yearly(json_path: str, output_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    year = data.get("year", "2026")
    months = data.get("months", [])
    top_technologies = data.get("top_technologies", [])
    predictions = data.get("predictions", [])
    video_title = f"Tech Year in Review {year}"

    print(f"🎬 Generating: {video_title}")
    work_dir = tempfile.mkdtemp(prefix="techai_yearly_")
    slide_data = []

    # Opening
    opening = (f"Welcome to the Tech Year in Review for {year}. "
               f"We'll walk through the biggest moments month by month, "
               f"count down the top 10 technologies, and share our predictions for {int(year)+1}.")
    img = render_title_slide(f"Tech Year in Review", year)
    img_path = os.path.join(work_dir, "slide_open.png")
    img.save(img_path)
    audio_path = os.path.join(work_dir, "audio_open.mp3")
    await generate_tts(opening, audio_path)
    slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Month-by-month
    for month_data in months:
        month_name = month_data.get("month", "")
        highlights = month_data.get("highlights", [])
        narration = month_data.get("narration",
                                     f"{month_name}: " + ". ".join(highlights))

        img = render_bullet_slide(month_name, highlights)
        img_path = os.path.join(work_dir, f"slide_{month_name.lower()}.png")
        img.save(img_path)
        audio_path = os.path.join(work_dir, f"audio_{month_name.lower()}.mp3")
        await generate_tts(narration, audio_path)
        slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Top 10 Technologies
    if top_technologies:
        tech_title = render_title_slide("Top 10 Technologies", year)
        tp = os.path.join(work_dir, "slide_top10_title.png")
        tech_title.save(tp)
        ap = os.path.join(work_dir, "audio_top10_title.mp3")
        await generate_tts(f"Now let's count down the top 10 technologies of {year}.", ap)
        slide_data.append({"image_path": tp, "audio_path": ap})

        # Show in groups of 5
        for chunk_start in range(0, len(top_technologies), 5):
            chunk = top_technologies[chunk_start:chunk_start+5]
            bullets = [f"#{chunk_start+i+1}: {t}" for i, t in enumerate(chunk)]
            narration = ". ".join(bullets)
            img = render_bullet_slide(f"Top 10 Technologies ({chunk_start+1}-{chunk_start+len(chunk)})", bullets)
            img_path = os.path.join(work_dir, f"slide_top10_{chunk_start}.png")
            img.save(img_path)
            audio_path = os.path.join(work_dir, f"audio_top10_{chunk_start}.mp3")
            await generate_tts(narration, audio_path)
            slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Predictions
    if predictions:
        pred_narration = (f"Here are our predictions for {int(year)+1}. " +
                          ". ".join(predictions[:5]))
        img = render_bullet_slide(f"Predictions for {int(year)+1}", predictions[:5])
        img_path = os.path.join(work_dir, "slide_predictions.png")
        img.save(img_path)
        audio_path = os.path.join(work_dir, "audio_predictions.mp3")
        await generate_tts(pred_narration, audio_path)
        slide_data.append({"image_path": img_path, "audio_path": audio_path})

    # Closing
    closing = (f"That's {year} in review! What a year for technology. "
               f"Subscribe for continued coverage in {int(year)+1}. Happy New Year and keep building!")
    img = render_bullet_slide("Thank You!", [f"What a year for tech", f"See you in {int(year)+1}", "Subscribe & share"])
    img_path = os.path.join(work_dir, "slide_close.png")
    img.save(img_path)
    audio_path = os.path.join(work_dir, "audio_close.mp3")
    await generate_tts(closing, audio_path)
    slide_data.append({"image_path": img_path, "audio_path": audio_path})

    assemble_video(slide_data, output_path, video_title)
    shutil.rmtree(work_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="TechAI Yearly Recap Generator")
    parser.add_argument("json_file", help="Path to yearly recap JSON file")
    parser.add_argument("--output", "-o", default=None, help="Output MP4 path")
    args = parser.parse_args()

    if args.output is None:
        args.output = os.path.join("pipeline", "output", "yearly-recap.mp4")

    asyncio.run(run_yearly(args.json_file, args.output))


if __name__ == "__main__":
    main()
