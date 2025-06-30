import json
import os
import cv2
import csv
import numpy as np

# ===== CONFIG =====
json_path = "/Users/samierraarora/Desktop/IIT JODHPUR/Final_final/image_1.json"
image_path = "/Users/samierraarora/Desktop/IIT JODHPUR/annotated pics/pic_2.jpg"
output_dir = "training_crops"
output_csv = "training_data.csv"

# ===== SETUP =====
os.makedirs(output_dir, exist_ok=True)

# ===== LOAD DATA =====
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

key = list(data.keys())[0]
annotations = data[key]["annotations"]

# ===== LOAD IMAGE =====
image = cv2.imread(image_path)
if image is None:
    raise ValueError(f"❌ Failed to load image from {image_path}")

# ===== PROCESS POLYGONS =====
rows = []
for polygon_id, info in annotations.items():
    text = info.get("text", "").strip()
    script_language = info.get("script_language", "").strip()
    points = np.array(info["coordinates"])

    # Crop the polygon
    rect = cv2.boundingRect(points)
    x, y, w, h = rect
    crop = image[y:y+h, x:x+w].copy()

    # Optional: mask the polygon shape (to keep only inside)
    mask = np.zeros(crop.shape[:2], np.uint8)
    points_shifted = points - points.min(axis=0)
    cv2.drawContours(mask, [points_shifted], -1, (255), -1, cv2.LINE_AA)
    crop_masked = cv2.bitwise_and(crop, crop, mask=mask)

    # Save crop
    filename = f"{polygon_id}.jpg"
    path_to_save = os.path.join(output_dir, filename)
    cv2.imwrite(path_to_save, crop_masked)

    # Record row
    rows.append([filename, text, script_language])

# ===== WRITE CSV =====
with open(output_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "label", "script_language"])
    writer.writerows(rows)

print(f"✅ Done! Crops saved in '{output_dir}', CSV saved as '{output_csv}'")
