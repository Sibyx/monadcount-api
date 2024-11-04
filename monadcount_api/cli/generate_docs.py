import json

import click
from fastapi.openapi.utils import get_openapi

from monadcount_api.core import settings
from monadcount_api.__main__ import app


@click.command()
@click.option("--output", help="Output filename", default="openapi.json")
def openapi(output):
    with open(output, "w") as f:
        json.dump(
            get_openapi(
                title=settings.NAME,
                version=settings.VERSION,
                description=settings.DESCRIPTION,
                routes=app.routes,
            ),
            f,
        )
