# Tamil OCR Web Application

Beautiful React + Tailwind CSS frontend with Flask backend for Tamil handwritten text recognition.

## 🎨 Features

- 📸 Drag & drop image upload
- 🔍 Real-time OCR processing
- ✨ AI-powered text refinement
- 📊 Statistics dashboard
- 📋 Copy to clipboard
- 🎯 Responsive design

## 🛠️ Tech Stack

**Frontend:**
- React 18
- Tailwind CSS
- Axios

**Backend:**
- Flask
- Tesseract OCR
- Sarvam AI
- Python 3.9+

## 📦 Installation

### Backend Setup

1. **Navigate to backend folder:**
```powershell
cd C:\Users\gokulp\Desktop\extraction\backend
```

2. **Install Python dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Start the Flask server:**
```powershell
python app.py
```

Server will run at: `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend folder:**
```powershell
cd C:\Users\gokulp\Desktop\extraction\frontend
```

2. **Install Node.js dependencies:**
```powershell
npm install
```

3. **Start the React development server:**
```powershell
npm start
```

Frontend will open at: `http://localhost:3000`

## 🚀 Usage

1. **Start Backend:**
   ```powershell
   cd backend
   python app.py
   ```

2. **Start Frontend (in new terminal):**
   ```powershell
   cd frontend
   npm start
   ```

3. **Open Browser:**
   - Go to `http://localhost:3000`
   - Upload a Tamil image
   - Click "Extract Text"
   - View results!

## 📁 Project Structure

```
extraction/
├── backend/
│   ├── app.py                  # Flask API server
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── index.js           # Entry point
│   │   └── index.css          # Tailwind styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── final_pipeline.py           # Original CLI pipeline
├── process_my_image.py         # CLI image processor
└── README.md
```

## 🔧 Prerequisites

- ✅ Python 3.9+
- ✅ Node.js 16+ and npm
- ✅ Tesseract OCR installed with Tamil language data
- ✅ Sarvam AI API key (already configured)

## 🎯 API Endpoints

### Health Check
```
GET http://localhost:5000/api/health
```

### OCR Processing
```
POST http://localhost:5000/api/ocr
Content-Type: multipart/form-data
Body: image file
```

**Response:**
```json
{
  "success": true,
  "raw_text": "Tamil text from OCR",
  "refined_text": "Refined Tamil text",
  "image_preview": "data:image/png;base64,..."
}
```

## 🎨 UI Features

- **Drag & Drop Zone** - Easy image upload
- **Image Preview** - See uploaded image before processing
- **Loading States** - Visual feedback during processing
- **Results Display** - Side-by-side comparison of raw and refined text
- **Statistics** - Character count and metrics
- **Copy Button** - Quick copy to clipboard
- **Responsive Design** - Works on all screen sizes

## 🐛 Troubleshooting

**Backend not starting:**
- Make sure Tesseract is installed
- Check if port 5000 is available
- Verify Python dependencies are installed

**Frontend not connecting:**
- Ensure backend is running on port 5000
- Check CORS is enabled in Flask
- Verify API URL in App.js

**OCR not working:**
- Confirm Tesseract path in app.py
- Check Tamil language data is installed
- Test with `python test_tesseract.py`

## 📝 Notes

- Backend must be running before starting frontend
- Sarvam AI requires internet connection
- Larger images may take longer to process
- Supported formats: JPG, PNG, JPEG

## 🚀 Production Deployment

For production:
1. Build React app: `npm run build`
2. Serve static files with Flask
3. Use production WSGI server (Gunicorn/uWSGI)
4. Configure proper CORS policies
5. Add authentication if needed

---

Made with ❤️ for Tamil text recognition
