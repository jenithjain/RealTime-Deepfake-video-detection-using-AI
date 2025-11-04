# 🚀 MLOps Quick Start Guide

Get started with the MLOps pipeline in 5 minutes!

---

## 📁 Step 1: Prepare Your Data

### Option A: Using Images

```bash
# Create data structure
mlops/data/train/
├── real/
│   ├── real_001.jpg
│   ├── real_002.jpg
│   └── ...
└── fake/
    ├── fake_001.jpg
    ├── fake_002.jpg
    └── ...
```

### Option B: Using Videos

```bash
# Create data structure
mlops/data/videos/
├── real/
│   ├── real_video_001.mp4
│   ├── real_video_002.mp4
│   └── ...
└── fake/
    ├── fake_video_001.mp4
    ├── fake_video_002.mp4
    └── ...
```

**Note:** The training script will automatically extract frames from videos!

---

## 🎯 Step 2: Configure Training

Edit `mlops/training/config.yaml`:

```yaml
data:
  mode: images  # Change to 'videos' if using videos
  
training:
  batch_size: 32
  epochs: 50
  learning_rate: 0.001
```

---

## 🏋️ Step 3: Train Model

```bash
# Activate venv
.\venv\Scripts\activate

# Train model
python mlops/training/train_model.py \
    --data mlops/data/train \
    --version v1.0.0 \
    --epochs 50
```

**Output:**
```
Using device: cuda
Loaded 1000 images (500 real, 500 fake)
🚀 Starting training for 50 epochs...
Epoch 1/50: Train Loss: 0.4523, Train Acc: 78.50%, Val Loss: 0.3821, Val Acc: 82.30%
...
✅ Training complete!
   Best validation accuracy: 95.20%
   Model saved to: mlops/registry/models/v1.0.0
```

---

## 📊 Step 4: Evaluate Model

```bash
# View model info
python mlops/registry/model_registry.py

# Output:
# 📋 Model Registry
# Production: None
# Staging: None
# Registered models: 1
```

---

## 🚀 Step 5: Deploy Model

### Deploy to Staging

```bash
python mlops/deployment/deploy.py \
    --version v1.0.0 \
    --env staging
```

### Deploy to Production

```bash
python mlops/deployment/deploy.py \
    --version v1.0.0 \
    --env production
```

**Output:**
```
✅ Model v1.0.0 deployed to production
   Source: mlops/registry/models/v1.0.0/model.pth
   Target: weights/best_model.pth
   Metrics: {'accuracy': 0.952, 'f1_score': 0.948}

🔄 Restart backend server to load new model:
   python backend_server.py
```

---

## 📈 Step 6: Monitor Production

```bash
# Start backend with monitoring
python backend_server.py

# In another terminal, view monitoring report
python mlops/monitoring/monitor.py

# Output:
# ============================================================
# 📊 PRODUCTION MONITORING REPORT
# ============================================================
# 
# 📈 Overall Metrics:
#   Total Predictions: 1523
#   Fake Detected: 742
#   Real Detected: 781
#   Average Confidence: 94.50%
#   Average Latency: 125.30ms
#   Errors: 0
# 
# ✅ No active alerts
```

---

## 🔄 Step 7: Retrain & Update

When you have new data or want to improve the model:

```bash
# 1. Add new data to mlops/data/train/

# 2. Train new version
python mlops/training/train_model.py \
    --version v1.1.0 \
    --epochs 50

# 3. Compare with production
python -c "
from mlops.registry.model_registry import ModelRegistry
registry = ModelRegistry()
registry.compare_models('v1.0.0', 'v1.1.0')
"

# 4. If better, deploy
python mlops/deployment/deploy.py \
    --version v1.1.0 \
    --env production
```

---

## 🎯 Common Commands

### List All Models
```bash
python -c "
from mlops.registry.model_registry import ModelRegistry
registry = ModelRegistry()
for model in registry.list_models():
    print(f\"{model['version']}: {model['metrics']}\")
"
```

### Rollback to Previous Version
```bash
python mlops/deployment/deploy.py \
    --version v1.0.0 \
    --rollback
```

### View Monitoring Metrics
```bash
python mlops/monitoring/monitor.py
```

---

## 📊 Full Workflow Example

```bash
# 1. Prepare data
mkdir -p mlops/data/train/real mlops/data/train/fake
# Add your images...

# 2. Train
python mlops/training/train_model.py --version v1.0.0

# 3. Deploy
python mlops/deployment/deploy.py --version v1.0.0 --env production

# 4. Start backend
python backend_server.py

# 5. Monitor
python mlops/monitoring/monitor.py
```

---

## ✅ You're Done!

Your MLOps pipeline is now running:
- ✅ Model trained and versioned
- ✅ Deployed to production
- ✅ Monitoring active
- ✅ Ready for retraining

**Next:** Integrate with CI/CD for automated training and deployment!

---

## 🎉 Advanced Features

### A/B Testing
Deploy multiple versions and compare:
```bash
# Deploy v1.0.0 to 50% traffic
# Deploy v1.1.0 to 50% traffic
# Compare metrics after 24 hours
```

### Automated Retraining
Set up cron job or GitHub Actions:
```yaml
# .github/workflows/retrain.yml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  
jobs:
  retrain:
    runs-on: ubuntu-latest
    steps:
      - name: Train model
        run: python mlops/training/train_model.py --version v$(date +%Y%m%d)
```

---

**Your MLOps pipeline is production-ready!** 🚀
