"""Encrypt / decrypt face vectors (Fernet = AES-128-CBC + HMAC).

The key is generated once and saved in secret.key (never commit this file).
"""
import os

import numpy as np
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def _load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    try:
        os.chmod(KEY_FILE, 0o600)   # only the owner can read it
    except OSError:
        pass
    return key


_fernet = Fernet(_load_key())


def encrypt_vector(vector):
    """128-d numpy vector -> encrypted bytes."""
    raw = np.asarray(vector, dtype=np.float64).tobytes()
    return _fernet.encrypt(raw)


def decrypt_vector(token):
    """Encrypted bytes -> 128-d numpy vector."""
    raw = _fernet.decrypt(token)
    return np.frombuffer(raw, dtype=np.float64)