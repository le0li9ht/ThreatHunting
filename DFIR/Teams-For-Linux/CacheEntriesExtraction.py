#Author: Ashokkrishna Vemuri
import struct
import datetime
from pathlib import Path
from prettytable import PrettyTable  # pip install prettytable

def parse_entry_count(path):
    path = Path(path).expanduser().resolve()  # This is the fix you need
    with path.open("rb") as f:
        data = f.read()
    if len(data) < 28:
        print("File too small to contain valid metadata.")
        return
    # Offset 0x14 (20 decimal) → 8-byte unsigned integer (Q)
    entry_count = struct.unpack_from("<Q", data, 20)[0]

    print(f"\nActual Entry Count: {entry_count}")

def parse_last_used_time(raw_time):
    try:
        # Chromium stores time as microseconds since Windows epoch (1601-01-01)
        WINDOWS_EPOCH = datetime.datetime(1601, 1, 1)
        dt = WINDOWS_EPOCH + datetime.timedelta(microseconds=raw_time)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "Invalid"

def parse_index_file(path):
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        print(f"File not found: {path}")
        return

    with path.open("rb") as f:
        data = f.read()

    entry_count = struct.unpack_from("<Q", data, 20)[0]
    print(f"Total entries Parsed: {entry_count}")

    entry_start = 40
    entry_size = 24
    table = PrettyTable()
    table.field_names = ["Entry Hash(Hash Key)", "Cache Entry Last Used Time(UTC)", "Entry Size (Bytes)"]

    for i in range(entry_count):
        offset = entry_start + i * entry_size
        if offset + entry_size > len(data) - 8:
            break

        hash_bytes = data[offset:offset+8]
        last_used_raw = struct.unpack_from("<Q", data, offset+8)[0]
        entry_size_val = struct.unpack_from("<Q", data, offset+16)[0]

        entry_hash = hash_bytes[::-1].hex()
        last_used_str = parse_last_used_time(last_used_raw)

        table.add_row([entry_hash, last_used_str, entry_size_val])

    # Read the last 8 bytes: last modified time of the cache directory
    if len(data) >= 8:
        raw_modified = struct.unpack_from("<q", data, len(data) - 8)[0]
        modified_str = parse_last_used_time(raw_modified)
        print(f"Last Modified Time: {modified_str} ({raw_modified})")
    else:
        print("Could not extract last modified time")

    print("\nCache Entry Summary:\n")
    print(table)

if __name__ == "__main__":
    user_input = input("Enter path to the-real-index file (press Enter to use default): ").strip()
    default_path = "~/snap/teams-for-linux/current/.config/teams-for-linux/Partitions/teams-4-linux/Cache/Cache_Data/index-dir/the-real-index"
    path = user_input if user_input else default_path
    parse_entry_count(path)
    parse_index_file(path)

