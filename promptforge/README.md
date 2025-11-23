# ✨ PromptForge - Your Ultimate AI Prompt Library

**Live Demo**: [Launch PromptForge](#)

---

## 🎉 Features

✅ **70+ Curated AI Prompts** across 8 professional categories  
✅ **Community Submissions** - Users can contribute their own prompts  
✅ **Beautiful Modern UI** - Clean, professional design  
✅ **Dark Mode** - Easy on the eyes  
✅ **Smart Search & Filter** - Find prompts instantly  
✅ **One-Click Copy** - Seamless workflow integration  
✅ **Mobile Responsive** - Works perfectly on all devices  
✅ **Zero Dependencies** - Pure HTML/CSS/JavaScript  

---

## 📂 Files

- `index.html` - Main application (single-page app)
- `prompts_database.js` - Database with 70+ prompts
- `README.md` - This file

---

## 🚀 Quick Start

### Local Development (30 seconds)
```bash
# Just open the file
open index.html

# Or serve with Python
python3 -m http.server 8000
# Visit: http://localhost:8000
```

### Deploy Online (5 minutes)

#### Option 1: GitHub Pages
```bash
# Already in blacklab-ai-apps repo
git add promptforge/
git commit -m "Add PromptForge"
git push origin master

# Enable GitHub Pages in repo settings
# Your URL: https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/
```

#### Option 2: Netlify
1. Drag the `promptforge` folder to [Netlify Drop](https://app.netlify.com/drop)
2. Get instant live URL
3. Done! 🎉

---

## 📊 Prompt Categories

1. **📊 Marketing** (10 prompts)
   - SEO, Social Media, Email Marketing, Landing Pages, etc.

2. **💻 Coding** (12 prompts)
   - Python, React, SQL, API Design, DevOps, Testing, etc.

3. **✍️ Writing** (8 prompts)
   - Professional Emails, LinkedIn, Documentation, Press Releases, etc.

4. **💼 Business** (8 prompts)
   - Business Models, SWOT, Pitch Decks, Strategy, etc.

5. **📋 Project Management** (8 prompts)
   - Agile, Risk Assessment, Stakeholder Management, etc.

6. **🎨 Design** (8 prompts)
   - UX Research, Design Systems, Personas, Wireframes, etc.

7. **🎓 Education** (6 prompts)
   - Curriculum Design, Lesson Plans, Assessments, etc.

8. **📈 Data Science** (6 prompts)
   - ML, Data Analysis, Visualization, A/B Testing, etc.

---

## 🎯 How It Works

### For Users
1. Browse prompts by category or search
2. Click any prompt to view details
3. Copy with one click
4. Use in ChatGPT, Claude, or any AI tool

### For Contributors
1. Click "➕ Submit Prompt" button
2. Fill out the form
3. Submit instantly
4. Prompt appears in library immediately

**Note**: Submissions are stored in browser's localStorage (local only). For shared submissions across users, integrate a backend (see Upgrade Path below).

---

## 🛠️ Customization

### Change Colors
Edit in `index.html` `<style>` section:
```css
:root {
    --primary: #6366f1;      /* Main brand color */
    --secondary: #ec4899;    /* Accent color */
}
```

### Add Categories
Edit in `index.html` JavaScript section:
```javascript
const categories = [
    { id: 'new-category', name: 'New Category', icon: '🔥', count: 0 },
    // Add your categories...
];
```

### Modify Prompts
Edit `prompts_database.js` file directly.

---

## 📈 Upgrade Path

### Phase 1: Backend Integration
- **Firebase/Supabase** for real database
- User authentication
- Shared community prompts
- Admin approval queue

### Phase 2: Advanced Features
- Prompt ratings & reviews
- User profiles & reputation
- Collections & favorites
- Prompt versioning
- API access

### Phase 3: Monetization
- Premium prompts
- Subscription tiers
- Team features
- Analytics dashboard

---

## 🎊 Tech Stack

- **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
- **Storage**: localStorage (can upgrade to Firebase/Supabase)
- **Hosting**: Any static host (GitHub Pages, Netlify, Vercel)
- **Dependencies**: ZERO! ✨

---

## 📱 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

## 🤝 Contributing

Want to add prompts or features?

1. Fork the repository
2. Add your prompts to `prompts_database.js`
3. Test locally
4. Submit PR with description

---

## 📄 License

Part of BlackLab AI Apps  
© 2025 - Built with ❤️ for the AI community

---

## 🔗 Links

- **Home**: [BlackLab AI Apps](https://rajatagarwal14.github.io/blacklab-ai-apps/)
- **GitHub**: [Repository](https://github.com/rajatagarwal14/blacklab-ai-apps)
- **Issues**: [Report a bug](https://github.com/rajatagarwal14/blacklab-ai-apps/issues)

---

**⭐ Star the repo if you find it useful!**
