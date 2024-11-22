import click
from sqlmodel import select, Session

from monadcount_api.db import UploadedFile, engine
from monadcount_api.tasks import extractor, extractor_fail


@click.command()
def enqueue():
    with Session(engine) as session:
        statement = select(UploadedFile).where(UploadedFile.state == UploadedFile.FileState.pending)
        results = session.exec(statement)

        for uploaded_file in results:
            extractor.send_with_options(args=(uploaded_file.id,), on_failure=extractor_fail)
