# Start PlacementGPT frontend (PowerShell)
$env:WATCHPACK_POLLING = "true"
$env:CHOKIDAR_USEPOLLING = "true"

Write-Host "Starting PlacementGPT frontend..." -ForegroundColor Cyan
Write-Host "Wait until you see:  Ready in Xs" -ForegroundColor Yellow
Write-Host "Then open: http://localhost:3000" -ForegroundColor Green
Write-Host ""

Set-Location $PSScriptRoot
npx next dev
