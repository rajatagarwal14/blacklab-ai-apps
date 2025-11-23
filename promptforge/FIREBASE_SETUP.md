# 🔥 Firebase Quick Setup Guide

You're seeing the **"api-key-not-valid"** error because Firebase isn't configured yet. Here's how to fix it in 5 minutes:

---

## Step 1: Create Firebase Project (2 minutes)

1. Go to **[Firebase Console](https://console.firebase.google.com)**
2. Click **"Add project"** (or select existing)
3. Enter project name: `promptforge` (or any name)
4. Disable Google Analytics (optional)
5. Click **"Create project"**
6. Wait for setup to complete
7. Click **"Continue"**

---

## Step 2: Enable Authentication (1 minute)

1. In Firebase Console, click **"Authentication"** in left sidebar
2. Click **"Get started"**
3. Go to **"Sign-in method"** tab
4. Click on **"Email/Password"**
5. Toggle **"Enable"** switch
6. Click **"Save"**

---

## Step 3: Enable Firestore Database (1 minute)

1. In Firebase Console, click **"Firestore Database"**
2. Click **"Create database"**
3. Select **"Start in test mode"** (we'll secure it later)
4. Choose location (closest to your users)
5. Click **"Enable"**

---

## Step 4: Get Firebase Config (1 minute)

1. In Firebase Console, click **⚙️ Settings** icon (top left)
2. Click **"Project settings"**
3. Scroll down to **"Your apps"** section
4. Click **"</>" (Web)** icon
5. Register app:
   - **App nickname**: `PromptForge Admin`
   - Don't check Firebase Hosting
   - Click **"Register app"**
6. Copy the **firebaseConfig** object:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};
```

---

## Step 5: Update admin.html (30 seconds)

### Option A: Edit Locally

1. Open `promptforge/admin.html` in your code editor
2. Find **line 423** (search for `firebaseConfig`)
3. Replace the placeholder values with your config:

```javascript
const firebaseConfig = {
    apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",           // ← YOUR KEY
    authDomain: "promptforge-xxxx.firebaseapp.com",          // ← YOUR DOMAIN
    projectId: "promptforge-xxxx",                           // ← YOUR PROJECT ID
    storageBucket: "promptforge-xxxx.appspot.com",           // ← YOUR BUCKET
    messagingSenderId: "123456789012",                       // ← YOUR SENDER ID
    appId: "1:123456789012:web:abcdef1234567890"            // ← YOUR APP ID
};
```

4. Save the file
5. Commit and push:
```bash
git add promptforge/admin.html
git commit -m "Configure Firebase"
git push origin master
```

### Option B: Edit on GitHub

1. Go to your repo: https://github.com/rajatagarwal14/blacklab-ai-apps
2. Navigate to `promptforge/admin.html`
3. Click **✏️ Edit** button
4. Find line 423 (`const firebaseConfig = {`)
5. Replace the values with your Firebase config
6. Click **"Commit changes"**
7. Wait 1-2 minutes for GitHub Pages to update

---

## Step 6: Create Admin Account (1 minute)

After updating the config:

1. Go to: https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html
2. Click **"First Time Setup"**
3. Credentials are pre-filled:
   - Email: `admin@blacklab.ai`
   - Password: `987654321`
4. Click **"Create Admin Account"**
5. ✅ You'll be logged in automatically!

---

## Verification Checklist

✅ Firebase project created  
✅ Authentication enabled (Email/Password)  
✅ Firestore Database created  
✅ Firebase config copied  
✅ admin.html updated with real config  
✅ Changes pushed to GitHub  
✅ Admin account created  

---

## Common Issues

### "api-key-not-valid"
**Problem**: Firebase config not updated  
**Solution**: Make sure you replaced ALL placeholder values in admin.html

### "auth/user-not-found"
**Problem**: No admin account exists yet  
**Solution**: Click "First Time Setup" to create one

### "Firebase: No Firebase App"
**Problem**: Firebase SDK not loaded  
**Solution**: Check internet connection, Firebase CDN should load automatically

### Config looks correct but still error
**Problem**: GitHub Pages cache  
**Solution**: Wait 2-3 minutes, then hard refresh (Cmd+Shift+R)

---

## Next Steps

After Firebase is configured and admin account created:

1. ✅ **Deploy Backend** - Follow `BACKEND_SETUP.md`
2. ✅ **Update API_URL** - Point to your Render deployment
3. ✅ **Enable API Mode** - Set `USE_API = true` in `index.html`
4. ✅ **Start Managing** - Approve submissions, view analytics!

---

## Security Notes

### ⚠️ Important

- Your Firebase config (apiKey) is **safe to expose publicly** - it identifies your project
- The real security is in **Firestore Security Rules** (set them up!)
- Always use **Authentication** to protect admin actions
- Never commit **firebase-credentials.json** (backend service account key)

### Firestore Security Rules

After testing, update your Firestore rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only authenticated users can read prompts
    match /prompts/{promptId} {
      allow read: if true;  // Public read
      allow write: if request.auth != null;  // Auth required for write
    }
    
    // Only authenticated users can submit
    match /submissions/{submissionId} {
      allow read, write: if request.auth != null;
    }
    
    // Only authenticated users can access analytics
    match /analytics/{analyticsId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

---

## Your Firebase Config Summary

After completing setup, your config should look like:

```javascript
// ✅ CORRECT - Real values
const firebaseConfig = {
    apiKey: "AIzaSyABC123XYZ...",
    authDomain: "promptforge-a1b2c.firebaseapp.com",
    projectId: "promptforge-a1b2c",
    storageBucket: "promptforge-a1b2c.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdef1234567890"
};

// ❌ WRONG - Placeholder values (will cause api-key-not-valid error)
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    // ...
};
```

---

## Need Help?

1. Check all steps above are completed
2. Verify Firebase config in admin.html has real values
3. Wait 2-3 minutes after pushing to GitHub
4. Try hard refresh (Cmd+Shift+R or Ctrl+F5)
5. Check browser console for specific errors

---

**Total Time: ~5 minutes** ⏱️

Once done, your admin panel will be fully functional! 🎉
