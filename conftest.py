"""
Root-level pytest configuration.
Allows running `pytest` from any directory in the project.
"""
import sys
import os

# Ensure each module's root is importable
sys.path.insert(0, os.path.dirname(__file__))
