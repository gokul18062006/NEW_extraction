from final_pipeline import process_user_image

# INSTRUCTIONS:
# 1. Place your Tamil image in this folder (C:\Users\gokulp\Desktop\extraction\)
# 2. Change the filename below to match your image name
# 3. Run: python process_my_image.py

# Change this to your image filename:
IMAGE_PATH = "sample_tamil.png"  # e.g., "tamil_handwritten.jpg", "scan.png", etc.

# Process the image
print("\n" + "="*70)
print("🖼️  PROCESSING YOUR IMAGE")
print("="*70)

try:
    result = process_user_image(IMAGE_PATH)
    
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)
    print(f"\n📄 Raw OCR Text:\n   {result['raw_text']}")
    print(f"\n✨ Refined Text (Sarvam AI):\n   {result['corrected_text']}")
    print("\n" + "="*70)
    
except FileNotFoundError:
    print(f"\n❌ ERROR: Image '{IMAGE_PATH}' not found!")
    print("\n💡 Please:")
    print(f"   1. Copy your image to: C:\\Users\\gokulp\\Desktop\\extraction\\")
    print(f"   2. Update IMAGE_PATH in this script")
    print("="*70)
except Exception as e:
    print(f"\n❌ ERROR: {e}")
