from datetime import datetime

from pydantic import BaseModel


class FileHeader(BaseModel):
    identifier: str
    version: int
    start_time: datetime
    wifi_mac: str
    wifi_mac: str
    bt_mac: str
