from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import requests
import io
import base64
import cv2
import numpy as np
import os
from google.cloud import vision
from google.oauth2 import service_account

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Sarvam API Configuration
SARVAM_API_KEY = "sk_d41xmh38_KcD1rFHkxPUC7szKimSU098l"
SARVAM_TRANSLATE_URL = "https://api.sarvam.ai/translate"

# Google Cloud Vision configuration
# Set this to your Google Cloud credentials JSON file path
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)
USE_GOOGLE_VISION = os.path.exists(GOOGLE_CREDENTIALS_PATH) if GOOGLE_CREDENTIALS_PATH else False

# Initialize Google Vision client if credentials are available
try:
    if USE_GOOGLE_VISION:
        vision_client = vision.ImageAnnotatorClient()
        print("✅ Google Cloud Vision API enabled")
    else:
        vision_client = None
        print("⚠️  Google Cloud Vision not configured. Using Tesseract only.")
except Exception as e:
    vision_client = None
    USE_GOOGLE_VISION = False
    print(f"⚠️  Google Cloud Vision initialization failed: {e}")

def preprocess_image(image):
    """Enhance image quality for better OCR"""
    # Convert PIL to OpenCV format
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding for better contrast
    threshold = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(threshold, None, 10, 7, 21)
    
    # Convert back to PIL Image
    return Image.fromarray(denoised)

def extract_text_with_google_vision(image):
    """Extract text using Google Cloud Vision API (Best for handwriting)"""
    try:
        if not USE_GOOGLE_VISION or vision_client is None:
            return None
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create Vision API image object
        vision_image = vision.Image(content=img_byte_arr)
        
        # Perform text detection with language hints for Tamil
        response = vision_client.document_text_detection(
            image=vision_image,
            image_context={"language_hints": ["ta"]}
        )
        
        if response.error.message:
            raise Exception(response.error.message)
        
        # Extract full text
        if response.full_text_annotation:
            return response.full_text_annotation.text.strip()
        
        return None
        
    except Exception as e:
        print(f"Google Vision Error: {e}")
        return None

def extract_text_with_tesseract(image):
    """Extract Tamil text using Tesseract OCR with preprocessing"""
    try:
        # Preprocess image for better accuracy
        processed_image = preprocess_image(image)
        
        # Configure Tesseract for better handwriting recognition
        custom_config = r'--oem 3 --psm 6'
        
        raw_text = pytesseract.image_to_string(
            processed_image, 
            lang='tam',
            config=custom_config
        )
        return raw_text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_image(image):
    """Extract Tamil text using Google Vision (primary) or Tesseract (fallback)"""
    # Try Google Cloud Vision first (better for handwriting)
    if USE_GOOGLE_VISION:
        google_text = extract_text_with_google_vision(image)
        if google_text:
            print("✅ Used Google Cloud Vision API")
            return google_text
    
    # Fallback to Tesseract
    print("⚠️  Using Tesseract OCR (fallback)")
    return extract_text_with_tesseract(image)

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
