# 🏗️ Real-Time Deepfake Detection - Project Architecture

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Directory Structure](#directory-structure)
5. [Technology Stack](#technology-stack)
6. [Module Descriptions](#module-descriptions)
7. [Communication Flow](#communication-flow)
8. [Model Architecture](#model-architecture)

---

## 🎯 System Overview

**Project Name:** Real-Time Deepfake Detection Browser Extension  
**Purpose:** Detect deepfake videos in real-time while browsing (YouTube, social media, etc.)  
**Architecture Type:** Client-Server with Browser Extension

### High-Level Components:
```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         BROWSER EXTENSION (Chrome/Edge)              │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │  │
│  │  │   Popup    │  │  Content   │  │  Background  │  │  │
│  │  │    UI      │  │   Script   │  │    Script    │  │  │
│  │  └────────────┘  └────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕ HTTP                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              OVERLAY (Iframe)                        │  │
│  │         Real-time Results Display                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND SERVER (Flask)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Flask REST API                          │  │
│  │    /health  |  /analyze                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Deepfake Detection Engine                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │  │
│  │  │   Face     │  │  EfficientNet│ │   Temporal   │  │  │
│  │  │ Detection  │  │     Model    │  │   Tracker    │  │  │
│  │  └────────────┘  └────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  TRAINED MODEL WEIGHTS                      │
│              weights/best_model.pth                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Architecture

### 1. **Browser Extension Layer**

#### A. **Popup UI** (`extension/popup.html`, `popup.js`, `popup.css`)
- **Purpose:** User interface for controlling detection
- **Responsibilities:**
  - Start/Stop detection
  - Display real-time results
  - Configure settings (backend URL, interval)
  - Test backend connectivity
  - Show metrics (accuracy, confidence, frames analyzed)

#### B. **Content Script** (`extension/content.js`)
- **Purpose:** Injected into web pages to capture video frames
- **Responsibilities:**
  - Detect `<video>` elements on the page
  - Capture video frames using Canvas API
  - Send frames to backend for analysis
  - Create and manage overlay iframe
  - Handle video state (playing, paused, etc.)
  - Communicate with background script

#### C. **Background Script** (`extension/background.js`)
- **Purpose:** Service worker managing extension lifecycle
- **Responsibilities:**
  - Route messages between popup and content script
  - Manage detection state across tabs
  - Handle extension icon and badge
  - Coordinate backend health checks
  - Store persistent settings

#### D. **Overlay UI** (`extension/overlay.html`, `overlay.css`)
- **Purpose:** Real-time results display on video
- **Responsibilities:**
  - Show detection results (REAL/FAKE)
  - Display confidence scores
  - Show temporal average
  - Visualize stability metrics
  - Provide close/stop controls

### 2. **Backend Server Layer**

#### A. **Flask API Server** (`backend_server.py`)
- **Purpose:** REST API for frame analysis
- **Endpoints:**
  - `GET /health` - Health check and model status
  - `POST /analyze` - Analyze video frame for deepfakes
- **Responsibilities:**
  - Receive image frames from extension
  - Coordinate detection pipeline
  - Return analysis results as JSON
  - Handle CORS for browser requests
  - Manage model lifecycle

#### B. **Deepfake Detection Engine** (`deepfake_detection.py`)
- **Purpose:** Core AI detection logic
- **Components:**
  - **DeepfakeDetector Class:**
    - Main detection orchestrator
    - Manages 3-layer detection system
    - Handles preprocessing and inference
  - **TemporalTracker Class:**
    - Tracks predictions across frames
    - Calculates temporal averages
    - Determines confidence levels
    - Manages stability scores
  - **Model Inference:**
    - EfficientNet-B0 neural network
    - Sigmoid activation for probabilities
    - GradCAM visualization (optional)

#### C. **Face Detection Module** (`face_detection.py`)
- **Purpose:** Detect and extract faces from frames
- **Technology:** OpenCV Haar Cascade
- **Responsibilities:**
  - Locate faces in video frames
  - Return bounding box coordinates
  - Handle multiple faces (uses first detected)

### 3. **AI Model Layer**

#### A. **EfficientNet-B0 Model**
- **Architecture:** Convolutional Neural Network
- **Input:** 224x224 RGB face images
- **Output:** Single probability (0-1) for fake likelihood
- **Pretrained:** ImageNet weights
- **Fine-tuned:** On deepfake datasets

#### B. **Model Weights** (`weights/best_model.pth`)
- **Format:** PyTorch state dictionary
- **Size:** ~20MB
- **Contains:** Trained parameters for all layers

### 4. **Training Pipeline**

#### A. **Training Script** (`train.json` - Jupyter Notebook)
- **Purpose:** Fine-tune model on custom datasets
- **Features:**
  - Data augmentation
  - Class balancing
  - Early stopping
  - Learning rate scheduling
  - Validation metrics

#### B. **Dataset Structure**
```
train/
├── fake/  (80,080 images)
└── real/  (85,517 images)

test/
├── fake/  (3,398 images)
└── real/  (3,370 images)

valid/
├── fake/
└── real/
```

---

## 🔄 Data Flow

### **Detection Flow (Step-by-Step):**

```
1. USER INTERACTION
   └─> User clicks "Start Detection" in popup
       │
       ├─> popup.js sends message to background.js
       │
2. BACKGROUND COORDINATION
   └─> background.js validates backend health
       │
       ├─> Sends "startDetection" message to content.js
       │
3. FRAME CAPTURE (Content Script)
   └─> content.js finds <video> element
       │
       ├─> Captures frame using Canvas API (every 1 second)
       │
       ├─> Converts to PNG data URL
       │
       ├─> Converts to Blob
       │
4. BACKEND REQUEST
   └─> content.js sends POST to /analyze endpoint
       │
       ├─> FormData with image blob
       │
5. BACKEND PROCESSING
   └─> backend_server.py receives frame
       │
       ├─> Decodes image with OpenCV
       │
       ├─> face_detection.py detects faces
       │   └─> Returns bounding box [x, y, w, h]
       │
       ├─> Extracts face region
       │
       ├─> deepfake_detection.py analyzes face
       │   │
       │   ├─> Preprocesses face (resize, normalize)
       │   │
       │   ├─> EfficientNet-B0 inference
       │   │   └─> Returns logit
       │   │
       │   ├─> Sigmoid activation
       │   │   └─> fake_probability (0-1)
       │   │
       │   ├─> TemporalTracker updates
       │   │   ├─> Adds to rolling window (30 frames)
       │   │   ├─> Calculates temporal average
       │   │   ├─> Computes stability score
       │   │   └─> Determines confidence level
       │   │
6. RESPONSE
   └─> backend_server.py returns JSON:
       {
         "fake_probability": 0.249,
         "real_probability": 0.751,
         "confidence_level": "REAL",
         "temporal_average": 0.290,
         "stability_score": 0.945,
         "faces_detected": 1,
         "frame_count": 31
       }
       │
7. DISPLAY RESULTS
   └─> content.js receives response
       │
       ├─> Updates overlay iframe
       │   └─> Shows REAL/FAKE, confidence, metrics
       │
       ├─> Sends to background.js
       │   └─> Forwards to popup.js
       │       └─> Updates popup UI
       │
8. REPEAT
   └─> Loop continues every 1 second until stopped
```

---

## 📁 Directory Structure

```
Realtime-Deepfake-Detection/
│
├── extension/                      # Browser Extension
│   ├── manifest.json              # Extension configuration
│   ├── popup.html                 # Popup UI structure
│   ├── popup.js                   # Popup logic
│   ├── popup.css                  # Popup styling
│   ├── content.js                 # Content script (frame capture)
│   ├── background.js              # Background service worker
│   ├── overlay.html               # Results overlay structure
│   ├── overlay.css                # Overlay styling
│   └── icons/                     # Extension icons
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
│
├── weights/                        # Model Weights
│   └── best_model.pth             # Trained EfficientNet-B0
│
├── train/                          # Training Dataset
│   ├── fake/                      # 80,080 fake images
│   └── real/                      # 85,517 real images
│
├── test/                           # Test Dataset
│   ├── fake/                      # 3,398 fake images
│   └── real/                      # 3,370 real images
│
├── valid/                          # Validation Dataset
│   ├── fake/
│   └── real/
│
├── backend_server.py               # Flask REST API server
├── deepfake_detection.py           # Core detection engine
├── face_detection.py               # Face detection module
├── train.json                      # Training notebook (Jupyter)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── PROJECT_ARCHITECTURE.md         # This file
```

---

## 🛠️ Technology Stack

### **Frontend (Browser Extension)**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Extension Framework | Chrome Extension Manifest V3 | Browser integration |
| UI | HTML5, CSS3, JavaScript (ES6+) | User interface |
| Video Capture | Canvas API | Frame extraction |
| Communication | Chrome Extension APIs | Message passing |
| HTTP Client | Fetch API | Backend requests |

### **Backend (Server)**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Flask 3.1.3 | REST API server |
| CORS | Flask-CORS | Cross-origin requests |
| Image Processing | OpenCV (cv2) | Frame decoding, face detection |
| Face Detection | Haar Cascade Classifier | Locate faces |
| Deep Learning | PyTorch 2.5.1 | Neural network inference |
| Model | EfficientNet-B0 | Deepfake classification |
| Image Utils | PIL/Pillow | Image manipulation |
| Numerical | NumPy | Array operations |

### **AI/ML**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | PyTorch | Deep learning |
| Architecture | EfficientNet-B0 | CNN backbone |
| Pretrained | ImageNet | Transfer learning |
| Activation | Sigmoid | Probability output |
| Visualization | GradCAM (optional) | Explainability |

### **Training**
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Notebook | Jupyter | Interactive training |
| Data Loading | torchvision.datasets | Dataset management |
| Augmentation | torchvision.transforms | Data preprocessing |
| Optimization | Adam/SGD | Weight updates |
| Scheduler | ReduceLROnPlateau | Learning rate adjustment |
| Metrics | scikit-learn | Evaluation |

---

## 📦 Module Descriptions

### **1. Extension Modules**

#### **manifest.json**
```json
{
  "manifest_version": 3,
  "permissions": ["storage", "tabs", "scripting"],
  "host_permissions": ["http://localhost:5000/*"],
  "content_scripts": [auto-inject on all pages],
  "background": {service_worker},
  "action": {popup}
}
```

#### **popup.js**
- **Functions:**
  - `startDetection()` - Initiates frame capture
  - `stopDetection()` - Halts detection
  - `testBackend()` - Checks backend health
  - `testContentScript()` - Verifies content script
  - `updateResults()` - Refreshes UI with metrics

#### **content.js**
- **State Management:**
  - `window.deepfakeDetection` - Global state object
  - `overlayIframe` - Overlay element reference
  - `captureInterval` - Timer for frame capture
  - `isCapturing` - Detection status flag

- **Functions:**
  - `captureTab()` - Captures video frame to canvas
  - `analyzeFrame()` - Sends frame to backend
  - `startDetection()` - Begins capture loop
  - `stopDetection()` - Ends capture loop
  - `createOverlay()` - Injects results overlay
  - `updateOverlay()` - Updates overlay with results

#### **background.js**
- **Functions:**
  - `handleStartDetection()` - Validates and starts detection
  - `handleStopDetection()` - Stops detection
  - Message routing between popup and content script

### **2. Backend Modules**

#### **backend_server.py**
- **Routes:**
  - `GET /health` - Returns model status
    ```json
    {
      "status": "healthy",
      "model_loaded": true,
      "device": "cpu"
    }
    ```
  
  - `POST /analyze` - Analyzes frame
    ```json
    {
      "fake_probability": 0.249,
      "real_probability": 0.751,
      "confidence_level": "REAL",
      "temporal_average": 0.290,
      "stability_score": 0.945,
      "faces_detected": 1,
      "frame_count": 31,
      "face_bbox": {"x": 1514, "y": 431, "width": 752, "height": 752}
    }
    ```

#### **deepfake_detection.py**

**Classes:**

1. **TemporalTracker**
   - **Attributes:**
     - `score_history` - Deque of recent predictions
     - `window_size` - Number of frames to track (60)
     - `high_confidence_threshold` - Threshold for alerts (0.75)
   
   - **Methods:**
     - `update(score)` - Add new prediction
     - `get_temporal_average()` - Calculate mean
     - `get_stability_score()` - Calculate consistency
     - `get_confidence_level()` - Classify as REAL/FAKE
     - `should_trigger_forensic_analysis()` - Alert logic

2. **DeepfakeDetector**
   - **Attributes:**
     - `temporal_tracker` - TemporalTracker instance
     - `enable_gradcam` - GradCAM visualization flag
     - `frame_count` - Total frames processed
   
   - **Methods:**
     - `preprocess_face(face_img)` - Enhance face quality
     - `analyze_face(face_img)` - Run inference
     - `get_box_color(confidence)` - Color coding
     - `draw_detection_overlay()` - Visualization
     - `process_frame()` - Full pipeline

#### **face_detection.py**
- **Function:**
  - `detect_bounding_box(img)` - Returns list of [x, y, w, h]
- **Classifier:**
  - Haar Cascade frontal face detector
  - Parameters: `scaleFactor=1.1`, `minNeighbors=5`

---

## 🔗 Communication Flow

### **Message Passing (Extension)**

```
Popup ←→ Background ←→ Content Script
  │         │              │
  │         │              └─> Captures frames
  │         │              └─> Sends to backend
  │         │              └─> Updates overlay
  │         │
  │         └─> Routes messages
  │         └─> Manages state
  │         └─> Validates backend
  │
  └─> User interface
  └─> Settings
  └─> Results display
```

### **HTTP Communication**

```
Extension (Content Script)
    │
    │ POST /analyze
    │ Content-Type: multipart/form-data
    │ Body: { frame: <image blob> }
    ↓
Backend Server (Flask)
    │
    │ Process frame
    │ Run detection
    ↓
    │ JSON Response
    │ {
    │   fake_probability: 0.249,
    │   confidence_level: "REAL",
    │   ...
    │ }
    ↓
Extension (Content Script)
    │
    └─> Update UI
```

---

## 🧠 Model Architecture

### **EfficientNet-B0 Structure**

```
Input: 224×224×3 RGB Image
    ↓
┌─────────────────────────────────────┐
│  Stem (Conv + BatchNorm + Swish)    │
│  Output: 112×112×32                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  MBConv Blocks (Mobile Inverted     │
│  Residual Bottleneck)               │
│  - 16 blocks total                  │
│  - Squeeze-and-Excitation           │
│  - Depthwise separable convolutions │
│  Output: 7×7×1280                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Global Average Pooling             │
│  Output: 1280                       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Fully Connected Layer              │
│  Output: 1 (logit)                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Sigmoid Activation                 │
│  Output: Probability (0-1)          │
└─────────────────────────────────────┘
    ↓
Output: Fake Probability
```

### **Preprocessing Pipeline**

```
Raw Face Image
    ↓
Resize to 224×224
    ↓
Convert to RGB
    ↓
Normalize with ImageNet stats
  mean = [0.485, 0.456, 0.406]
  std  = [0.229, 0.224, 0.225]
    ↓
Convert to Tensor
    ↓
Add Batch Dimension
    ↓
Move to Device (CPU/GPU)
    ↓
Ready for Inference
```

### **Temporal Smoothing**

```
Frame 1: fake_prob = 0.25
Frame 2: fake_prob = 0.23
Frame 3: fake_prob = 0.27
...
Frame 30: fake_prob = 0.24
    ↓
Temporal Average = mean([0.25, 0.23, 0.27, ..., 0.24])
                 = 0.29
    ↓
Stability Score = 1 - (std_dev / mean)
                = 0.945
    ↓
Confidence Level = "REAL" (if avg < 0.5)
                 = "FAKE" (if avg >= 0.5)
```

---

## 🔐 Security & Performance

### **Security Considerations**
- **CORS:** Enabled for localhost only
- **Input Validation:** Image format and size checks
- **Error Handling:** Try-catch blocks prevent crashes
- **Permissions:** Minimal extension permissions

### **Performance Optimizations**
- **Frame Rate:** 1 FPS (configurable)
- **Batch Processing:** Single frame per request
- **Model Loading:** Once at startup
- **Caching:** Temporal tracker reduces jitter
- **Async Processing:** Non-blocking operations

---

## 📊 Metrics & Monitoring

### **Real-Time Metrics**
- **Fake Probability:** 0-1 (model output)
- **Real Probability:** 1 - fake_probability
- **Temporal Average:** Rolling mean of 30 frames
- **Stability Score:** Prediction consistency
- **Frames Analyzed:** Total count
- **Confidence Level:** REAL or FAKE classification

### **Model Evaluation Metrics**
- **Accuracy:** Correct predictions / Total
- **Precision:** True Positives / (TP + FP)
- **Recall:** True Positives / (TP + FN)
- **F1 Score:** Harmonic mean of precision/recall
- **AUC-ROC:** Area under ROC curve

---

## 🎯 Use Cases

1. **Real-Time Video Monitoring**
   - User watches YouTube video
   - Extension analyzes in background
   - Alerts if deepfake detected

2. **Social Media Verification**
   - User scrolls through Facebook/Twitter
   - Extension checks video posts
   - Provides authenticity scores

3. **News Verification**
   - User watches news clips
   - Extension validates video authenticity
   - Helps combat misinformation

---

## 🔄 Future Enhancements

### **Planned Features**
- Multi-face detection and tracking
- Video-level aggregation
- Forensic analysis (Layer 3)
- Export detection reports
- Cloud deployment
- Mobile app version

### **Model Improvements**
- Larger models (EfficientNet-B4, B7)
- Ensemble methods
- Attention mechanisms
- Temporal CNNs for video sequences

---

## 📝 Configuration Files

### **Extension Configuration** (`manifest.json`)
- Permissions and host access
- Content script injection rules
- Background service worker
- Web accessible resources

### **Python Dependencies** (`requirements.txt`)
```
torch==2.5.1
torchvision
efficientnet-pytorch
opencv-python
flask==3.1.3
flask-cors
pillow
numpy
facenet-pytorch
pytorch-grad-cam
```

---

## 🎓 Key Concepts

### **Transfer Learning**
- Start with ImageNet pretrained weights
- Fine-tune on deepfake datasets
- Faster convergence, better accuracy

### **Temporal Smoothing**
- Average predictions across frames
- Reduces false positives
- More stable results

### **Three-Layer Detection**
1. **Layer 1:** Real-time frame analysis
2. **Layer 2:** Temporal tracking
3. **Layer 3:** Forensic analysis (future)

---

This architecture document provides a complete overview of the system for creating architecture diagrams, documentation, or presentations.
