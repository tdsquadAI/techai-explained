# TechAI Explained — Automation Guide

## Daily Brief Pipeline

### How It Works

1. **Fetch News** — `fetch_news.py` pulls RSS feeds for each topic (`.NET`, `AI`, `Cloud`, `Dev`)
2. **Generate Brief** — Summarizes top stories into a structured JSON brief
3. **Create Video** — `generate_brief_video.py` produces a short video with TTS narration
4. **Upload** — Artifacts are stored; YouTube upload runs when API keys are configured

### Topics

| Topic       | Schedule      | Config Key |
|-------------|---------------|------------|
| .NET        | Daily         | `dotnet`   |
| AI          | Daily         | `ai`       |
| Cloud       | Daily         | `cloud`    |
| Dev (General) | Daily      | `dev`      |
| Security    | Sundays only  | `security` |
| Game Dev    | Sundays only  | `gamedev`  |

### Schedule

- **Daily at 06:00 UTC** — English briefs for all daily topics
- **Sundays** — Extra topics (Security, GameDev) + weekly summary
- **Manual trigger** — Run anytime via `workflow_dispatch`

### Adding a New Topic

1. Add an RSS feed entry in `pipeline/daily-briefs/topics.json`
2. If it should run daily, add it to the `for topic in ...` loop in `daily-briefs.yml`
3. If weekly, add it to the Sunday block

### Changing the Schedule

Edit the cron expression in `.github/workflows/daily-briefs.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # Minute Hour DayOfMonth Month DayOfWeek
```

## Hebrew Support

Hebrew briefs use a separate config (`topics_he.json`) with Hebrew-language RSS sources. The pipeline installs Noto fonts for Hebrew text rendering in videos.

To add Hebrew topics, update `topics_he.json` and the Hebrew generation step in the workflow.

## GitHub Actions Workflows

### `daily-briefs.yml`

- **Trigger:** Daily schedule + manual dispatch
- **Inputs:** Topics (comma-separated), Language (en/he/both)
- **Artifacts:** Stored for 30 days under `daily-briefs-{run_number}`

### `content-calendar.yml`

- **Trigger:** Every Monday at 07:00 UTC + manual dispatch
- **Creates:** Weekly content plan issue + daily brief tracking issues
- **Labels:** `content-calendar`, `daily-brief`, `automation`

## Affiliate Links

Managed in `config/affiliates.json`. Current integrations:

| Partner      | Status         |
|-------------|----------------|
| Gumroad     | ✅ Active       |
| DigitalOcean| ⏳ Pending signup |
| AWS         | ⏳ Pending signup |
| Cloudflare  | ⏳ Pending signup |
| JetBrains   | ⏳ Pending signup |
| AdSense     | ⏳ Pending signup |
| BuyMeACoffee| ⏳ Pending setup  |

## YouTube Upload

Currently a placeholder. When configured, set these secrets:

- `YOUTUBE_API_KEY`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`

The upload step will automatically activate when `YOUTUBE_API_KEY` is present.

## Secrets Required

| Secret                 | Repo              | Purpose                    |
|------------------------|-------------------|----------------------------|
| `YOUTUBE_API_KEY`      | techai-explained  | YouTube Data API           |
| `YOUTUBE_CLIENT_ID`    | techai-explained  | YouTube OAuth              |
| `YOUTUBE_CLIENT_SECRET`| techai-explained  | YouTube OAuth              |
| `GUMROAD_ACCESS_TOKEN` | techai-explained  | Gumroad API access         |
| `ADSENSE_PUBLISHER_ID` | techai-explained  | AdSense integration        |

## Content Calendar

The content calendar workflow auto-creates GitHub issues every Monday:
- One weekly overview issue with all content tasks
- Seven daily brief tracking issues

Labels are auto-applied for filtering.
