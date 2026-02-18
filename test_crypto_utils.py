"""
Unit tests for cryptographic utilities
Tests symmetric encryption, asymmetric encryption, and password hashing
Updated for the final Healthcare System implementation
"""
import unittest
import os
from crypto_utils import SymmetricEncryption, HashUtils


class TestSymmetricEncryption(unittest.TestCase):
    """Test cases for symmetric encryption"""
    
    def test_generate_key(self):
        """Test key generation"""
        key = SymmetricEncryption.generate_key()
        self.assertEqual(len(key), 32)  # 256 bits
        self.assertIsInstance(key, bytes)
        
        # Keys should be unique
        key2 = SymmetricEncryption.generate_key()
        self.assertNotEqual(key, key2)
    
    def test_derive_key_from_password(self):
        """Test key derivation from password"""
        password = "test_password_123"
        key1, salt1 = SymmetricEncryption.derive_key_from_password(password)
        
        self.assertEqual(len(key1), 32)
        self.assertEqual(len(salt1), 16)
        self.assertIsInstance(key1, bytes)
        self.assertIsInstance(salt1, bytes)
        
        # Same password with same salt should produce same key
        key2, _ = SymmetricEncryption.derive_key_from_password(password, salt1)
        self.assertEqual(key1, key2)
        
        # Different salt should produce different key
        key3, salt3 = SymmetricEncryption.derive_key_from_password(password)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(salt1, salt3)
    
    def test_encrypt_decrypt(self):
        """Test encryption and decryption"""
        key = SymmetricEncryption.generate_key()
        plaintext = "Sensitive patient data: John Doe, DOB: 1990-01-01, Blood Type: A+"
        
        # Encrypt
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        self.assertIsInstance(ciphertext, str)
        self.assertNotEqual(plaintext, ciphertext)
        self.assertGreater(len(ciphertext), 0)
        
        # Decrypt
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_unicode(self):
        """Test encryption with unicode characters"""
        key = SymmetricEncryption.generate_key()
        plaintext = "Patient: José García, Diagnosis: 中文测试, Notes: ñ á é í ó ú"
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_empty_string(self):
        """Test encryption of empty string"""
        key = SymmetricEncryption.generate_key()
        plaintext = ""
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_special_characters(self):
        """Test encryption with special characters"""
        key = SymmetricEncryption.generate_key()
        plaintext = "Special chars: !@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)
    
    def test_decrypt_wrong_key(self):
        """Test that decryption with wrong key fails"""
        key1 = SymmetricEncryption.generate_key()
        key2 = SymmetricEncryption.generate_key()
        plaintext = "Secret patient data"
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key1)
        
        with self.assertRaises(Exception):
            SymmetricEncryption.decrypt(ciphertext, key2)
    
    def test_encrypt_different_ciphertexts(self):
        """Test that same plaintext produces different ciphertexts (due to random IV)"""
        key = SymmetricEncryption.generate_key()
        plaintext = "Patient medical record"
        
        ciphertext1 = SymmetricEncryption.encrypt(plaintext, key)
        ciphertext2 = SymmetricEncryption.encrypt(plaintext, key)
        
        # Different IVs should produce different ciphertexts
        self.assertNotEqual(ciphertext1, ciphertext2)
        
        # But both should decrypt to same plaintext
        self.assertEqual(
            SymmetricEncryption.decrypt(ciphertext1, key),
            SymmetricEncryption.decrypt(ciphertext2, key)
        )
    
    def test_large_data_encryption(self):
        """Test encryption of large data"""
        key = SymmetricEncryption.generate_key()
        plaintext = "A" * 50000  # 50KB of data
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)
    
    def test_multiline_data_encryption(self):
        """Test encryption of multiline data"""
        key = SymmetricEncryption.generate_key()
        plaintext = """Patient Name: John Doe
Date of Birth: 1990-01-01
Blood Type: A+
Allergies: Penicillin, Peanuts
Medical History:
- 2020: Appendectomy
- 2021: Flu vaccination
- 2022: Annual checkup"""
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)
    
    def test_json_data_encryption(self):
        """Test encryption of JSON-like data"""
        key = SymmetricEncryption.generate_key()
        plaintext = '{"name":"John Doe","age":30,"diagnosis":"Healthy"}'
        
        ciphertext = SymmetricEncryption.encrypt(plaintext, key)
        decrypted = SymmetricEncryption.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)


class TestHashUtils(unittest.TestCase):
    """Test cases for password hashing"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "secure_password_123"
        hash_value, salt = HashUtils.hash_password(password)
        
        self.assertEqual(len(hash_value), 32)
        self.assertEqual(len(salt), 16)
        self.assertIsInstance(hash_value, bytes)
        self.assertIsInstance(salt, bytes)
        
        # Same password with same salt should produce same hash
        hash_value2, _ = HashUtils.hash_password(password, salt)
        self.assertEqual(hash_value, hash_value2)
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "my_secure_password_2024"
        hash_value, salt = HashUtils.hash_password(password)
        
        result = HashUtils.verify_password(password, hash_value, salt)
        self.assertTrue(result)
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hash_value, salt = HashUtils.hash_password(password)
        
        result = HashUtils.verify_password(wrong_password, hash_value, salt)
        self.assertFalse(result)
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive"""
        password = "MyPassword123"
        wrong_case = "mypassword123"
        hash_value, salt = HashUtils.hash_password(password)
        
        result = HashUtils.verify_password(wrong_case, hash_value, salt)
        self.assertFalse(result)
    
    def test_hash_password_different_salts(self):
        """Test that same password with different salts produces different hashes"""
        password = "test_password"
        hash1, salt1 = HashUtils.hash_password(password)
        hash2, salt2 = HashUtils.hash_password(password)
        
        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(salt1, salt2)
    
    def test_hash_empty_password(self):
        """Test hashing empty password"""
        password = ""
        hash_value, salt = HashUtils.hash_password(password)
        
        self.assertEqual(len(hash_value), 32)
        self.assertEqual(len(salt), 16)
        self.assertTrue(HashUtils.verify_password(password, hash_value, salt))
    
    def test_hash_unicode_password(self):
        """Test hashing password with unicode characters"""
        password = "пароль密码🔒password"
        hash_value, salt = HashUtils.hash_password(password)
        
        self.assertTrue(HashUtils.verify_password(password, hash_value, salt))
        self.assertFalse(HashUtils.verify_password("wrong", hash_value, salt))
    
    def test_hash_long_password(self):
        """Test hashing very long password"""
        password = "a" * 500  # 500 character password
        hash_value, salt = HashUtils.hash_password(password)
        
        self.assertTrue(HashUtils.verify_password(password, hash_value, salt))
    
    def test_verify_password_wrong_salt(self):
        """Test verification fails with wrong salt"""
        password = "test_password"
        hash_value, salt = HashUtils.hash_password(password)
        wrong_salt = os.urandom(16)
        
        result = HashUtils.verify_password(password, hash_value, wrong_salt)
        self.assertFalse(result)
    
    def test_hash_special_characters_password(self):
        """Test hashing password with special characters"""
        password = "P@ssw0rd!#$%^&*()"
        hash_value, salt = HashUtils.hash_password(password)
        
        self.assertTrue(HashUtils.verify_password(password, hash_value, salt))
        self.assertFalse(HashUtils.verify_password("P@ssw0rd", hash_value, salt))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)