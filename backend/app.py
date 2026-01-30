from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import requests
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Sarvam API Configuration
SARVAM_API_KEY = "sk_d41xmh38_KcD1rFHkxPUC7szKimSU098l"
SARVAM_TRANSLATE_URL = "https://api.sarvam.ai/translate"

def extract_text_from_image(image):
    """Extract Tamil text using Tesseract OCR"""
    try:
        raw_text = pytesseract.image_to_string(image, lang='tam')
        return raw_text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def refine_text_with_sarvam(raw_text):
    """Refine text using Sarvam AI (Tamil→English→Tamil)"""
    if not raw_text or raw_text.strip() == "":
        return raw_text
    
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Step 1: Tamil to English
        payload_to_en = {
            "input": raw_text,
            "source_language_code": "ta-IN",
            "target_language_code": "en-IN",
            "speaker_gender": "Male",
            "mode": "formal",
            "model": "mayura:v1",
            "enable_preprocessing": True
        }
        
        response_en = requests.post(SARVAM_TRANSLATE_URL, headers=headers, json=payload_to_en, timeout=30)
        
        if response_en.status_code == 200:
            english_text = response_en.json().get("translated_text", "")
            
            # Step 2: English to Tamil
            payload_to_ta = {
                "input": english_text,
                "source_language_code": "en-IN",
                "target_language_code": "ta-IN",
                "speaker_gender": "Male",
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": True
            }
            
            response_ta = requests.post(SARVAM_TRANSLATE_URL, headers=headers, json=payload_to_ta, timeout=30)
            
            if response_ta.status_code == 200:
                return response_ta.json().get("translated_text", raw_text)
        
        return raw_text
    except Exception as e:
        print(f"Sarvam Error: {e}")
        return raw_text

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Tamil OCR API is running"})

@app.route('/api/ocr', methods=['POST'])
def process_ocr():
    """Process uploaded image and return OCR results"""
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        
        # Read image
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        
        # Extract text
        raw_text = extract_text_from_image(image)
        
        # Refine text
        refined_text = refine_text_with_sarvam(raw_text)
        
        # Convert image to base64 for preview
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "raw_text": raw_text,
            "refined_text": refined_text,
            "image_preview": f"data:image/png;base64,{img_str}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Tamil OCR API Server...")
    print("📍 Server running at: http://localhost:5000")
    print("🔗 API Endpoint: http://localhost:5000/api/ocr")
    app.run(debug=True, port=5000)
