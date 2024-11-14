import struct
from pathlib import Path

from monadcount_api.extractor.helpers import format_mac_address
from monadcount_api.extractor.schema import FileHeader


class FileParser:
    FILE_HEADER_FORMAT = "4sI Q 6s 6s"

    def __init__(self, file_path: Path):
        self._file = open(file_path, "rb")

        file_header_size = struct.calcsize(self.FILE_HEADER_FORMAT)
        file_header_data = self._file.read(file_header_size)

        payload = struct.unpack(self.FILE_HEADER_FORMAT, file_header_data)

        self.header = FileHeader(
            identifier=payload[0].decode("utf-8"),
            version=payload[1],
            start_time=payload[2],
            wifi_mac=format_mac_address(payload[3]),
            bt_mac=format_mac_address(payload[4]),

        )

    def close(self):
        self._file.close()
