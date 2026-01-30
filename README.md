# Tamil Handwritten Text Recognition System

🌟 **AI-Powered Tamil OCR with Web Interface** 🌟

## Overview
This project implements a two-stage pipeline for Tamil handwritten text recognition with both **CLI** and **Web Interface** options:

1. **Stage 1**: OCR (Optical Character Recognition) - Extract raw text from images using Tesseract
2. **Stage 2**: Text Correction with Sarvam AI - Clean and correct the OCR output via Tamil→English→Tamil translation

## 🚀 Features

✅ **Dual Interface**: Command-line and beautiful web UI  
✅ **High Accuracy**: Tesseract OCR + Sarvam AI refinement  
✅ **Dataset Included**: 7,000 Tamil images for testing  
✅ **Real-time Processing**: Fast OCR with AI correction  
✅ **Modern UI**: React + Tailwind CSS responsive design  

## Pipeline Architecture
```
User Uploads Tamil Image
         ↓
   Tesseract OCR (Tamil Language Model)
         ↓
   Raw Tamil Text (may contain errors)
         ↓
   Sarvam AI API (Tamil→English→Tamil)
         ↓
   Clean & Corrected Tamil Text
```

## 📁 Project Structure

```
extraction/
├── backend/                    # Flask API server
│   ├── app.py                 # REST API endpoints
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React web application
│   ├── src/
│   │   ├── App.js            # Main UI component
│   │   ├── index.js          # Entry point
│   │   └── index.css         # Tailwind styles
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── final_pipeline.py          # CLI pipeline (main)
├── process_my_image.py        # CLI image processor
├── load_dataset.py            # Dataset loader & viewer
├── test_tesseract.py          # Tesseract verification
├── README.md                  # This file
└── WEB_APP_README.md          # Detailed web app setup
```

## 🛠️ Installation

### Prerequisites

1. **Python 3.9+**
2. **Node.js 16+ and npm** (for web interface)
3. **Tesseract OCR with Tamil language data**

### Step 1: Install Tesseract OCR

Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

**⚠️ IMPORTANT**: During installation, select **Tamil (tam)** language data!

**Verify installation:**
```powershell
python test_tesseract.py
```

You should see: ✅ SUCCESS! Tamil language is installed!

### Step 2: Install Python Dependencies

```powershell
pip install transformers torch pillow requests datasets pytesseract flask flask-cors
```

### Step 3: Install Frontend Dependencies (Optional - for Web UI)

```powershell
cd frontend
npm install
```

## 🎯 Usage Options

### Option 1: Command Line Interface (CLI)

**Test with dataset images:**
```powershell
python final_pipeline.py
```

**Process your own image:**
1. Copy your Tamil image to the `extraction` folder
2. Edit `process_my_image.py` line 9:
   ```python
   IMAGE_PATH = "your_image.jpg"
   ```
3. Run:
   ```powershell
   python process_my_image.py
   ```

**Or use Python directly:**
```python
from final_pipeline import process_user_image

result = process_user_image("your_tamil_image.jpg")
print(f"Raw OCR: {result['raw_text']}")
print(f"Corrected: {result['corrected_text']}")
```

### Option 2: Web Interface (Recommended)

**1. Start Backend Server:**
```powershell
cd backend
python app.py
```
Server runs at: `http://localhost:5000`

**2. Start Frontend (in new terminal):**
```powershell
cd frontend
npm start
```
App opens at: `http://localhost:3000`

**3. Use the Web Interface:**
- Drag & drop Tamil images
- Click "Extract Text"
- View results with side-by-side comparison
- Copy refined text to clipboard

📖 **See [WEB_APP_README.md](WEB_APP_README.md) for detailed web setup instructions**

## 📊 Dataset

- **Source**: Hugging Face - `Nevidu/tamil_synthetic_ocr`
- **Size**: 7,000 Tamil text images
- **Format**: PNG images with ground truth Tamil text
- **Purpose**: Testing, validation, and fine-tuning

**Load and explore dataset:**
```powershell
python load_dataset.py
```

## 🔧 API Configuration

The project uses **Sarvam AI** for Tamil text refinement:
- Translation API for text correction
- Tamil→English→Tamil pipeline for best results
- API key is pre-configured in the code

## 📱 Web UI Features

- 📸 **Drag & Drop Upload** - Easy image selection
- 🔄 **Real-time Processing** - Live OCR with loading states
- 📊 **Statistics Dashboard** - Character counts and metrics
- 📋 **Copy to Clipboard** - One-click text copying
- 🎨 **Beautiful Design** - Modern gradient UI with Tailwind CSS
- 📱 **Responsive** - Works on desktop, tablet, and mobile

## 🧪 Testing

**Test Tesseract installation:**
```powershell
python test_tesseract.py
```

**Test with dataset images:**
```powershell
python final_pipeline.py
```

**Test web API:**
```powershell
# Start backend
cd backend
python app.py

# In browser, visit:
http://localhost:5000/api/health
```

## 🐛 Troubleshooting

**"TesseractNotFoundError"**
- Install Tesseract from the link above
- Update path in `final_pipeline.py` line 11

**"Tamil language not found"**
- Reinstall Tesseract
- Check ☑ Tamil (tam) during installation

**Web app not connecting:**
- Ensure backend is running on port 5000
- Start frontend after backend
- Check CORS is enabled

**Sarvam API errors:**
- Check internet connection
- Verify API key is valid
- Falls back to raw OCR if API fails

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Test Tesseract | `python test_tesseract.py` |
| CLI Processing | `python process_my_image.py` |
| Load Dataset | `python load_dataset.py` |
| Start Backend | `cd backend && python app.py` |
| Start Frontend | `cd frontend && npm start` |
| Build Frontend | `cd frontend && npm run build` |

## 🚀 Future Improvements

- [ ] Fine-tune TrOCR model on Tamil dataset
- [ ] Add confidence scores for OCR results
- [ ] Implement batch processing for multiple images
- [x] ✅ Add web interface (React + Tailwind)
- [ ] Mobile app version
- [ ] PDF document support
- [ ] User authentication for web app

## 📄 License

This project is for educational and research purposes.

## 🙏 Acknowledgments

- **Tesseract OCR** - Open-source OCR engine
- **Sarvam AI** - Tamil language processing
- **Hugging Face** - Dataset hosting
- **React & Tailwind CSS** - Frontend framework



cd backend
python app.py


cd frontend
npm start