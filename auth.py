from crypto_utils import sha256_hash
from data_store import PRIVATE_KEYS, USERS


def authenticate(username: str, password: str):
    user = USERS.get(username)
    if not user:
        return None, None

    if sha256_hash(password) != user["password"]:
        return None, None

    return user, PRIVATE_KEYS[username]
