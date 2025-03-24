FROM python:3.10-slim-buster as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
