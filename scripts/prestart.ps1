param(
    [string]$ComposeFile = "docker-compose.example.yml"
)

Write-Host "Pre-start: using compose file $ComposeFile"

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "Python not found in PATH. Please install Python or run scripts/check_ports.ps1 manually."
    exit 2
}

.
\scripts\check_ports.ps1 -ComposeFile $ComposeFile
if ($LASTEXITCODE -ne 0) {
    Write-Error "Port conflict detected. Aborting docker compose up."
    exit $LASTEXITCODE
}

Write-Host "Ports available. Starting docker compose..."
docker compose -f $ComposeFile up --build -d
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Docker compose started. Use 'docker compose ps' to check services."
