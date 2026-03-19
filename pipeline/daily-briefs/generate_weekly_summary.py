"""
Weekly Summary Generator for TechAI Explained.
Reads all daily brief JSONs from the past 7 days,
picks the top 10 stories across all topics,
and generates a longer video grouped by topic section.
"""
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Re-use video generation helpers from the brief video module
from generate_brief_video import (
    _gradient_bg, _get_font, _get_bold_font, _draw_topic_badge,
    generate_tts, compose_video_ffmpeg, TOPIC_COLORS, WIDTH, HEIGHT,
)

try:
    from PIL import ImageDraw
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


def collect_weekly_stories(output_root, end_date_str=None):
    """Gather all daily brief items from the past 7 days."""
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    stories_by_topic = {}
    for day_offset in range(7):
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


def make_section_header_slide(topic_id, topic_name, count, output_path):
    """Create a topic section divider slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)
    color = TOPIC_COLORS.get(topic_id, (100, 100, 255))

    # Colored bar
    draw.rectangle([0, HEIGHT // 2 - 60, WIDTH, HEIGHT // 2 + 60], fill=color)
    font = _get_bold_font(64)
    draw.text((120, HEIGHT // 2 - 40), topic_name, fill="white", font=font)

    sub_font = _get_font(32)
    draw.text(
        (120, HEIGHT // 2 + 80),
        f"{count} top stories this week",
        fill=(200, 200, 230),
        font=sub_font,
    )

    img.save(output_path)


def make_stats_slide(stories_by_topic, date_range, output_path):
    """Create a 'week in numbers' slide."""
    img = _gradient_bg()
    draw = ImageDraw.Draw(img)

    title_font = _get_bold_font(56)
    draw.text((120, 80), "Week in Numbers", fill="white", font=title_font)

    date_font = _get_font(28)
    draw.text((120, 160), date_range, fill=(140, 140, 180), font=date_font)

    total_stories = sum(len(v["items"]) for v in stories_by_topic.values())
    total_topics = len(stories_by_topic)

    stats_font = _get_bold_font(42)
    val_font = _get_font(32)
    y = 260
    stats = [
        (f"{total_stories}", "total stories covered"),
        (f"{total_topics}", "topic categories"),
        (f"7", "days of coverage"),
    ]
    for val, label in stats:
        draw.text((160, y), val, fill=(0, 200, 255), font=stats_font)
        draw.text((300, y + 8), label, fill=(200, 200, 230), font=val_font)
        y += 80

    # Per-topic breakdown
    y += 40
    for tid, data in stories_by_topic.items():
        color = TOPIC_COLORS.get(tid, (100, 100, 255))
        draw.rectangle([160, y + 5, 180, y + 25], fill=color)
        draw.text(
            (200, y),
            f"{data['topic_name']}: {len(data['items'])} stories",
            fill=(200, 200, 230),
            font=val_font,
        )
        y += 45

    brand_font = _get_bold_font(28)
    draw.text((120, HEIGHT - 80), "TechAI Explained", fill=(100, 100, 140), font=brand_font)
    img.save(output_path)


async def generate_weekly_summary(end_date_str=None):
    """Main entry point for weekly summary generation."""
    output_root = Path(__file__).parent / "output"
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=6)
    date_range = f"{start_date.strftime('%b %d')} – {end_date.strftime('%b %d, %Y')}"
    date_str = end_date.strftime("%Y-%m-%d")

    stories_by_topic = collect_weekly_stories(output_root, end_date_str)

    if not stories_by_topic:
        print("No stories found for the past 7 days.")
        return

    # Pick top stories per topic (max 3 each, 10 total)
    top_stories = {}
    total_picked = 0
    for tid, data in stories_by_topic.items():
        picked = data["items"][:3]
        if picked:
            top_stories[tid] = {"topic_name": data["topic_name"], "items": picked}
            total_picked += len(picked)
        if total_picked >= 10:
            break

    # Create output dir
    out_dir = output_root / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    slides_dir = out_dir / "_weekly_slides"
    audio_dir = out_dir / "_weekly_audio"
    slides_dir.mkdir(exist_ok=True)
    audio_dir.mkdir(exist_ok=True)

    slides = []
    audio_files = []
    idx = 0

    # Intro narration
    intro_text = f"Welcome to the TechAI Weekly Roundup for {date_range}. Here are the top stories from the week."
    from generate_brief_video import make_title_slide

    intro_brief = {
        "topic_id": "dev",
        "topic_name": "TechAI Weekly Roundup",
        "date": date_range,
        "items": [],
    }
    intro_slide = str(slides_dir / "intro.png")
    make_title_slide(intro_brief, intro_slide)
    slides.append(intro_slide)
    intro_audio = str(audio_dir / "intro.mp3")
    await generate_tts(intro_text, intro_audio)
    audio_files.append(intro_audio)
    idx += 1

    # Stats slide
    stats_slide = str(slides_dir / "stats.png")
    make_stats_slide(stories_by_topic, date_range, stats_slide)
    slides.append(stats_slide)
    stats_narration = f"This week we covered {sum(len(v['items']) for v in stories_by_topic.values())} stories across {len(stories_by_topic)} topics."
    stats_audio = str(audio_dir / "stats.mp3")
    await generate_tts(stats_narration, stats_audio)
    audio_files.append(stats_audio)
    idx += 1

    # Topic sections
    for tid, data in top_stories.items():
        # Section header
        header_slide = str(slides_dir / f"header_{tid}.png")
        make_section_header_slide(tid, data["topic_name"], len(data["items"]), header_slide)
        slides.append(header_slide)
        header_audio = str(audio_dir / f"header_{tid}.mp3")
        await generate_tts(f"Let's look at {data['topic_name']}.", header_audio)
        audio_files.append(header_audio)

        # Story slides
        from generate_brief_video import make_item_slide
        dummy_brief = {"topic_id": tid, "topic_name": data["topic_name"], "items": data["items"]}
        for i, item in enumerate(data["items"]):
            slide_path = str(slides_dir / f"{tid}_item_{i}.png")
            make_item_slide(dummy_brief, i, item, slide_path)
            slides.append(slide_path)

            narration = f"{item['headline']}. {item['summary']}"
            audio_path = str(audio_dir / f"{tid}_item_{i}.mp3")
            await generate_tts(narration, audio_path)
            audio_files.append(audio_path)

    # Outro
    from generate_brief_video import make_outro_slide
    outro_brief = {"topic_id": "dev", "topic_name": "TechAI Weekly Roundup"}
    outro_slide = str(slides_dir / "outro.png")
    make_outro_slide(outro_brief, outro_slide)
    slides.append(outro_slide)
    outro_audio = str(audio_dir / "outro.mp3")
    await generate_tts("That's the TechAI Weekly Roundup. Subscribe for daily updates!", outro_audio)
    audio_files.append(outro_audio)

    # Compose video
    output_path = out_dir / "weekly-roundup.mp4"
    compose_video_ffmpeg(slides, audio_files, str(output_path))

    # Cleanup
    import shutil
    shutil.rmtree(slides_dir, ignore_errors=True)
    shutil.rmtree(audio_dir, ignore_errors=True)

    print(f"Weekly summary saved: {output_path}")


if __name__ == "__main__":
    end_date = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(generate_weekly_summary(end_date))
