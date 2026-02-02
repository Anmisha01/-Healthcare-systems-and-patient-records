import pytest

pytest.importorskip("PyQt5")

from main import LoginDialog
from PyQt5 import QtWidgets


def test_get_credentials_when_accepted(monkeypatch):
    dlg = LoginDialog()
    # simulate user input and accepted dialog
    monkeypatch.setattr(dlg, "exec_", lambda: QtWidgets.QDialog.Accepted)
    monkeypatch.setattr(dlg.user, "text", lambda: " alice ")
    monkeypatch.setattr(dlg.pwd, "text", lambda: " secret ")

    user, pwd = dlg.get_credentials()
    assert user == "alice"
    assert pwd == "secret"


def test_get_credentials_when_rejected(monkeypatch):
    dlg = LoginDialog()
    monkeypatch.setattr(dlg, "exec_", lambda: QtWidgets.QDialog.Rejected)

    user, pwd = dlg.get_credentials()
    assert user is None and pwd is None
