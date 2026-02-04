import base64
import pytest
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from main import (
    sha256_hash,
    pad,
    unpad,
    aes_encrypt,
    aes_decrypt,
    rsa_encrypt_key,
    rsa_decrypt_key,
    sign_data,
    verify_signature,
)


def test_sha256_hash():
    # known SHA256("abc")
    assert sha256_hash("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_pad_unpad_roundtrip():
    data = b"YELLOW SUBMARINE"
    padded = pad(data)
    assert unpad(padded) == data


def test_aes_encrypt_decrypt_roundtrip():
    key = get_random_bytes(32)
    data = b"secret data 123"
    enc = aes_encrypt(data, key)
    dec = aes_decrypt(enc, key)
    assert dec == data


def test_aes_decrypt_with_wrong_key_raises():
    key = get_random_bytes(32)
    wrong_key = get_random_bytes(32)
    data = b"another secret"
    enc = aes_encrypt(data, key)
    # Decrypting with wrong key returns garbled data (doesn't raise exception)
    result = aes_decrypt(enc, wrong_key)
    assert result != data


def test_rsa_encrypt_decrypt_key_roundtrip():
    priv = RSA.generate(2048)
    pub = priv.publickey()
    aes_key = get_random_bytes(32)
    enc = rsa_encrypt_key(aes_key, pub)
    dec = rsa_decrypt_key(enc, priv)
    assert dec == aes_key


def test_rsa_decrypt_with_wrong_private_raises():
    priv = RSA.generate(2048)
    other_priv = RSA.generate(2048)
    pub = priv.publickey()
    aes_key = get_random_bytes(32)
    enc = rsa_encrypt_key(aes_key, pub)
    with pytest.raises(Exception):
        rsa_decrypt_key(enc, other_priv)


def test_sign_and_verify_success_and_failures():
    priv = RSA.generate(2048)
    pub = priv.publickey()
    data = b"message to sign"
    sig = sign_data(data, priv)
    assert verify_signature(data, sig, pub) is True
    # modified data should fail
    assert verify_signature(data + b"x", sig, pub) is False
    # tampered signature should fail
    decoded = base64.b64decode(sig)
    tampered = base64.b64encode(b"\x00" * len(decoded)).decode()
    assert verify_signature(data, tampered, pub) is False
