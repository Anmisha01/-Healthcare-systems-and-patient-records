"""
Healthcare System - Main Entry Point
Secure patient records management with encryption and authentication
"""
import sys
import os
import traceback

# Debug output
print("🏥 Healthcare System Starting...")
print(f"Python: {sys.version}")
print(f"Working Directory: {os.getcwd()}")
print(f"Display: {os.environ.get('DISPLAY', 'NOT SET')}")
print("-" * 50)

# Import PyQt5 with error handling
try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt
    print("✓ PyQt5 imported successfully")
except ImportError as e:
    print(f"✗ ERROR: PyQt5 not found!")
    print(f"  {e}")
    print("\nInstall PyQt5:")
    print("  sudo pacman -S python-pyqt5")
    print("  OR")
    print("  pip install PyQt5")
    sys.exit(1)

# Import application modules
try:
    from login_ui import LoginWindow
    print("✓ login_ui imported successfully")
except ImportError as e:
    print(f"✗ ERROR: Cannot import LoginWindow!")
    print(f"  {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from main_ui import MainWindow
    print("✓ main_ui imported successfully")
except ImportError as e:
    print(f"✗ ERROR: Cannot import MainWindow!")
    print(f"  {e}")
    traceback.print_exc()
    sys.exit(1)

print("-" * 50)


class HealthcareApp:
    """Main application controller"""
    
    def __init__(self):
        print("Initializing application...")
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Healthcare System")
        self.login_window = None
        self.main_window = None
        print("✓ QApplication created")
        
    def start(self):
        """Start the application"""
        try:
            print("Creating login window...")
            self.show_login()
            print("✓ Login window created and shown")
            print("\n" + "="*50)
            print("🚀 Application is running!")
            print("   If you don't see a window, check:")
            print("   1. DISPLAY environment variable")
            print("   2. X11/Wayland is running")
            print("   3. No errors above")
            print("="*50 + "\n")
            return self.app.exec_()
        except Exception as e:
            print(f"\n✗ FATAL ERROR in start():")
            print(f"  {e}")
            traceback.print_exc()
            return 1
    
    def show_login(self):
        """Show login window"""
        try:
            self.login_window = LoginWindow()
            self.login_window.login_successful.connect(self.on_login_success)
            self.login_window.show()
            
            # Only try to raise/activate on X11, not Wayland
            if os.environ.get('XDG_SESSION_TYPE') != 'wayland':
                self.login_window.raise_()
                self.login_window.activateWindow()
            
        except Exception as e:
            print(f"✗ ERROR creating login window:")
            print(f"  {e}")
            traceback.print_exc()
            raise
    
    def on_login_success(self, session_token, username):
        """Handle successful login"""
        try:
            print(f"\n✓ Login successful: {username}")
            
            # Hide (don't close) login window to avoid signal issues
            if self.login_window:
                self.login_window.hide()
            
            # Show main window
            print("Opening main window...")
            self.main_window = MainWindow(session_token, username)
            
            # Connect logout to show login again
            MainWindow.logout_requested = self.on_logout
            
            self.main_window.show()
            
            # Only try to raise/activate on X11, not Wayland
            if os.environ.get('XDG_SESSION_TYPE') != 'wayland':
                self.main_window.raise_()
                self.main_window.activateWindow()
            
            print("✓ Main window opened")
            
            # Now safely close and cleanup login window after main window is shown
            if self.login_window:
                self.login_window.close()
                self.login_window.deleteLater()  # Schedule for deletion
                self.login_window = None
            
        except Exception as e:
            print(f"✗ ERROR in on_login_success:")
            print(f"  {e}")
            traceback.print_exc()
    
    def on_logout(self):
        """Handle logout - return to login screen"""
        try:
            print("\n✓ Handling logout - returning to login screen")
            
            # Safely close main window
            if self.main_window:
                self.main_window.hide()
                self.main_window.deleteLater()  # Schedule for deletion
                self.main_window = None
            
            # Show login window again
            self.show_login()
            
        except Exception as e:
            print(f"✗ ERROR in on_logout:")
            print(f"  {e}")
            traceback.print_exc()


def main():
    """Main entry point"""
    try:
        print("Starting Healthcare App...")
        app = HealthcareApp()
        exit_code = app.start()
        print(f"\nApplication exited with code: {exit_code}")
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n✓ Application interrupted by user (Ctrl+C)")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ FATAL ERROR:")
        print(f"  {e}")
        traceback.print_exc()
        print("\nRun 'python diagnose.py' for detailed diagnostics")
        sys.exit(1)


if __name__ == '__main__':
    main()