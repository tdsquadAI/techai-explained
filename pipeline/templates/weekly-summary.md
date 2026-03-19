# Weekly Summary Template

## Format
- Duration: 5-8 minutes
- Title: "TechAI Weekly — Week of {date}"
- Top 5 stories of the week (approx. 1 min each)
- 1 deeper dive on the biggest story
- Closing with subscribe CTA

## JSON Input Format

```json
{
  "week_of": "March 17, 2026",
  "stories": [
    {
      "headline": "Story headline",
      "bullets": ["Point 1", "Point 2", "Point 3"],
      "narration": "Full narration text for the story."
    }
  ],
  "deep_dive": {
    "title": "Deep dive topic",
    "sections": [
      {
        "title": "Section title",
        "bullets": ["Bullet 1", "Bullet 2"],
        "narration": "Narration for this deep dive section."
      }
    ]
  }
}
```

## Generation Command

```powershell
python pipeline/generate_weekly_summary.py pipeline/templates/sample-weekly.json --output pipeline/output/weekly-summary.mp4
```
