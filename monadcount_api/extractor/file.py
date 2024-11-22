import struct
from pathlib import Path

from monadcount_api.extractor.drivers.l2pk_v1 import L2PKv1
from monadcount_api.extractor.drivers.l2pk_v2 import L2PKv2
from monadcount_api.extractor.helpers import format_mac_address
from monadcount_api.extractor.schema import FileHeader


class FileParser:
    FILE_HEADER_FORMAT = "4sI Q 6s 6s"
    FILE_HEADER_SIZE = struct.calcsize(FILE_HEADER_FORMAT)

    def __init__(self, file_path: Path):
        self._file = open(file_path, "rb")
        self._file_path = file_path

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

        match f"{self.header.identifier.upper()}v{self.header.version}":
            case "L2PKv1":
                self._driver = L2PKv1(self.header.wifi_mac)
            case "L2PKv2":
                self._driver = L2PKv2(self.header.wifi_mac)
            case _:
                self._driver = None

    def __enter__(self):
        return self

    def __iter__(self):
        self._file.seek(self.FILE_HEADER_SIZE)
        return self

    def __next__(self):
        if not self._driver:
            # FIXME: maybe a GenericDriver will be nicer solution - using ABC
            raise StopIteration

        try:
            result = self._driver(self._file)
        except ValueError:
            # logging.warning("Probably corrupted")
            print("\t Corrupted")
            raise StopIteration

        if not result:
            raise StopIteration

        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
