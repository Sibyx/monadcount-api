from pathlib import Path

import click
from sqlmodel import Session

from monadcount_api.db import engine
from monadcount_api.extractor.file import FileParser


@click.command()
@click.option("--directory", type=Path, default="data", help="Output filename")
@click.option("--dry-run", is_flag=True, show_default=True, default=False, help="Do not actually commit to database")
@click.option("--batch", type=int, default=100_000, help="Commit batch size")
def import_measurements(directory, dry_run, batch):
    with Session(engine) as session:
        record_counter = 0  # Counter for tracking number of records

        for file_path in directory.rglob("*.bin"):
            with FileParser(file_path) as parser:
                item_index = 0
                for measurement in parser:
                    record_counter += 1
                    item_index += 1
                    session.add(measurement)

                    # Commit every batch records if not dry run
                    if record_counter >= batch:
                        record_counter = 0  # Reset counter after commit

                        if not dry_run:
                            session.commit()

                print(parser.header)

            # Commit any remaining records
            if record_counter > 0 and not dry_run:
                session.commit()
