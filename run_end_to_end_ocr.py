from IndicPhotoOCR.ocr import OCR
import csv

# === CONFIG ===
image_path = "test_images/pic_2.jpg"  # update to your image path
output_csv = "ocr_results_from_image.csv"

# === RUN OCR ===
ocr_system = OCR(verbose=True, identifier_lang="auto")  # uses CPU by default
results = ocr_system.ocr(image_path)

# === WRITE CSV ===
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_name", "polygon_id", "script_language", "recognized_text"])
    for idx, item in enumerate(results):
        writer.writerow([image_path, f"polygon_{idx}", item.get("lang", ""), item.get("text", "")])

print(f"\n✅ Done. Output saved to {output_csv}")
