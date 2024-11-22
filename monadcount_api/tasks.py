import collections

import clickhouse_connect
import dramatiq
from dramatiq.brokers.redis import RedisBroker
import sentry_sdk
from sentry_sdk.integrations.dramatiq import DramatiqIntegration
from sqlmodel import Session

from monadcount_api.core import settings
from monadcount_api.db import UploadedFile, engine
from monadcount_api.extractor.file import FileParser


def create_broker():
    return RedisBroker(url=str(settings.REDIS_URL))


dramatiq.set_broker(create_broker())

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0, integrations=[DramatiqIntegration()]
    )


@dramatiq.actor(time_limit=600_000)
def extractor(uploaded_file_id: int):

    clickhouse = clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_HOST,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DB,
    )
    L2pkRecord = collections.namedtuple(
        "L2pkRecord", ["device", "uploaded_file_id", "happened_at", "rssi", "channel", "header", "payload"]
    )

    with Session(engine) as session:
        uploaded_file: UploadedFile = session.get(UploadedFile, uploaded_file_id)

        uploaded_file.state = UploadedFile.FileState.processing
        session.add(uploaded_file)
        session.commit()

        record_counter = 0
        batch = []

        with FileParser(settings.DATA_DIR / uploaded_file.file_path) as parser:
            for measurement in parser:
                record_counter += 1

                batch.append(
                    L2pkRecord(
                        device=measurement.device_id,
                        uploaded_file_id=uploaded_file.id,
                        happened_at=measurement.happened_at,
                        rssi=measurement.additional_data["rssi"],
                        channel=measurement.additional_data["channel"],
                        header=measurement.additional_data["header"],
                        payload=measurement.additional_data.get("payload"),
                    )
                )

                # Commit every batch records if not dry run
                if record_counter >= 500_000:
                    record_counter = 0  # Reset counter after commit
                    clickhouse.insert(
                        f"{parser.header.identifier}_v{parser.header.version}".lower(),
                        batch,
                        column_names=L2pkRecord._fields,
                    )

        if batch:
            clickhouse.insert(
                f"{parser.header.identifier}_v{parser.header.version}".lower(),
                batch,
                column_names=L2pkRecord._fields,
            )

        uploaded_file.state = UploadedFile.FileState.done
        session.add(uploaded_file)
        session.commit()
