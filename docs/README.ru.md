Это проект по информационной безопасности. В команде, вместе с нашими одноклассниками, мы создаём веб-приложение на Django.

## Установка и запуск

Клонирование проекта из репозитория

```bash
git clone https://github.com/skeiigi/ToDoRun.git
```

Переход в каталог проекта

```bash
cd ToDoRun
```

## Запуск (автоматизация)

```bash
chmod +x deployment-environment.sh
./deployment-environment.sh
```

## Запуск (вручную)

Создание вирусной среды

```bash
python -m venv venv  # Windows
python3 -m venv myenv  # Mac/Linux
```

Активация вирусной среды

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # если ошибка
.\venv\Scripts\Activate.ps1  # windows poweshell
source myenv/bin/activate  # mac/linux
```

Загрузка зависимостей проекта

```bash
pip install -r requirements.txt
```

## Запуск проекта

Запуск скрипта

```bash
chmod +x project-app.sh
./project-app.sh
```

Ручной запуск

```bash
cd src
python manage.py runserver
```
