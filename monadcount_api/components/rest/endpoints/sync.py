import os
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from starlette.requests import Request
from starlette.responses import JSONResponse

from monadcount_api.components.rest.auth import get_current_username
from monadcount_api.core import settings
from monadcount_api.db import get_db, Device, UploadedFile
from monadcount_api.extractor.file import FileParser
from monadcount_api.tasks import extractor, extractor_fail

router = APIRouter()


@router.post("/sync")
async def upload_file(
    request: Request,
    device_id: str = Header(..., alias="Device-ID"),
    file_type: str = Header(..., alias="File-Type"),
    username: str = Depends(get_current_username),
    session: Session = Depends(get_db),
):
    # Read the raw body
    content = await request.body()

    # Handle the device
    device = session.get(Device, device_id)

    if device is None:
        # Create a new device
        device = Device(mac_address=device_id)
        session.add(device)

    # Update last_seen
    device.last_seen = datetime.now()
    session.add(device)
    session.commit()

    # Save the file
    dir_path = device_id.replace(":", "_")
    os.makedirs(os.path.join(settings.DATA_DIR, dir_path), exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file_type}.bin"
    file_path = os.path.join(dir_path, filename)
    absolute_file_path = Path(os.path.join(settings.DATA_DIR, file_path))

    with open(absolute_file_path, "wb") as f:
        f.write(content)

    file = FileParser(absolute_file_path)

    # Create an UploadedFile record
    uploaded_file = UploadedFile(
        device_id=device.mac_address,
        file_type=file.header.identifier,
        file_path=file_path,
        happened_at=file.header.start_time,
        version=file.header.version,
        additional_data=file.header.model_dump(),
    )
    session.add(uploaded_file)
    session.commit()
    session.refresh(uploaded_file)

    extractor.send_with_options(args=(uploaded_file.id,), on_failure=extractor_fail)

    return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)
