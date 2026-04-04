# Startup Catch-Up Script for TechAI Content Empire
# Run this when the devbox starts up after hibernation
# Generates missed daily briefs, pushes unpushed commits, launches Ralphs

$repoRoot = "$env:USERPROFILE\source\repos\techai-explained"
$today = Get-Date -Format "yyyy-MM-dd"

Write-Host "=== TechAI Startup Catch-Up ===" -ForegroundColor Cyan
Write-Host "Date: $today"
Write-Host ""

# 0. Git pull latest to ensure we have newest scripts and configs
Write-Host "--- Pulling latest from repo ---" -ForegroundColor Cyan
Push-Location $repoRoot
git pull --quiet 2>$null
Write-Host "  Pulled latest" -ForegroundColor Green
Pop-Location
Write-Host ""

# 1. Check and generate missing daily briefs (last 7 days)
Write-Host "--- Checking daily briefs ---" -ForegroundColor Cyan
$outputDir = "$repoRoot\pipeline\daily-briefs\output"
$topics = @("dotnet", "ai", "cloud", "dev")

# Add weekly topics on Sundays
if ((Get-Date).DayOfWeek -eq 'Sunday') {
    $topics += @("security", "gamedev")
}

for ($i = 0; $i -le 6; $i++) {
    $date = (Get-Date).AddDays(-$i).ToString("yyyy-MM-dd")
    $dateDir = "$outputDir\$date"

    if (-not (Test-Path "$dateDir\dotnet-brief.json")) {
        Write-Host "  Missing briefs for $date - generating..." -ForegroundColor Yellow
        foreach ($topic in $topics) {
            try {
                python "$repoRoot\pipeline\daily-briefs\fetch_news.py" $topic $date 2>$null
            } catch {
                Write-Host "    Warning: Failed to fetch $topic for $date" -ForegroundColor Red
            }
        }
        Write-Host "  Done for $date" -ForegroundColor Green
    } else {
        Write-Host "  $date - already generated" -ForegroundColor DarkGray
    }
}

# 2. Generate videos for today if briefs exist but videos don't
Write-Host ""
Write-Host "--- Checking video generation ---" -ForegroundColor Cyan
$todayDir = "$outputDir\$today"
if (Test-Path "$todayDir") {
    $briefs = Get-ChildItem "$todayDir" -Filter "*-brief.json" -ErrorAction SilentlyContinue
    foreach ($brief in $briefs) {
        $videoName = $brief.BaseName + ".mp4"
        if (-not (Test-Path "$todayDir\$videoName")) {
            Write-Host "  Generating video: $videoName" -ForegroundColor Yellow
            try {
                python "$repoRoot\pipeline\daily-briefs\generate_brief_video.py" $brief.FullName 2>$null
                Write-Host "  Generated $videoName" -ForegroundColor Green
            } catch {
                Write-Host "  Warning: Failed to generate $videoName" -ForegroundColor Red
            }
        } else {
            Write-Host "  $videoName - already exists" -ForegroundColor DarkGray
        }
    }
} else {
    Write-Host "  No briefs directory for today yet" -ForegroundColor DarkGray
}

# 3. Push any unpushed commits for all repos
Write-Host ""
Write-Host "--- Pushing unpushed commits ---" -ForegroundColor Cyan
$repos = @(
    "$env:USERPROFILE\source\repos\techai-explained",
    "$env:USERPROFILE\source\repos\content-empire",
    "$env:USERPROFILE\source\repos\jellybolt-games"
)

foreach ($repo in $repos) {
    if (Test-Path $repo) {
        Push-Location $repo
        try {
            $unpushed = git --no-pager log --oneline "@{u}..HEAD" 2>$null
            if ($unpushed) {
                $repoName = Split-Path $repo -Leaf
                Write-Host "  Pushing unpushed commits for $repoName..." -ForegroundColor Yellow
                $token = gh auth token --user tdsquadAI 2>$null
                if ($token) {
                    git push "https://tdsquadAI:$token@github.com/tdsquadAI/$repoName.git" HEAD 2>$null
                    Write-Host "  Pushed!" -ForegroundColor Green
                } else {
                    # Fallback to default push
                    git push 2>$null
                    Write-Host "  Pushed (default remote)!" -ForegroundColor Green
                }
            } else {
                $repoName = Split-Path $repo -Leaf
                Write-Host "  $repoName - nothing to push" -ForegroundColor DarkGray
            }
        } catch {
            Write-Host "  Warning: Push failed for $repo" -ForegroundColor Red
        }
        Pop-Location
    }
}

# 4. Launch Ralphs for each repo
Write-Host ""
Write-Host "--- Launching Ralphs ---" -ForegroundColor Cyan
foreach ($repoName in @("techai-explained", "jellybolt-games", "content-empire")) {
    $repoPath = "$env:USERPROFILE\source\repos\$repoName"
    if (Test-Path $repoPath) {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$repoPath'; `$host.UI.RawUI.WindowTitle = 'Ralph-$repoName'; copilot -p 'You are Ralph watching $repoName. Check issues, PRs, CI. Act autonomously.'" -WindowStyle Minimized
        Write-Host "  Ralph-$repoName launched" -ForegroundColor Green
    } else {
        Write-Host "  $repoName - repo not found, skipping" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "=== Startup catch-up complete! ===" -ForegroundColor Green
Write-Host "Time: $(Get-Date -Format 'HH:mm:ss')"
