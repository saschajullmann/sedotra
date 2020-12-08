#!/bin/zsh

docker-compose exec backend alembic revision --autogenerate -m "$1"