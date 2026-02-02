from Crypto.PublicKey import RSA
from crypto_utils import sha256_hash

doctor_key = RSA.generate(2048)
nurse_key = RSA.generate(2048)
patient_key = RSA.generate(2048)

USERS = {
    "doctor1": {
        "password": sha256_hash("docpass123"),
        "role": "doctor",
        "pub": doctor_key.publickey()
    },
    "nurse1": {
        "password": sha256_hash("nursepwd"),
        "role": "nurse",
        "pub": nurse_key.publickey()
    },
    "patient1": {
        "password": sha256_hash("patientpwd"),
        "role": "patient",
        "pub": patient_key.publickey()
    }
}

PRIVATE_KEYS = {
    "doctor1": doctor_key,
    "nurse1": nurse_key,
    "patient1": patient_key
}

PATIENT_RECORDS = []
AUDIT_LOG = []
