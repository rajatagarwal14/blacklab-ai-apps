# 🔄 Frontend API Integration Guide

## What Was Updated

The main `index.html` has been updated to support **both static and API modes**.

### ✅ Changes Made:

1. **API Configuration Added**
   ```javascript
   const API_URL = 'https://promptforge-api.onrender.com';
   const USE_API = false; // Toggle between static and API mode
   ```

2. **New API Functions**
   - `loadCategories()` - Fetches categories with real counts from API
   - `loadPromptsFromAPI()` - Fetches all approved prompts from API
   - `updateStats()` - Updates dashboard statistics

3. **Updated Functions**
   - `copyPrompt()` - Now tracks copy events via API
   - `handleSubmission()` - Submits to API (pending admin approval)
   - `loadCommunityPrompts()` - Skips when using API mode

4. **Smart Fallback**
   - If API fails, automatically falls back to static `prompts_database.js`
   - Works offline with localStorage as before

---

## 🚀 How to Enable API Mode

### Before Deployment (Current State)
```javascript
const USE_API = false; // Uses static prompts_database.js
```
- ✅ Works immediately on GitHub Pages
- ✅ No backend required
- ❌ Submissions stored locally (not shared)
- ❌ No analytics tracking
- ❌ Static prompt counts

### After Backend Deployment
```javascript
const API_URL = 'https://your-api.onrender.com'; // Your actual API URL
const USE_API = true; // Enable API mode
```
- ✅ Real-time prompts from database
- ✅ Shared submissions (visible to all after approval)
- ✅ Analytics tracking (copies, views)
- ✅ Live category counts
- ✅ Admin-approved content only

---

## 📋 Step-by-Step Activation

### Step 1: Deploy Backend First
Follow `BACKEND_SETUP.md` to:
1. Create Firebase project
2. Deploy API to Render
3. Get your API URL (e.g., `https://promptforge-api.onrender.com`)

### Step 2: Update Configuration
Edit `promptforge/index.html` lines 147-148:

```javascript
// Before
const API_URL = 'https://promptforge-api.onrender.com'; // Update with your Render URL
const USE_API = false; // Set to true after deploying backend

// After
const API_URL = 'https://YOUR-ACTUAL-API.onrender.com';
const USE_API = true;
```

### Step 3: Test Locally
```bash
cd /Users/rajat/Downloads/blacklab-ai-apps/promptforge
python3 -m http.server 8000
# Visit: http://localhost:8000
```

Check browser console:
- ✅ Should see API calls to your Render URL
- ✅ Prompts load from API
- ✅ Submissions go to API (pending approval message)

### Step 4: Deploy to GitHub Pages
```bash
git add promptforge/index.html
git commit -m "Enable API mode for PromptForge"
git push origin master
```

### Step 5: Verify Live
Visit: `https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/`

Test:
- ✅ Prompts load from database
- ✅ Categories show real counts
- ✅ Copy tracking works
- ✅ Submissions create pending reviews in admin panel

---

## 🎯 Current Behavior

### With `USE_API = false` (Default)
```
User visits site
  ↓
Loads prompts_database.js (70 static prompts)
  ↓
Renders from static file
  ↓
Submissions → localStorage (local only)
```

### With `USE_API = true` (After backend deployed)
```
User visits site
  ↓
Fetches from API (GET /api/prompts)
  ↓
Renders approved prompts from database
  ↓
Copy → Tracks via API (POST /api/prompts/{id}/copy)
  ↓
Submit → API (POST /api/submissions) → Admin approval queue
  ↓
Admin approves → Appears for all users
```

---

## 🔍 Features Comparison

| Feature | Static Mode (`USE_API = false`) | API Mode (`USE_API = true`) |
|---------|--------------------------------|----------------------------|
| Prompt Loading | Static file (70 prompts) | Database (all approved) |
| User Submissions | localStorage only | Sent to admin for approval |
| Copy Tracking | No tracking | Tracked in analytics |
| Category Counts | Static numbers | Real-time from database |
| Shared Content | No | Yes (after approval) |
| Analytics | No | Full dashboard |
| Admin Panel | Can't access data | Full control |
| Offline Mode | Works | Requires internet |
| Setup Time | 0 minutes | 30 minutes |
| Monthly Cost | $0 | $0-8 |

---

## 🐛 Troubleshooting

### API Not Loading
1. Check browser console for errors
2. Verify API URL is correct
3. Ensure backend is deployed and running
4. Check CORS settings in backend

### Prompts Not Appearing
1. Verify backend has prompts in database
2. Check if prompts are marked as `approved: true`
3. Run migration script to add initial prompts

### Submissions Not Working
1. Check network tab - should POST to `/api/submissions`
2. Verify response is 200/201
3. Check admin panel for pending submissions

### Falls Back to Static
This is normal if:
- API_URL is wrong
- Backend is not deployed
- Backend is sleeping (Render free tier)
- Network issue

---

## 📊 Migration Checklist

- [ ] Backend deployed to Render
- [ ] Firebase project created
- [ ] Initial prompts migrated to database
- [ ] Admin user created
- [ ] API URL updated in `index.html`
- [ ] `USE_API = true` set
- [ ] Tested locally
- [ ] Deployed to GitHub Pages
- [ ] Verified live site works
- [ ] Admin panel accessible

---

## 💡 Best Practices

### During Development
```javascript
const USE_API = false; // Use static mode
```
- Fast development
- No API dependency
- Works offline

### After Backend Ready
```javascript
const USE_API = true; // Switch to API
```
- Live data
- Real analytics
- Shared submissions

### Production Recommendation
Keep both modes functional:
- API mode for dynamic content
- Fallback to static if API fails
- Better user experience

---

## 🎊 You're Ready!

The frontend is now **API-ready**. Once you deploy the backend:

1. Update `API_URL` with your Render URL
2. Set `USE_API = true`
3. Commit and push

Users will get:
- ✅ Real-time prompts from database
- ✅ Submission approval workflow
- ✅ Analytics tracking
- ✅ Admin-curated content

**Current state**: Works perfectly with static mode (no backend needed)  
**After backend**: Full dynamic functionality with admin control

---

**Questions?** Check `BACKEND_SETUP.md` for backend deployment.
