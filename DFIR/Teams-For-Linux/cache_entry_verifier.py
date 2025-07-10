import struct
import zlib
import hashlib
from pathlib import Path

def parse_simple_cache_stream0(file_path):
    file_path = Path(file_path).expanduser().resolve()
    if not file_path.is_file():
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) < 48:
        print("❌ File too small to be a valid stream_0 cache file.")
        return

    # --- Parse Header ---
    initial_magic, version, key_length, key_hash = struct.unpack_from("<QIII", data, 0)
    EXPECTED_MAGIC = 0xfcfb6d1ba7725c30
    if initial_magic != EXPECTED_MAGIC:
        print(f"❌ Invalid initial magic: 0x{initial_magic:016x}")
        return

    key_offset = 24
    key_bytes = data[key_offset:key_offset + key_length]
    offset_after_key = key_offset + key_length

    # --- Parse EOF ---
    EOF_STRUCT_SIZE = 24
    eof_offset = len(data) - EOF_STRUCT_SIZE
    if eof_offset < offset_after_key:
        print("❌ File too small: EOF overlaps with stream data.")
        return

    try:
        final_magic, flags, data_crc32, stream_size = struct.unpack_from("<QIIQ", data, eof_offset)
    except struct.error:
        print("❌ Failed to unpack EOF structure.")
        return

    EXPECTED_FINAL_MAGIC = 0xf4fa6f45970d41d8
    if final_magic != EXPECTED_FINAL_MAGIC:
        print(f"❌ Invalid final magic: 0x{final_magic:016x}")
        return

    has_crc32 = bool(flags & 0x01)
    has_sha256 = bool(flags & 0x02)

    # --- SHA256 Verification ---
    sha256_bytes = None
    calculated_sha256 = None
    sha256_match = None
    sha256_offset = eof_offset - 32 if has_sha256 else eof_offset

    if has_sha256:
        if sha256_offset < offset_after_key:
            print("❌ File too small: SHA256 overlaps with stream data.")
            return
        sha256_bytes = data[sha256_offset:eof_offset]
        calculated_sha256 = hashlib.sha256(key_bytes).digest()
        sha256_match = (sha256_bytes == calculated_sha256)

    # --- Stream Data for Output ---
    stream_start = offset_after_key
    stream_end = stream_start + stream_size
    if stream_end > sha256_offset:
        print("❌ File too small: stream overlaps with SHA256 or EOF.")
        return

    stream_data = data[stream_start:stream_end]

    # --- CRC32 Verification (corrected logic) ---
    crc_match = None
    calculated_crc32 = None
    if has_crc32:
        true_stream_end = sha256_offset
        true_stream_start = true_stream_end - stream_size
        stream_data_for_crc = data[true_stream_start:true_stream_end]

        calculated_crc32 = zlib.crc32(stream_data_for_crc) & 0xFFFFFFFF
        crc_match = (calculated_crc32 == data_crc32)

    # --- Print Summary ---
    print("\n🧾 Chromium Simple Cache - Stream_0\n")
    print(f"📄 File:              {file_path.name}")
    print(f"📂 Location:          {file_path.parent}")
    print(f"🔮Starting MagicNumber: {hex(initial_magic)}")
    print(f"🔢 Version:           {version}")
    print(f"🔑 Key Length:        {key_length} bytes")
    print(f"🔑 Key:               {key_bytes.decode(errors='replace')}")
    print(f"🧊EOF MagicNumber: {hex(final_magic)}")
    print(f"📦 Stream Size:       {stream_size} bytes")
    print(f"🧪 Flags:             0x{flags:02x} (CRC32: {has_crc32}, SHA256: {has_sha256})")

    if has_crc32:
        print(f"\n📛 Stored CRC32:       0x{data_crc32:08x}")
        print(f"✅ Calculated CRC32:   0x{calculated_crc32:08x}")
        print(f"🔍 CRC Match:          {crc_match}")
    else:
        print("📛 CRC32:              Not present")

    if has_sha256:
        print(f"\n🔐 SHA256 (file):      {sha256_bytes.hex()}")
        print(f"🔐 SHA256 (calculated):{calculated_sha256.hex()}")
        print(f"🔐 SHA256 Match:       {sha256_match}")
    else:
        print("🔐 SHA256:             Not present")

'''
    # --- Output Stream Content ---
    if output_file:
        output_path = Path(output_file).expanduser().resolve()
        with open(output_path, "wb") as f_out:
            f_out.write(stream_data)
        print(f"\n📤 Stream content saved to: {output_path}")

    return stream_data
'''
# ==== Interactive CLI ====
if __name__ == "__main__":
    try:
        user_path = input("📥 Enter path to stream_0 cache file: ").strip()
        if not user_path:
            print("❌ No file path provided.")
        else:
            parse_simple_cache_stream0(user_path)
    except KeyboardInterrupt:
        print("\n🚫 Interrupted by user.")
