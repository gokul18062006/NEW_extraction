from paddleocr import PaddleOCR
from PIL import Image
import requests
import json
from datasets import load_dataset
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Sarvam API Configuration
SARVAM_API_KEY = "sk_d41xmh38_KcD1rFHkxPUC7szKimSU098l"
SARVAM_API_URL = "https://api.sarvam.ai/translate"

class TamilOCRPipeline:
    def __init__(self):
        print("Loading PaddleOCR for Tamil...")
        # Initialize PaddleOCR with Tamil language
        self.ocr = PaddleOCR(lang='ta', use_angle_cls=True)
        print("✅ PaddleOCR loaded successfully!")
        
    def extract_text_from_image(self, image):
        """Extract text from image using PaddleOCR"""
        print("\n[Step 1] Processing image through PaddleOCR...")
        
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image_np = np.array(image)
        else:
            image_np = image
        
        # Extract text
        results = self.ocr.ocr(image_np, cls=True)
        
        # Combine all detected text
        if results and results[0]:
            raw_text = " ".join([line[1][0] for line in results[0]])
        else:
            raw_text = ""
        
        print(f"[PaddleOCR] Raw Text: {raw_text}")
        if results and results[0]:
            print(f"[Confidence] Detected {len(results[0])} text regions")
        
        return raw_text
    
    def correct_text_with_sarvam(self, raw_text):
        """Correct text using Sarvam AI API"""
        print("\n[Step 2] Correcting text with Sarvam AI...")
        
        if not raw_text or raw_text.strip() == "":
            print("[Warning] No text to correct")
            return raw_text
        
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Sarvam API payload - Tamil to Tamil translation for text refinement
        payload = {
            "input": raw_text,
            "source_language_code": "ta-IN",
            "target_language_code": "ta-IN",
            "speaker_gender": "Male",
            "mode": "formal",
            "model": "mayura:v1",
            "enable_preprocessing": True
        }
        
        try:
            response = requests.post(
                SARVAM_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                corrected_text = result.get("translated_text", raw_text)
                print(f"[Sarvam] Corrected Text: {corrected_text}")
                return corrected_text
            else:
                print(f"[Sarvam Error] Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                print("✋ Using raw text as fallback...")
                return raw_text
                
        except Exception as e:
            print(f"[Sarvam Error] {str(e)}")
            print("✋ Using raw text as fallback...")
            return raw_text
    
    def process_image(self, image):
        """Complete pipeline: Image -> PaddleOCR -> Sarvam -> Clean Text"""
        print("\n" + "="*70)
        print("🚀 STARTING TAMIL OCR PIPELINE")
        print("="*70)
        
        # Step 1: Extract text with PaddleOCR
        raw_text = self.extract_text_from_image(image)
        
        # Step 2: Correct with Sarvam
        corrected_text = self.correct_text_with_sarvam(raw_text)
        
        print("\n" + "="*70)
        print("✅ PIPELINE COMPLETED")
        print("="*70)
        print(f"\n📄 RAW TEXT (PaddleOCR):   {raw_text}")
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
        print(f"  PaddleOCR Output:    {result['raw_text']}")
        print(f"  Sarvam Output:       {result['corrected_text']}")
        
        # Simple similarity check
        if result['raw_text'].strip() == ground_truth.strip():
            print(f"  ✅ PERFECT MATCH!")
        elif ground_truth.strip() in result['raw_text'] or result['raw_text'] in ground_truth:
            print(f"  🟡 PARTIAL MATCH")
        else:
            print(f"  ⚠️  Different output")
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

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌟 TAMIL HANDWRITTEN TEXT RECOGNITION SYSTEM 🌟")
    print("="*70)
    print("Pipeline: Image → PaddleOCR → Sarvam AI → Clean Text")
    print("="*70 + "\n")
    
    # Test with dataset
    test_with_dataset()
    
    print("\n" + "="*70)
    print("💡 TO PROCESS YOUR OWN IMAGE:")
    print("="*70)
    print("  result = process_user_image('path/to/your/tamil_image.jpg')")
    print("  print(f'Final Output: {result[\"corrected_text\"]}')")
    print("="*70 + "\n")
