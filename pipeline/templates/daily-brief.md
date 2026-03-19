# Daily Brief Template

## Format
- Duration: 60-90 seconds
- Title: "TechAI Daily Brief — {date}"
- 3 tech news items per day
- Quick slide per item (headline + 1-2 bullets)
- Closing: "Subscribe for daily updates"

## JSON Input Format

```json
{
  "date": "2026-03-19",
  "items": [
    {
      "headline": "Story headline here",
      "bullets": [
        "Key point 1",
        "Key point 2"
      ]
    },
    {
      "headline": "Second story",
      "bullets": [
        "Key point 1",
        "Key point 2"
      ]
    },
    {
      "headline": "Third story",
      "bullets": [
        "Key point 1",
        "Key point 2"
      ]
    }
  ]
}
```

## Generation Command

```powershell
python pipeline/generate_daily_brief.py pipeline/templates/sample-daily.json --output pipeline/output/daily-brief.mp4
```
