"""
Unit tests for authentication system
Tests user registration, login, and session management
Updated for the final Healthcare System implementation
"""
import unittest
import os
import json
import tempfile
from datetime import datetime, timedelta
from auth_system import AuthSystem


class TestAuthSystem(unittest.TestCase):
    """Test cases for authentication system"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.auth = AuthSystem(users_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_register_user_success(self):
        """Test successful user registration"""
        success, message = self.auth.register_user('doctor1', 'password123', 'doctor')
        self.assertTrue(success)
        self.assertEqual(message, "User registered successfully")
        self.assertIn('doctor1', self.auth.users)
    
    def test_register_user_with_all_roles(self):
        """Test registration with different roles"""
        roles = ['doctor', 'nurse', 'admin']
        for i, role in enumerate(roles):
            success, msg = self.auth.register_user(f'user{i}', 'password123', role)
            self.assertTrue(success)
            self.assertEqual(self.auth.users[f'user{i}']['role'], role)
    
    def test_register_user_duplicate(self):
        """Test registration with duplicate username"""
        self.auth.register_user('doctor1', 'password123', 'doctor')
        success, message = self.auth.register_user('doctor1', 'another_pass', 'nurse')
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists")
    
    def test_register_user_short_password(self):
        """Test registration with short password"""
        success, message = self.auth.register_user('doctor2', 'short', 'doctor')
        self.assertFalse(success)
        self.assertEqual(message, "Password must be at least 8 characters")
    
    def test_register_user_minimum_password_length(self):
        """Test registration with exactly 8 character password"""
        success, message = self.auth.register_user('doctor3', 'pass1234', 'doctor')
        self.assertTrue(success)
    
    def test_register_user_empty_username(self):
        """Test registration with empty username"""
        success, message = self.auth.register_user('', 'password123', 'doctor')
        # Empty username should still register (no validation for empty)
        # but this could be enhanced in future
        self.assertTrue(success)
    
    def test_authenticate_success(self):
        """Test successful authentication"""
        self.auth.register_user('doctor4', 'password123', 'doctor')
        session_token, message = self.auth.authenticate('doctor4', 'password123')
        
        self.assertIsNotNone(session_token)
        self.assertEqual(message, "Login successful")
        self.assertIn(session_token, self.auth.sessions)
        self.assertIsInstance(session_token, str)
        self.assertGreater(len(session_token), 20)  # Token should be long
    
    def test_authenticate_wrong_username(self):
        """Test authentication with wrong username"""
        self.auth.register_user('doctor5', 'password123', 'doctor')
        session_token, message = self.auth.authenticate('wrong_user', 'password123')
        
        self.assertIsNone(session_token)
        self.assertEqual(message, "Invalid username or password")
    
    def test_authenticate_wrong_password(self):
        """Test authentication with wrong password"""
        self.auth.register_user('doctor6', 'password123', 'doctor')
        session_token, message = self.auth.authenticate('doctor6', 'wrong_password')
        
        self.assertIsNone(session_token)
        self.assertEqual(message, "Invalid username or password")
    
    def test_authenticate_case_sensitive_username(self):
        """Test that username authentication is case sensitive"""
        self.auth.register_user('doctor7', 'password123', 'doctor')
        session_token, message = self.auth.authenticate('Doctor7', 'password123')
        
        self.assertIsNone(session_token)
    
    def test_authenticate_case_sensitive_password(self):
        """Test that password authentication is case sensitive"""
        self.auth.register_user('doctor8', 'Password123', 'doctor')
        session_token, message = self.auth.authenticate('doctor8', 'password123')
        
        self.assertIsNone(session_token)
    
    def test_verify_session_valid(self):
        """Test verification of valid session"""
        self.auth.register_user('doctor9', 'password123', 'doctor')
        session_token, _ = self.auth.authenticate('doctor9', 'password123')
        
        session = self.auth.verify_session(session_token)
        self.assertIsNotNone(session)
        self.assertEqual(session['username'], 'doctor9')
        self.assertEqual(session['role'], 'doctor')
        self.assertIn('expires', session)
    
    def test_verify_session_invalid(self):
        """Test verification of invalid session"""
        session = self.auth.verify_session('invalid_token_12345')
        self.assertIsNone(session)
    
    def test_verify_session_expired(self):
        """Test verification of expired session"""
        self.auth.register_user('doctor10', 'password123', 'doctor')
        session_token, _ = self.auth.authenticate('doctor10', 'password123')
        
        # Manually expire the session
        self.auth.sessions[session_token]['expires'] = datetime.now() - timedelta(hours=1)
        
        session = self.auth.verify_session(session_token)
        self.assertIsNone(session)
        self.assertNotIn(session_token, self.auth.sessions)  # Should be removed
    
    def test_logout(self):
        """Test user logout"""
        self.auth.register_user('doctor11', 'password123', 'doctor')
        session_token, _ = self.auth.authenticate('doctor11', 'password123')
        
        result = self.auth.logout(session_token)
        self.assertTrue(result)
        self.assertNotIn(session_token, self.auth.sessions)
        
        # Verify session is invalid after logout
        session = self.auth.verify_session(session_token)
        self.assertIsNone(session)
    
    def test_logout_invalid_token(self):
        """Test logout with invalid token"""
        result = self.auth.logout('invalid_token')
        self.assertFalse(result)
    
    def test_user_persistence(self):
        """Test that users are saved to file and persist"""
        self.auth.register_user('doctor12', 'password123', 'doctor')
        
        # Create new auth instance with same file
        new_auth = AuthSystem(users_file=self.temp_file.name)
        self.assertIn('doctor12', new_auth.users)
        
        # Test authentication with persisted user
        session_token, message = new_auth.authenticate('doctor12', 'password123')
        self.assertIsNotNone(session_token)
    
    def test_user_data_structure(self):
        """Test that user data is stored correctly"""
        self.auth.register_user('doctor13', 'password123', 'doctor')
        
        user_data = self.auth.users['doctor13']
        self.assertIn('password_hash', user_data)
        self.assertIn('salt', user_data)
        self.assertIn('role', user_data)
        self.assertIn('created_at', user_data)
        self.assertEqual(user_data['role'], 'doctor')
    
    def test_multiple_roles(self):
        """Test registration and authentication with different roles"""
        self.auth.register_user('doctor14', 'password123', 'doctor')
        self.auth.register_user('nurse1', 'password123', 'nurse')
        self.auth.register_user('admin1', 'password123', 'admin')
        
        self.assertEqual(self.auth.users['doctor14']['role'], 'doctor')
        self.assertEqual(self.auth.users['nurse1']['role'], 'nurse')
        self.assertEqual(self.auth.users['admin1']['role'], 'admin')
        
        # Verify sessions have correct roles
        token1, _ = self.auth.authenticate('doctor14', 'password123')
        token2, _ = self.auth.authenticate('nurse1', 'password123')
        token3, _ = self.auth.authenticate('admin1', 'password123')
        
        self.assertEqual(self.auth.verify_session(token1)['role'], 'doctor')
        self.assertEqual(self.auth.verify_session(token2)['role'], 'nurse')
        self.assertEqual(self.auth.verify_session(token3)['role'], 'admin')
    
    def test_concurrent_sessions(self):
        """Test multiple concurrent sessions for same user"""
        self.auth.register_user('doctor15', 'password123', 'doctor')
        
        token1, _ = self.auth.authenticate('doctor15', 'password123')
        token2, _ = self.auth.authenticate('doctor15', 'password123')
        token3, _ = self.auth.authenticate('doctor15', 'password123')
        
        self.assertNotEqual(token1, token2)
        self.assertNotEqual(token2, token3)
        self.assertNotEqual(token1, token3)
        
        # All sessions should be valid
        self.assertIsNotNone(self.auth.verify_session(token1))
        self.assertIsNotNone(self.auth.verify_session(token2))
        self.assertIsNotNone(self.auth.verify_session(token3))
    
    def test_session_expiration_time(self):
        """Test that session expiration is set correctly"""
        self.auth.register_user('doctor16', 'password123', 'doctor')
        session_token, _ = self.auth.authenticate('doctor16', 'password123')
        
        session = self.auth.sessions[session_token]
        expires = session['expires']
        
        # Should expire in approximately 8 hours
        time_diff = expires - datetime.now()
        self.assertGreater(time_diff.total_seconds(), 7.5 * 3600)  # At least 7.5 hours
        self.assertLess(time_diff.total_seconds(), 8.5 * 3600)  # At most 8.5 hours
    
    def test_password_not_stored_plaintext(self):
        """Test that passwords are not stored in plaintext"""
        password = 'my_secret_password'
        self.auth.register_user('doctor17', password, 'doctor')
        
        # Read file directly
        with open(self.temp_file.name, 'r') as f:
            file_content = f.read()
        
        # Password should not appear in file
        self.assertNotIn(password, file_content)
    
    def test_multiple_users_different_passwords(self):
        """Test multiple users with different passwords"""
        users = [
            ('user1', 'password1'),
            ('user2', 'password2'),
            ('user3', 'password3'),
        ]
        
        for username, password in users:
            self.auth.register_user(username, password, 'doctor')
        
        # Each should authenticate with correct password
        for username, password in users:
            token, msg = self.auth.authenticate(username, password)
            self.assertIsNotNone(token)
        
        # Wrong passwords should fail
        token, msg = self.auth.authenticate('user1', 'password2')
        self.assertIsNone(token)


if __name__ == '__main__':
    unittest.main(verbosity=2)