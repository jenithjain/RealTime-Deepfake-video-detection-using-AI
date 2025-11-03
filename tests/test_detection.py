"""
Unit tests for deepfake detection logic
"""

import pytest
import sys
import os
import numpy as np
import cv2

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from deepfake_detection import DeepfakeDetector, TemporalTracker

def test_temporal_tracker_initialization():
    """Test TemporalTracker initializes correctly"""
    tracker = TemporalTracker()
    
    assert tracker.window_size == 60
    assert tracker.fake_count == 0
    assert tracker.real_count == 0
    assert tracker.current_verdict == 'REAL'
    assert len(tracker.score_history) == 0

def test_temporal_tracker_update():
    """Test TemporalTracker updates correctly"""
    tracker = TemporalTracker()
    
    # Add a fake probability
    tracker.update(0.7)  # High fake probability
    
    assert len(tracker.score_history) == 1
    assert tracker.fake_count == 1
    assert tracker.real_count == 0

def test_temporal_tracker_voting():
    """Test voting system works correctly"""
    tracker = TemporalTracker()
    
    # Add mostly fake predictions
    for _ in range(7):
        tracker.update(0.6)  # Fake
    
    for _ in range(3):
        tracker.update(0.2)  # Real
    
    # Should classify as FAKE (7 > 3)
    assert tracker.current_verdict == 'FAKE'
    assert tracker.fake_count == 7
    assert tracker.real_count == 3

def test_temporal_tracker_reset():
    """Test tracker reset works"""
    tracker = TemporalTracker()
    
    # Add some data
    tracker.update(0.7)
    tracker.update(0.8)
    
    # Reset
    tracker.reset()
    
    assert len(tracker.score_history) == 0
    assert tracker.fake_count == 0
    assert tracker.real_count == 0
    assert tracker.current_verdict == 'REAL'

def test_detector_initialization():
    """Test DeepfakeDetector initializes correctly"""
    detector = DeepfakeDetector(enable_gradcam=False)
    
    assert detector.temporal_tracker is not None
    assert detector.frame_count == 0
    assert detector.enable_gradcam == False

def test_detector_reset():
    """Test detector reset works"""
    detector = DeepfakeDetector()
    
    # Simulate some processing
    detector.frame_count = 10
    detector.temporal_tracker.update(0.5)
    
    # Reset
    detector.reset()
    
    assert detector.frame_count == 0
    assert len(detector.temporal_tracker.score_history) == 0

def test_temporal_average():
    """Test temporal average calculation"""
    tracker = TemporalTracker()
    
    # Add some scores
    scores = [0.3, 0.4, 0.5, 0.6, 0.7]
    for score in scores:
        tracker.update(score)
    
    avg = tracker.get_temporal_average()
    expected_avg = sum(scores) / len(scores)
    
    assert abs(avg - expected_avg) < 0.01  # Allow small floating point error

def test_stability_score():
    """Test stability score calculation"""
    tracker = TemporalTracker()
    
    # Add consistent scores (should be stable)
    for _ in range(20):
        tracker.update(0.5)
    
    stability = tracker.get_stability_score()
    
    # High stability (low variance)
    assert stability > 0.9

def test_voting_stats():
    """Test voting statistics"""
    tracker = TemporalTracker()
    
    # Add some predictions
    tracker.update(0.6)  # Fake
    tracker.update(0.3)  # Real
    tracker.update(0.7)  # Fake
    
    stats = tracker.get_voting_stats()
    
    assert stats['fake_count'] == 2
    assert stats['real_count'] == 1
    assert stats['total_frames'] == 3

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
