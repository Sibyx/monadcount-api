import base64
import struct
from datetime import datetime
from typing import BinaryIO, Optional

from monadcount_api.db import Measurement


class L2PKv2:
    BLOCK_FORMAT = "q B B b B H 36s H 128s"
    BLOCK_SIZE = struct.calcsize(BLOCK_FORMAT)

    def __init__(self, device_id: str):
        self._device_id = device_id

    def __call__(self, f: BinaryIO) -> Optional[Measurement]:
        packet_data = f.read(self.BLOCK_SIZE)

        if len(packet_data) < self.BLOCK_SIZE:
            return None

        payload = struct.unpack(self.BLOCK_FORMAT, packet_data)

        measurement = Measurement(
            device_id=self._device_id,
            happened_at=datetime.fromtimestamp(payload[0] / 1000),
            additional_data={
                "frame_type": payload[1],
                "frame_subtype": payload[2],
                "rssi": payload[3],
                "channel": payload[4],
                "header": base64.b64encode(bytes(payload[6][: payload[5]])).decode("utf-8"),
                "payload": base64.b64encode(bytes(payload[8][: payload[7]])).decode("utf-8"),
            },
        )

        return measurement
