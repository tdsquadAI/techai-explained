# fetch-credentials.ps1 — Downloads credentials from private GitHub gist
# Run on any authenticated machine to get brand credentials locally
# Usage: .\fetch-credentials.ps1

$ErrorActionPreference = "Stop"
$GIST_ID = "fcdbcbc3849b06fc199186be07e4da75"
$OUTPUT_DIR = "C:\temp\brand-credentials"

Write-Host "Fetching brand credentials from private gist..."

# Ensure gh is authenticated
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Not authenticated with GitHub CLI. Run 'gh auth login' first." -ForegroundColor Red
    exit 1
}

# Create output directory
if (-not (Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null
}

# Fetch the gist
try {
    $gistContent = gh gist view $GIST_ID --raw 2>&1
    if ($LASTEXITCODE -eq 0) {
        Set-Content "$OUTPUT_DIR\all-credentials.md" -Value $gistContent -Encoding UTF8
        Write-Host "OK: Credentials saved to $OUTPUT_DIR\all-credentials.md" -ForegroundColor Green
        
        # Also create individual .env files for each brand
        $brands = @{
            "techai-explained" = @{
                BRAND_EMAIL = "techaiexplained@sharebot.net"
                BRAND_NAME = "TechAI Explained"
                GUMROAD_STORE_URL = "https://tdsquad.gumroad.com"
                EDGE_TTS_VOICE_EN = "en-US-GuyNeural"
                EDGE_TTS_VOICE_HE = "he-IL-AvriNeural"
            }
            "content-empire" = @{
                BRAND_EMAIL = "contentempire@sharebot.net"
                BRAND_NAME = "Content Empire"
                GUMROAD_STORE_URL = "https://tdsquad.gumroad.com"
            }
            "jellybolt-games" = @{
                BRAND_EMAIL = "jellybolt@sharebot.net"
                BRAND_NAME = "JellyBolt Games"
            }
        }
        
        foreach ($brand in $brands.Keys) {
            $envContent = ""
            foreach ($key in $brands[$brand].Keys) {
                $envContent += "$key=$($brands[$brand][$key])`n"
            }
            $repoPath = "C:\Users\tamirdresher\source\repos\$brand"
            if (Test-Path $repoPath) {
                Set-Content "$repoPath\.env" -Value $envContent.TrimEnd() -Encoding UTF8
                Write-Host "  Created .env in $repoPath" -ForegroundColor Cyan
            }
        }
        
        Write-Host "`nDone! Credentials are available locally." -ForegroundColor Green
    } else {
        Write-Host "ERROR: Could not fetch gist. Output: $gistContent" -ForegroundColor Red
    }
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
