# Build and serve PlacementGPT frontend (works reliably on OneDrive)
$env:WATCHPACK_POLLING = "true"

Write-Host "Building frontend (one-time, ~1 min)..." -ForegroundColor Cyan
Set-Location $PSScriptRoot
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Check errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting server at http://localhost:3000" -ForegroundColor Green
npm run start
