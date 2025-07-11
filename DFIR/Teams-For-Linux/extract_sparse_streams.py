#!/usr/bin/env python3

import struct
from pathlib import Path

SPARSE_RANGE_MAGIC = 0xeb97bf016553676b
ENTRY_HEADER_SIZE = 24
SPARSE_RANGE_HEADER_SIZE = 28


def parse_s_file(file_path, output_dir):
    try:
        data = Path(file_path).read_bytes()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    if len(data) < ENTRY_HEADER_SIZE:
        print("❌ File too short to be valid.")
        return

    # Entry Header (24 bytes)
    magic_number, version, key_len, key_hash = struct.unpack_from("<QIII", data, 0)
    print(f"🔹 Magic Number   : 0x{magic_number:016x}")
    print(f"🔹 Version        : {version}")
    print(f"🔹 Key Length     : {key_len}")
    print(f"🔹 Key Hash       : 0x{key_hash:08x}")

    # Extract Key (URL)
    key_offset = ENTRY_HEADER_SIZE
    key = data[key_offset:key_offset + key_len]
    try:
        key_str = key.decode('utf-8', errors='replace')
    except:
        key_str = repr(key)
    print(f"🔹 Key (URL)      : {key_str}")

    # Sparse Ranges Start Here
    sparse_offset = key_offset + key_len
    index = 0
    stream_data_combined = bytearray()

    while sparse_offset + SPARSE_RANGE_HEADER_SIZE <= len(data):
        try:
            sparse_magic, stream_offset, stream_len, crc32, unknown = struct.unpack_from("<QQQII", data, sparse_offset)
        except struct.error:
            print(f"❌ Error: Incomplete sparse range header at offset {sparse_offset}")
            break

        if sparse_magic != SPARSE_RANGE_MAGIC:
            print(f"⚠️ Invalid sparse magic at offset {sparse_offset}: 0x{sparse_magic:016x}")
            break

        print(f"\n🔸 Sparse Range #{index + 1}")
        print(f"   • Header Offset   : 0x{sparse_offset:08x}")
        print(f"   • Sparse Magic    : 0x{sparse_magic:016x}")
        print(f"   • Stream Offset   : {stream_offset}")
        print(f"   • Stream Length   : {stream_len}")
        print(f"   • CRC32           : 0x{crc32:08x}")
        print(f"   • Unknown         : 0x{unknown:08x}")

        # Read stream data (immediately follows header + 4 byte padding)
        stream_start = sparse_offset + SPARSE_RANGE_HEADER_SIZE + 4
        stream_end = stream_start + stream_len

        if stream_end > len(data):
            print(f"❌ Error: Stream data exceeds file size at index {index}")
            break

        chunk = data[stream_start:stream_end]
        stream_data_combined.extend(chunk)

        # Move to next sparse range
        sparse_offset = stream_end
        index += 1

    if index == 0:
        print("⚠️ No valid sparse ranges found.")
    else:
        print(f"\n✅ Parsed {index} sparse range(s) successfully.")

        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)

        # Write combined stream data to file in output_dir
        out_file = output_dir / f"{file_path.stem}.reconstructed.bin"
        try:
            out_file.write_bytes(stream_data_combined)
            print(f"✅ Reconstructed stream saved to: {out_file}")
        except Exception as e:
            print(f"❌ Failed to write reconstructed stream: {e}")


if __name__ == "__main__":
    from sys import argv
    if len(argv) != 2:
        print("Usage: python3 parse_s_file.py <folder_with__s_files>")
    else:
        input_folder = Path(argv[1])
        if not input_folder.is_dir():
            print(f"❌ Not a directory: {input_folder}")
        else:
            output_folder = Path.cwd() / "extracted_stream_s_files"
            s_files = list(input_folder.glob("*_s"))
            if not s_files:
                print("⚠️ No '_s' files found in the given directory.")
            else:
                for file in s_files:
                    parse_s_file(file, output_folder)

