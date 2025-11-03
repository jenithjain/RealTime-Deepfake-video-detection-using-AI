# 🚀 Quick Setup Instructions

Follow these steps to get your DevOps pipeline running in **30 minutes**.

---

## ⚡ Quick Start (5 Steps)

### Step 1: Test Locally with Docker (5 minutes)

```bash
# Build and run
docker-compose up

# In another terminal, test
curl http://localhost:5000/health
```

**Expected output:**
```json
{"status":"healthy","model_loaded":true,"device":"cpu"}
```

✅ If this works, your Docker setup is correct!

---

### Step 2: Run Tests (5 minutes)

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/ -v
```

**Expected output:**
```
tests/test_api.py::test_health_endpoint PASSED
tests/test_api.py::test_stats_endpoint PASSED
tests/test_detection.py::test_temporal_tracker_initialization PASSED
...
========== 15 passed in 5.23s ==========
```

✅ If tests pass, your code is working!

---

### Step 3: Set Up GCP (10 minutes)

#### 3.1 Create GCP Project (if needed)
1. Go to: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: `deepfake-detection`
4. Click "Create"

#### 3.2 Enable Required APIs
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com
```

#### 3.3 Create Service Account
```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Create service account
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions" \
    --project=$PROJECT_ID

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Create key
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com

# Display key (copy this for GitHub)
cat key.json
```

✅ Save the `key.json` contents - you'll need it for GitHub!

---

### Step 4: Configure GitHub Secrets (5 minutes)

1. Go to your GitHub repository
2. Click: `Settings` → `Secrets and variables` → `Actions`
3. Click: `New repository secret`

Add these 3 secrets:

| Secret Name | Value | Where to Find |
|------------|-------|---------------|
| `GCP_PROJECT_ID` | `your-project-id` | From Step 3.1 |
| `GCP_SA_KEY` | Contents of `key.json` | From Step 3.3 |
| `GCS_BUCKET` | `deepfake-models-bucket` | Create in GCP Console |

#### Create GCS Bucket:
```bash
gsutil mb -p $PROJECT_ID -l us-central1 gs://deepfake-models-bucket
```

✅ Secrets configured!

---

### Step 5: Deploy! (5 minutes)

```bash
# Commit and push
git add .
git commit -m "Add DevOps infrastructure"
git push origin main
```

#### Watch Deployment:
1. Go to GitHub → Actions tab
2. Watch the pipeline run (takes ~5 minutes)
3. Once complete, you'll see: ✅ Deployment Successful!
4. Click on the workflow to see your service URL

✅ **Your app is now live on Cloud Run!**

---

## 🎉 Success! What You've Accomplished

✅ **Dockerized** your application  
✅ **Automated testing** with pytest  
✅ **CI/CD pipeline** with GitHub Actions  
✅ **Cloud deployment** on GCP Cloud Run  
✅ **Auto-scaling** production service  

---

## 🧪 Test Your Deployed Service

```bash
# Get your service URL from GitHub Actions output
export SERVICE_URL="https://deepfake-backend-xxx.run.app"

# Test health endpoint
curl $SERVICE_URL/health

# Test with the browser extension
# Update extension/popup.js:
# Change: http://localhost:5000
# To: https://deepfake-backend-xxx.run.app
```

---

## 📊 View Monitoring

1. Go to: https://console.cloud.google.com/run
2. Click on `deepfake-backend`
3. View real-time metrics:
   - Request count
   - Response time
   - Error rate
   - CPU/Memory usage

---

## 🔄 Making Changes

Every time you push code, it automatically:
1. ✅ Runs tests
2. ✅ Builds Docker image
3. ✅ Deploys to Cloud Run
4. ✅ Notifies you of status

```bash
# Make a change
echo "# Updated" >> README.md

# Push
git add .
git commit -m "Update README"
git push

# Watch it deploy automatically!
```

---

## 🆘 Common Issues

### Issue: "Permission denied" in GCP

**Solution:**
```bash
# Re-grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/owner"
```

### Issue: Tests fail in GitHub Actions

**Solution:**
- Check that all dependencies are in `requirements.txt`
- Run tests locally first: `pytest tests/ -v`

### Issue: Docker build fails

**Solution:**
```bash
# Clean and rebuild
docker system prune -a
docker-compose build --no-cache
```

---

## 📚 Next Steps

1. **Update Extension:** Point to production URL
2. **Add More Tests:** Increase coverage
3. **Set Up Monitoring:** Create alerts
4. **Implement MLOps:** Automate model training
5. **Add Documentation:** Update README

---

## ✅ Verification Checklist

- [ ] Docker runs locally
- [ ] Tests pass locally
- [ ] GCP project created
- [ ] Service account created
- [ ] GitHub secrets configured
- [ ] Pipeline runs successfully
- [ ] Service deployed to Cloud Run
- [ ] Health endpoint responds
- [ ] Extension connects to production

---

**🎉 Congratulations! Your DevOps pipeline is live!**

For detailed information, see [DEVOPS_GUIDE.md](DEVOPS_GUIDE.md)
