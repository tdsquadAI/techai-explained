# TechAI Explained — Video Production Pipeline

## Overview

Automated slide-based video pipeline that converts markdown scripts into
full YouTube videos with **multiple visual slides**, TTS narration, and
fade transitions — not just a single image with audio.

## How It Works

```
Script (.md) ──► Parse Slides ──► Render Images (1920×1080)
                                          │
                                          ├──► TTS Audio (edge-tts)
                                          │
                                          ▼
                                   Assemble Video (moviepy)
                                          │
                                          ▼
                                    Final MP4 (1080p 30fps)
```

Each script section becomes its own slide with appropriate layout:
- **Title slides** — big centered title + subtitle
- **Bullet slides** — title + 3-7 bullet points
- **Code slides** — title + syntax-highlighted code block
- **Diagram slides** — title + ASCII/text diagram rendered in monospace
- **Comparison slides** — multi-column table
- **Quote slides** — large centered quote text

## Directory Structure

```
pipeline/
├── config.py                 # Voice, color, font, output settings
├── slide_templates.py        # Pillow-based slide renderers
├── generate_video.py         # Main video generator (script → MP4)
├── generate_daily_brief.py   # Daily tech brief generator (JSON → MP4)
├── generate_weekly_summary.py # Weekly summary generator (JSON → MP4)
├── generate_yearly_recap.py  # Yearly recap generator (JSON → MP4)
├── scripts/                  # Video scripts in slide-format markdown
├── templates/                # Templates & sample JSON for daily/weekly/yearly
├── output/                   # Generated MP4 videos
├── voice/                    # Generated audio files
└── visuals/                  # Supporting diagrams and images
```

## Script Format

Scripts use markdown with `## [TYPE] Title` markers:

```markdown
---
title: "Video Title"
duration: "10 minutes"
voice: "en-US-GuyNeural"
---

## [TITLE] Main Title
Subtitle text

## [BULLETS] Section Name
- Point one
- Point two
- Point three

## [CODE] Code Example
\`\`\`python
def hello():
    print("Hello, world!")
\`\`\`

## [DIAGRAM] Architecture
\`\`\`
User ──► API ──► Database
\`\`\`

## [COMPARISON] Feature Comparison
| Feature | Option A | Option B |
|---------|----------|----------|
| Speed   | Fast     | Slow     |

## [QUOTE] Key Insight
> "Start simple, iterate fast."
```

## Quick Start

### Prerequisites

```powershell
pip install edge-tts Pillow moviepy
# ffmpeg must be available in PATH
```

### Generate a Video

```powershell
cd C:\\Users\\tdsquadai\\source\repos\techai-explained
python pipeline/generate_video.py pipeline/scripts/01-ai-agents-explained.md --output pipeline/output/01-ai-agents-explained.mp4
```

### Generate a Daily Brief

```powershell
python pipeline/generate_daily_brief.py pipeline/templates/sample-daily.json --output pipeline/output/daily-brief.mp4
```

### Generate a Weekly Summary

```powershell
python pipeline/generate_weekly_summary.py pipeline/templates/sample-weekly.json --output pipeline/output/weekly-summary.mp4
```

### Generate a Yearly Recap

```powershell
python pipeline/generate_yearly_recap.py pipeline/templates/sample-yearly.json --output pipeline/output/yearly-recap.mp4
```

## Available Scripts

| # | Script | Topic |
|---|--------|-------|
| 01 | ai-agents-explained | AI Agent architecture patterns |
| 02 | rag-explained | Retrieval-Augmented Generation |
| 03 | docker-vs-podman | Container runtime comparison |
| 04 | why-kubernetes-won | K8s dominance and future |
| 05 | microservices-are-dead | Post-microservices architecture |
| 06 | ai-code-review | AI-powered code review |
| 07 | distributed-tracing | Cross-service request tracing |
| 08 | platform-engineer-tools | Essential platform engineering tools |
| 09 | dev-productivity-2026 | Modern developer productivity stack |

## YouTube Upload Tracking

All upload triggers download a named daily-brief artifact from an explicit,
successful `Daily Tech Briefs` run on `main` in the same repository. Scheduled
and manual runs resolve the requested UTC date (today by default); automatic
`workflow_run` uploads preserve the source artifact's content date, including
across midnight. Missing, expired, or video-free artifacts fail the job instead
of reporting an empty upload as successful. Artifacts already contain their
date directory, so downloads extract into the output root without nesting it twice.

כל הפעלות ההעלאה מורידות תוצר בשם מוגדר מריצת `Daily Tech Briefs` מוצלחת
בענף `main` באותו מאגר. הפעלות מתוזמנות וידניות מאתרות את תאריך ה-UTC
המבוקש (היום כברירת מחדל); הפעלה אוטומטית שומרת על תאריך התוכן המקורי גם
בחציית חצות. תוצר חסר, שפג תוקפו או שאינו מכיל סרטונים מכשיל את המשימה.
ההורדה שומרת על תיקיית התאריך המקורית ללא יצירת תיקייה כפולה.

`pipeline/upload-tracker.json` tracks series videos by filename and daily
briefs by `YYYY-MM-DD/filename`. English and Hebrew filenames are distinct.
Rerunning a date skips its uploaded briefs without blocking later dates.
Legacy filename-only brief records suppress uploads only on their recorded
upload day, because they do not contain a content date. When retrying an old
brief uploaded on a different day, verify its channel entry and add the
date-qualified tracker record before retrying to avoid duplicates.

מעקב העלאות: סרטוני סדרה מזוהים לפי שם הקובץ, ותקצירים יומיים לפי
`YYYY-MM-DD/filename`. קבצים באנגלית ובעברית נפרדים. הרצה חוזרת של אותו
תאריך מדלגת על תקצירים שכבר הועלו, בלי לחסום תאריכים חדשים.
רשומות ישנות ללא תאריך תוכן מונעות העלאה חוזרת רק ביום ההעלאה המתועד.
לפני ניסיון חוזר של תקציר ישן שהועלה ביום אחר, יש לבדוק את הסרטון בערוץ
ולהוסיף רשומת מעקב עם תאריך התוכן כדי למנוע כפילות.

Run the upload-tracking regression tests with:

```powershell
python -m unittest discover -s pipeline\daily-briefs -p test_upload_to_youtube.py
node --test .github\scripts\resolve-brief-artifact.test.cjs
```

## Customization

Edit `pipeline/config.py` to change:
- **Voice**: TTS voice name, speed, pitch
- **Colors**: Background gradient, text, accents
- **Fonts**: Title, body, code font sizes
- **Output**: Resolution, FPS, bitrate
