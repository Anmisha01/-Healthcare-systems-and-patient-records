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
# Install Python from python.org
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

## First-Time Setup

1. **Start the application**: `python main.py`
2. **Create an account**: Click "Create New Account"
3. **Fill in details**:
   - Username: (your choice)
   - Password: (minimum 8 characters)
   - Confirm Password
   - Role: doctor/nurse/admin
4. **Click Register**
5. **Login** with your credentials
6. **Start managing patients!**

## Usage Guide

### Adding a Patient

1. Click the **"Add Patient"** tab
2. Fill in patient information:
   - Name (required)
   - Date of Birth (required, format: YYYY-MM-DD)
   - Blood Type (required, e.g., A+, O-, B+)
   - Allergies (optional)
   - Medical History (optional)
3. Click **"Add Patient"**
4. Patient ID will be displayed

### Viewing Patients

1. Go to the **"Patients"** tab
2. All patients are listed in a table
3. Use the search bar to filter by name
4. **Double-click** any patient to view full details

### Patient Details

1. Double-click a patient in the Patients tab
2. Switch to **"Patient Details"** tab
3. View complete patient information and visit history

## Project Structure

```
healthcare_system/
├── crypto_utils.py          # Cryptographic utilities (AES-256, PBKDF2)
├── auth_system.py           # Authentication & authorization
├── patient_records.py       # Encrypted patient data management
├── login_ui.py              # PyQt5 login interface
├── main_ui.py               # Main application interface
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── users.json              # User database (auto-created)
└── patient_records.json    # Encrypted patient records (auto-created)
```

## Security Features

### Password Security
- **Algorithm**: PBKDF2HMAC with SHA-256
- **Iterations**: 100,000 (prevents brute-force)
- **Salt**: Random 16-byte salt per password
- **Storage**: Only hash and salt stored, never plaintext

### Data Encryption
- **Algorithm**: AES-256-GCM (Authenticated Encryption)
- **Key Derivation**: PBKDF2HMAC from master password
- **IV**: Random 12-byte initialization vector per record
- **Authentication**: 16-byte authentication tag
- **Storage**: All patient data encrypted at rest

### Session Security
- **Tokens**: Cryptographically secure random tokens (32 bytes)
- **Expiration**: 8-hour automatic session timeout
- **Validation**: Token verification on each operation

## Data Storage

### users.json
Stores user accounts with hashed passwords:
```json
{
  "username": {
    "password_hash": "base64_encoded_hash",
    "salt": "base64_encoded_salt",
    "role": "doctor",
    "created_at": "ISO_timestamp"
  }
}
```

### patient_records.json
Stores encrypted patient records:
```json
{
  "patient_id": {
    "data": "encrypted_patient_data_base64",
    "last_updated": "ISO_timestamp"
  }
}
```

## Troubleshooting

### Import Error: LoginWindow

**Problem**: `ImportError: cannot import name 'LoginWindow'`

**Solution**:
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Re-run
python main.py
```

### ModuleNotFoundError: PyQt5

**Problem**: PyQt5 not installed

**Solution**:
```bash
# Arch Linux
sudo pacman -S python-pyqt5

# Ubuntu/Debian
sudo apt install python3-pyqt5

# macOS/Windows
pip install PyQt5
```

### Qt Platform Plugin Error

**Problem**: Qt platform plugin issues

**Solution**:
```bash
# Arch Linux
sudo pacman -S qt5-wayland  # for Wayland
sudo pacman -S qt5-x11extras  # for X11

# Set environment variable
export QT_QPA_PLATFORM=xcb  # or wayland
```

### Permission Denied on users.json or patient_records.json

**Problem**: Cannot write to data files

**Solution**:
```bash
# Check file permissions
ls -la *.json

# Fix permissions
chmod 644 users.json patient_records.json
```

## 🧪 Testing

Run the included tests:

```bash
# Test crypto utilities
python -c "from crypto_utils import SymmetricEncryption; \
key = SymmetricEncryption.generate_key(); \
enc = SymmetricEncryption.encrypt('test', key); \
print('Encryption:', SymmetricEncryption.decrypt(enc, key))"

# Test authentication
python -c "from auth_system import AuthSystem; \
auth = AuthSystem('test.json'); \
print(auth.register_user('test', 'password123', 'doctor'))"

# Test patient records
python -c "from patient_records import PatientRecords; \
pr = PatientRecords('test_pr.json'); \
id = pr.add_patient('Test', '1990-01-01', 'A+'); \
print('Patient ID:', id[:8])"
```

## Updating

To update the system:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
# Remove virtual environment (if used)
rm -rf venv/

# Remove data files (WARNING: This deletes all data!)
rm users.json patient_records.json

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Configuration

### Change Master Encryption Password

Edit `main_ui.py` and `patient_records.py`:

```python
# In main_ui.py, line ~18:
self.patient_records = PatientRecords(master_password='YOUR_NEW_PASSWORD')
```

**WARNING**: Changing the password will make existing encrypted data unreadable!

### Change Session Timeout

Edit `auth_system.py`, line ~56:

```python
'expires': datetime.now() + timedelta(hours=24)  # Changed to 24 hours
```

## Support

### Common Issues

1. **Login fails**: Check username/password, ensure user is registered
2. **Blank screen**: Check console for errors, verify PyQt5 installation
3. **Data not saving**: Check file permissions in project directory
4. **Encryption errors**: Ensure consistent master password

### Getting Help

1. Check this README thoroughly
2. Review error messages in console
3. Verify all dependencies are installed
4. Ensure Python 3.8+ is being used

## License

This project is released under the MIT License.

## Important Notes

- **Backup your data**: Regularly backup `users.json` and `patient_records.json`
- **Secure the master password**: If lost, encrypted data cannot be recovered
- **Production use**: Review and adjust security settings for your requirements
- **HIPAA compliance**: Ensure additional organizational policies are in place

## Default Master Password

The default master password for encryption is `changeme`. 

**CRITICAL**: Change this in production by editing `patient_records.py` or the environment variable before adding real patient data!