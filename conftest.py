"""Pytest configuration."""

import os

# Set Qt platform to offscreen mode to prevent GUI crashes in CI
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
