#!/bin/sh

create_user() {
  if id "celeryuser" &>/dev/null; then
    echo "Пользователь celeryuser уже существует, пропускаем создание."
  else
    echo "Создание пользователя celeryuser..."
    adduser --disabled-password --gecos '' celeryuser
  fi
}

if [ "$CONTAINER_TYPE" == "backend" ]; then
  echo "Waiting for postgres..."
  sleep 5
  alembic upgrade head
  uvicorn src.main:app --host 0.0.0.0 --port 8000
elif [ "$CONTAINER_TYPE" == "celery" ]; then
  echo "Запуск Celery worker..."

  create_user

  su celeryuser -c 'celery -A src.celery_tasks.celery worker --loglevel=INFO'
fi