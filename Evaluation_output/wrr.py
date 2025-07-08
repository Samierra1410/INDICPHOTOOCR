import json
import unicodedata
from difflib import SequenceMatcher
from indic_transliteration.sanscript import transliterate, DEVANAGARI, ITRANS

# === CONFIGURATION ===
gt_path = "/Users/samierraarora/IndicPhotoOCR/IndicPhotoOCR/IndicPhotoOCR2/Evaluation_output/evaluation_result.json"
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

total_gt = 0
correct = 0

lang_stats = {
    "english": {"correct": 0, "total": 0},
    "hindi_marathi": {"correct": 0, "total": 0}
}

for image_name, gt_entry in gt_data.items():
    gt_annotations = gt_entry.get("annotations", {})

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

        # Use script_language
        gt_lang = gt_poly.get("script_language", "").lower()
        if not gt_lang:
            if any('\u0900' <= c <= '\u097F' for c in gt_poly.get("text", "")):
                gt_lang = "hindi"
            else:
                gt_lang = "english"

        if gt_lang in ["hindi", "marathi"]:
            lang_key = "hindi_marathi"
        else:
            lang_key = "english"

        total_gt += 1
        lang_stats[lang_key]["total"] += 1

        # Transliterate GT text only for Hindi/Marathi
        if lang_key == "hindi_marathi":
            gt_translit = normalize_text(transliterate(gt_text, DEVANAGARI, ITRANS))
        else:
            gt_translit = gt_text

        match_found = False

        # Try singles
        for ocr_word in flat_ocr_words:
            try:
                if lang_key == "hindi_marathi":
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
                    if lang_key == "hindi_marathi":
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
                    if lang_key == "hindi_marathi":
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
            lang_stats[lang_key]["correct"] += 1
        else:
            print(f"❌ MISMATCH: GT='{gt_text}' ({gt_lang}) vs OCR='{flat_ocr_words}' in {image_name}")

# === WRR CALCULATION ===
overall_wrr = correct / total_gt if total_gt else 0
english_wrr = (lang_stats["english"]["correct"] / lang_stats["english"]["total"]) if lang_stats["english"]["total"] else 0
hindi_marathi_wrr = (lang_stats["hindi_marathi"]["correct"] / lang_stats["hindi_marathi"]["total"]) if lang_stats["hindi_marathi"]["total"] else 0

# === PRINT & SAVE ===
result = {
    "overall": {
        "total_ground_truth_words": total_gt,
        "correctly_recognized_words": correct,
        "wrr": round(overall_wrr, 4)
    },
    "english": {
        "total_ground_truth_words": lang_stats["english"]["total"],
        "correctly_recognized_words": lang_stats["english"]["correct"],
        "wrr": round(english_wrr, 4)
    },
    "hindi_marathi": {
        "total_ground_truth_words": lang_stats["hindi_marathi"]["total"],
        "correctly_recognized_words": lang_stats["hindi_marathi"]["correct"],
        "wrr": round(hindi_marathi_wrr, 4)
    }
}
print(json.dumps(result, indent=2, ensure_ascii=False))

with open("evaluation_result_split.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)


































