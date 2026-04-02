#!/usr/bin/env python3
"""
Post articles from src/articles/devto/ to Dev.to via API.
Usage: python post-to-devto.py [--article <slug>] [--dry-run]

Environment variables:
  DEVTO_API_KEY  - Dev.to API key (required)
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error
import argparse
from pathlib import Path

DEVTO_API_BASE = "https://dev.to/api"
ARTICLES_DIR = Path(__file__).parent.parent / "src" / "articles" / "devto"
TRACKING_FILE = ARTICLES_DIR / "posted.json"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()

    frontmatter = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Parse lists like ["tag1", "tag2"]
            if value.startswith("[") and value.endswith("]"):
                items = re.findall(r'"([^"]+)"|\'([^\']+)\'', value)
                value = [a or b for a, b in items]
            # Parse booleans
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            # Strip surrounding quotes
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            frontmatter[key] = value

    return frontmatter, body


def load_tracking() -> dict:
    """Load the posted articles tracking file."""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE) as f:
            return json.load(f)
    return {}


def save_tracking(tracking: dict):
    """Save the posted articles tracking file."""
    with open(TRACKING_FILE, "w") as f:
        json.dump(tracking, f, indent=2)


def get_existing_devto_articles(api_key: str) -> list[dict]:
    """Fetch existing articles from Dev.to to check for duplicates."""
    articles = []
    for page in range(1, 10):
        req = urllib.request.Request(
            f"{DEVTO_API_BASE}/articles/me?per_page=100&page={page}",
            headers={"api-key": api_key},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                page_articles = json.loads(resp.read())
                if not page_articles:
                    break
                articles.extend(page_articles)
        except urllib.error.HTTPError:
            break
    return articles


def post_article(api_key: str, frontmatter: dict, body: str, dry_run: bool) -> dict | None:
    """Post a single article to Dev.to."""
    tags = frontmatter.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    payload = {
        "article": {
            "title": frontmatter.get("title", "Untitled"),
            "body_markdown": body,
            "published": frontmatter.get("published", False),
            "tags": tags[:4],  # Dev.to max 4 tags
        }
    }

    if frontmatter.get("canonical_url"):
        payload["article"]["canonical_url"] = frontmatter["canonical_url"]

    if frontmatter.get("description"):
        payload["article"]["description"] = frontmatter["description"]

    if dry_run:
        print(f"  [DRY RUN] Would post: {payload['article']['title']}")
        print(f"  Tags: {payload['article']['tags']}")
        print(f"  Published: {payload['article']['published']}")
        print(f"  Canonical: {payload['article'].get('canonical_url', 'none')}")
        return {"id": "dry-run", "url": "https://dev.to/dry-run"}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{DEVTO_API_BASE}/articles",
        data=data,
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  ERROR {e.code}: {error_body}", file=sys.stderr)
        return None


def process_article(filepath: Path, api_key: str, tracking: dict, dry_run: bool, force: bool) -> bool:
    """Process and post a single article file."""
    slug = filepath.stem
    print(f"\nProcessing: {slug}")

    if not force and slug in tracking:
        print(f"  SKIP — already posted (Dev.to ID: {tracking[slug]['devto_id']})")
        return False

    content = filepath.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    if not frontmatter.get("title"):
        print(f"  SKIP — no title in frontmatter")
        return False

    result = post_article(api_key, frontmatter, body, dry_run)
    if result is None:
        print(f"  FAILED to post {slug}")
        return False

    article_url = result.get("url", result.get("path", "unknown"))
    article_id = result.get("id", "unknown")

    print(f"  ✓ Posted — ID: {article_id}, URL: {article_url}")

    if not dry_run:
        tracking[slug] = {
            "devto_id": article_id,
            "url": article_url,
            "title": frontmatter.get("title"),
        }

    return True


def main():
    parser = argparse.ArgumentParser(description="Post articles to Dev.to")
    parser.add_argument("--article", help="Specific article slug to post (or 'all')", default="all")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without posting")
    parser.add_argument("--force", action="store_true", help="Re-post even if already tracked")
    args = parser.parse_args()

    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        print("ERROR: DEVTO_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not ARTICLES_DIR.exists():
        print(f"ERROR: Articles directory not found: {ARTICLES_DIR}", file=sys.stderr)
        sys.exit(1)

    tracking = load_tracking()
    posted_count = 0

    if args.article == "all":
        files = sorted(ARTICLES_DIR.glob("*.md"))
    else:
        filepath = ARTICLES_DIR / f"{args.article}.md"
        if not filepath.exists():
            print(f"ERROR: Article not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        files = [filepath]

    print(f"Dev.to Article Poster — {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Found {len(files)} article(s) to process")

    for filepath in files:
        if process_article(filepath, api_key, tracking, args.dry_run, args.force):
            posted_count += 1

    if not args.dry_run and posted_count > 0:
        save_tracking(tracking)
        print(f"\nTracking saved to {TRACKING_FILE}")

    print(f"\nDone — {posted_count} article(s) posted")


if __name__ == "__main__":
    main()
