# 🚀 DevOps Implementation Guide

Complete guide for deploying Real-Time Deepfake Detection with CI/CD, Docker, and MLOps.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Setup](#docker-setup)
4. [GitHub Actions CI/CD](#github-actions-cicd)
5. [GCP Cloud Run Deployment](#gcp-cloud-run-deployment)
6. [MLOps Automation](#mlops-automation)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### Required Accounts:
- ✅ GitHub account
- ✅ Google Cloud Platform (GCP) account with billing enabled
- ✅ Docker installed locally

### Required Tools:
```bash
# Check if installed
python --version  # Should be 3.9+
docker --version
git --version
```

---

## 🔧 Local Development Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/Real-Time-Deepfake-Detection.git
cd Real-Time-Deepfake-Detection
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Backend Locally
```bash
python backend_server.py
```

Visit: http://localhost:5000/health

---

## 🐳 Docker Setup

### Step 1: Build Docker Image
```bash
docker build -t deepfake-backend .
```

### Step 2: Run Container
```bash
docker run -p 5000:5000 deepfake-backend
```

### Step 3: Use Docker Compose (Recommended)
```bash
docker-compose up
```

This starts:
- Backend API on port 5000
- Automatic restart on code changes (development mode)

### Step 4: Test Docker Container
```bash
# Check health
curl http://localhost:5000/health

# Expected response:
# {"status":"healthy","model_loaded":true,"device":"cpu"}
```

---

## 🔄 GitHub Actions CI/CD

### Step 1: Set Up GitHub Secrets

Go to: `Settings → Secrets and variables → Actions → New repository secret`

Add these secrets:

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `GCP_PROJECT_ID` | Your GCP project ID | GCP Console → Project Info |
| `GCP_SA_KEY` | Service account JSON key | See below |
| `GCS_BUCKET` | Cloud Storage bucket name | Create in GCP Console |

### Step 2: Create GCP Service Account

```bash
# 1. Create service account
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions"

# 2. Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# 3. Create and download key
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 4. Copy contents of key.json to GCP_SA_KEY secret
cat key.json
```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add DevOps infrastructure"
git push origin main
```

### Step 4: Watch CI/CD Pipeline

1. Go to GitHub repository
2. Click "Actions" tab
3. Watch the pipeline run:
   - ✅ Run Tests
   - ✅ Build Docker Image
   - ✅ Deploy to Cloud Run

---

## ☁️ GCP Cloud Run Deployment

### Automatic Deployment (via GitHub Actions)

Every push to `main` branch automatically deploys to Cloud Run!

### Manual Deployment

```bash
# 1. Authenticate
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Build and push image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/deepfake-backend

# 4. Deploy to Cloud Run
gcloud run deploy deepfake-backend \
    --image gcr.io/YOUR_PROJECT_ID/deepfake-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2
```

### Get Service URL

```bash
gcloud run services describe deepfake-backend \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

---

## 🤖 MLOps Automation

### Automated Model Training

Training runs automatically every Sunday at 2 AM UTC.

### Manual Training Trigger

1. Go to GitHub → Actions
2. Select "MLOps - Model Training"
3. Click "Run workflow"
4. Fill in parameters:
   - Dataset source: `gcs` or `kaggle`
   - Epochs: `10`
5. Click "Run workflow"

### Model Versioning

Models are stored in GCS:
```
gs://YOUR_BUCKET/models/
├── v1/
│   ├── best_model.pth
│   ├── metrics.json
│   └── training_log.txt
├── v2/
│   └── ...
└── production/
    └── best_model.pth  (current production model)
```

---

## 📊 Monitoring & Logging

### View Logs

```bash
# Cloud Run logs
gcloud run services logs read deepfake-backend \
    --region us-central1 \
    --limit 50

# Follow logs in real-time
gcloud run services logs tail deepfake-backend \
    --region us-central1
```

### GCP Console Monitoring

1. Go to: https://console.cloud.google.com/run
2. Click on `deepfake-backend`
3. View:
   - Request count
   - Response time
   - Error rate
   - CPU/Memory usage

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

View coverage report: `htmlcov/index.html`

---

## 🔧 Troubleshooting

### Issue: Docker build fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t deepfake-backend .
```

### Issue: Tests fail locally

**Solution:**
```bash
# Ensure all dependencies installed
pip install -r requirements.txt
pip install pytest

# Run tests with verbose output
pytest tests/ -v -s
```

### Issue: GitHub Actions deployment fails

**Solution:**
1. Check GitHub Secrets are set correctly
2. Verify GCP service account has correct permissions
3. Check Cloud Run quotas in GCP Console

### Issue: Cloud Run service crashes

**Solution:**
```bash
# Check logs
gcloud run services logs read deepfake-backend --region us-central1

# Common fixes:
# 1. Increase memory: --memory 4Gi
# 2. Increase timeout: --timeout 600
# 3. Check model weights are accessible
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GCP Cloud Run Documentation](https://cloud.google.com/run/docs)
- [pytest Documentation](https://docs.pytest.org/)

---

## ✅ Checklist

Before deploying to production:

- [ ] All tests passing locally
- [ ] Docker image builds successfully
- [ ] GitHub secrets configured
- [ ] GCP service account created
- [ ] Cloud Run service deployed
- [ ] Extension updated with production URL
- [ ] Monitoring dashboard set up
- [ ] Documentation updated

---

**Need help?** Check the troubleshooting section or create an issue on GitHub.
