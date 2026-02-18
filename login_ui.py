"""
PyQt5 Login Interface for Healthcare System
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QMessageBox, QDialog, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from auth_system import AuthSystem


class LoginWindow(QMainWindow):
    """Modern login window with authentication"""
    
    login_successful = pyqtSignal(str, str)  # session_token, username
    
    def __init__(self):
        super().__init__()
        # Ensure window is properly deleted when closed
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.auth_system = AuthSystem()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Healthcare System - Login')
        self.setFixedSize(600, 750)  # Even larger for better spacing
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8;
            }
            QLabel {
                color: #2d3748;
            }
            QLineEdit {
                padding: 18px;
                border: 2px solid #cbd5e0;
                border-radius: 10px;
                background-color: white;
                font-size: 16px;
                min-height: 50px;
            }
            QLineEdit:focus {
                border-color: #4299e1;
                border-width: 3px;
            }
            QPushButton {
                padding: 18px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                min-height: 55px;
            }
            QPushButton#loginButton {
                background-color: #4299e1;
                color: white;
                border: none;
                font-size: 18px;
            }
            QPushButton#loginButton:hover {
                background-color: #3182ce;
            }
            QPushButton#registerButton {
                background-color: white;
                color: #4299e1;
                border: 2px solid #4299e1;
                font-size: 16px;
            }
            QPushButton#registerButton:hover {
                background-color: #ebf8ff;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with generous spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 50, 60, 50)
        layout.setSpacing(0)  # We'll control spacing manually
        
        # Header with larger font
        header = QLabel('🏥 Healthcare System')
        header.setFont(QFont('Arial', 32, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2d3748;")
        layout.addWidget(header)
        
        layout.addSpacing(10)
        
        subtitle = QLabel('Secure Patient Records Management')
        subtitle.setFont(QFont('Arial', 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #718096;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(50)
        
        # Username section - label closer to input
        username_label = QLabel('Username')
        username_label.setFont(QFont('Arial', 14, QFont.Bold))
        username_label.setStyleSheet("color: #2d3748;")
        username_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(username_label)
        
        layout.addSpacing(8)  # Small gap between label and input
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.username_input)
        
        layout.addSpacing(25)  # Gap between input groups
        
        # Password section - label closer to input
        password_label = QLabel('Password')
        password_label.setFont(QFont('Arial', 14, QFont.Bold))
        password_label.setStyleSheet("color: #2d3748;")
        password_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(password_label)
        
        layout.addSpacing(8)  # Small gap between label and input
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(35)  # Gap before buttons
        
        # Login button - larger and more prominent
        self.login_button = QPushButton('Login')
        self.login_button.setObjectName('loginButton')
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        layout.addSpacing(15)
        
        # Register button
        self.register_button = QPushButton('Create New Account')
        self.register_button.setObjectName('registerButton')
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.show_register_dialog)
        layout.addWidget(self.register_button)
        
        layout.addStretch()
        
        # Footer with larger text
        footer = QLabel('🔒 Encrypted • Secure • HIPAA Compliant')
        footer.setFont(QFont('Arial', 11))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #a0aec0;")
        layout.addWidget(footer)
        
        central_widget.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        session_token, message = self.auth_system.authenticate(username, password)
        
        if session_token:
            QMessageBox.information(self, 'Success', message)
            self.login_successful.emit(session_token, username)
            self.close()
        else:
            QMessageBox.critical(self, 'Error', message)
            self.password_input.clear()
    
    def show_register_dialog(self):
        """Show registration dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle('Register New User')
        dialog.setFixedSize(550, 650)
        
        # Apply consistent styling
        dialog.setStyleSheet("""
            QDialog {
                background-color: #f0f4f8;
            }
            QLabel {
                color: #2d3748;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 15px;
                border: 2px solid #cbd5e0;
                border-radius: 8px;
                background-color: white;
                font-size: 15px;
                min-height: 45px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4299e1;
                border-width: 3px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #4a5568;
            }
            QPushButton {
                padding: 15px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                min-height: 50px;
            }
            QPushButton#registerBtn {
                background-color: #48bb78;
                color: white;
                border: none;
            }
            QPushButton#registerBtn:hover {
                background-color: #38a169;
            }
            QPushButton#cancelBtn {
                background-color: white;
                color: #718096;
                border: 2px solid #cbd5e0;
            }
            QPushButton#cancelBtn:hover {
                background-color: #f7fafc;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(0)  # Manual spacing control
        
        # Title
        title = QLabel('Create New Account')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2d3748; font-size: 20px;")
        layout.addWidget(title)
        
        layout.addSpacing(30)
        
        # Username - label closer to input
        username_label = QLabel('Username:')
        username_label.setFont(QFont('Arial', 14, QFont.Bold))
        username_label.setStyleSheet("color: #2d3748;")
        layout.addWidget(username_label)
        
        layout.addSpacing(8)  # Small gap
        
        username_input = QLineEdit()
        username_input.setPlaceholderText('Choose a username')
        layout.addWidget(username_input)
        
        layout.addSpacing(18)  # Gap between groups
        
        # Password - label closer to input
        password_label = QLabel('Password (minimum 8 characters):')
        password_label.setFont(QFont('Arial', 14, QFont.Bold))
        password_label.setStyleSheet("color: #2d3748;")
        layout.addWidget(password_label)
        
        layout.addSpacing(8)  # Small gap
        
        password_input = QLineEdit()
        password_input.setPlaceholderText('Create a strong password')
        password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_input)
        
        layout.addSpacing(18)  # Gap between groups
        
        # Confirm password - label closer to input
        confirm_label = QLabel('Confirm Password:')
        confirm_label.setFont(QFont('Arial', 14, QFont.Bold))
        confirm_label.setStyleSheet("color: #2d3748;")
        layout.addWidget(confirm_label)
        
        layout.addSpacing(8)  # Small gap
        
        confirm_input = QLineEdit()
        confirm_input.setPlaceholderText('Re-enter your password')
        confirm_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(confirm_input)
        
        layout.addSpacing(18)  # Gap between groups
        
        # Role - label closer to dropdown
        role_label = QLabel('Role:')
        role_label.setFont(QFont('Arial', 14, QFont.Bold))
        role_label.setStyleSheet("color: #2d3748;")
        layout.addWidget(role_label)
        
        layout.addSpacing(8)  # Small gap
        
        role_combo = QComboBox()
        role_combo.addItems(['doctor', 'nurse', 'admin'])
        layout.addWidget(role_combo)
        
        layout.addSpacing(30)  # Gap before buttons
        
        # Buttons with better styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        register_btn = QPushButton('Register')
        register_btn.setObjectName('registerBtn')
        register_btn.setCursor(Qt.PointingHandCursor)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setObjectName('cancelBtn')
        cancel_btn.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(register_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        def register():
            username = username_input.text().strip()
            password = password_input.text()
            confirm = confirm_input.text()
            role = role_combo.currentText()
            
            if not username or not password:
                QMessageBox.warning(dialog, 'Error', 'All fields are required')
                return
            
            if password != confirm:
                QMessageBox.warning(dialog, 'Error', 'Passwords do not match')
                return
            
            success, message = self.auth_system.register_user(username, password, role)
            
            if success:
                QMessageBox.information(dialog, 'Success', message)
                dialog.accept()
            else:
                QMessageBox.critical(dialog, 'Error', message)
        
        register_btn.clicked.connect(register)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())