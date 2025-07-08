import os
import json
from IndicPhotoOCR.ocr import OCR

# Define your image folder and output folder
image_folder = "/Users/samierraarora/IndicPhotoOCR/IndicPhotoOCR/IndicPhotoOCR2/og_pics"
output_folder = "/Users/samierraarora/IndicPhotoOCR/IndicPhotoOCR/IndicPhotoOCR2/output_final"
os.makedirs(output_folder, exist_ok=True)

# Create OCR object
ocr_system = OCR(verbose=True, identifier_lang="auto", device="cpu")

# Supported image extensions
valid_exts = (".jpg", ".jpeg", ".png")

# Iterate over each file in the folder
for filename in os.listdir(image_folder):
    if filename.lower().endswith(valid_exts):
        image_path = os.path.join(image_folder, filename)
        print(f"\nProcessing: {image_path}")
        
        # Run OCR
        try:
            result = ocr_system.ocr(image_path)
        except Exception as e:
            print(f" Failed on {filename}: {e}")
            continue
        
        # Save JSON output
        json_name = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(output_folder, json_name)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f" Saved to: {json_path}")
