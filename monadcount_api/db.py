from enum import Enum
from typing import Optional, Dict, List
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, JSON, Column, Relationship

from monadcount_api.core import settings

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Device(SQLModel, table=True):
    __tablename__ = "devices"

    mac_address: str = Field(primary_key=True)
    geom: Optional[str] = Field(sa_column=Column(Geometry(geometry_type="POINT", srid=998999)))
    last_seen: Optional[datetime] = None

    uploaded_files: List["UploadedFile"] = Relationship(back_populates="device")


class Measurement(SQLModel, table=True):
    __tablename__ = "measurements"

    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(foreign_key="devices.mac_address")
    happened_at: datetime
    additional_data: Optional[Dict] = Field(sa_column=Column(JSON))


class UploadedFile(SQLModel, table=True):
    __tablename__ = "uploaded_files"

    class FileState(str, Enum):
        pending = "pending"
        processing = "processing"
        processed = "processed"
        failed = "failed"

    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(foreign_key="devices.mac_address")
    file_type: str
    file_path: str
    created_at: datetime = Field(default_factory=datetime.now)
    state: FileState = Field(default=FileState.pending)

    device: Optional[Device] = Relationship(back_populates="uploaded_files")
