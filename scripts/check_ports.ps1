param(
    [string]$ComposeFile = "docker-compose.example.yml",
    [string]$Ports = "",
    [string]$Host = "127.0.0.1"
)

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "Python not found in PATH. Install Python or run the script with 'python scripts/check_free_ports.py'"
    exit 2
}

$args = @()
if ($ComposeFile) { $args += "--compose-file"; $args += $ComposeFile }
if ($Ports) { $args += "--ports"; $args += $Ports }
if ($Host) { $args += "--host"; $args += $Host }

python scripts/check_free_ports.py @args
exit $LASTEXITCODE
