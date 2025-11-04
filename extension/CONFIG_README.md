# 🔧 Extension Configuration

## Quick Start

**To switch between local and production backends, edit ONE file:**

📁 **`extension/config.js`**

---

## 🎯 How to Use

### **For Local Testing:**

Open `extension/config.js` and set:

```javascript
const ENVIRONMENT = 'local';  // Uses http://localhost:5000
```

### **For Production (Cloud Run):**

Open `extension/config.js` and set:

```javascript
const ENVIRONMENT = 'production';  // Uses Cloud Run URL
```

---

## 📋 Configuration Options

### **Backend URLs:**

```javascript
// PRODUCTION: Cloud Run deployment
const PRODUCTION_URL = 'https://deepfake-backend-kpu7yogeia-uc.a.run.app';

// LOCAL: For testing on localhost
const LOCAL_URL = 'http://localhost:5000';
```

### **Other Settings:**

```javascript
CAPTURE_INTERVAL: 1000,  // Frame capture interval in milliseconds
TIMEOUT: 30000           // Backend connection timeout in milliseconds
```

---

## 🚀 After Changing Config

1. **Save** `config.js`
2. **Reload extension** in browser:
   - Go to `chrome://extensions/` or `edge://extensions/`
   - Click reload button 🔄 on the extension
3. **Test** the extension

---

## 📊 How It Works

All extension files now use `CONFIG.BACKEND_URL` instead of hardcoded URLs:

- ✅ `popup.js` - Uses CONFIG for default URL
- ✅ `content.js` - Uses CONFIG for API calls
- ✅ `background.js` - Uses CONFIG for health checks

**One change in `config.js` updates the entire extension!**

---

## 🎯 Example Workflow

### **Testing Locally:**

```bash
# 1. Set config to local
# Edit config.js: ENVIRONMENT = 'local'

# 2. Start local backend
python backend_server.py

# 3. Reload extension
# chrome://extensions/ → Reload

# 4. Test on YouTube
```

### **Using Production:**

```bash
# 1. Set config to production
# Edit config.js: ENVIRONMENT = 'production'

# 2. Reload extension
# chrome://extensions/ → Reload

# 3. Test on YouTube
# (Backend is already running on Cloud Run)
```

---

## ✅ Benefits

- 🎯 **Single source of truth** - Change one file, not five
- 🔄 **Easy switching** - Toggle between local/production
- 🛡️ **No mistakes** - Can't forget to update a file
- 📦 **Clean code** - No hardcoded URLs scattered everywhere

---

**That's it! Just edit `config.js` and reload the extension!** 🚀
