# Pre-Commit

[Назад](../../README.md)

#### Обновление зависимостей

```bash
pip install -r requirements.txt
```

#### Установка линтеров и форматеров

```bash
pre-commit install
```

#### Ручной запуск без коммита

```bash
pre-commit run --all-files
```

#### Автоматический запуск и коммит

```bash
git commit -m "сообщение"
```


#### Коммит без проверки

```bash
git commit -m "сообщение" --no-verify
```
