import pytesseract
from PIL import Image

# Set Tesseract path (update if your installation path is different)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    # Check if Tesseract is working
    print("Testing Tesseract installation...\n")
    print("Tesseract version:")
    print(pytesseract.get_tesseract_version())
    
    # Check available languages
    print("\nAvailable languages:")
    langs = pytesseract.get_languages()
    print(langs)
    
    if 'tam' in langs:
        print("\n✅ SUCCESS! Tamil language is installed!")
        print("\nYou can now run: python final_pipeline.py")
    else:
        print("\n❌ ERROR: Tamil language not found!")
        print("Please reinstall Tesseract and select Tamil language data.")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure Tesseract is installed")
    print("2. Check the path in this script matches your installation")
    print("3. Reinstall and select Tamil language data")
