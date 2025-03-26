FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# TODO: раскоментить перед деплоем 
# FROM gcr.io/distroless/python3-debian11
# COPY --from=builder /usr/lib/python3.11/site-packages /usr/lib/python3.11/site-packages
# COPY --from=builder /app /app
# ENV PYTHONPATH="/app:/usr/lib/python3.11/site-packages"
# WORKDIR /app

EXPOSE 8000

# TODO: раскоментить перед деплоем 
# CMD ["/usr/bin/env", "python3", "src/manage.py", "runserver", "0.0.0.0:8000"]

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
