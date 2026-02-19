# Google Cloud Vision API Setup Guide

This guide will help you set up Google Cloud Vision API for better handwritten Tamil text recognition.

## Why Google Cloud Vision?

- ✅ **Much better accuracy** for handwritten text (80-95% vs Tesseract's 40-60%)
- ✅ **Neural network-based** recognition
- ✅ **Supports Tamil script** natively
- ✅ **Free tier**: 1,000 OCR requests/month
- ✅ **Production-ready** with high reliability

## Setup Steps

### 1. Create a Google Cloud Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Accept the terms of service

### 2. Create a New Project

1. Click on the project dropdown at the top
2. Click **"New Project"**
3. Enter project name: `tamil-ocr` (or your choice)
4. Click **"Create"**

### 3. Enable Vision API

1. Go to [Vision API page](https://console.cloud.google.com/apis/library/vision.googleapis.com)
2. Make sure your project is selected
3. Click **"Enable"**

### 4. Create Service Account Credentials

1. Go to [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click **"Create Credentials"** → **"Service Account"**
3. Enter service account details:
   - Name: `tamil-ocr-service`
   - Click **"Create and Continue"**
4. Grant role: **"Project" → "Owner"** (or "Cloud Vision API User")
5. Click **"Continue"** → **"Done"**

### 5. Generate JSON Key

1. Click on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Choose **"JSON"**
5. Click **"Create"** - a JSON file will download

### 6. Save Credentials File

1. Rename the downloaded JSON file to: `google-credentials.json`
2. Save it in the project backend folder:
   ```
   C:\Users\gokulp\Desktop\tamil_extraction\NEW_extraction\backend\google-credentials.json
   ```

### 7. Set Environment Variable

**Option A: PowerShell (Current Session)**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\gokulp\Desktop\tamil_extraction\NEW_extraction\backend\google-credentials.json"
```

**Option B: System Environment Variable (Permanent)**
1. Press `Win + X` → **System**
2. Click **"Advanced system settings"**
3. Click **"Environment Variables"**
4. Under **"User variables"**, click **"New"**
5. Variable name: `GOOGLE_APPLICATION_CREDENTIALS`
6. Variable value: `C:\Users\gokulp\Desktop\tamil_extraction\NEW_extraction\backend\google-credentials.json`
7. Click **"OK"** on all dialogs

### 8. Restart Backend Server

**Stop the current server** (press Ctrl+C in the terminal)

**Start it again:**
```powershell
cd C:\Users\gokulp\Desktop\tamil_extraction\NEW_extraction
C:/Users/gokulp/Desktop/tamil_extraction/.venv/Scripts/python.exe backend/app.py
```

You should see: **"✅ Google Cloud Vision API enabled"**

## Testing

1. Upload a Tamil handwritten image to http://localhost:3000
2. Click "Extract Text"
3. You should see much better accuracy!

## Pricing

- **Free tier**: 1,000 requests/month
- **After free tier**: $1.50 per 1,000 requests
- **Your usage**: If you process 10 images/day = ~300/month (FREE)

## Troubleshooting

**❌ "Google Cloud Vision not configured"**
- Make sure `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set
- Verify the JSON file path is correct
- Restart the backend server after setting the variable

**❌ "Permission denied" error**
- Make sure Vision API is enabled for your project
- Check service account has correct permissions

**❌ "Quota exceeded"**
- You've used more than 1,000 requests this month
- Upgrade to paid tier or wait until next month
- System automatically falls back to Tesseract

## Fallback Behavior

If Google Cloud Vision is not configured or fails:
- ✅ System **automatically falls back** to Tesseract OCR
- ⚠️  Accuracy will be lower for handwriting
- ✅ No errors - system continues to work

## Security Note

🔒 **IMPORTANT**: Never commit `google-credentials.json` to Git!

The file is already added to `.gitignore` to prevent accidental commits.

---

**Need help?** Check the [Google Cloud Vision documentation](https://cloud.google.com/vision/docs/ocr)
