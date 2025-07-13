import os
from PIL import Image, ImageDraw, ImageOps
from IndicPhotoOCR.ocr import OCR

# === CONFIGURATION ===
ocr_system = OCR(verbose=True, device="cpu")
input_folder = "/Users/samierraarora/INDICPHOTOOCR-2/Original_photos"
output_folder = "/Users/samierraarora/INDICPHOTOOCR-2/Outputs/detected_outputs"
os.makedirs(output_folder, exist_ok=True)

# === PROCESS EACH IMAGE ===
for file in os.listdir(input_folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(input_folder, file)
        print(f"\n🔍 Processing: {image_path}")

        detections = ocr_system.detect(image_path)

        # Open image, fix rotation via EXIF
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)  # ✅ fixes orientation based on EXIF
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)

        for det in detections:
            if isinstance(det, list) and len(det) >= 3:
                flat_coords = [tuple(point) for point in det]
                xs = [p[0] for p in flat_coords]
                ys = [p[1] for p in flat_coords]
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)
                draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="green", width=3)

        output_path = os.path.join(output_folder, file)
        img.save(output_path)
        print(f"✅ Saved to: {output_path}")








