# 🔗 Frontend ↔ Backend Linking Guide

**IMPORTANT**: These are **cross-references that must be updated AFTER initial deployment** because you won't know the exact URLs until each service is deployed.

---

## 📋 The Linking Dependency

```
┌─────────────────┐     Deploy First      ┌─────────────────┐
│   BACKEND       │ ──────────────────→   │   FRONTEND      │
│   (Render)      │   Gets live URL       │   (Vercel)      │
└─────────────────┘                       └─────────────────┘
        ▲                                        │
        │                                        │
        │     Update CORS                        │
        │     Update VITE_API_URL                │
        └────────────────────────────────────────┘
              Update AFTER both deployed
```

---

## 🚀 Step-by-Step Linking Process

### **Phase 1: Deploy Backend First**

```bash
# 1. Push to GitHub
git add .
git commit -m "feat: production ready"
git push origin main

# 2. Deploy to Render (via Blueprint or manual)
# - Connect repo to Render
# - It will create: https://seo-agent-api-xxxx.onrender.com
# - Note this URL!
```

**Backend Live URL**: `https://your-backend-name.onrender.com`

---

### **Phase 2: Deploy Frontend**

```bash
# 1. In Vercel Dashboard → Add New Project
# 2. Import same GitHub repo
# 3. Root Directory: frontend
# 4. Add Environment Variable:
#    VITE_API_URL = https://your-backend-name.onrender.com/api
# 5. Deploy
# - It will create: https://seo-agent-xxxx.vercel.app
# - Note this URL!
```

**Frontend Live URL**: `https://your-frontend-name.vercel.app`

---

### **Phase 3: Link Them Together**

#### **A. Update Backend CORS** (In Render Dashboard)
```
Environment Variables → ALLOWED_ORIGINS = https://your-frontend-name.vercel.app
```
> **Note**: Add `,https://www.your-frontend-name.vercel.app` if using www

**Save → Auto-redeploy triggers**

---

#### **B. Verify Frontend API URL** (In Vercel Dashboard)
```
Settings → Environment Variables → VITE_API_URL
Value: https://your-backend-name.onrender.com/api
```
> Should already be set from Phase 2, just verify

---

### **Phase 4: Test the Connection**

```bash
# 1. Open frontend URL
open https://your-frontend-name.vercel.app

# 2. Check browser console - no CORS errors!

# 3. Click "Create Blog Page" - should work end-to-end

# 4. Check backend logs - requests from Vercel domain
```

---

## 🔧 Configuration Files Reference

### **Backend** (`render.yaml`)
```yaml
envVars:
  - key: ALLOWED_ORIGINS
    value: "https://your-frontend-name.vercel.app"  # ← UPDATE AFTER VERCEL DEPLOY
```

### **Frontend** (`.env.example` / Vercel Dashboard)
```env
VITE_API_URL=https://your-backend-name.onrender.com/api  # ← SET IN VERCEL DASHBOARD
```

### **Frontend** (`vercel.json`)
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-name.onrender.com/api/$1"  # ← UPDATE
    }
  ]
}
```

---

## 📝 Quick Reference Card

| Where | Variable | When to Set | Value Format |
|-------|----------|-------------|--------------|
| **Render Dashboard** | `ALLOWED_ORIGINS` | After Vercel deploy | `https://xxx.vercel.app` |
| **Vercel Dashboard** | `VITE_API_URL` | During Vercel deploy | `https://xxx.onrender.com/api` |
| **vercel.json** | `rewrites.destination` | Before frontend deploy | `https://xxx.onrender.com/api` |

---

## ⚠️ Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Setting `ALLOWED_ORIGINS` before Vercel deploy | Wait for Vercel URL first! |
| Using `http://` instead of `https://` | Always use HTTPS in production |
| Forgetting trailing slash in API URL | Use `.../api` not `.../api/` |
| Not redeploying after changing env vars | Both platforms auto-redeploy on env change |
| Using Render's default URL in vercel.json | Use YOUR actual backend URL |

---

## 🔄 After Custom Domain Setup (Optional)

If you add custom domains later:

```bash
# Backend (Render) - Add custom domain
# Frontend (Vercel) - Add custom domain

# Then update:
ALLOWED_ORIGINS=https://app.yourdomain.com,https://www.yourdomain.com
VITE_API_URL=https://api.yourdomain.com/api
```

---

## ✅ Verification Checklist

- [ ] Backend deployed → Got `https://xxx.onrender.com`
- [ ] Frontend deployed with `VITE_API_URL` → Got `https://xxx.vercel.app`
- [ ] Updated `ALLOWED_ORIGINS` in Render with Vercel URL
- [ ] Both redeployed after env changes
- [ ] Open frontend → No CORS errors in console
- [ ] Click "Create Blog Page" → Works end-to-end
- [ ] Check backend logs → Requests from Vercel domain

---

## 🆘 Troubleshooting

### CORS Error in Browser Console
```
Access to fetch at 'https://xxx.onrender.com/api/...' 
from origin 'https://xxx.vercel.app' has been blocked by CORS policy
```
→ **Fix**: Update `ALLOWED_ORIGINS` in Render Dashboard with exact Vercel URL

### "Failed to fetch" / Network Error
```
TypeError: Failed to fetch
```
→ **Fix**: Check `VITE_API_URL` in Vercel includes `/api` suffix and uses HTTPS

### Backend Not Receiving Requests
→ **Fix**: Check `vercel.json` rewrites point to correct backend URL

---

**Remember**: The URLs are only known AFTER deployment. Deploy backend → Get URL → Deploy frontend with that URL → Update backend with frontend URL → Done! 🎯