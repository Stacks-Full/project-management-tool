## Python path
This might help with some issues with some text editors or IDEs not autodetecting pyproject.toml
export PYTHONPATH=$PYTHONPATH:$(pwd)

## Alembic usage
Alembic has been configured to automatically generate migration scripts.  

We just need to define a table in `backend/app/core/models.py` and run:
```sh
docker compose exec backend alembic revision --autogenerate -m "<name of migration script>"
```

> [!NOTE]
> Since we run the database inside a docker network, we need to run alembic inside the docker container as well and we
> can't run it outside (i.e., creating a python virtual environment and installing alembic)

If we made a change to an existing model with an existing migration script, we just need to run the command again and
alembic will automatically "diff" the changes and make a new migration script.
