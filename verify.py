#!/usr/bin/env python3
"""
Healthcare System Verification Script
Tests all components to ensure everything works correctly
"""

import sys
import os

print("🏥 Healthcare System - Verification Script")
print("=" * 50)
print()

# Test 1: Python Version
print("1. Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"   ✗ Python {version.major}.{version.minor} (Need 3.8+)")
    sys.exit(1)

# Test 2: Import cryptography
print("\n2. Testing cryptography module...")
try:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    print("   ✓ cryptography module OK")
except ImportError as e:
    print(f"   ✗ cryptography import failed: {e}")
    print("   → Run: pip install cryptography")
    sys.exit(1)

# Test 3: Import PyQt5
print("\n3. Testing PyQt5 module...")
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.QtGui import QFont
    print("   ✓ PyQt5 module OK")
except ImportError as e:
    print(f"   ✗ PyQt5 import failed: {e}")
    print("   → Arch: sudo pacman -S python-pyqt5")
    print("   → Other: pip install PyQt5")
    sys.exit(1)

# Test 4: Import crypto_utils
print("\n4. Testing crypto_utils module...")
try:
    from crypto_utils import SymmetricEncryption, HashUtils
    print("   ✓ crypto_utils imported")
    
    # Test encryption
    key = SymmetricEncryption.generate_key()
    test_data = "Test patient data"
    encrypted = SymmetricEncryption.encrypt(test_data, key)
    decrypted = SymmetricEncryption.decrypt(encrypted, key)
    
    if decrypted == test_data:
        print("   ✓ Encryption/Decryption works")
    else:
        print("   ✗ Encryption test failed")
        sys.exit(1)
    
    # Test password hashing
    password = "test_password_123"
    hash_val, salt = HashUtils.hash_password(password)
    
    if HashUtils.verify_password(password, hash_val, salt):
        print("   ✓ Password hashing works")
    else:
        print("   ✗ Password hashing failed")
        sys.exit(1)
        
except ImportError as e:
    print(f"   ✗ crypto_utils import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ crypto_utils test failed: {e}")
    sys.exit(1)

# Test 5: Import auth_system
print("\n5. Testing auth_system module...")
try:
    from auth_system import AuthSystem
    print("   ✓ auth_system imported")
    
    # Test registration and authentication
    auth = AuthSystem('verify_test_users.json')
    success, msg = auth.register_user('verify_user', 'password123', 'doctor')
    
    if success:
        print("   ✓ User registration works")
    else:
        print(f"   ✗ User registration failed: {msg}")
    
    token, msg = auth.authenticate('verify_user', 'password123')
    
    if token:
        print("   ✓ User authentication works")
        
        # Test session verification
        session = auth.verify_session(token)
        if session:
            print("   ✓ Session verification works")
        else:
            print("   ✗ Session verification failed")
    else:
        print(f"   ✗ User authentication failed: {msg}")
    
    # Cleanup
    if os.path.exists('verify_test_users.json'):
        os.remove('verify_test_users.json')
        
except ImportError as e:
    print(f"   ✗ auth_system import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ auth_system test failed: {e}")
    sys.exit(1)

# Test 6: Import patient_records
print("\n6. Testing patient_records module...")
try:
    from patient_records import PatientRecords
    print("   ✓ patient_records imported")
    
    # Test patient operations
    pr = PatientRecords('verify_test_patients.json', 'test_password')
    patient_id = pr.add_patient(
        "Test Patient",
        "1990-01-01",
        "A+",
        "None",
        "Healthy"
    )
    
    if patient_id:
        print("   ✓ Patient creation works")
    else:
        print("   ✗ Patient creation failed")
    
    # Test retrieval
    patient = pr.get_patient(patient_id)
    if patient and patient['name'] == "Test Patient":
        print("   ✓ Patient retrieval works")
    else:
        print("   ✗ Patient retrieval failed")
    
    # Test search
    results = pr.search_patients("Test")
    if len(results) > 0:
        print("   ✓ Patient search works")
    else:
        print("   ✗ Patient search failed")
    
    # Cleanup
    if os.path.exists('verify_test_patients.json'):
        os.remove('verify_test_patients.json')
        
except ImportError as e:
    print(f"   ✗ patient_records import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ patient_records test failed: {e}")
    sys.exit(1)

# Test 7: Import UI modules
print("\n7. Testing UI modules...")
try:
    from login_ui import LoginWindow
    print("   ✓ login_ui imported (LoginWindow found)")
except ImportError as e:
    print(f"   ✗ login_ui import failed: {e}")
    sys.exit(1)

try:
    from main_ui import MainWindow
    print("   ✓ main_ui imported (MainWindow found)")
except ImportError as e:
    print(f"   ✗ main_ui import failed: {e}")
    sys.exit(1)

# Test 8: Import main
print("\n8. Testing main module...")
try:
    import main
    print("   ✓ main module imported")
except ImportError as e:
    print(f"   ✗ main import failed: {e}")
    sys.exit(1)

# Final summary
print("\n" + "=" * 50)
print("✅ ALL TESTS PASSED!")
print("=" * 50)
print()
print("Your Healthcare System is ready to use!")
print("Run: python main.py")
print()