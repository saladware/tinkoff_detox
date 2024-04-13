```sh
pip install .
alembic revision --autogenerate
alembic upgrade head
uvicorn --factory tinkoff_detox:get_app
```