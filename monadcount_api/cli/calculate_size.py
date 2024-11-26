import os
from pathlib import Path

import click
from sqlalchemy.sql.operators import is_
from sqlmodel import select, Session

from monadcount_api.core import settings
from monadcount_api.db import UploadedFile, engine
from monadcount_api.extractor.file import FileParser


@click.command()
def calculate_size():
    with Session(engine) as session:
        statement = select(UploadedFile).where(is_(UploadedFile.filesize, None))
        results = session.exec(statement)

        for uploaded_file in results:
            absolute_file_path = Path(os.path.join(settings.DATA_DIR, uploaded_file.file_path))
            file = FileParser(absolute_file_path)

            uploaded_file.filesize = file.size
            session.add(uploaded_file)

        session.commit()
