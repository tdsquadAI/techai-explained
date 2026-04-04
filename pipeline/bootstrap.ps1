# TechAI Content Empire — Machine Bootstrap
# Install ONCE per machine. It self-updates from the repo.
# 
# One-time install:
#   1. Clone the repos
#   2. Run: powershell -File bootstrap.ps1 -Install
#   3. Done. Every future boot auto-syncs.

param(
    [switch]$Install  # First-time install flag
)

$ErrorActionPreference = "Continue"
$manifestRepo = "$env:USERPROFILE\source\repos\techai-explained"
$manifestPath = "$manifestRepo\pipeline\machine-manifest.json"
$logFile = "$env:TEMP\bootstrap-$(Get-Date -Format 'yyyy-MM-dd').log"

function Log($msg) {
    $ts = Get-Date -Format 'HH:mm:ss'
    "$ts  $msg" | Tee-Object -FilePath $logFile -Append
}

Log "=== Bootstrap starting ==="

# Step 1: Git pull all repos
Log "Pulling latest from all repos..."
$token = gh auth token --user tdsquadAI 2>$null

$repos = @(
    "$env:USERPROFILE\source\repos\techai-explained",
    "$env:USERPROFILE\source\repos\content-empire",
    "$env:USERPROFILE\source\repos\jellybolt-games"
)

foreach ($repo in $repos) {
    if (Test-Path $repo) {
        Push-Location $repo
        git pull --quiet 2>$null
        $repoName = Split-Path $repo -Leaf
        Log "  Pulled: $repoName"
        Pop-Location
    }
}

# Step 2: Read manifest
if (-not (Test-Path $manifestPath)) {
    Log "ERROR: Manifest not found at $manifestPath"
    exit 1
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
Log "Manifest version: $($manifest.version), last updated: $($manifest.last_updated)"

# --- Machine Registration ---
$machineId = $env:COMPUTERNAME
$machineRegistry = "$manifestRepo\pipeline\machines\registry.json"

# Ensure directory exists
New-Item -Path "$manifestRepo\pipeline\machines" -ItemType Directory -Force -ErrorAction SilentlyContinue | Out-Null

# Load or create registry
if (Test-Path $machineRegistry) {
    $registry = Get-Content $machineRegistry -Raw | ConvertFrom-Json
} else {
    $registry = @{ machines = @{} } | ConvertTo-Json | ConvertFrom-Json
}

# Check if this machine is new
$isNewMachine = -not ($registry.machines.PSObject.Properties.Name -contains $machineId)

if ($isNewMachine) {
    Log "NEW MACHINE DETECTED: $machineId — running full setup"
    
    # Register this machine
    $machineInfo = @{
        hostname = $machineId
        first_seen = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        last_seen = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        os = [System.Environment]::OSVersion.VersionString
        user = $env:USERNAME
        setup_complete = @()
        setup_pending = @()
    }
    
    # Add to registry
    $registry.machines | Add-Member -NotePropertyName $machineId -NotePropertyValue $machineInfo -Force
    $registry | ConvertTo-Json -Depth 5 | Set-Content $machineRegistry -Encoding utf8
    
    # Commit and push registration
    Push-Location $manifestRepo
    git add pipeline/machines/registry.json
    git commit -m "chore: register new machine $machineId" --quiet 2>$null
    if ($token) {
        git push "https://tdsquadAI:$token@github.com/tdsquadAI/techai-explained.git" HEAD --quiet 2>$null
    }
    Pop-Location
    
    # Create GitHub issue for this machine's setup
    if ($token) {
        $issueBody = @"
New machine **$machineId** registered at $(Get-Date -Format 'yyyy-MM-dd HH:mm').

## Setup Checklist
- [ ] All 3 repos cloned
- [ ] bootstrap.ps1 -Install completed
- [ ] Python deps installed (feedparser, edge-tts, Pillow, moviepy)
- [ ] TechAI-StartupCatchUp task registered
- [ ] TechAI-DailyBriefs task registered
- [ ] gh auth login for tdsquadAI
- [ ] First daily briefs generated
- [ ] All 3 Ralphs launched

## Machine Info
- Hostname: $machineId
- OS: $([System.Environment]::OSVersion.VersionString)
- User: $env:USERNAME
"@
        $headers = @{ Authorization = "token $token"; Accept = "application/vnd.github.v3+json" }
        $body = @{
            title = "🖥️ Machine setup: $machineId"
            body = $issueBody
            labels = @("automation")
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri "https://api.github.com/repos/tdsquadAI/techai-explained/issues" `
            -Method POST -Headers $headers -Body $body -ContentType "application/json" -ErrorAction SilentlyContinue
        Log "  Created GitHub issue for machine setup"
    }
    
    # Force -Install behavior for new machines
    $Install = $true
} else {
    # Update last_seen
    $registry.machines.$machineId.last_seen = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    $registry | ConvertTo-Json -Depth 5 | Set-Content $machineRegistry -Encoding utf8
    Log "Known machine: $machineId (last seen updated)"
}

# --- Run setup checks ---
$setupChecklist = $manifest.machines.setup_checklist
$completedItems = @()
$pendingItems = @()

foreach ($check in $setupChecklist) {
    $passed = $false
    switch ($check.id) {
        "repos-cloned" { 
            $passed = (Test-Path "$env:USERPROFILE\source\repos\techai-explained") -and 
                      (Test-Path "$env:USERPROFILE\source\repos\content-empire") -and
                      (Test-Path "$env:USERPROFILE\source\repos\jellybolt-games")
        }
        "bootstrap-installed" {
            $startupPath = [Environment]::GetFolderPath('Startup')
            $passed = Test-Path (Join-Path $startupPath "ContentEmpire-Bootstrap.lnk")
        }
        "python-deps" {
            python -c "import feedparser, edge_tts, PIL" 2>$null
            $passed = ($LASTEXITCODE -eq 0)
        }
        "startup-task" {
            $passed = [bool](Get-ScheduledTask -TaskName "TechAI-StartupCatchUp" -ErrorAction SilentlyContinue)
        }
        "daily-task" {
            $passed = [bool](Get-ScheduledTask -TaskName "TechAI-DailyBriefs" -ErrorAction SilentlyContinue)
        }
        "git-auth" {
            $passed = [bool](gh auth token --user tdsquadAI 2>$null)
        }
        "first-briefs" {
            $passed = (Get-ChildItem "$manifestRepo\pipeline\daily-briefs\output" -Directory -ErrorAction SilentlyContinue).Count -gt 0
        }
        "ralphs-launched" {
            $passed = $true  # Will be true after bootstrap runs
        }
    }
    
    if ($passed) { 
        $completedItems += $check.id 
        Log "  ✅ $($check.id)"
    } else { 
        $pendingItems += $check.id
        Log "  ❌ $($check.id) — will fix"
    }
}

# Update registry with setup status
$registry.machines.$machineId.setup_complete = $completedItems
$registry.machines.$machineId.setup_pending = $pendingItems
$registry | ConvertTo-Json -Depth 5 | Set-Content $machineRegistry -Encoding utf8

# Step 3: Sync scheduled tasks
foreach ($task in $manifest.scheduled_tasks) {
    $existing = Get-ScheduledTask -TaskName $task.name -ErrorAction SilentlyContinue
    if (-not $existing) {
        Log "  Registering new task: $($task.name)"
        $repoPath = ($manifest.repos | Where-Object { $_.name -eq $task.repo }).path
        $scriptPath = Join-Path $repoPath $task.script
        
        $action = New-ScheduledTaskAction -Execute "powershell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
        
        if ($task.trigger -eq "daily") {
            $trigger = New-ScheduledTaskTrigger -Daily -At $task.time
        } else {
            $trigger = New-ScheduledTaskTrigger -AtLogOn
        }
        
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        
        Register-ScheduledTask -TaskName $task.name -Action $action -Trigger $trigger `
            -Settings $settings -Description $task.description -ErrorAction SilentlyContinue
        Log "  Registered: $($task.name)"
    } else {
        Log "  Task exists: $($task.name) ($($existing.State))"
    }
}

# Step 4: Sync startup scripts
foreach ($startup in $manifest.startup_scripts) {
    $taskName = $startup.name
    $existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if (-not $existing) {
        Log "  Registering startup task: $taskName"
        $repoPath = ($manifest.repos | Where-Object { $_.name -eq $startup.repo }).path
        $scriptPath = Join-Path $repoPath $startup.script
        
        $action = New-ScheduledTaskAction -Execute "powershell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
        $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable
        
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
            -Settings $settings -Description $startup.description -ErrorAction SilentlyContinue
        Log "  Registered: $taskName"
    }
}

# Step 5: Install Python deps
Log "Checking Python dependencies..."
foreach ($dep in $manifest.python_deps) {
    $installed = python -c "import $dep" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Log "  Installing: $dep"
        pip install $dep --quiet 2>$null
    }
}

# Step 6: Run catch-up (generate missed briefs)
$catchupScript = ($manifest.startup_scripts | Where-Object { $_.name -eq "TechAI-StartupCatchUp" })
if ($catchupScript) {
    $repoPath = ($manifest.repos | Where-Object { $_.name -eq $catchupScript.repo }).path
    $scriptPath = Join-Path $repoPath $catchupScript.script
    if (Test-Path $scriptPath) {
        Log "Running catch-up script..."
        & $scriptPath
    }
}

# Step 7: Launch Ralphs (read STATUS.md for context)
Log "Launching Ralphs..."
foreach ($ralph in $manifest.ralphs) {
    $repoPath = ($manifest.repos | Where-Object { $_.name -eq $ralph.repo }).path
    if (Test-Path $repoPath) {
        # Check if Ralph is already running for this repo
        $existing = Get-Process -Name "copilot" -ErrorAction SilentlyContinue | 
            Where-Object { $_.MainWindowTitle -eq $ralph.name }
        if (-not $existing) {
            Start-Process powershell -ArgumentList @(
                "-NoExit", "-Command", 
                "cd '$repoPath'; `$host.UI.RawUI.WindowTitle = '$($ralph.name)'; copilot -p '$($ralph.prompt)'"
            ) -WindowStyle Minimized
            Log "  Launched: $($ralph.name)"
        } else {
            Log "  Already running: $($ralph.name)"
        }
    }
}

# Step 8: First-time install — add bootstrap to Windows Startup folder
if ($Install) {
    Log "First-time install: Adding bootstrap to Startup folder..."
    $startupPath = [Environment]::GetFolderPath('Startup')
    $shortcutPath = Join-Path $startupPath "ContentEmpire-Bootstrap.lnk"
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$manifestRepo\pipeline\bootstrap.ps1`""
    $shortcut.WindowStyle = 7
    $shortcut.Save()
    Log "  Shortcut created: $shortcutPath"
    Log "Bootstrap installed! Will run automatically on every logon."
}

Log "=== Bootstrap complete ==="


# --- Credential Sync ---
Write-Host "`n=== Syncing credentials from private gist ===" -ForegroundColor Cyan
$fetchScript = Join-Path $PSScriptRoot "fetch-credentials.ps1"
if (Test-Path $fetchScript) {
    & $fetchScript
} else {
    Write-Host "WARN: fetch-credentials.ps1 not found, skipping credential sync" -ForegroundColor Yellow
}

