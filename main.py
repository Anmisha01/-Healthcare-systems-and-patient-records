import sys
from PyQt5 import QtWidgets

# bring core components into a single entrypoint so tests and the
# rest of the system can import from `main` to exercise the full app
from gui_login import LoginDialog
from auth import authenticate
from crypto_utils import (
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
from data_store import USERS, PRIVATE_KEYS, PATIENT_RECORDS, AUDIT_LOG


def main():
    app = QtWidgets.QApplication(sys.argv)

    login = LoginDialog()
    username, password = login.get_credentials()

    if not username:
        return

    user, privkey = authenticate(username, password)

    if not user:
        QtWidgets.QMessageBox.critical(None, "Error", "Invalid username or password")
        return

    QtWidgets.QMessageBox.information(
        None,
        "Success",
        f"Welcome {username} ({user['role']})"
    )

    sys.exit(app.exec_())


def run_auth_cli(username: str, password: str):
    """Programmatic authentication helper usable by tests and a CLI.

    Returns (user_dict, private_key) the same as `auth.authenticate`.
    """
    return authenticate(username, password)


if __name__ == "__main__":
    main()
    