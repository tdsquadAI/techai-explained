# Yearly Recap Template

## Format
- Duration: 15-20 minutes
- Title: "Tech Year in Review {year}"
- Month-by-month highlights
- Top 10 technologies
- Predictions for next year

## JSON Input Format

```json
{
  "year": "2026",
  "months": [
    {
      "month": "January",
      "highlights": ["Highlight 1", "Highlight 2", "Highlight 3"],
      "narration": "January started with..."
    }
  ],
  "top_technologies": [
    "Technology 1",
    "Technology 2",
    "..."
  ],
  "predictions": [
    "Prediction 1",
    "Prediction 2",
    "..."
  ]
}
```

## Generation Command

```powershell
python pipeline/generate_yearly_recap.py pipeline/templates/sample-yearly.json --output pipeline/output/yearly-recap.mp4
```
