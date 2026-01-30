from PIL import Image
import requests
import json
from datasets import load_dataset
import pytesseract

# NOTE: Make sure Tesseract is installed on your system
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# After installation, set the path below if needed:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Sarvam API Configuration
SARVAM_API_KEY = "sk_d41xmh38_KcD1rFHkxPUC7szKimSU098l"
# Using English translation for text refinement (Tamil->English->Tamil gives better correction)
SARVAM_TRANSLATE_URL = "https://api.sarvam.ai/translate"

class TamilOCRPipeline:
    def __init__(self):
        print("✅ Tamil OCR Pipeline initialized!")
        # Try to set Tesseract path if it exists
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        except:
            pass
        
    def extract_text_from_image(self, image):
        """Extract text from image using Tesseract OCR"""
        print("\n[Step 1] Processing image through Tesseract OCR...")
        
        try:
            # Extract Tamil text using Tesseract
            raw_text = pytesseract.image_to_string(image, lang='tam')
            raw_text = raw_text.strip()
            
            print(f"[Tesseract OCR] Raw Text: {raw_text}")
            return raw_text
        except Exception as e:
            print(f"[Tesseract Error] {str(e)}")
            print("Note: Please install Tesseract OCR and Tamil language data")
            print("Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            return ""
    
    def correct_text_with_sarvam(self, raw_text):
        """Correct text using Sarvam AI API - Translate to English and back for correction"""
        print("\n[Step 2] Refining text with Sarvam AI (Tamil→English→Tamil)...")
        
        if not raw_text or raw_text.strip() == "":
            print("[Warning] No text to correct")
            return raw_text
        
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            # Step 2a: Translate Tamil to English (helps identify and fix OCR errors)
            payload_to_en = {
                "input": raw_text,
                "source_language_code": "ta-IN",
                "target_language_code": "en-IN",
                "speaker_gender": "Male",
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": True
            }
            
            response_en = requests.post(
                SARVAM_TRANSLATE_URL,
                headers=headers,
                json=payload_to_en,
                timeout=30
            )
            
            if response_en.status_code == 200:
                english_text = response_en.json().get("translated_text", "")
                print(f"[Sarvam] English translation: {english_text}")
                
                # Step 2b: Translate back to Tamil (refined version)
                payload_to_ta = {
                    "input": english_text,
                    "source_language_code": "en-IN",
                    "target_language_code": "ta-IN",
                    "speaker_gender": "Male",
                    "mode": "formal",
                    "model": "mayura:v1",
                    "enable_preprocessing": True
                }
                
                response_ta = requests.post(
                    SARVAM_TRANSLATE_URL,
                    headers=headers,
                    json=payload_to_ta,
                    timeout=30
                )
                
                if response_ta.status_code == 200:
                    corrected_text = response_ta.json().get("translated_text", raw_text)
                    print(f"[Sarvam] Refined Tamil: {corrected_text}")
                    return corrected_text
            
            print(f"[Sarvam] Could not refine text, using OCR output")
            return raw_text
                
        except Exception as e:
            print(f"[Sarvam Error] {str(e)}")
            print("✋ Using raw text as fallback...")
            return raw_text
    
    def process_image(self, image):
        """Complete pipeline: Image -> Tesseract OCR -> Sarvam -> Clean Text"""
        print("\n" + "="*70)
        print("🚀 STARTING TAMIL OCR PIPELINE")
        print("="*70)
        
        # Step 1: Extract text with Tesseract
        raw_text = self.extract_text_from_image(image)
        
        # Step 2: Correct with Sarvam
        corrected_text = self.correct_text_with_sarvam(raw_text)
        
        print("\n" + "="*70)
        print("✅ PIPELINE COMPLETED")
        print("="*70)
        print(f"\n📄 RAW TEXT (Tesseract):   {raw_text}")
        print(f"✨ CORRECTED TEXT (Sarvam): {corrected_text}")
        print("="*70 + "\n")
        
        return {
            "raw_text": raw_text,
            "corrected_text": corrected_text
        }

def test_with_dataset():
    """Test pipeline with images from the loaded dataset"""
    print("📦 Loading Tamil OCR dataset...")
    dataset = load_dataset("Nevidu/tamil_synthetic_ocr")
    
    # Initialize pipeline
    pipeline = TamilOCRPipeline()
    
    # Test with first 3 images from dataset
    print("\n\n🧪 Testing with dataset images...\n")
    
    for i in range(3):
        example = dataset['data'][i]
        image = example['image']
        ground_truth = example['text']
        
        print(f"\n{'='*70}")
        print(f"📸 TEST IMAGE #{i+1}")
        print(f"{'='*70}")
        print(f"🎯 GROUND TRUTH: {ground_truth}")
        
        # Process image
        result = pipeline.process_image(image)
        
        # Compare
        print(f"\n📊 COMPARISON:")
        print(f"  Ground Truth:        {ground_truth}")
        print(f"  Tesseract Output:    {result['raw_text']}")
        print(f"  Sarvam Output:       {result['corrected_text']}")
        
        # Simple similarity check
        if result['raw_text'].strip() == ground_truth.strip():
            print(f"  ✅ PERFECT MATCH!")
        else:
            print(f"  ⚠️  Needs improvement/fine-tuning")
        print("\n")

def process_user_image(image_path):
    """Process a user-uploaded image"""
    print(f"\n🖼️  Processing user image: {image_path}\n")
    pipeline = TamilOCRPipeline()
    
    # Load image
    image = Image.open(image_path).convert("RGB")
    
    # Process
    result = pipeline.process_image(image)
    
    return result

def save_sample_image_for_testing():
    """Save a sample image from dataset for testing user upload"""
    print("📥 Saving sample image for testing...")
    dataset = load_dataset("Nevidu/tamil_synthetic_ocr")
    sample_image = dataset['data'][0]['image']
    sample_image.save("sample_tamil.png")
    print("✅ Saved as 'sample_tamil.png'")
    return "sample_tamil.png"

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌟 TAMIL HANDWRITTEN TEXT RECOGNITION SYSTEM 🌟")
    print("="*70)
    print("Pipeline: Image → Tesseract OCR → Sarvam AI → Clean Text")
    print("="*70 + "\n")
    
    # Test with dataset
    test_with_dataset()
    
    # Save a sample image
    sample_path = save_sample_image_for_testing()
    
    print("\n" + "="*70)
    print("💡 TO PROCESS YOUR OWN IMAGE:")
    print("="*70)
    print(f"  result = process_user_image('{sample_path}')")
    print("  print(f'Final Output: {{result[\"corrected_text\"]}}')")
    print("\n  Or upload your own Tamil handwritten image:")
    print("  result = process_user_image('your_image.jpg')")
    print("="*70 + "\n")
