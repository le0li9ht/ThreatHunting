import os
import struct
from pathlib import Path
import csv

# Magic number constants
EXPECTED_MAGIC = 0xfcfb6d1ba7725c30
base_output = Path.cwd() / "extracted_artefacts"

# Supported file types by header and optional footer
FILE_SIGNATURES = [
    (b"\x1f\x8b\x08", b"", "application/gzip", "gz"),
    (b"\xFF\xD8\xFF", b"\xFF\xD9", "image/jpeg", "jpg"),
    (b"\x89PNG\r\n\x1a\n", b"IEND", "image/png", "png"),
    (b"GIF87a", b"\x00\x3b", "image/gif", "gif"),
    (b"GIF89a", b"\x00\x3b", "image/gif", "gif"),
    (b"\x00\x00\x01\x00", b"", "image/x-icon", "ico"),
    (b"BM", b"", "image/bmp", "bmp"),
    (b"%PDF-", b"%%EOF", "application/pdf", "pdf"),
    (b"ID3", b"", "audio/mpeg", "mp3"),
    (b"OggS", b"", "audio/ogg", "ogg"),
    (b"\x52\x49\x46\x46", b"WAVE", "audio/wav", "wav"),
    (b"fLaC", b"", "audio/flac", "flac"),
]


def detect_mime_and_extension(data):
    for header, footer, mime, ext in FILE_SIGNATURES:
        if data.startswith(header):
            if footer and footer in data:
                end_index = data.find(footer) + len(footer)
                return mime, ext, end_index
            return mime, ext, len(data)
    if data.lstrip().startswith(b"{"):
        return "application/json", "json", len(data)
    if b"<html" in data[:100].lower():
        return "text/html", "html", len(data)
    return "application/octet-stream", "bin", len(data)


def extract_stream1_from_cache(cache_file, images_dir, others_dir):
    try:
        with open(cache_file, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"❌ Error reading {cache_file}: {e}")
        return

    if len(data) < 48:
        return

    try:
        initial_magic, version, key_len, key_hash = struct.unpack_from("<QIII", data, 0)
    except Exception:
        return

    if initial_magic != EXPECTED_MAGIC:
        return

    key_offset = 24
    stream1_start = key_offset + key_len

    if stream1_start >= len(data):
        return

    # Guess end offset
    mime, ext, stream1_len = detect_mime_and_extension(data[stream1_start:])
    stream1_data = data[stream1_start:stream1_start + stream1_len]

    # Write output
    output_name = Path(cache_file).stem + f"_stream1.{ext}"
    output_dir = images_dir if mime.startswith("image/") else others_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_name

    with open(output_path, "wb") as out:
        out.write(stream1_data)
    # Extract key string (URL)
    try:
        key_bytes = data[24:24 + key_len]
        key_str = key_bytes.decode("utf-8", errors="replace")
    except:
        key_str = "?"

    # Write to index.csv
    index_path = base_output / "index.csv"
    with index_path.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not index_path.exists() or index_path.stat().st_size == 0:
            writer.writerow(["hashkey_file", "url_key", "mime_type", "output_file"])
        writer.writerow([Path(cache_file).stem, key_str, mime, output_path.name])


def extract_all_cache_files(user_input_path):
    cache_root = Path(user_input_path).expanduser().resolve()
    if not cache_root.exists():
        print(f"❌ Path not found: {cache_root}")
        return

    base_output = Path.cwd() / "extracted_artefacts"
    images_dir = base_output / "images"
    others_dir = base_output / "others"

    for file in cache_root.rglob("*_0"):
        extract_stream1_from_cache(file, images_dir, others_dir)

    print(f"✅ Extraction complete. Results saved to: {base_output}")


# === Entry Point ===
if __name__ == "__main__":
    try:
        user_input = input("📂 Enter path to Chromium cache folder: ").strip()
        if not user_input:
            print("❌ No path provided.")
        else:
            extract_all_cache_files(user_input)
    except KeyboardInterrupt:
        print("\n🚫 Interrupted by user.")
