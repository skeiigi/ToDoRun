# To Do Run

Это проект по информационной безопасности. В команде, вместе с нашими одноклассниками, мы создаём веб-приложение на Django.

[Назад](../README.md)

## Установка и запуск

Клонирование проекта из репозитория

```bash
git clone https://github.com/skeiigi/ToDoRun.git
```

Переход в каталог проекта

```bash
cd ToDoRun
```

## Перед запуском скриптов

Нужно открыть **Git Bash**, найти репозиторий ToDoRun с помощью **cd**.
<br><br>**ВАЖНО** ("/")<br>
```bash
D:/one/two/three/ToDoRun
```

## Запуск (автоматизация)

```bash
chmod +x deployment-environment.sh
./deployment-environment.sh
```

В PowerShell __(рекомендованно для Windows)__

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deployment-environment.ps1
```

## Запуск и миграция (вручную)

Создание вирусной среды

```bash
python -m venv venv  # Windows
python3 -m venv myenv  # Mac/Linux
```

Активация вирусной среды

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # если есть ошибка
.\venv\Scripts\Activate.ps1  # Windows PowerShell
source myenv/bin/activate  # Mac/Linux
```

Загрузка зависимостей проекта

```bash
pip install -r requirements.txt
```

## Начать миграцию (вручную)

```bash
cd src
python manage.py makemigrations
python manage.py migrate
cd ..
```

## Запуск проекта

Запуск скрипта

```bash
chmod +x project-app.sh
./project-app.sh
```

В PowerShell __(рекомендованно для Windows)__

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\project-app.ps1
```

Ручной запуск

```bash
cd src
python manage.py runserver
```
