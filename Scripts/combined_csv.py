import json
import unicodedata
import csv
from difflib import SequenceMatcher
from indic_transliteration.sanscript import transliterate, DEVANAGARI, ITRANS

# === CONFIGURATION ===
gt_path = "/Users/samierraarora/IndicPhotoOCR/IndicPhotoOCR/IndicPhotoOCR2/Annotations/annotated_files.json"
ocr_path = "/Users/samierraarora/IndicPhotoOCR/IndicPhotoOCR/IndicPhotoOCR2/Outputs/ocr_output/combined_ocr_output.json"
similarity_threshold = 0.6

def normalize_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return ''.join(ch for ch in text if ch.isalnum()).lower()

def is_similar(a, b, threshold=similarity_threshold):
    return SequenceMatcher(None, a, b).ratio() >= threshold

# === LOAD FILES ===
with open(gt_path, "r", encoding="utf-8") as f:
    gt_data = json.load(f)
with open(ocr_path, "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

# === STATS ===
overall_total_gt = 0
overall_correct = 0
per_image_data = []

for image_name, gt_entry in gt_data.items():
    gt_annotations = gt_entry.get("annotations", {})
    total_gt = 0
    correct = 0

    flat_ocr_words = []
    ocr_entry = ocr_data.get(image_name, {})
    ocr_annotations_list = []
    if isinstance(ocr_entry, dict) and "annotations" in ocr_entry:
        ocr_annotations_list = ocr_entry["annotations"]
    elif isinstance(ocr_entry, list):
        ocr_annotations_list = ocr_entry

    for ocr_words in ocr_annotations_list:
        for word in ocr_words:
            if isinstance(word, str):
                nw = normalize_text(word)
                if nw and not nw.isdigit():
                    flat_ocr_words.append(nw)

    for poly_key, gt_poly in gt_annotations.items():
        gt_text = normalize_text(gt_poly.get("text", ""))
        if len(gt_text) <= 2 or gt_text.isdigit():
            continue

        gt_lang = gt_poly.get("script_language", "").lower()
        if not gt_lang:
            if any('\u0900' <= c <= '\u097F' for c in gt_poly.get("text", "")):
                gt_lang = "hindi"
            else:
                gt_lang = "english"

        if gt_lang in ["hindi", "marathi"]:
            gt_translit = normalize_text(transliterate(gt_text, DEVANAGARI, ITRANS))
        else:
            gt_translit = gt_text

        total_gt += 1
        overall_total_gt += 1

        match_found = False
        # Try singles
        for ocr_word in flat_ocr_words:
            try:
                if gt_lang in ["hindi", "marathi"]:
                    ocr_trans = normalize_text(transliterate(ocr_word, DEVANAGARI, ITRANS))
                else:
                    ocr_trans = ocr_word
                if ocr_trans == gt_translit or is_similar(ocr_trans, gt_translit):
                    match_found = True
                    break
            except Exception:
                continue

        # Try bigrams
        if not match_found and len(flat_ocr_words) > 1:
            for i in range(len(flat_ocr_words) - 1):
                combined = flat_ocr_words[i] + flat_ocr_words[i+1]
                try:
                    if gt_lang in ["hindi", "marathi"]:
                        combined_trans = normalize_text(transliterate(combined, DEVANAGARI, ITRANS))
                    else:
                        combined_trans = combined
                    if combined_trans == gt_translit or is_similar(combined_trans, gt_translit):
                        match_found = True
                        break
                except Exception:
                    continue

        # Try trigrams
        if not match_found and len(flat_ocr_words) > 2:
            for i in range(len(flat_ocr_words) - 2):
                triple = flat_ocr_words[i] + flat_ocr_words[i+1] + flat_ocr_words[i+2]
                try:
                    if gt_lang in ["hindi", "marathi"]:
                        triple_trans = normalize_text(transliterate(triple, DEVANAGARI, ITRANS))
                    else:
                        triple_trans = triple
                    if triple_trans == gt_translit or is_similar(triple_trans, gt_translit):
                        match_found = True
                        break
                except Exception:
                    continue

        if match_found:
            correct += 1
            overall_correct += 1
        else:
            print(f"❌ MISMATCH: GT='{gt_text}' ({gt_lang}) vs OCR='{flat_ocr_words}' in {image_name}")

    wrr = (correct / total_gt) if total_gt else 0
    per_image_data.append({
        "Image Name": image_name,
        "Total Words": total_gt,
        "Recognized Words": correct,
        "Word Recognition Rate": round(wrr, 4)
    })

# === OVERALL WRR CALC ===
overall_wrr = (overall_correct / overall_total_gt) if overall_total_gt else 0
overall_wrr_percent = (overall_wrr * 100)

# === WRITE CSV ===
with open("wrr_per_image.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Image Name", "Total Words", "Recognized Words", "Word Recognition Rate (%)"])
    for record in per_image_data:
        wrr_percent = f"{record['Word Recognition Rate']*100:.2f}%"
        writer.writerow([
            record['Image Name'],
            record['Total Words'],
            record['Recognized Words'],
            wrr_percent
        ])
    writer.writerow([])
    writer.writerow([
        "TOTAL / AVERAGE",
        overall_total_gt,
        overall_correct,
        f"{overall_wrr_percent:.2f}%"
    ])

# === PRINT SUMMARY ===
print(f"\n✅ Completed writing to wrr_per_image.csv")
print(f"Total Ground Truth Words: {overall_total_gt}")
print(f"Total Correctly Recognized Words: {overall_correct}")
print(f"Overall WRR: {overall_wrr_percent:.2f}%")

# === WRITE MARKDOWN TABLE ===
with open("wrr_table.md", "w", encoding="utf-8") as mdfile:
    mdfile.write("| Image Name | Total Words | Recognized Words | Word Recognition Rate (%) |\n")
    mdfile.write("|------------|-------------|------------------|---------------------------|\n")
    
    for record in per_image_data:
        wrr_percent = f"{record['Word Recognition Rate']*100:.2f}%"
        mdfile.write(f"| {record['Image Name']} | {record['Total Words']} | {record['Recognized Words']} | {wrr_percent} |\n")
    
    mdfile.write(f"| **TOTAL / AVERAGE** | **{overall_total_gt}** | **{overall_correct}** | **{overall_wrr_percent:.2f}%** |\n")

print(f"\n✅ Also wrote wrr_table.md for GitHub Markdown table format.")





