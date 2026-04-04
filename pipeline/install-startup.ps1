# Register the startup catch-up script to run at logon
# Run this once (elevated not required for user-level task)

$scriptPath = "$env:USERPROFILE\source\repos\techai-explained\pipeline\startup-catchup.ps1"

# --- Method 1: Windows Scheduled Task (AtLogOn) ---
Write-Host "=== Installing TechAI Startup Catch-Up ===" -ForegroundColor Cyan

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

try {
    Unregister-ScheduledTask -TaskName "TechAI-StartupCatchUp" -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask `
        -TaskName "TechAI-StartupCatchUp" `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Catches up on missed daily briefs and launches Ralphs after devbox wake"
    Write-Host "  Scheduled task 'TechAI-StartupCatchUp' registered for logon." -ForegroundColor Green
} catch {
    Write-Host "  Warning: Could not register scheduled task (may need elevation): $_" -ForegroundColor Yellow
}

# --- Method 2: Startup folder shortcut (belt-and-suspenders) ---
$startupPath = [Environment]::GetFolderPath('Startup')
$shortcutPath = Join-Path $startupPath "TechAI-CatchUp.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$shortcut.WindowStyle = 7  # Minimized
$shortcut.Description = "TechAI startup catch-up script"
$shortcut.Save()
Write-Host "  Startup shortcut created at: $shortcutPath" -ForegroundColor Green

Write-Host ""
Write-Host "=== Installation complete! ===" -ForegroundColor Green
Write-Host "The catch-up script will run automatically at every logon."
Write-Host "To run it manually: & '$scriptPath'"
