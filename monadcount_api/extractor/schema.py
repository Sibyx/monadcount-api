from datetime import datetime

from pydantic import BaseModel
from pydantic_extra_types.mac_address import MacAddress


class FileHeader(BaseModel):
    identifier: str
    version: int
    start_time: datetime
    wifi_mac: str
    wifi_mac: str
    bt_mac: str


class Measurement(BaseModel):
    mac_address: MacAddress
    happened_at: datetime
    additional_data: dict
