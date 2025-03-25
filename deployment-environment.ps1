<#
    нужен для легкой сборки проекта под кажду систему Powershell
#>

$ErrorActionPreference = "Stop"

$REPO_URL = "https://github.com/skeiigi/ToDoRun.git"
$PROJECT_DIR = "ToDoRun"
$VENV_DIR = "venv"
$PLATFORM = $PSVersionTable.Platform

if (-not $PLATFORM) {
    $PLATFORM = "Windows"
}


if ($PLATFORM -eq "Unix" -or $PLATFORM -eq "Linux" -or $PLATFORM -eq "MacOS") {
    python3 -m venv $VENV_DIR
    $ACTIVATE_CMD = ". ./$VENV_DIR/bin/activate.ps1"
} 
elseif ($PLATFORM -eq "Windows") {
    python -m venv $VENV_DIR
    $ACTIVATE_CMD = ". .\$VENV_DIR\Scripts\Activate.ps1"
} 
else {
    exit 1
}

Invoke-Expression $ACTIVATE_CMD

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}


Set-Location src


if (Test-Path "db.sqlite3") {
    Remove-Item db.sqlite3
    Get-ChildItem -Path . -Recurse -Filter "*.py" | 
        Where-Object { $_.FullName -like "*migrations*" -and $_.Name -ne "__init__.py" } | 
        Remove-Item
} 


if (Test-Path "organ/migrations") {
    Get-ChildItem -Path "organ/migrations" -Filter "*.py" |
        Where-Object { $_.Name -ne "__init__.py" } |
        Remove-Item
}

python manage.py makemigrations

python manage.py migrate

python manage.py showmigrations


Set-Location ..

exit 0