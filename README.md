<p align="center">
  <img src="./static/pics/bharatOCR.png" alt="BharatOCR Logo" width="25%">
  <h3 align="center">
 BharatOCR - Comprehensive Scene Text Recognition Toolkit </br> across 13 Indian Languages
  </h3>
</p>
<hr style="width: 100%; border: 1px solid #000;">

BharatOCR is an advanced OCR toolkit designed for detecting, identifying, and recognizing text across 13 Indian languages, including Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Meitei Odia, Punjabi, Tamil, Telugu, Urdu, and English. Built to handle the unique scripts and complex structures of Indian languages, BharatOCR provides robust detection and recognition capabilities, making it a valuable tool for processing multilingual documents and enhancing document analysis in these diverse scripts.

![](contents/visualizeBharatOCR.png)
<hr style="width: 100%; border: 1px solid #000;">

## Table of Content
[Updates](https://github.com/Bhashini-IITJ/BharatOCR/blob/main/README.md#updates)</br>
[Installation](https://github.com/Bhashini-IITJ/BharatOCR/blob/main/README.md#installation)<br>
[How to use](https://github.com/Bhashini-IITJ/BharatOCR/blob/main/README.md#how-to-use)</br>
[Acknowledgement](https://github.com/Bhashini-IITJ/BharatOCR/blob/main/README.md#acknowledgement)</br>
[Contact us](https://github.com/Bhashini-IITJ/BharatOCR/blob/main/README.md#contact-us)</br>

<hr style="width: 100%; border: 1px solid #000;">


## Updates
<b>[September 2024]:</b> Private repository created.
<b>[November 2024]:</b> Added language support for 9 additional models in the recognition module. 
<hr style="width: 100%; border: 1px solid #000;">

## Installation
Currently we need to manually create virtual environemnt.
```python
conda create -n bharatocr python=3.9 -y
conda activate bharatocr


git clone https://github.com/Bhashini-IITJ/BharatOCR.git
cd BharatOCR

pip install pip-tools
make clean-reqs reqs  # Regenerate all the requirements files
# Use specific platform build. Other PyTorch 2.0 options: cu118, cu121, rocm5.7
platform=cu118
# Generate requirements files for specified PyTorch platform
make torch-${platform}
# Install the project and core + train + test dependencies. Subsets: [train,test,bench,tune]
pip install -r requirements/core.${platform}.txt -e .[train,test]
pip install opencv-python==4.10.0.84
pip install shapely==2.0.6
pip install openai-clip==1.0.1
pip install lmdb==1.5.1

python setup.py sdist bdist_wheel
pip install dist/bharatOCR-1.0.1-py3-none-any.whl
```

## Config
Currently this model works for hindi v/s english script identification and thereby hindi and english recognition.

Detection Model: EAST\
ScripIndetification Model: Hindi v/s English\
Recognition Model: Hindi, English 

## How to use
### Detection

```python
>>> from bharatOCR.ocr import OCR
# Create an object of OCR
>>> ocr_system = OCR()

# Get detections
>>> detections = ocr_system.detect("demo_images/image_141.jpg")

# Running text detection...
# 4334 text boxes before nms
# 1.027989387512207

# Save and visualize the detection results
>>> ocr_system.visualize_detection("demo_images/image_141.jpg", detections)
# Image saved at: test.png
```

## Recognition
```python
>>> from bharatOCR.ocr import OCR
# Create an object of OCR
>>> ocr_system = OCR()

# Get recognitions
ocr_system.recognise("demo_images/cropped_image/image_141_0.jpg", "hindi")
# Recognizing text in detected area...
# 'मण्डी'
```

## Detection + Recognition
```python
>>> from bharatOCR.ocr import OCR
# Create an object of OCR
>>> ocr_system = OCR()
# Complete pipeline
results=ocr_system.ocr("demo_images/image_141.jpg")
# Running text detection...
# 4334 text boxes before nms
# 0.9715704917907715
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Recognized word: रोड
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Recognized word: बाराखम्ब
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Using cache found in /DATA1/ocrteam/.cache/torch/hub/baudm_parseq_main
# Recognized word: barakhaml
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Recognized word: हाऊस
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Using cache found in /DATA1/ocrteam/.cache/torch/hub/baudm_parseq_main
# Recognized word: mandi
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Using cache found in /DATA1/ocrteam/.cache/torch/hub/baudm_parseq_main
# Recognized word: chowk
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Recognized word: मण्डी
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Using cache found in /DATA1/ocrteam/.cache/torch/hub/baudm_parseq_main
# Recognized word: road
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Using cache found in /DATA1/ocrteam/.cache/torch/hub/baudm_parseq_main
# Recognized word: house
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Using cache found in /DATA1/ocrteam/.cache/torch/hub/baudm_parseq_main
# Recognized word: rajiv
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Recognized word: राजीव
# Identifying script for the cropped area...
# Recognizing text in detected area...
# Recognized word: चौक


```

<!-- ## Training -->

## Acknowledgement

Text Recognition - [PARseq](https://github.com/baudm/parseq)\
EAST re-implemenation [repository](https://github.com/foamliu/EAST).<br/>
[Bhashini](https://bhashini.gov.in/)
## Contact us
For any queries, please contact us at:
- [Anik De](mailto:anekde@gmail.com)

