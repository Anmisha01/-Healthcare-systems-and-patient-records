import pytest
from Crypto.PublicKey import RSA

from main import PRIVATE_KEYS, USERS, authenticate


def test_auth_success():
    user, priv = authenticate("doctor1", "docpass123")
    assert user == USERS["doctor1"]
    assert priv == PRIVATE_KEYS["doctor1"]
    assert isinstance(priv, RSA.RsaKey)


def test_auth_wrong_password():
    user, priv = authenticate("doctor1", "wrongpassword")
    assert user is None and priv is None


def test_auth_unknown_user():
    user, priv = authenticate("unknown_user", "irrelevant")
    assert user is None and priv is None
