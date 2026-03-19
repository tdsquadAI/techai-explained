# Daily Brief Scheduler for TechAI Explained
# Run this as a Windows Scheduled Task or keep running in background

param(
    [int]$IntervalHours = 24,
    [string]$RunTime = "06:00"  # Generate briefs at 6 AM
)

$repoRoot = "C:\Users\tamirdresher\source\repos\techai-explained"
$pipelineDir = "$repoRoot\pipeline\daily-briefs"

# Topics to generate daily
$dailyTopics = @("dotnet", "ai", "cloud", "dev")
# Topics to generate weekly (on Sundays)
$weeklyTopics = @("security", "gamedev")

function Generate-DailyBriefs {
    param([string]$Date)

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Generating daily briefs for $Date" -ForegroundColor Cyan

    foreach ($topic in $dailyTopics) {
        Write-Host "  Fetching news for: $topic" -ForegroundColor Yellow
        python "$pipelineDir\fetch_news.py" $topic $Date

        $briefJson = "$pipelineDir\output\$Date\$topic-brief.json"
        if (Test-Path $briefJson) {
            Write-Host "  Generating video for: $topic" -ForegroundColor Green
            python "$pipelineDir\generate_brief_video.py" $briefJson
        }
    }

    # Check if Sunday for weekly topics
    if ((Get-Date $Date).DayOfWeek -eq 'Sunday') {
        foreach ($topic in $weeklyTopics) {
            Write-Host "  Generating weekly brief for: $topic" -ForegroundColor Magenta
            python "$pipelineDir\fetch_news.py" $topic $Date
            $briefJson = "$pipelineDir\output\$Date\$topic-brief.json"
            if (Test-Path $briefJson) {
                python "$pipelineDir\generate_brief_video.py" $briefJson
            }
        }
    }

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - All briefs generated!" -ForegroundColor Green
}

function Start-Scheduler {
    Write-Host "TechAI Daily Brief Scheduler Started" -ForegroundColor Cyan
    Write-Host "Generating briefs every $IntervalHours hours at $RunTime" -ForegroundColor Yellow
    Write-Host "Daily topics: $($dailyTopics -join ', ')"
    Write-Host "Weekly topics: $($weeklyTopics -join ', ') (Sundays only)"
    Write-Host ""

    while ($true) {
        $now = Get-Date
        $targetTime = Get-Date -Hour ([int]$RunTime.Split(':')[0]) -Minute ([int]$RunTime.Split(':')[1]) -Second 0

        if ($now -gt $targetTime) {
            $targetTime = $targetTime.AddDays(1)
        }

        $waitSeconds = ($targetTime - $now).TotalSeconds
        Write-Host "Next run at: $targetTime (waiting $([Math]::Round($waitSeconds/3600, 1)) hours)"

        Start-Sleep -Seconds $waitSeconds

        $today = Get-Date -Format 'yyyy-MM-dd'
        Generate-DailyBriefs -Date $today
    }
}

# If called with -Now, generate immediately
if ($args -contains '-Now') {
    Generate-DailyBriefs -Date (Get-Date -Format 'yyyy-MM-dd')
} else {
    Start-Scheduler
}
