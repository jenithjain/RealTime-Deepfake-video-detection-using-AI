"""
Pytest configuration and fixtures
"""

import pytest
import os
import sys

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory"""
    return os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    # Set environment variables for testing
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DEVICE'] = 'cpu'
    
    yield
    
    # Cleanup after tests
    pass
