# 🚀 PromptForge Backend Setup Guide

## Features Added

✅ **Admin Panel** - Approve/reject submissions with authentication  
✅ **Analytics Dashboard** - Track popular prompts, copies, categories  
✅ **REST API** - Full API for external apps to access prompts  
✅ **Firebase Integration** - Real-time database, authentication, analytics  
✅ **Render Deployment** - Production-ready backend hosting  

---

## 📁 Project Structure

```
promptforge/
├── index.html              # Frontend (existing)
├── admin.html             # Admin panel (new)
├── prompts_database.js    # Static prompts (existing)
└── backend/
    ├── app.py                      # Flask API
    ├── requirements.txt            # Python dependencies
    ├── render.yaml                 # Render config
    └── firebase-credentials.json   # Firebase credentials (you'll create this)
```

---

## 🔥 Step 1: Create Firebase Project

### 1.1 Go to Firebase Console
1. Visit https://console.firebase.google.com/
2. Click "Add Project"
3. Name it: `promptforge`
4. Enable Google Analytics (optional)
5. Create project

### 1.2 Enable Firestore Database
1. In Firebase console, go to "Build" → "Firestore Database"
2. Click "Create database"
3. Start in **production mode**
4. Choose location (e.g., us-central)
5. Enable

### 1.3 Enable Authentication
1. Go to "Build" → "Authentication"
2. Click "Get started"
3. Enable "Email/Password" sign-in method
4. Click "Save"

### 1.4 Create Admin User
1. In Authentication tab, click "Add user"
2. Email: `your-email@example.com`
3. Password: `your-secure-password`
4. Click "Add user"

### 1.5 Get Firebase Credentials
1. Go to Project Settings (⚙️ icon)
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Save the JSON file
5. Rename it to `firebase-credentials.json`
6. Place it in `promptforge/backend/` folder

### 1.6 Get Firebase Web Config
1. In Project Settings, scroll to "Your apps"
2. Click web icon (</>) to add web app
3. Register app name: "PromptForge Admin"
4. Copy the `firebaseConfig` object
5. We'll use this in admin.html

---

## 🐍 Step 2: Set Up Backend Locally

### 2.1 Install Python Dependencies

```bash
cd /Users/rajat/Downloads/blacklab-ai-apps/promptforge/backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Add Firebase Credentials
```bash
# Make sure firebase-credentials.json is in backend/ folder
ls firebase-credentials.json  # Should show the file
```

### 2.3 Update Admin Emails in app.py
Edit `backend/app.py` line ~32:
```python
admins = ['your-email@example.com']  # Add your admin email(s)
```

### 2.4 Test Locally
```bash
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

Test the API:
```bash
# In another terminal
curl http://localhost:5000/health
```

Should return:
```json
{"status": "healthy", "service": "PromptForge API", "version": "1.0.0"}
```

---

## 🌐 Step 3: Deploy Backend to Render

### 3.1 Create Render Account
1. Go to https://render.com/
2. Sign up with GitHub
3. Connect your repository

### 3.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect to `blacklab-ai-apps` repository
3. Configure:
   - **Name**: `promptforge-api`
   - **Region**: Oregon (US West)
   - **Branch**: `master`
   - **Root Directory**: `promptforge/backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

### 3.3 Add Environment Variables
1. In Render dashboard, go to "Environment"
2. Add **FIREBASE_CREDENTIALS** as secret file:
   - Click "Add Secret File"
   - Filename: `firebase-credentials.json`
   - Content: Paste your Firebase credentials JSON
   - Click "Save"

### 3.4 Deploy
1. Click "Create Web Service"
2. Wait for deployment (3-5 minutes)
3. Your API URL will be: `https://promptforge-api.onrender.com`

### 3.5 Test Production API
```bash
curl https://promptforge-api.onrender.com/health
```

---

## 🎨 Step 4: Update Frontend

### 4.1 Update admin.html Firebase Config
Edit `promptforge/admin.html` around line 340:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

Replace with YOUR Firebase config from Step 1.6

### 4.2 Update API URL in admin.html
Edit `promptforge/admin.html` around line 349:

```javascript
const API_URL = 'https://promptforge-api.onrender.com';  // Your Render URL
```

### 4.3 Optional: Update index.html to Use API
Currently, index.html uses localStorage. To connect to the backend:

Create `promptforge/config.js`:
```javascript
const API_CONFIG = {
    baseURL: 'https://promptforge-api.onrender.com'
};
```

---

## 📊 Step 5: Migrate Existing Prompts to Firestore

Create `backend/migrate_prompts.py`:

```python
import firebase_admin
from firebase_admin import credentials, firestore
import sys
sys.path.append('..')
# Import your prompts from prompts_database.js
# You'll need to manually convert or use this script

cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add your 70 prompts to Firestore
prompts = [
    {
        'title': 'SEO Blog Post Generator',
        'category': 'marketing',
        'text': '...',
        'approved': True,
        'copy_count': 0,
        'view_count': 0
    },
    # Add all 70 prompts...
]

for prompt in prompts:
    db.collection('prompts').add(prompt)
    print(f"Added: {prompt['title']}")

print("Migration complete!")
```

Run:
```bash
python migrate_prompts.py
```

---

## 🔑 Step 6: Access Admin Panel

### 6.1 Deploy Updated Files
```bash
cd /Users/rajat/Downloads/blacklab-ai-apps
git add promptforge/
git commit -m "Add backend API and admin panel"
git push origin master
```

### 6.2 Access Admin Panel
1. Go to: `https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html`
2. Login with your Firebase admin email/password
3. You'll see the admin dashboard!

---

## 📡 API Endpoints

### Public Endpoints (No Auth Required)

#### Get All Prompts
```bash
GET /api/prompts
GET /api/prompts?category=marketing
GET /api/prompts?search=seo
```

#### Get Single Prompt
```bash
GET /api/prompts/{id}
```

#### Track Copy
```bash
POST /api/prompts/{id}/copy
```

#### Submit Prompt
```bash
POST /api/submissions
Content-Type: application/json

{
  "title": "My Prompt",
  "category": "coding",
  "text": "Prompt text here...",
  "author": "John Doe"
}
```

#### Get Categories
```bash
GET /api/categories
```

### Admin Endpoints (Requires Auth Token)

#### Get Pending Submissions
```bash
GET /api/admin/submissions
Authorization: Bearer {firebase_token}
```

#### Approve Submission
```bash
POST /api/admin/submissions/{id}/approve
Authorization: Bearer {firebase_token}
```

#### Reject Submission
```bash
POST /api/admin/submissions/{id}/reject
Authorization: Bearer {firebase_token}
Content-Type: application/json

{
  "reason": "Rejection reason"
}
```

#### Get Analytics Stats
```bash
GET /api/analytics/stats
Authorization: Bearer {firebase_token}
```

#### Get Popular Prompts
```bash
GET /api/analytics/popular?limit=10
Authorization: Bearer {firebase_token}
```

---

## 🎯 Usage Examples

### For External Apps

#### Python Example
```python
import requests

API_URL = 'https://promptforge-api.onrender.com'

# Get all prompts
response = requests.get(f'{API_URL}/api/prompts')
prompts = response.json()['prompts']

# Get marketing prompts
response = requests.get(f'{API_URL}/api/prompts?category=marketing')
marketing_prompts = response.json()['prompts']

# Submit a prompt
new_prompt = {
    'title': 'My Custom Prompt',
    'category': 'coding',
    'text': 'Create a Python function that...',
    'author': 'API User'
}
response = requests.post(f'{API_URL}/api/submissions', json=new_prompt)
```

#### JavaScript Example
```javascript
const API_URL = 'https://promptforge-api.onrender.com';

// Fetch prompts
fetch(`${API_URL}/api/prompts?category=coding`)
  .then(res => res.json())
  .then(data => {
    console.log(`Found ${data.count} prompts`);
    data.prompts.forEach(prompt => {
      console.log(prompt.title);
    });
  });

// Submit prompt
fetch(`${API_URL}/api/submissions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'New Prompt',
    category: 'writing',
    text: 'Write a professional email...',
    author: 'John Doe'
  })
})
.then(res => res.json())
.then(data => console.log('Submitted:', data));
```

---

## 💰 Costs

### Current Setup (Free Tier)
- **GitHub Pages**: Free
- **Render**: Free (with limitations)
  - Auto-sleep after 15 min of inactivity
  - 750 hours/month free
- **Firebase**:
  - Firestore: 50K reads, 20K writes/day free
  - Authentication: Unlimited
  - Storage: 1GB free

### Upgrade Path
If you get traffic and need always-on:
- **Render Standard**: $7/month (always on)
- **Firebase Blaze Plan**: Pay-as-you-go (very cheap for small apps)

---

## 🔒 Security Best Practices

1. **Never commit** `firebase-credentials.json` to Git
2. Add to `.gitignore`:
   ```
   backend/firebase-credentials.json
   backend/venv/
   backend/__pycache__/
   ```

3. **Set Firestore Rules** (in Firebase Console):
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Only allow admin users to write
       match /prompts/{prompt} {
         allow read: if true;
         allow write: if false;  // Use API only
       }
       match /submissions/{submission} {
         allow read: if false;
         allow write: if true;  // Anyone can submit
       }
       match /analytics/{doc} {
         allow read, write: if false;  // API only
       }
     }
   }
   ```

4. **Enable CORS properly** for production

---

## 🎊 You're Done!

Your PromptForge now has:
✅ Full backend API on Render  
✅ Firebase database with real-time sync  
✅ Admin panel for managing submissions  
✅ Analytics dashboard  
✅ Public API for external apps  

**Admin Panel URL**: https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html  
**API URL**: https://promptforge-api.onrender.com  
**Main App**: https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/  

---

## 📞 Support

Questions? Issues? Check:
1. Render logs: Dashboard → Logs
2. Firebase console for database/auth issues
3. Browser console for frontend errors

Good luck! 🚀
