import pytest
import os

# Skip this module if no real display (CI environment)
if not os.environ.get('CI') and not os.environ.get('DISPLAY'):
    pytest.skip("GUI tests require display", allow_module_level=True)

pytest.importorskip("PyQt5")

from main import LoginDialog
from PyQt5 import QtWidgets


@pytest.mark.skip(reason="GUI tests require display server - run manually")
def test_get_credentials_when_accepted(monkeypatch):
    dlg = LoginDialog()
    # simulate user input and accepted dialog
    monkeypatch.setattr(dlg, "exec_", lambda: QtWidgets.QDialog.Accepted)
    monkeypatch.setattr(dlg.user, "text", lambda: " alice ")
    monkeypatch.setattr(dlg.pwd, "text", lambda: " secret ")

    user, pwd = dlg.get_credentials()
    assert user == "alice"
    assert pwd == "secret"


@pytest.mark.skip(reason="GUI tests require display server - run manually")
def test_get_credentials_when_rejected(monkeypatch):
    dlg = LoginDialog()
    monkeypatch.setattr(dlg, "exec_", lambda: QtWidgets.QDialog.Rejected)

    user, pwd = dlg.get_credentials()
    assert user is None and pwd is None
