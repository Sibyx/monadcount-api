import json
import uuid
from enum import Enum
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, JSON, Column, Relationship

from monadcount_api.core import settings


def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that FastAPI does.
    """
    return json.dumps(*args, default=jsonable_encoder, **kwargs)


engine = create_engine(settings.database_url, json_serializer=_custom_json_serializer)
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
    last_seen: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    uploaded_files: List["UploadedFile"] = Relationship(back_populates="device")


class UploadedFile(SQLModel, table=True):
    __tablename__ = "uploaded_files"

    class FileState(str, Enum):
        pending = "pending"
        processing = "processing"
        done = "done"
        failed = "failed"
        archived = "archived"

    class FileType(str, Enum):
        csip = "CSIP"
        l2pk = "L2PK"

    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(foreign_key="devices.mac_address")
    state: FileState = Field(default=FileState.pending)
    file_type: str
    version: int = Field(default=1)
    file_path: str
    happened_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True)), default=None)
    filesize: Optional[int] = Field(default=None)
    additional_data: Optional[Dict] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)), default_factory=datetime.now)

    device: Optional[Device] = Relationship(back_populates="uploaded_files")
    measurements: List["Measurement"] = Relationship(back_populates="uploaded_file")


class Measurement(SQLModel, table=True):
    __tablename__ = "measurements"

    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str = Field(foreign_key="devices.mac_address")
    uploaded_file_id: Optional[int] = Field(foreign_key="uploaded_files.id")
    happened_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    additional_data: Optional[Dict] = Field(sa_column=Column(JSON))

    uploaded_file: Optional[UploadedFile] = Relationship(back_populates="measurements")


class Structure(SQLModel, table=True):
    __tablename__ = "structures"

    class StructureType(str, Enum):
        room = "room"
        wall = "wall"

    id: Optional[UUID] = Field(default=uuid.uuid4, primary_key=True)
    category: StructureType
    title: Optional[str]
    geom: Optional[str] = Field(sa_column=Column(Geometry(geometry_type="POLYGON", srid=998999)))
