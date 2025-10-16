"""
Flask Backend Server for Browser Extension
Handles frame analysis requests from the browser extension
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import base64
import torch
import torch.nn.functional as F

print("=" * 60)
print("🚀 Starting Backend Server...")
print("=" * 60)
print("Loading models (this may take 10-30 seconds)...")

from deepfake_detection import DeepfakeDetector, mtcnn, model, DEVICE
from face_detection import detect_bounding_box

print("✓ Models loaded successfully!")
print("=" * 60)

app = Flask(__name__)
# Enable CORS for browser extension with specific settings
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize detector
print("Initializing detector...")
detector = DeepfakeDetector(enable_gradcam=False)
print("✓ Detector initialized!")
print("=" * 60)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'device': DEVICE
    }), 200

@app.route('/reset', methods=['POST'])
def reset_detector():
    """Reset detector state (frame count and temporal tracker)"""
    try:
        detector.reset()
        return jsonify({
            'success': True,
            'message': 'Detector reset successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_frame():
    """
    Analyze a single frame for deepfake detection
    Expects: multipart/form-data with 'frame' field containing image
    Returns: JSON with detection results
    """
    try:
        # Check if frame is in request
        if 'frame' not in request.files:
            return jsonify({'error': 'No frame provided'}), 400
        
        file = request.files['frame']
        
        # Read image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Detect faces
        faces = detect_bounding_box(frame)
        
        if len(faces) == 0:
            return jsonify({
                'faces_detected': 0,
                'message': 'No faces detected in frame'
            }), 200
        
        # Analyze first face (can be extended to analyze all faces)
        x, y, w, h = faces[0]
        face_region = frame[y:y + h, x:x + w]
        
        # Get prediction
        fake_prob, real_score, gradcam = detector.analyze_face(face_region)
        
        # Debug logging
        print(f"[DEBUG] Raw fake_prob: {fake_prob}, real_score: {real_score}")
        
        if fake_prob is None:
            return jsonify({
                'faces_detected': len(faces),
                'error': 'Face analysis failed'
            }), 200
        
        # Update temporal tracker
        detector.temporal_tracker.update(fake_prob)
        confidence_level = detector.temporal_tracker.get_confidence_level()
        temporal_avg = detector.temporal_tracker.get_temporal_average()
        stability = detector.temporal_tracker.get_stability_score()
        
        # Increment frame count
        detector.frame_count += 1
        
        # Prepare response
        response = {
            'success': True,
            'faces_detected': len(faces),
            'fake_probability': float(fake_prob),
            'real_probability': float(1 - fake_prob),
            'confidence_level': confidence_level,
            'temporal_average': float(temporal_avg),
            'stability_score': float(stability),
            'frame_count': detector.frame_count,
            'face_bbox': {
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h)
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error analyzing frame: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get current detection statistics"""
    try:
        return jsonify({
            'frame_count': detector.frame_count,
            'temporal_average': float(detector.temporal_tracker.get_temporal_average()),
            'stability_score': float(detector.temporal_tracker.get_stability_score()),
            'confidence_level': detector.temporal_tracker.get_confidence_level(),
            'history_length': len(detector.temporal_tracker.score_history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎭 Deepfake Detection Backend Server")
    print("=" * 60)
    print(f"✓ Device: {DEVICE}")
    print(f"✓ Model loaded: {model is not None}")
    print(f"✓ Detector ready: {detector is not None}")
    print("\n🌐 Server running on http://localhost:5000")
    print("=" * 60)
    print("✅ READY! You can now use the extension.")
    print("=" * 60 + "\n")
    
    # Run Flask server
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
