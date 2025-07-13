import json
import unicodedata
import csv
from difflib import SequenceMatcher

# === CONFIGURATION ===
gt_path = "/Users/samierraarora/INDICPHOTOOCR-2/Annotations/annotated_files.json"
ocr_path = "/Users/samierraarora/INDICPHOTOOCR-2/Outputs/ocr_outputs/combined_output.json"
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

# === OVERALL STATS ===
overall_total_gt = 0
overall_correct = 0
per_image_data = []

for image_name, gt_entry in gt_data.items():
    gt_annotations = gt_entry.get("annotations", {})
    total_gt = 0
    correct = 0

    # Flatten OCR words
    flat_ocr_words = []
    ocr_entry = ocr_data.get(image_name, {})
    ocr_annotations_list = ocr_entry.get("annotations", []) if isinstance(ocr_entry, dict) else ocr_entry
    for ocr_words in ocr_annotations_list:
        for word in ocr_words:
            nw = normalize_text(word)
            if nw and not nw.isdigit():
                flat_ocr_words.append(nw)

    # Compare each GT
    for poly_key, gt_poly in gt_annotations.items():
        gt_text = normalize_text(gt_poly.get("text", ""))
        if len(gt_text) <= 2 or gt_text.isdigit():
            continue

        total_gt += 1
        overall_total_gt += 1

        match_found = False

        # Try single words
        for ocr_word in flat_ocr_words:
            if ocr_word == gt_text or is_similar(ocr_word, gt_text):
                match_found = True
                break

        # Try bigrams
        if not match_found and len(flat_ocr_words) > 1:
            for i in range(len(flat_ocr_words) - 1):
                combined = flat_ocr_words[i] + flat_ocr_words[i+1]
                if combined == gt_text or is_similar(combined, gt_text):
                    match_found = True
                    break

        # Try trigrams
        if not match_found and len(flat_ocr_words) > 2:
            for i in range(len(flat_ocr_words) - 2):
                triple = flat_ocr_words[i] + flat_ocr_words[i+1] + flat_ocr_words[i+2]
                if triple == gt_text or is_similar(triple, gt_text):
                    match_found = True
                    break

        if match_found:
            correct += 1
            overall_correct += 1
        else:
            print(f"❌ MISMATCH: GT='{gt_text}' vs OCR='{flat_ocr_words}' in {image_name}")

    wrr = (correct / total_gt) if total_gt else 0
    per_image_data.append({
        "Image Name": image_name,
        "Total Words": total_gt,
        "Recognized Words": correct,
        "Word Recognition Rate": round(wrr, 4)
    })

# === OVERALL WRR
overall_wrr = (overall_correct / overall_total_gt) if overall_total_gt else 0
overall_wrr_percent = (overall_wrr * 100)

# === WRITE CSV
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

# === WRITE MARKDOWN
with open("wrr_table.md", "w", encoding="utf-8") as mdfile:
    mdfile.write("| Image Name | Total Words | Recognized Words | Word Recognition Rate (%) |\n")
    mdfile.write("|------------|-------------|------------------|---------------------------|\n")
    for record in per_image_data:
        wrr_percent = f"{record['Word Recognition Rate']*100:.2f}%"
        mdfile.write(f"| {record['Image Name']} | {record['Total Words']} | {record['Recognized Words']} | {wrr_percent} |\n")
    mdfile.write(f"| **TOTAL / AVERAGE** | **{overall_total_gt}** | **{overall_correct}** | **{overall_wrr_percent:.2f}%** |\n")

# === SUMMARY
print(f"\n✅ CSV written to wrr_per_image.csv")
print(f"✅ Markdown table written to wrr_table.md (for GitHub display)")
print(f"Total Words: {overall_total_gt}, Correctly Recognized: {overall_correct}, Overall WRR: {overall_wrr_percent:.2f}%")






