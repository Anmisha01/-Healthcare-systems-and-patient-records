import pytest
from Crypto.PublicKey import RSA

from main import USERS, PRIVATE_KEYS, PATIENT_RECORDS, AUDIT_LOG
from main import sha256_hash


def test_users_structure_and_roles():
    assert isinstance(USERS, dict)
    # expected users
    for username, expected_role in [("doctor1", "doctor"), ("nurse1", "nurse"), ("patient1", "patient")]:
        assert username in USERS
        user = USERS[username]
        assert user["role"] == expected_role
        # stored password should be a sha256 hex digest
        assert user["password"] == sha256_hash({
            "doctor1": "docpass123",
            "nurse1": "nursepwd",
            "patient1": "patientpwd"
        }[username])


def test_private_keys_and_publics_match():
    assert isinstance(PRIVATE_KEYS, dict)
    for username, priv in PRIVATE_KEYS.items():
        assert isinstance(priv, RSA.RsaKey)
        pub_from_priv = priv.publickey().export_key()
        pub_stored = USERS[username]["pub"].export_key()
        assert pub_from_priv == pub_stored


def test_patient_records_and_audit_log_initially_empty():
    assert isinstance(PATIENT_RECORDS, list)
    assert isinstance(AUDIT_LOG, list)
    assert len(PATIENT_RECORDS) == 0
    assert len(AUDIT_LOG) == 0
