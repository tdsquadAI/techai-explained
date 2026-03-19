"""
Monthly Recap Generator for TechAI Explained.
Reads all daily brief JSONs from the past 30 days,
picks the top 15-20 stories across all topics,
and generates a 10-15 minute recap video grouped by topic.
"""
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from generate_brief_video import (
    _gradient_bg, _get_font, _get_bold_font, _draw_topic_badge,
    generate_tts, compose_video_ffmpeg, make_item_slide, make_outro_slide,
    TOPIC_COLORS, WIDTH, HEIGHT,
)

try:
    from PIL import ImageDraw
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


def collect_monthly_stories(output_root, end_date_str=None, days=30):
    """Gather all daily brief items from the past N days."""
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    stories_by_topic = {}
    for day_offset in range(days):
        day = end_date - timedelta(days=day_offset)
        day_str = day.strftime("%Y-%m-%d")
        day_dir = output_root / day_str

        if not day_dir.exists():
            continue

        for brief_file in day_dir.glob("*-brief.json"):
            with open(brief_file) as f:
                brief = json.load(f)
            topic_id = brief["topic_id"]
            topic_name = brief["topic_name"]
            if topic_id not in stories_by_topic:
                stories_by_topic[topic_id] = {
                    "topic_name": topic_name,
                    "items": [],
                }
            for item in brief["items"]:
                item["date"] = brief["date"]
                stories_by_topic[topic_id]["items"].append(item)

    return stories_by_topic


def make_month_title_slide(month_name, year, story_count, topic_count, output_path):
    """Create the monthly recap title slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)

    title_font = _get_bold_font(72)
    draw.text((120, 240), f"{month_name} {year}", fill="white", font=title_font)

    sub_font = _get_bold_font(48)
    draw.text((120, 340), "Monthly Tech Recap", fill=(0, 200, 255), font=sub_font)

    stats_font = _get_font(32)
    draw.text(
        (120, 460),
        f"{story_count} stories · {topic_count} topics",
        fill=(180, 180, 220),
        font=stats_font,
    )

    brand_font = _get_bold_font(28)
    draw.text((120, HEIGHT - 80), "TechAI Explained", fill=(100, 100, 140), font=brand_font)

    img.save(output_path)


def make_topic_summary_slide(topic_id, topic_name, items, output_path):
    """Create a summary slide listing headlines for a topic."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    color = TOPIC_COLORS.get(topic_id, (100, 100, 255))

    # Topic header bar
    draw.rectangle([0, 40, WIDTH, 120], fill=color)
    header_font = _get_bold_font(48)
    draw.text((120, 50), topic_name, fill="white", font=header_font)

    # List headlines
    item_font = _get_font(28)
    y = 160
    for i, item in enumerate(items[:8]):
        bullet = f"• {item['headline'][:70]}"
        if len(item["headline"]) > 70:
            bullet += "…"
        draw.text((140, y), bullet, fill=(200, 200, 230), font=item_font)
        y += 50
        if y > HEIGHT - 120:
            break

    count_font = _get_font(24)
    draw.text(
        (120, HEIGHT - 80),
        f"{len(items)} stories this month",
        fill=(140, 140, 180),
        font=count_font,
    )

    img.save(output_path)


async def generate_monthly_recap(end_date_str=None):
    """Main entry point for monthly recap generation."""
    output_root = Path(__file__).parent / "output"
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    month_name = end_date.strftime("%B")
    year = end_date.year
    date_str = end_date.strftime("%Y-%m-%d")

    stories_by_topic = collect_monthly_stories(output_root, end_date_str, days=30)

    if not stories_by_topic:
        print("No stories found for the past 30 days.")
        return

    total_stories = sum(len(v["items"]) for v in stories_by_topic.values())

    # Output directories
    out_dir = output_root / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    slides_dir = out_dir / "_monthly_slides"
    audio_dir = out_dir / "_monthly_audio"
    slides_dir.mkdir(exist_ok=True)
    audio_dir.mkdir(exist_ok=True)

    slides = []
    audio_files = []

    # Title slide
    title_slide = str(slides_dir / "title.png")
    make_month_title_slide(month_name, year, total_stories, len(stories_by_topic), title_slide)
    slides.append(title_slide)

    title_audio = str(audio_dir / "title.mp3")
    await generate_tts(
        f"Welcome to the TechAI Monthly Recap for {month_name} {year}. "
        f"We covered {total_stories} stories across {len(stories_by_topic)} topics. "
        f"Let's dive in.",
        title_audio,
    )
    audio_files.append(title_audio)

    # Per-topic sections: summary slide + top 3-4 detail slides
    for tid, data in stories_by_topic.items():
        # Topic summary slide
        summary_slide = str(slides_dir / f"summary_{tid}.png")
        make_topic_summary_slide(tid, data["topic_name"], data["items"], summary_slide)
        slides.append(summary_slide)

        summary_audio = str(audio_dir / f"summary_{tid}.mp3")
        await generate_tts(
            f"In {data['topic_name']}, we covered {len(data['items'])} stories. Here are the highlights.",
            summary_audio,
        )
        audio_files.append(summary_audio)

        # Top detail items (max 4 per topic)
        top_items = data["items"][:4]
        dummy_brief = {"topic_id": tid, "topic_name": data["topic_name"], "items": top_items}
        for i, item in enumerate(top_items):
            slide_path = str(slides_dir / f"{tid}_detail_{i}.png")
            make_item_slide(dummy_brief, i, item, slide_path)
            slides.append(slide_path)

            narration = f"{item['headline']}. {item['summary']}"
            audio_path = str(audio_dir / f"{tid}_detail_{i}.mp3")
            await generate_tts(narration, audio_path)
            audio_files.append(audio_path)

    # Outro
    outro_slide = str(slides_dir / "outro.png")
    outro_brief = {"topic_id": "dev", "topic_name": "Monthly Recap"}
    make_outro_slide(outro_brief, outro_slide)
    slides.append(outro_slide)

    outro_audio = str(audio_dir / "outro.mp3")
    await generate_tts(
        f"That's the TechAI Monthly Recap for {month_name} {year}. "
        "Subscribe for daily briefs and never miss a story. See you next month!",
        outro_audio,
    )
    audio_files.append(outro_audio)

    # Compose video
    output_path = out_dir / "monthly-recap.mp4"
    compose_video_ffmpeg(slides, audio_files, str(output_path))

    # Cleanup
    import shutil
    shutil.rmtree(slides_dir, ignore_errors=True)
    shutil.rmtree(audio_dir, ignore_errors=True)

    print(f"Monthly recap saved: {output_path}")


if __name__ == "__main__":
    end_date = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(generate_monthly_recap(end_date))
