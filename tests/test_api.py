"""
Unit tests for Flask API endpoints
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_server import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test /health endpoint returns OK"""
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'model_loaded' in data
    assert 'device' in data

def test_health_endpoint_structure(client):
    """Test /health endpoint response structure"""
    response = client.get('/health')
    data = response.get_json()
    
    # Check all required fields exist
    required_fields = ['status', 'model_loaded', 'device']
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

def test_stats_endpoint(client):
    """Test /stats endpoint"""
    response = client.get('/stats')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'frame_count' in data
    assert 'temporal_average' in data
    assert 'stability_score' in data

def test_reset_endpoint(client):
    """Test /reset endpoint"""
    response = client.post('/reset')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'message' in data

def test_analyze_endpoint_no_file(client):
    """Test /analyze endpoint without file"""
    response = client.post('/analyze')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_cors_headers(client):
    """Test CORS headers are present"""
    response = client.get('/health')
    
    # Check CORS headers
    assert 'Access-Control-Allow-Origin' in response.headers

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
