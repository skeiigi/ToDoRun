#!/bin/bash

# нужен для старта проекта

set -e

PROJECT_ROOT=$(dirname "$(readlink -f "$0" || realpath "$0")")
SRC_DIR="$PROJECT_ROOT/src"
MANAGE_PY="$SRC_DIR/manage.py"

echo "[START]: Проверка виртуалки"

if [ -z "$VIRTUAL_ENV" ]; then
    echo "[ERROR]: Виртуальное окружение не активировано"
    echo "         Активируй его командой: source venv/bin/activate (Linux/Mac)"
    echo "         или source venv/Scripts/activate (Windows Git Bash)"
    echp "         или запусти файл deployment-environment.sh"
    exit 1
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo "[ERROR]: Файл manage.py не найден по пути: $MANAGE_PY"
    exit 1
fi

if ! python -c "import django" &> /dev/null; then
    echo "[ERROR]: Django нету"
    echo "         Установите его командой: pip install django"
    exit 1
fi

echo "[START]: Запуск Django-сервера"
cd "$SRC_DIR"
python manage.py runserver

echo "[START]: Сервер остановлен"
