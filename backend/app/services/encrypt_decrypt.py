import base64
import hashlib

import cryptography.fernet
from cryptography.fernet import Fernet

from core.salt import SALT


def decrypt(text: str) -> str:
    crypt = text.encode()
    key = hashlib.md5(SALT).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode())
    f = Fernet(key_64)
    try:
        decrypted_text = f.decrypt(crypt).decode()
    except cryptography.fernet.InvalidToken:
        decrypted_text = text
    return decrypted_text


def encrypt(text: str) -> str:
    key = hashlib.md5(SALT).hexdigest()
    key_64 = base64.urlsafe_b64encode(key.encode())
    cipher = Fernet(key_64).encrypt(text.encode())
    return cipher.decode()
