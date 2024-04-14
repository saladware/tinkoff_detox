# Tinkoff Detox API

Tinkoff Detox API - это небольшой REST API для фильтрации токсичного контента

## Установка и запуск

```sh
pip install .
alembic revision --autogenerate
alembic upgrade head
uvicorn --factory tinkoff_detox:get_app
```