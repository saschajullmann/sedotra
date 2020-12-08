#!/bin/bash
# wait for DB

while ! nc -z db 5432; do
  sleep 0.1
done

alembic upgrade head

python initial-data.py

uvicorn app.main:app --reload --host 0.0.0.0 --port 5000