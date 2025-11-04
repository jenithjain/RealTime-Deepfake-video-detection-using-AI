# Dockerfile for Real-Time Deepfake Detection Backend
# Optimized for GCP Cloud Run deployment

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and PyTorch
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend_server.py .
COPY deepfake_detection.py .
COPY face_detection.py .

# Create weights directory and copy trained model
RUN mkdir -p weights
COPY weights/best_model.pth weights/

# Expose port for Cloud Run
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEVICE=cpu
ENV PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# Run the application
CMD ["python", "backend_server.py"]
