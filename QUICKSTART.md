# Quick Start Guide

Get the PrimeTrade Backend API running in **5 minutes**.

## Prerequisites
- Python 3.10+
- PostgreSQL (or use SQLite for quick testing)

## Setup

### Option 1: Docker (Fastest)
1. **Run with one command**:
   ```bash
   docker compose up --build
   ```
2. **Access the app**: http://localhost

### Option 2: Local Installation
### 1. Clone & Navigate
```bash
git clone <repository-url>
cd backend_primetrade_ai
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
copy .env.example .env

# Edit .env - Minimum required:
# For SQLite (quickest):
DATABASE_URL=sqlite:///primetrade.db
JWT_SECRET_KEY=your-secret-key-change-this
SECRET_KEY=your-flask-secret-key
```

### 4. Initialize Database
```bash
python src/backend/app.py
# Database will be created automatically
```

### 5. Run Backend
```bash
flask run
# Backend: http://localhost:5000
# API Docs: http://localhost:5000/api/docs
```

### 6. Open Frontend
```bash
# Open in browser:
# file:///path/to/src/frontend/index.html
# OR use Live Server extension in VS Code
```

## Quick Test

### Register User (Postman/curl)
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

### Create Task (use token from login)
```bash
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"title":"My Task","description":"Test","status":"pending"}'
```

## Common Issues

**Issue**: `ModuleNotFoundError`
**Fix**: Ensure virtual environment is activated

**Issue**: Database connection error
**Fix**: Check DATABASE_URL in .env

**Issue**: CORS error in frontend
**Fix**: Update ALLOWED_ORIGINS in .env with your frontend URL

## Next Steps
- See [README.md](README.md) for detailed documentation
- Run tests: `pytest tests/`
- View API docs: http://localhost:5000/api/docs
