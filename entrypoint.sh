#!/bin/sh

if [ "$CONTAINER_TYPE" == "backend" ]; then
  echo "Waiting for postgres..."
  sleep 5
  alembic upgrade head
  uvicorn src.main:app --host 0.0.0.0 --port 8000
elif [ "$CONTAINER_TYPE" == "celery" ]; then
  echo "Запуск Celery worker..."
  celery -A src.celery_tasks.celery worker --loglevel=info
fi