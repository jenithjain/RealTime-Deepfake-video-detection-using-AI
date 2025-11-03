"""
Unit tests for face detection
"""

import pytest
import sys
import os
import numpy as np
import cv2

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from face_detection import detect_bounding_box

def create_test_image(width=640, height=480):
    """Create a simple test image"""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Add some color
    img[:, :] = (100, 150, 200)
    return img

def test_detect_bounding_box_empty_image():
    """Test face detection on empty image"""
    img = create_test_image()
    faces = detect_bounding_box(img)
    
    # Should return empty list (no faces in blank image)
    assert isinstance(faces, list)

def test_detect_bounding_box_none_input():
    """Test face detection with None input"""
    faces = detect_bounding_box(None)
    
    # Should return empty list
    assert faces == []

def test_detect_bounding_box_invalid_dimensions():
    """Test face detection with invalid dimensions"""
    # Too small image
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    faces = detect_bounding_box(img)
    
    # Should return empty list
    assert faces == []

def test_detect_bounding_box_grayscale():
    """Test face detection with grayscale image"""
    # Create grayscale image
    img = np.zeros((480, 640), dtype=np.uint8)
    img[:, :] = 128
    
    faces = detect_bounding_box(img)
    
    # Should handle grayscale without error
    assert isinstance(faces, list)

def test_face_box_format():
    """Test that face boxes have correct format"""
    img = create_test_image()
    faces = detect_bounding_box(img)
    
    # If faces detected, check format
    for face in faces:
        assert len(face) == 4  # (x, y, w, h)
        x, y, w, h = face
        assert isinstance(x, (int, np.integer))
        assert isinstance(y, (int, np.integer))
        assert isinstance(w, (int, np.integer))
        assert isinstance(h, (int, np.integer))
        assert w > 0 and h > 0  # Width and height should be positive

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
