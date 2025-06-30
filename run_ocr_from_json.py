import json
import csv
from indic_transliteration.sanscript import transliterate

# === CONFIG ===
json_path = "/Users/samierraarora/Desktop/IIT JODHPUR/Final_final/image_1.json"
image_name = "pic_2.jpg"
output_csv = "ocr_results.csv"

# === Language mapping ===
language_map = {
    "Hindi": "devanagari",
    "Marathi": "devanagari",
    "Punjabi": "gurmukhi",
    "Gujarati": "gujarati",
    "Tamil": "tamil",
    "Telugu": "telugu",
    "Kannada": "kannada",
    "Malayalam": "malayalam",
    "Bengali": "bengali",
    "Assamese": "bengali",
    "Odia": "oriya",
    "Urdu": "arabic",
    "English": None
}

# === Load JSON ===
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

key = list(data.keys())[0]
annotations = data[key]["annotations"]

# === Write CSV ===
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_name", "polygon_id", "script_language", "recognized_text"])

    for polygon_id, polygon_data in annotations.items():
        text = polygon_data.get("text", "").strip()
        lang = polygon_data.get("script_language", "").strip()

        if not text:
            recognized_text = ""
        elif lang == "English":
            recognized_text = text
        else:
            target_script = language_map.get(lang)
            if target_script:
                recognized_text = transliterate(text, "itrans", target_script)
            else:
                recognized_text = text

        writer.writerow([image_name, polygon_id, lang, recognized_text])

print(f"✅ Done. Output saved to {output_csv}")






































