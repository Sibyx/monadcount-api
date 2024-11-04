import click

from monadcount_api.cli import generate_docs


@click.group()
def cli():
    pass


cli.add_command(generate_docs.openapi, name="openapi")

if __name__ == "__main__":
    cli()
