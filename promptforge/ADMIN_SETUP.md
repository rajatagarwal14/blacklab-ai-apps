# 🔐 PromptForge Admin Account Setup

There are **3 easy ways** to create your admin account:

---

## Option 1: Web Interface (Easiest) ✨

1. Go to admin panel: [https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html](https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html)

2. Click **"First Time Setup"** button

3. Fill in:
   - **Email**: `admin@promptforge.com` (or your email)
   - **Password**: Choose a secure password (min 6 chars)
   - **Confirm Password**: Enter same password

4. Click **"Create Admin Account"**

5. You'll be automatically logged in! 🎉

**Note**: This requires Firebase to be already configured in `admin.html`

---

## Option 2: Python Script (Recommended) 🐍

### Prerequisites
```bash
cd promptforge/backend
pip install firebase-admin
```

### Steps

1. **Get Firebase Credentials**
   - Go to [Firebase Console](https://console.firebase.google.com)
   - Select your project
   - Go to **Project Settings** → **Service Accounts**
   - Click **"Generate New Private Key"**
   - Save as `firebase-credentials.json` in `backend/` folder

2. **Run the Script**
   ```bash
   python create_admin.py
   ```

3. **Follow Prompts**
   ```
   Enter admin email (default: admin@promptforge.com): admin@example.com
   Enter admin password (min 6 chars): YourSecurePassword123
   ```

4. **Success!**
   ```
   ✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!
   📧 Email:    admin@example.com
   🔑 Password: YourSecurePassword123
   🆔 UID:      abc123xyz...
   👑 Role:     Admin
   ```

### Command Line Arguments
```bash
# Interactive mode (prompts for input)
python create_admin.py

# Non-interactive mode
python create_admin.py --email admin@example.com --password SecurePass123

# List all existing users
python create_admin.py --list
```

---

## Option 3: Firebase Console (Manual) 🔧

1. Go to [Firebase Console](https://console.firebase.google.com)

2. Select your **PromptForge** project

3. Click **Authentication** in left sidebar

4. Click **Users** tab

5. Click **"Add User"** button

6. Fill in:
   - **Email**: `admin@promptforge.com`
   - **Password**: Your secure password
   - **User ID**: (auto-generated)

7. Click **"Add User"**

8. ✅ Done! You can now login at the admin panel

**Note**: This method doesn't automatically set admin custom claims, so the script method is preferred.

---

## Login to Admin Panel

After creating your account:

1. Go to: [https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html](https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html)

2. Enter your **email** and **password**

3. Click **"Login"**

4. You'll see the admin dashboard with:
   - 📊 Statistics
   - 📝 Pending submissions
   - 📈 Analytics
   - 🔥 Popular prompts

---

## Default Credentials

If you use the quick setup, default credentials are:

- **Email**: `admin@promptforge.com`
- **Password**: Whatever you choose during setup

⚠️ **Important**: Change the default password after first login!

---

## Security Best Practices

### ✅ DO:
- Use a strong password (12+ characters, mix of letters, numbers, symbols)
- Keep your Firebase credentials secure
- Don't commit `firebase-credentials.json` to git
- Use a dedicated admin email
- Enable 2FA on your Firebase account

### ❌ DON'T:
- Share your admin credentials
- Use weak passwords like "123456" or "password"
- Commit credentials to public repositories
- Leave default credentials unchanged

---

## Troubleshooting

### "No authentication token provided"
**Solution**: Make sure you're logged in. The admin panel requires authentication.

### "Admin access required"
**Solution**: Your account doesn't have admin privileges. Run the Python script to set custom claims.

### "Invalid authentication token"
**Solution**: Your session expired. Logout and login again.

### "firebase-credentials.json not found"
**Solution**: Download the Firebase service account key and save it in `backend/` folder.

### "Email already in use"
**Solution**: This email is already registered. Use the login form instead, or choose a different email.

---

## Advanced: Custom Admin Claims

To properly restrict admin access, you should use Firebase custom claims.

### Using the Python Script (Automated)
The `create_admin.py` script automatically sets custom claims:
```python
auth.set_custom_user_claims(user.uid, {
    'admin': True,
    'role': 'admin'
})
```

### Manual Setup via Firebase Admin SDK
```python
import firebase_admin
from firebase_admin import auth

# Get user by email
user = auth.get_user_by_email('admin@example.com')

# Set admin claims
auth.set_custom_user_claims(user.uid, {'admin': True})
```

### Verify Claims in Frontend
Update `admin.html` to check for admin claim:
```javascript
const idTokenResult = await user.getIdTokenResult();
if (!idTokenResult.claims.admin) {
    alert('You are not an admin!');
    return;
}
```

---

## Next Steps After Setup

1. ✅ **Create admin account** (using any method above)
2. ✅ **Login to admin panel**
3. ✅ **Deploy backend to Render** (see `BACKEND_SETUP.md`)
4. ✅ **Update API_URL** in `index.html` and `admin.html`
5. ✅ **Enable API mode** (`USE_API = true` in `index.html`)
6. ✅ **Start managing prompts!**

---

## Quick Reference

| Method | Difficulty | Time | Prerequisites |
|--------|------------|------|---------------|
| **Web Interface** | ⭐ Easy | 1 min | Firebase configured |
| **Python Script** | ⭐⭐ Medium | 5 min | Python, Firebase key |
| **Firebase Console** | ⭐⭐⭐ Hard | 3 min | Firebase access |

---

## Support

If you need help:
1. Check the troubleshooting section above
2. Review `BACKEND_SETUP.md` for Firebase setup
3. Check Firebase Console for user status
4. Verify your Firebase credentials are correct

---

**Your PromptForge admin account is ready! 🎉**

Now you can approve submissions, view analytics, and manage your prompt library.
