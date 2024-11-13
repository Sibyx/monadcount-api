import click

from monadcount_api.cli import generate_docs
from monadcount_api.cli import import_v1


@click.group()
def cli():
    pass


cli.add_command(generate_docs.openapi, name="openapi")
cli.add_command(import_v1.import_v1, name="import_v1")

if __name__ == "__main__":
    cli()
