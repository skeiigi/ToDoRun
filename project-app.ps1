<#
    нужен для старта проекта
#>

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$SRC_DIR = Join-Path $PROJECT_ROOT "src"
$MANAGE_PY = Join-Path $SRC_DIR "manage.py"


if (-not $env:VIRTUAL_ENV) {
    exit 1
}

if (-not (Test-Path $MANAGE_PY)) {
    exit 1
}

try {
    python -c "import django" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw
    }
}
catch {
    exit 1
}


try {
    Set-Location $SRC_DIR
    python manage.py runserver
}
finally {
    Write-Host "[START]: Stop server" -ForegroundColor Green
}
