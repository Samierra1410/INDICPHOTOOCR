import json
import csv
from indic_transliteration.sanscript import transliterate, SCHEMES

# Load the annotated JSON file
json_path = "/Users/samierraarora/Desktop/IIT JODHPUR/Final_final/image_1.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract the inner dictionary
annotations = data["original_pic 2"]["annotations"]

# Mapping language names to scheme (as expected by indic-transliteration)
lang_map = {
    "Hindi": "devanagari",
    "Marathi": "devanagari",
    "Gujarati": "gujarati",
    "Punjabi": "gurmukhi",
    "Bengali": "bengali",
    "Tamil": "tamil",
    "Telugu": "telugu",
    "Kannada": "kannada",
    "Malayalam": "malayalam",
    "English": None  # No transliteration
}

output_rows = []
image_name = "pic_2.jpg"

for polygon_id, info in annotations.items():
    text = info.get("text", "").strip()
    lang = info.get("script_language", "").strip()

    # Check if transliteration is needed
    if lang in lang_map and lang_map[lang]:
        recognized_text = transliterate(text, "iast", lang_map[lang])
    else:
        recognized_text = text  # Keep English or unknown language as-is

    output_rows.append([image_name, polygon_id, lang, recognized_text])

# Write to CSV
output_path = "ocr_results.csv"
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["image_name", "polygon_id", "script_language", "recognized_text"])
    writer.writerows(output_rows)

print(f"✅ Done. CSV saved to {output_path}")
