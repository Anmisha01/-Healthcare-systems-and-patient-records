import base64
import hashlib
import json

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15


def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def pad(data):
    l = AES.block_size - len(data) % AES.block_size
    return data + bytes([l]) * l


def unpad(data):
    return data[: -data[-1]]


def aes_encrypt(data: bytes, key: bytes) -> str:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(pad(data))).decode()


def aes_decrypt(enc: str, key: bytes) -> bytes:
    raw = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_CBC, raw[:16])
    return unpad(cipher.decrypt(raw[16:]))


def rsa_encrypt_key(aes_key: bytes, pubkey: RSA.RsaKey) -> str:
    return base64.b64encode(PKCS1_OAEP.new(pubkey).encrypt(aes_key)).decode()


def rsa_decrypt_key(enc: str, privkey: RSA.RsaKey) -> bytes:
    return PKCS1_OAEP.new(privkey).decrypt(base64.b64decode(enc))


def sign_data(data: bytes, privkey: RSA.RsaKey) -> str:
    h = SHA256.new(data)
    return base64.b64encode(pkcs1_15.new(privkey).sign(h)).decode()


def verify_signature(data: bytes, sig: str, pubkey: RSA.RsaKey) -> bool:
    try:
        pkcs1_15.new(pubkey).verify(SHA256.new(data), base64.b64decode(sig))
        return True
    except:
        return False
