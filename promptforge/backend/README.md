# 🎯 PromptForge Backend - Quick Start

## What Was Added

✅ **Flask REST API** (`backend/app.py`)
  - Public endpoints for prompts, submissions, categories
  - Admin endpoints for approvals, analytics
  - Firebase integration for database & auth

✅ **Admin Panel** (`admin.html`)
  - Authentication with Firebase
  - Approve/reject submissions
  - Analytics dashboard
  - Popular prompts tracking

✅ **Deployment Ready**
  - `requirements.txt` for Python dependencies
  - `render.yaml` for Render deployment
  - `.gitignore` for security

## Quick Setup (5 Steps)

### 1️⃣ Create Firebase Project
- Go to https://console.firebase.google.com/
- Create project named "promptforge"
- Enable Firestore & Authentication
- Download credentials JSON

### 2️⃣ Install Dependencies Locally
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Add Firebase Credentials
- Place `firebase-credentials.json` in `backend/` folder
- Update admin emails in `app.py` (line 32)

### 4️⃣ Deploy to Render
- Push code to GitHub
- Create web service on Render
- Add Firebase credentials as secret file
- Deploy!

### 5️⃣ Update Frontend URLs
- Update API URL in `admin.html`
- Update Firebase config in `admin.html`

## Full Documentation

See `BACKEND_SETUP.md` for complete step-by-step guide.

## API Endpoints

**Public**:
- `GET /api/prompts` - Get all prompts
- `POST /api/submissions` - Submit prompt
- `GET /api/categories` - Get categories

**Admin** (requires auth):
- `GET /api/admin/submissions` - Pending submissions
- `POST /api/admin/submissions/{id}/approve` - Approve
- `GET /api/analytics/stats` - Analytics

## Costs

- GitHub Pages: **Free**
- Render Free Tier: **Free** (with sleep)
- Firebase Free Tier: **Free** (generous limits)

**Total: $0/month** (with limitations)

Upgrade to $7/month Render for always-on service.

---

**Need help?** Check BACKEND_SETUP.md for detailed instructions!
