# Healthcate System and Patient Records

Small example project demonstrating simple authentication, symmetric/asymmetric crypto helpers, and a PyQt5 login UI.

**Quick summary**
- Python project using PyCryptodome and PyQt5 for a tiny demonstrator of crypto primitives and a login dialog.

**Prerequisites**
- Python 3.8+
- pip

**Recommended packages**
- PyQt5
- pycryptodome
- pytest (for running tests)

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install PyQt5 pycryptodome pytest
```

**Run the GUI app**

```bash
python main.py
```

This launches the login dialog (`LoginDialog`) from `gui_login.py` and authenticates using the in-memory `USERS` defined in `data_store.py`.

**Programmatic auth (CLI helper)**

You can use the programmatic helper `run_auth_cli()` from `main` without launching the GUI, e.g.: 

```bash
python -c "from main import run_auth_cli; print(run_auth_cli('doctor1','docpass123'))"
```

**Run tests**

From the project root:

```bash
pytest -q
```

The tests exercise the crypto utilities, the data store, the auth logic and the gui login behavior (PyQt5 is required for GUI tests).

**Project layout**

- `main.py` — unified entrypoint and exports for tests/CLI; starts GUI when run directly.
- `gui_login.py` — PyQt5 login dialog (`LoginDialog`).
- `auth.py` — authentication logic using `data_store.USERS`.
- `data_store.py` — in-memory users, RSA keypairs, patient records and audit log.
- `crypto_utils.py` — helper functions: hashing, AES, RSA key-wrap, signing/verification.
- `tests/` — pytest-based unit tests.

**Notes**
- The project stores keys and secrets only in memory for demonstration/testing purposes — do not use this pattern for production secrets.
- If you want, I can add a `requirements.txt` or a minimal CLI to run common operations.
