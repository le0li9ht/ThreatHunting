#Author: Ashokkrishna Vemuri
import os
import struct
import csv
import mimetypes
import os

def get_folder_path_from_user():
    try:
        folder_path = input("📁 Enter custom folder path where you saved your Teams' Cache folder (e.g., ~/Documents or /home/user/Cache): ").strip()
        folder_path = os.path.expanduser(folder_path)

        if not os.path.isdir(folder_path):
            print(f"❌ Not a valid directory: {folder_path}")
            return None

        print(f"✅ Directory found: {folder_path}")
        return folder_path
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

# Example usage
CACHE_FOLDER = get_folder_path_from_user()
if not CACHE_FOLDER:
    fallback_path = "~/snap/teams-for-linux/current/.config/teams-for-linux/Partitions/teams-4-linux/Cache/Cache_Data"
    CACHE_FOLDER = os.path.expanduser(fallback_path)
    print(f"\n⚠️ Using fallback path: {CACHE_FOLDER} \n\n")
#CACHE_FOLDER = "~/snap/teams-for-linux/current/.config/teams-for-linux/Partitions/teams-4-linux/Cache/Cache_Data"
OUTPUT_FOLDER = "./cache_images"
CSV_OUTPUT = os.path.join(OUTPUT_FOLDER, "images_index.csv")

MAGIC_HEADER = 0xfcfb6d1ba7725c30
MAGIC_EOF = 0xf4fa6f45970d41d8

def read_simple_file_header(f):
    data = f.read(24)
    if len(data) < 24:
        return None
    magic, version, key_length, key_hash, _ = struct.unpack("<QIIII", data)
    if magic != MAGIC_HEADER:
        return None
    return {"version": version, "key_length": key_length, "key_hash": key_hash}

def read_simple_file_eof(data):
    if len(data) < 24:
        return None
    final_magic, flags, crc32, stream_size, _ = struct.unpack("<QIIII", data[-24:])
    if final_magic != MAGIC_EOF:
        return None
    return {"flags": flags, "crc32": crc32, "stream_size": stream_size}

def parse_http_headers(raw_bytes):
    try:
        text = raw_bytes.decode("utf-8", errors="replace")
        headers = {}
        lines = text.split("\r\n")
        for line in lines:
            if ": " in line:
                key, val = line.split(": ", 1)
                headers[key.lower()] = val
        return headers
    except:
        return {}

def get_file_extension(content_type, raw_data):
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0])
        if ext:
            return ext.lstrip(".")
    if raw_data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    elif raw_data.startswith(b"\x89PNG"):
        return "png"
    elif raw_data.startswith(b"GIF87a") or raw_data.startswith(b"GIF89a"):
        return "gif"
    elif raw_data.startswith(b"RIFF") and b"WEBP" in raw_data[:16]:
        return "webp"
    elif raw_data.startswith(b"BM"):
        return "bmp"
    elif raw_data.startswith(b"II*\x00") or raw_data.startswith(b"MM\x00*"):
        return "tiff"
    elif raw_data.lstrip().startswith(b"<?xml") or b"<svg" in raw_data[:300]:
        return "svg"
    elif raw_data.startswith(b"\x00\x00\x01\x00"):
        return "ico"
    return "bin"

def extract_image(file_path, index):
    with open(file_path, "rb") as f:
        header = read_simple_file_header(f)
        if not header:
            return None
        key = f.read(header["key_length"])
        url = key.decode("utf-8", errors="replace")

        rest = f.read()
        eof = read_simple_file_eof(rest)
        if eof:
            content = rest[:-24]
        else:
            content = rest

        split = content.find(b"\r\n\r\n")
        if split == -1:
            raw_headers = b""
            raw_body = content
        else:
            raw_headers = content[:split]
            raw_body = content[split+4:]

        headers = parse_http_headers(raw_headers)
        content_type = headers.get("content-type", "")

        ext = get_file_extension(content_type, raw_body)
        if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
            return None  # Not image-like

        filename = f"{index:05d}.{ext}"
        outpath = os.path.join(OUTPUT_FOLDER, filename)
        with open(outpath, "wb") as img:
            img.write(raw_body)

        return {
            "Index": index,
            "Filename": filename,
            "URL": url,
            "Content-Type": content_type
        }
        


def export_images():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    files = sorted(f for f in os.listdir(CACHE_FOLDER) if f.endswith("_0"))
    print(f"[i] Found {len(files)} Entries in {CACHE_FOLDER}")

    entries = []
    for i, fname in enumerate(files):
        fullpath = os.path.join(CACHE_FOLDER, fname)
        result = extract_image(fullpath, i)
        if result:
            print(f"[✓] Extracted: {result['Filename']} ← {result['URL']}")
            entries.append(result)

    if entries:
        with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Index", "Filename", "URL", "Content-Type"])
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry)

        print(f"[✓] Done! {len(entries)} images saved to {OUTPUT_FOLDER}")
        print(f"[→] CSV index written to {CSV_OUTPUT}")
    else:
        print("[!] No images detected in this cache set.")

if __name__ == "__main__":
    export_images()
