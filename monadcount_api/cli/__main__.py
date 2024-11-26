import click
from monadcount_api.cli import generate_docs
from monadcount_api.cli import calculate_size
from monadcount_api.cli import import_measurements
from monadcount_api.cli import enqueue


@click.group()
def cli():
    pass


cli.add_command(generate_docs.openapi, name="openapi")
cli.add_command(import_measurements.import_measurements, name="import_measurements")
cli.add_command(enqueue.enqueue, name="enqueue")
cli.add_command(calculate_size.calculate_size, name="calculate_size")

if __name__ == "__main__":
    cli()
