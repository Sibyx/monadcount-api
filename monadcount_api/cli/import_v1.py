import struct
from datetime import datetime
from pathlib import Path

import click

from monadcount_api.db import SessionLocal, Measurement
from monadcount_api.extractor.helpers import format_mac_address


@click.command()
@click.option("--directory", help="Output filename", default="data", type=Path)
def import_v1(directory):
    file_header_format = "4sI Q 6s 6s"
    captured_packet_format = "q 6s 6s b B H"

    file_header_size = struct.calcsize(file_header_format)
    captured_packet_size = struct.calcsize(captured_packet_format)

    db = SessionLocal()
    COMMIT_BATCH_SIZE = 100_000
    record_counter = 0  # Counter for tracking number of records

    for file_path in directory.rglob("*.bin"):
        with open(file_path, "rb") as f:
            # Read and parse the file header
            file_header_data = f.read(file_header_size)
            file_header = struct.unpack(file_header_format, file_header_data)

            identifier = file_header[0].decode("utf-8")
            version = file_header[1]
            start_time = file_header[2]
            wifi_mac = format_mac_address(file_header[3])
            bt_mac = format_mac_address(file_header[4])

            print(f"File Header {identifier}v{version} ({wifi_mac}): {start_time}")

            # Read and parse each captured packet
            print("\nCaptured Packets:")
            packet_index = 1
            while True:
                packet_data = f.read(captured_packet_size)
                if len(packet_data) < captured_packet_size:
                    break  # End of file

                packet = struct.unpack(captured_packet_format, packet_data)
                timestamp = packet[0]
                src_mac = format_mac_address(packet[1])
                dst_mac = format_mac_address(packet[2])
                rssi = packet[3]
                channel = packet[4]
                payload_len = packet[5]

                print(
                    f"Packet {packet_index}: {timestamp} | {src_mac} | {dst_mac} | {rssi} | {channel} | {payload_len}"
                )
                measurement = Measurement(
                    device_id=wifi_mac,
                    happened_at=datetime.fromtimestamp(timestamp),
                    additional_data={
                        "source_mac": src_mac,
                        "destination_mac": dst_mac,
                        "rssi": rssi,
                        "channel": channel,
                        "payload_length": payload_len,
                    },
                )
                db.add(measurement)
                record_counter += 1

                # Commit every 100,000 records
                if record_counter >= COMMIT_BATCH_SIZE:
                    db.commit()
                    record_counter = 0  # Reset counter after commit
                    print("Committed 100,000 records to the database.")

                packet_index += 1

    # Final commit for any remaining records
    if record_counter > 0:
        db.commit()
        print(f"Final commit of {record_counter} remaining records to the database.")

    db.close()
