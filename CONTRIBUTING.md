# Contributing to MonadCount API

## Development

We use [poetry](https://python-poetry.org/) for dependency management. Please write your source code according to the
[PEP8](https://www.python.org/dev/peps/pep-0008/) code-style. [black](https://github.com/psf/black) is used for
code-style and code-quality checks. Please, be sure that your IDE is following settings according to `.editorconfig`
file.

```shell script
# Run black
poetry run black .
```

## Migrations

We use [alembic](https://alembic.sqlalchemy.org/en/latest/) to organize database migrations automatically based on
the [SQLModel](https://sqlmodel.tiangolo.com/) models.

If you are using Docker image - the migrations are executed automatically in the container entrypoint
`conf/entrypoint.sh`.

### Creating migrations

```shell
alembic revision --autogenerate -m "UploadedFile refactor"
```

### Executing migrations

Using bellow you can synchronize database to the latest state (execute all un-executed migrations).

```shell
alembic upgrade head
```
