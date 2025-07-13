
# IndicPhotoOCR Dataset & Evaluation Contribution

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This repository contains a benchmark dataset of **52 natural scene images** with text in Indic scripts (like shop boards, hoardings, banners) annotated with polygons and transcriptions.  
It is intended to test and evaluate the [IndicPhotoOCR](https://github.com/Bhashini-IITJ/IndicPhotoOCR) system.  
The repo also includes scripts for batch processing and word recognition rate (WRR) evaluation.

---

## 📁 Project Structure
```
INDICPHOTOOCR-2/
├── Annotations/               # Contains annotated JSON files (ground truth)
│   ├── Annotated_photos/
│   ├── annotated_files.json   # JSON with polygon + text + script tags
├── Evaluation_output/         # WRR results as JSON, CSV & Markdown tables
│   ├── evaluation_result.json
│   ├── wrr.py
│   ├── wrr_per_image.csv
│   ├── wrr_table.md
├── Original_photos/           # 52 input scene images
├── Outputs/                   # Detected outputs, OCR outputs, combined CSV
│   ├── detected_outputs/
│   ├── ocr_outputs/
├── Scripts/                   # Python scripts for OCR, detection, WRR
│   ├── ocr.py
│   ├── ocr_detection.py
│   ├── run_ocr_folder.py
│   ├── combined_csv.py
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Features
- ✅ Contains **52 real-world images** from diverse Indian locations
- ✍️ Polygon annotations with transcriptions and script language tags (Hindi, Marathi, English)
- 🧪 Batch evaluation using WRR scripts
- 📁 Generates CSV + Markdown tables with per-image accuracy
- 🐍 Python scripts for full OCR + detection + WRR pipeline

---

## 🔧 Installation

To run the scripts and evaluate on your machine:

### Clone the repository
```bash
git clone https://github.com/<your-username>/INDICPHOTOOCR-2.git
cd INDICPHOTOOCR-2
```

### Create and activate a virtual environment
```bash
conda create -n indicphotoocr python=3.10 -y
conda activate indicphotoocr
```

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🖼️ Usage

➤ **Run OCR on a folder of images**
```bash
python Scripts/run_ocr_folder.py
```

➤ **Calculate WRR from annotations & OCR JSON**
```bash
python Evaluation_output/wrr.py
```

---

## 📦 Output Format

Results are stored in:
- `Evaluation_output/wrr_per_image.csv` ➔ Per image WRR scores
- `Evaluation_output/wrr_table.md` ➔ GitHub-ready markdown table
- `Evaluation_output/evaluation_result.json` ➔ Summary WRR stats by language

✅ **Example JSON output:**
```json
{
  "overall": {
    "total_ground_truth_words": 294,
    "correctly_recognized_words": 239,
    "wrr": 0.8129
  },
  "english": {
    "total_ground_truth_words": 176,
    "correctly_recognized_words": 142,
    "wrr": 0.8068
  },
  "hindi_marathi": {
    "total_ground_truth_words": 118,
    "correctly_recognized_words": 97,
    "wrr": 0.822
  }
}
```

---

## 📝 License
This project is licensed under the MIT License.  
You may use, modify, or distribute this dataset and code for research, benchmarking, and educational purposes.

---

## 🙌 Contribution to Main IndicPhotoOCR
This dataset and evaluation result set was created to enhance the [IndicPhotoOCR benchmark](https://github.com/Bhashini-IITJ/IndicPhotoOCR).

To contribute:

- Fork the original repository  
- Commit your dataset/scripts/improvements  
- Open a Pull Request (PR) describing your additions

---

## 🎓 Acknowledgements
For the successful completion of my project, I would like to thank:

**Internship Guide:**  
👨‍🏫 Prof. Anand Mishra  
Department of Computer Science & Engineering,  
Indian Institute of Technology Jodhpur.

**Internship Mentor:**  
👨‍💻 Prof. Anik De 
Department of Computer Science & Engineering,  
Indian Institute of Technology Jodhpur.

---

## 📩 Contact
For queries or collaboration, feel free to reach out via email or open an issue.

---

> 🚀 **Happy benchmarking IndicPhotoOCR!**





