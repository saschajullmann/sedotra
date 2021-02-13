#!/bin/bash
# wait for DB

# initial checks first
python /app/app/backend_pre_start.py

alembic upgrade head

python initial-data.py

uvicorn app.main:app --reload --host 0.0.0.0 --port 5000