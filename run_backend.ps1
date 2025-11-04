# Run backend server with correct Python version

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Cyan

# Check if venv exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Run with venv Python
Write-Host "✅ Using Python from venv" -ForegroundColor Green
& ".\venv\Scripts\python.exe" backend_server.py
