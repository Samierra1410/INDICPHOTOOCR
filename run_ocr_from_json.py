print("🔥 It finally runs!")

from IndicPhotoOCR.ocr import OCR

ocr = OCR(verbose=True, device="cpu")
result = ocr.ocr("/Users/samierraarora/Desktop/IIT JODHPUR/annotated pics/pic_2.jpg")
print("✅ OCR Result:", result)











