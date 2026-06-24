# Stop stuck frontend Node processes
Write-Host "Stopping Node processes on port 3000..." -ForegroundColor Yellow
$connections = netstat -ano | findstr ":3000" | findstr "LISTENING"
if ($connections) {
    $connections -split "`n" | ForEach-Object {
        $parts = $_ -split '\s+'
        $pid = $parts[-1]
        if ($pid -match '^\d+$') {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process $pid"
        }
    }
}
Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "Done. You can now restart the frontend." -ForegroundColor Green
