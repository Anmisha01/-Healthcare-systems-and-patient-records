"""
Authentication system for Healthcare application
Handles user registration, login, and session management
"""
import json
import os
import base64
from datetime import datetime, timedelta
from crypto_utils import HashUtils
import secrets


class AuthSystem:
    """Manages user authentication and authorization"""
    
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.users = self._load_users()
        self.sessions = {}
    
    def _load_users(self):
        """Load users from file"""
        if not os.path.exists(self.users_file):
            return {}
        
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def register_user(self, username, password, role='doctor'):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Hash password
        password_hash, salt = HashUtils.hash_password(password)
        
        # Store user data
        self.users[username] = {
            'password_hash': base64.b64encode(password_hash).decode(),
            'salt': base64.b64encode(salt).decode(),
            'role': role,
            'created_at': datetime.now().isoformat()
        }
        
        self._save_users()
        return True, "User registered successfully"
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if username not in self.users:
            return None, "Invalid username or password"
        
        user_data = self.users[username]
        password_hash = base64.b64decode(user_data['password_hash'])
        salt = base64.b64decode(user_data['salt'])
        
        if not HashUtils.verify_password(password, password_hash, salt):
            return None, "Invalid username or password"
        
        # Create session token
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            'username': username,
            'role': user_data['role'],
            'expires': datetime.now() + timedelta(hours=8)
        }
        
        return session_token, "Login successful"
    
    def verify_session(self, session_token):
        """Verify if session is valid"""
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        if datetime.now() > session['expires']:
            del self.sessions[session_token]
            return None
        
        return session
    
    def logout(self, session_token):
        """Logout user"""
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False