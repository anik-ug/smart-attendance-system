"""Demo script: shows what is really stored in the database."""
import os
import sqlite3

from crypto_utils import decrypt_vector

conn = sqlite3.connect("attendance.db")
rows = conn.execute("SELECT id, name, roll_no, encoding FROM users").fetchall()

print("=" * 70)
print("WHAT IS STORED IN THE DATABASE (users table)")
print("=" * 70)
for uid, name, roll, blob in rows:
    print(f"\nUser: {name} ({roll})")
    print(f"  Raw DB value (encrypted): {blob[:55]}...")
    print(f"  Size: {len(blob)} bytes  -> unreadable without secret.key")
    vec = decrypt_vector(blob)
    print(f"  After decryption (inside app only): {vec.shape[0]}-D vector, first 5 values = {vec[:5].round(4)}")

print("\n" + "=" * 70)
print("PHOTO CHECK")
print("=" * 70)
count = 0
if os.path.isdir("dataset"):
    for _, _, files in os.walk("dataset"):
        count += len([f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))])
print(f"Face images stored on disk: {count}")