import os
import sys

import pytest

# Skip entire module - it tests GUI functionality which can't run in headless CI
pytest.skip("GUI tests require display", allow_module_level=True)

pytest.importorskip("PyQt5")

from PyQt5 import QtWidgets


def test_main_user_cancels(monkeypatch):
    import main

    # Dummy QApplication
    class DummyApp:
        def __init__(self, argv):
            pass

        def exec_(self):
            return 0

    monkeypatch.setattr(QtWidgets, "QApplication", DummyApp)

    # LoginDialog that returns no credentials
    class DummyLogin:
        def get_credentials(self):
            return None, None

    monkeypatch.setattr(main, "LoginDialog", DummyLogin)

    called = {"auth": False, "critical": 0, "info": 0}

    def fake_auth(u, p):
        called["auth"] = True
        return None, None

    monkeypatch.setattr(main, "authenticate", fake_auth)

    def fake_critical(*a, **k):
        called["critical"] += 1

    def fake_info(*a, **k):
        called["info"] += 1

    monkeypatch.setattr(QtWidgets.QMessageBox, "critical", staticmethod(fake_critical))
    monkeypatch.setattr(QtWidgets.QMessageBox, "information", staticmethod(fake_info))

    # Should return without calling authenticate or message boxes
    res = main.main()
    assert res is None
    assert called["auth"] is False
    assert called["critical"] == 0
    assert called["info"] == 0


def test_main_invalid_credentials_shows_error(monkeypatch):
    import main

    class DummyApp:
        def __init__(self, argv):
            pass

        def exec_(self):
            return 0

    monkeypatch.setattr(QtWidgets, "QApplication", DummyApp)

    class DummyLogin:
        def get_credentials(self):
            return "doctor1", "badpass"

    monkeypatch.setattr(main, "LoginDialog", DummyLogin)

    monkeypatch.setattr(main, "authenticate", lambda u, p: (None, None))

    called = {"critical": 0, "info": 0}

    def fake_critical(*a, **k):
        called["critical"] += 1

    def fake_info(*a, **k):
        called["info"] += 1

    monkeypatch.setattr(QtWidgets.QMessageBox, "critical", staticmethod(fake_critical))
    monkeypatch.setattr(QtWidgets.QMessageBox, "information", staticmethod(fake_info))

    res = main.main()
    assert res is None
    assert called["critical"] == 1
    assert called["info"] == 0


def test_main_success_shows_welcome_and_exits(monkeypatch):
    import main

    class DummyApp:
        def __init__(self, argv):
            pass

        def exec_(self):
            return 0

    monkeypatch.setattr(QtWidgets, "QApplication", DummyApp)

    class DummyLogin:
        def get_credentials(self):
            return "doctor1", "docpass123"

    monkeypatch.setattr(main, "LoginDialog", DummyLogin)

    # fake authenticate returns a user dict with role
    monkeypatch.setattr(
        main, "authenticate", lambda u, p: ({"role": "doctor"}, object())
    )

    info_args = {}

    def fake_info(parent, title, text):
        info_args["title"] = title
        info_args["text"] = text

    monkeypatch.setattr(QtWidgets.QMessageBox, "information", staticmethod(fake_info))
    monkeypatch.setattr(
        QtWidgets.QMessageBox, "critical", staticmethod(lambda *a, **k: None)
    )

    # intercept sys.exit so test doesn't exit
    exits = {}

    def fake_exit(code=0):
        exits["code"] = code
        raise SystemExit(code)

    monkeypatch.setattr(sys, "exit", fake_exit)

    with pytest.raises(SystemExit) as exc:
        main.main()

    assert exc.value.code == 0
    assert info_args["title"] == "Success"
    assert "Welcome doctor1 (doctor)" in info_args["text"]
