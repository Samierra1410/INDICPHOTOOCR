import os
import json

input_folder = "/Users/samierraarora/IndicPhotoOCR/IndicPhotoOCR/IndicPhotoOCR2/Outputs/ocr_output"
output_combined_json = os.path.join(input_folder, "Outputs/ocr_output/combined_ocr_output.json")

combined_data = {}

for file in sorted(os.listdir(input_folder)):
    if file.endswith(".json") and file != "Outputs/ocr_output/combined_ocr_output.json":
        file_path = os.path.join(input_folder, file)
        image_id = os.path.splitext(file)[0]
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # If it's a list (like your case)
            if isinstance(data, list):
                combined_data[image_id] = {"annotations": data}
                print(f"✅ Added {file}: {len(data)} items")
            else:
                print(f"⚠️ Skipped {file}: unexpected format {type(data)}")

        except Exception as e:
            print(f"❌ Could not process {file}: {e}")

with open(output_combined_json, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 Combined JSON saved to {output_combined_json}")
print(f"📊 Total files combined: {len(combined_data)}")





