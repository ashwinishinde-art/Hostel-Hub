# ============================================================
# Hostel Hub - Cloudflare Quick Tunnel Launcher
# ============================================================
# This script starts your Flask app AND the Cloudflare tunnel.
# Anyone on any network can access your site via the tunnel URL.
# ============================================================

$ProjectDir  = "C:\Users\Admin\OneDrive\Desktop\Hostel-Hub"
$FlaskPort   = 5000
$cloudflared = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
$LogFile     = "$ProjectDir\tunnel.log"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   HOSTEL HUB - PUBLIC TUNNEL LAUNCHER  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: Check cloudflared is available ---
if (-not (Test-Path $cloudflared)) {
    Write-Host "[ERROR] cloudflared not found at: $cloudflared" -ForegroundColor Red
    Write-Host "        Run: winget install --id Cloudflare.cloudflared --source winget" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "[OK] cloudflared found." -ForegroundColor Green

# --- Step 2: Launch Flask app in a new window ---
Write-Host ""
Write-Host "[1/2] Starting Flask app on port $FlaskPort ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectDir'; python app.py"
Start-Sleep -Seconds 3

# --- Step 3: Start the Cloudflare Quick Tunnel ---
Write-Host "[2/2] Starting Cloudflare Quick Tunnel..." -ForegroundColor Yellow
Write-Host ""
Write-Host "--------------------------------------------------------" -ForegroundColor White
Write-Host " Watch for the tunnel URL that looks like:" -ForegroundColor White
Write-Host " https://some-random-words-1234.trycloudflare.com" -ForegroundColor Green
Write-Host "--------------------------------------------------------" -ForegroundColor White
Write-Host ""
Write-Host " Share that URL with anyone - they can access your site!" -ForegroundColor Cyan
Write-Host " Press Ctrl+C in this window to stop the tunnel." -ForegroundColor DarkGray
Write-Host ""

# Run tunnel and tee output to log file so the URL is captured
& $cloudflared tunnel --url "http://localhost:$FlaskPort" 2>&1 | Tee-Object -FilePath $LogFile
