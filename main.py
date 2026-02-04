import sys
import os

# Set Qt platform to offscreen if no display
if not os.environ.get('DISPLAY') and not os.environ.get('QT_QPA_PLATFORM'):
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Lazy import PyQt5 to avoid crashes in headless environments during test collection
QtWidgets = None
LoginDialog = None

def _ensure_pyqt5():
    """Lazily import and initialize PyQt5."""
    global QtWidgets, LoginDialog
    if QtWidgets is not None:
        return
    try:
        from PyQt5 import QtWidgets as _QtWidgets
        QtWidgets = _QtWidgets
        from gui_login import LoginDialog as _LoginDialog
        LoginDialog = _LoginDialog
    except Exception:
        pass

# bring core components into a single entrypoint so tests and the
# rest of the system can import from `main` to exercise the full app
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
    _ensure_pyqt5()
    if LoginDialog is None:
        print("Error: PyQt5 GUI not available")
        return
    
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
    