# 🤖 MLOps Pipeline for Deepfake Detection

Complete MLOps implementation for training, deploying, and monitoring deepfake detection models.

---

## 📋 Overview

This MLOps pipeline handles:
- ✅ **Data Management**: Videos and images
- ✅ **Model Training**: Automated training pipeline
- ✅ **Model Versioning**: Track and compare models
- ✅ **Deployment**: Automated deployment to production
- ✅ **Monitoring**: Real-time performance tracking
- ✅ **Retraining**: Automated retraining on new data

---

## 🚀 Quick Start

### 1. Prepare Training Data

```bash
# Place videos in mlops/data/videos/
# Or place images in mlops/data/images/

# Extract frames from videos (if needed)
python mlops/training/extract_frames.py
```

### 2. Train Model

```bash
# Train new model
python mlops/training/train_model.py --config mlops/training/config.yaml

# This will:
# - Load data from mlops/data/
# - Train EfficientNet-B0 model
# - Save model to mlops/registry/models/
# - Log metrics
```

### 3. Evaluate Model

```bash
# Evaluate model on test set
python mlops/evaluation/evaluate.py --model v1.0.0

# Compare with production model
python mlops/evaluation/evaluate.py --compare v1.0.0 v1.1.0
```

### 4. Deploy Model

```bash
# Deploy to staging
python mlops/deployment/deploy.py --version v1.0.0 --env staging

# Deploy to production
python mlops/deployment/deploy.py --version v1.0.0 --env production
```

### 5. Monitor Production

```bash
# Start monitoring
python mlops/monitoring/monitor.py

# View metrics
python mlops/monitoring/monitor.py --report
```

---

## 📊 Pipeline Workflow

```
1. DATA COLLECTION
   ├── Upload videos to mlops/data/videos/
   ├── Or upload images to mlops/data/images/
   └── Extract frames (if videos)
   
2. TRAINING
   ├── Load data
   ├── Train EfficientNet model
   ├── Validate on test set
   └── Save model with version
   
3. EVALUATION
   ├── Calculate metrics (accuracy, F1, AUC)
   ├── Compare with current production model
   └── Generate evaluation report
   
4. DEPLOYMENT
   ├── If metrics improved → Deploy to staging
   ├── Run integration tests
   └── If tests pass → Deploy to production
   
5. MONITORING
   ├── Track predictions in real-time
   ├── Monitor accuracy, latency
   ├── Detect data drift
   └── Alert if performance drops
   
6. RETRAINING
   ├── Collect misclassified examples
   ├── Add to training dataset
   └── Trigger automated retraining
```

---

## 🎯 Features

### Model Versioning
- Track all model versions
- Compare model performance
- Rollback to previous versions
- Store model metadata

### Automated Training
- Train on videos or images
- Hyperparameter tuning
- Early stopping
- Checkpoint saving

### Real-time Monitoring
- Track predictions
- Monitor accuracy
- Detect data drift
- Performance alerts

### A/B Testing
- Deploy multiple models
- Split traffic
- Compare performance
- Promote best model

---

## 📁 Folder Structure

```
mlops/
├── data/
│   ├── videos/              # Training videos (real & fake)
│   ├── images/              # Extracted frames or images
│   ├── train/               # Training data
│   ├── val/                 # Validation data
│   ├── test/                # Test data
│   └── metadata.json        # Dataset metadata
│
├── training/
│   ├── train_model.py       # Main training script
│   ├── extract_frames.py    # Extract frames from videos
│   ├── config.yaml          # Training configuration
│   ├── utils.py             # Training utilities
│   └── augmentation.py      # Data augmentation
│
├── evaluation/
│   ├── evaluate.py          # Model evaluation
│   ├── metrics.py           # Metrics calculation
│   └── reports/             # Evaluation reports
│
├── registry/
│   ├── model_registry.py    # Model versioning system
│   ├── models/              # Stored model versions
│   │   ├── v1.0.0/
│   │   ├── v1.1.0/
│   │   └── ...
│   └── metadata.json        # Model registry metadata
│
├── monitoring/
│   ├── monitor.py           # Production monitoring
│   ├── drift_detector.py    # Data drift detection
│   ├── logs/                # Monitoring logs
│   └── alerts/              # Alert configurations
│
├── deployment/
│   ├── deploy.py            # Deployment script
│   ├── rollback.py          # Rollback script
│   └── config/              # Deployment configs
│
└── README.md                # This file
```

---

## 🔧 Configuration

### Training Config (training/config.yaml)

```yaml
model:
  architecture: efficientnet-b0
  pretrained: true
  num_classes: 2

training:
  batch_size: 32
  epochs: 50
  learning_rate: 0.001
  optimizer: adam
  early_stopping: true
  patience: 5

data:
  train_split: 0.7
  val_split: 0.15
  test_split: 0.15
  augmentation: true
  image_size: 224

mlops:
  experiment_name: deepfake-detection
  model_version: v1.0.0
  track_metrics: true
```

---

## 📊 Metrics Tracked

### Training Metrics
- Loss (train & validation)
- Accuracy
- Precision
- Recall
- F1 Score
- AUC-ROC

### Production Metrics
- Prediction latency
- Throughput (predictions/sec)
- Error rate
- Confidence distribution
- Data drift score

---

## 🎯 Use Cases

### 1. Train New Model
```bash
python mlops/training/train_model.py \
    --data mlops/data/train \
    --version v1.0.0 \
    --epochs 50
```

### 2. Evaluate Model
```bash
python mlops/evaluation/evaluate.py \
    --model v1.0.0 \
    --test-data mlops/data/test
```

### 3. Compare Models
```bash
python mlops/evaluation/evaluate.py \
    --compare v1.0.0 v1.1.0
```

### 4. Deploy to Production
```bash
python mlops/deployment/deploy.py \
    --version v1.1.0 \
    --env production
```

### 5. Monitor Production
```bash
python mlops/monitoring/monitor.py \
    --dashboard
```

### 6. Rollback
```bash
python mlops/deployment/rollback.py \
    --to-version v1.0.0
```

---

## 🔄 Automated Retraining

The pipeline automatically retrains when:
- Performance drops below threshold
- Data drift detected
- New training data available
- Scheduled (weekly/monthly)

---

## 📈 Dashboard

Access monitoring dashboard:
```bash
python mlops/monitoring/dashboard.py
# Open http://localhost:8050
```

Shows:
- Real-time predictions
- Model performance
- Data drift
- Alerts

---

## 🚨 Alerts

Configured alerts for:
- Accuracy drop > 5%
- Latency > 500ms
- Error rate > 1%
- Data drift detected

---

## 🎉 Next Steps

1. ✅ Add training data to `mlops/data/`
2. ✅ Configure training in `mlops/training/config.yaml`
3. ✅ Train first model: `python mlops/training/train_model.py`
4. ✅ Evaluate model: `python mlops/evaluation/evaluate.py`
5. ✅ Deploy to production: `python mlops/deployment/deploy.py`
6. ✅ Monitor: `python mlops/monitoring/monitor.py`

**Your MLOps pipeline is ready!** 🚀
