#Author: Ashok Krishna.
import sqlite3
import os
import base64
import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from pathlib import Path

# === Chrome cookie decryption constants ===
PASSWORD = b'peanuts'
SALT = b'saltysalt'
IV = b' ' * 16  # 16 spaces
KEY_LENGTH = 16
ITERATIONS = 1

# === Path to copied DB (avoid lock issues) ===
user_input_path = input("Enter the path to the Chromium Cookies database file: ").strip()
COOKIES_DB_PATH = os.path.abspath(os.path.expanduser(user_input_path)) #"Cookies"

if not os.path.isfile(COOKIES_DB_PATH):
    print(f"Error: File not found at {COOKIES_DB_PATH}")
    exit(1)
# === Key derivation Function- using PFKDF2 algorithm ===
# This function transforms Hardcoded peanuts password to Strong AES Key.
def get_key():
    return PBKDF2(PASSWORD, SALT, dkLen=KEY_LENGTH, count=ITERATIONS)
#Chrome >=v24 encrypts cookies with a SHA256 hash of the host_key but the exact form varies depending on domain nesting. So this function brute-forces possible forms.
def try_host_digests(host_key):
    """Generate candidate host_key variations for SHA256 prefix match."""
    host_key = host_key.lstrip('.')
    parts = host_key.split('.')
    for i in range(len(parts) - 1):
        base = '.'.join(parts[i:])
        yield base
        yield '.' + base

def decode_jwt_if_possible(value):
    """Try to decode a JWT in the cookie."""
    try:
        for part in value.split():
            if part.count('.') == 2:
                header, payload, _ = part.split('.')
                header_dec = json.loads(base64.urlsafe_b64decode(header + '=='))
                payload_dec = json.loads(base64.urlsafe_b64decode(payload + '=='))
                return '[JWT] Header: ' + json.dumps(header_dec) + ' Payload: ' + json.dumps(payload_dec)
    except Exception:
        pass
    return value

#===Decrypt Cookie Function ===
def decrypt_cookie(encrypted_value, key, host_key):
    """Handles v10 format with optional SHA256 prefix (v24+)"""
    # strip version ID before decryption.
    if encrypted_value.startswith(b'v10'):
        encrypted_value = encrypted_value[3:]
    # Use AES-CBC mode to decrypt the cookie data
    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(encrypted_value)
    #Chrome uses PKCS#5 padding. So strip padding.
    pad_len = decrypted[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding")
    decrypted = decrypted[:-pad_len]
    # After decryption it verifies the SHA256(host_key) digest part whether its correct or wrong.
    if len(decrypted) >= 32:
        digest = decrypted[:32]
        payload = decrypted[32:]

        for variant in try_host_digests(host_key):
            if digest == hashlib.sha256(variant.encode()).digest():
                return decode_jwt_if_possible(payload.decode('utf-8', errors='ignore'))

        # No digest match; fallback
        return decode_jwt_if_possible(decrypted.decode('utf-8', errors='ignore'))
    else:
        return decrypted.decode('utf-8', errors='ignore')
# open the file Cookies database and read the file for all values.
def read_all_cookies():
    if not os.path.exists(COOKIES_DB_PATH):
        print(f"[!] File not found: {COOKIES_DB_PATH}")
        return

    key = get_key()
    conn = sqlite3.connect(COOKIES_DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT host_key, name, path, encrypted_value FROM cookies")
        rows = cursor.fetchall()

        if not rows:
            print("[!] No cookies found.")
            return

        print(f"[+] Decrypting {len(rows)} cookies...\n")
        print("Host,\tName,\t\tPath,\t\tDecrypted_CookieValue\n")
        # look over each cookie value and decrypt.
        for host, name, path, encrypted_value in rows:
            try:
                val = decrypt_cookie(encrypted_value, key, host)
            except Exception as e:
                val = f"[DECRYPTION FAILED] {e}"
            print(f"{host:<30} {name:<30} {path:<30} → {val}")
    finally:
        conn.close()
# Main function.
if __name__ == "__main__":
    read_all_cookies()

