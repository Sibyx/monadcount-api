def format_mac_address(mac_bytes):
    """Format MAC address bytes into standard MAC address string format like XX:XX:XX:XX:XX:XX."""
    return ":".join(f"{byte:02X}" for byte in mac_bytes)
