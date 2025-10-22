"""
Root conftest.py to configure pytest and paths.
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))