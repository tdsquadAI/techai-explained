# Creates a Windows Scheduled Task to run daily brief generation
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$env:USERPROFILE\source\repos\techai-explained\pipeline\daily-briefs\scheduler.ps1`" -Now"

$trigger = New-ScheduledTaskTrigger -Daily -At "06:00AM"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName "TechAI-DailyBriefs" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Generates daily tech news brief videos for TechAI Explained YouTube channel"

Write-Host "Scheduled task 'TechAI-DailyBriefs' installed. Runs daily at 6:00 AM."
