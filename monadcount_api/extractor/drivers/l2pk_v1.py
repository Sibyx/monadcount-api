import struct
from datetime import datetime
from typing import BinaryIO, Optional

from pydantic_extra_types.mac_address import MacAddress

from monadcount_api.extractor.helpers import format_mac_address
from monadcount_api.extractor.schema import Measurement


class L2PKv1:
    BLOCK_FORMAT = "q 6s 6s b B H"
    BLOCK_SIZE = struct.calcsize(BLOCK_FORMAT)

    def __init__(self, device_id: str):
        self._device_id = device_id

    def __call__(self, f: BinaryIO) -> Optional[Measurement]:
        packet_data = f.read(self.BLOCK_SIZE)

        if len(packet_data) < self.BLOCK_SIZE:
            return None

        payload = struct.unpack(self.BLOCK_FORMAT, packet_data)

        measurement = Measurement(
            mac_address=MacAddress(self._device_id),
            happened_at=datetime.fromtimestamp(payload[0]),
            additional_data={
                "source_mac": format_mac_address(payload[1]),
                "destination_mac": format_mac_address(payload[2]),
                "rssi": payload[3],
                "channel": payload[4],
                "payload_length": payload[5],
            },
        )

        return measurement
