import click
from sqlmodel import select, Session

from monadcount_api.db import UploadedFile, engine
from monadcount_api.tasks import extractor


@click.command()
def enqueue():
    with Session(engine) as session:
        statement = select(UploadedFile).where(UploadedFile.state == UploadedFile.FileState.pending)
        results = session.exec(statement)

        for uploaded_file in results:
            extractor.send(uploaded_file.id)
