"""
Fetches tech news from RSS feeds and filters by topic keywords.
Outputs a JSON file with the top 3-5 stories for video generation.
"""
import feedparser
import json
import re
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


def fetch_topic_news(topic_config, max_items=5):
    """Fetch and rank news items for a specific topic."""
    all_items = []
    for feed_url in topic_config['rss_feeds']:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:20]:
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                # Strip HTML tags
                summary = re.sub(r'<[^>]+>', '', summary)[:300]
                published = entry.get('published', entry.get('updated', ''))
                link = entry.get('link', '')

                # Score by keyword relevance
                text = (title + ' ' + summary).lower()
                score = sum(1 for kw in topic_config['keywords'] if kw.lower() in text)

                if score > 0:
                    all_items.append({
                        'title': title,
                        'summary': summary,
                        'link': link,
                        'published': published,
                        'score': score,
                        'source': feed_url
                    })
        except Exception as e:
            print(f"Warning: Failed to fetch {feed_url}: {e}", file=sys.stderr)

    # Sort by score (relevance) then recency
    all_items.sort(key=lambda x: x['score'], reverse=True)
    return all_items[:max_items]


def generate_brief_json(topic_id, date_str=None, config_file='topics.json'):
    """Generate the news brief JSON for a topic."""
    topics_path = Path(__file__).parent / config_file
    with open(topics_path, encoding='utf-8') as f:
        config = json.load(f)

    topic = next((t for t in config['topics'] if t['id'] == topic_id), None)
    if not topic:
        print(f"Unknown topic: {topic_id}")
        sys.exit(1)

    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    items = fetch_topic_news(topic)

    brief = {
        'topic_id': topic_id,
        'topic_name': topic['name'],
        'date': date_str,
        'intro': topic['intro'],
        'outro': topic['outro'],
        'items': [
            {
                'headline': item['title'],
                'summary': item['summary'][:200],
                'source_url': item['link']
            }
            for item in items
        ]
    }

    # Save to output directory
    output_dir = Path(__file__).parent / 'output' / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'{topic_id}-brief.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(brief, f, indent=2, ensure_ascii=False)

    print(f"Generated brief: {output_path}")
    return brief


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Fetch tech news for a topic')
    parser.add_argument('topic_id', help='Topic ID (e.g., dotnet, ai, cloud, dev)')
    parser.add_argument('date', nargs='?', default=None, help='Date (YYYY-MM-DD)')
    parser.add_argument('--config', default='topics.json', help='Config file (default: topics.json)')
    args = parser.parse_args()
    
    generate_brief_json(args.topic_id, args.date, args.config)
