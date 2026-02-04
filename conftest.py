"""Pytest configuration and fixtures."""
import sys
import os

# Set Qt platform to offscreen mode before any PyQt5 imports
if not os.environ.get('QT_QPA_PLATFORM'):
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'


def pytest_configure(config):
    """Configure pytest and set up mocking for PyQt5."""
    # Mock QApplication to prevent GUI initialization errors in CI
    try:
        from unittest.mock import MagicMock, patch
        from PyQt5 import QtWidgets
        
        # Monkeypatch QApplication to not initialize display
        original_init = QtWidgets.QApplication.__init__
        
        def mock_init(self, argv=None):
            """Mock QApplication initialization."""
            # Skip actual initialization
            pass
        
        QtWidgets.QApplication.__init__ = mock_init
    except Exception:
        pass


