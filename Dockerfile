FROM python:3.9

WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     libblas-dev \
#     liblapack-dev \
#     gfortran \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN sed -i 's/\r$//' /app/project-app.sh

# RUN python manage.py collectstatic --noinput

# FROM gcr.io/distroless/nodejs20
# WORKDIR /app
# COPY --from=builder /app/dist /app
# COPY --from=builder /app/node_modules /app/node_modules
# COPY --from=builder /app/.env /app/.env

# COPY --from=builder /app/wait-for-it.sh /usr/local/bin/wait-for-it.sh
# RUN chmod +x /usr/local/bin/wait-for-it.sh

# COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# COPY --from=builder /app /app

EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "to-do-run.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
