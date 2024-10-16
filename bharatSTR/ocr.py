import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/DATA/ocr_team_2/anik/github_repo/bharatSTR/bharatSTR') 
import os
import torch
from PIL import Image
import cv2
from East.infer_detect import predict as detect_text
from infer_script import predict as identify_script
from infer import recogniser as recognizer

import os
import torch
from PIL import Image
from East.infer_detect import predict as detect_text
from infer_script import predict as identify_script
from infer import bstr_onImage as recognizer

class OCR:
    def __init__(self, detect_model_checkpoint, image_path, device='cuda:0'):
        """
        Initialize the OCR system with model checkpoints and device configuration.

        Args:
            detect_model_checkpoint (str): Path to the text detection model checkpoint.
            device (str): Device for model execution, 'cpu' or 'cuda'.
        """
        self.detect_model_checkpoint = detect_model_checkpoint
        self.device = device
        self.image_path = image_path

    def run_detection(self, image_path):
        """Run the detection model to get bounding boxes of text areas."""
        print("Running text detection...")
        detections = detect_text(image_path, "cuda:0", self.detect_model_checkpoint)
        return detections['detections']  # List of bounding box coordinates

    def crop_and_identify_script(self, image, bbox):
        """
        Crop a text area from the image and identify its script language.

        Args:
            image (PIL.Image): The full image.
            bbox (list): Bounding box coordinates of the text area.

        Returns:
            str: Identified script language.
        """
        x_min, y_min, x_max, y_max = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cropped_image = image.crop((x_min, y_min, x_max, y_max))

        # Temporarily save the cropped image to pass to the script model
        cropped_path = 'temp_crop.jpg'
        cropped_image.save(cropped_path)

        # Predict script language, here we assume "hindi" as the model name
        print("Identifying script for the cropped area...")
        script_lang = identify_script(cropped_path, "hindi")  # Use "hindi" as the model name
        
        # Clean up temporary file
        os.remove(cropped_path)

        return script_lang

    def recognize_text_in_area(self, cropped_image_path, script_lang):
        """
        Recognize text in a cropped image area using the identified script.

        Args:
            cropped_image_path (str): Path to the cropped image area.
            script_lang (str): Language model to be used for recognition.

        Returns:
            str: Recognized text.
        """
        print("Recognizing text in detected area...")
        recognized_text = recognizer(cropped_image_path, script_lang)  # script_lang is the predicted class
        return recognized_text

    def ocr(self):
        """
        Process the image by detecting text areas, identifying script, and recognizing text.

        Args:
            image_path (str): Path to the input image.

        Returns:
            list: List of recognized words in order of detection.
        """
        recognized_words = []
        image = Image.open(self.image_path)
        
        # Run detection
        detections = self.run_detection(image)

        # Process each detected text area
        for bbox in detections:
            # Crop and identify script language
            script_lang = self.crop_and_identify_script(image, bbox)

            # Check if the script language is valid (for our case we assume it's "hindi")
            if script_lang:
                cropped_path = 'temp_crop.jpg'

                # Recognize text
                recognized_word = self.recognize_text_in_area(cropped_path, script_lang)
                recognized_words.append(recognized_word)
                print(f"Recognized word: {recognized_word}")

        return recognized_words

    def recogniser(self, cropped_image_path):
        """
        Load the desired model and return the recognized word.

        Args:
            cropped_image_path (str): Path to the cropped image to be recognized.

        Returns:
            str: Recognized word.
        """
        print("Recognizing text from the cropped image...")
        recognized_word = recognizer(cropped_image_path, "hindi")  # Using "hindi" as the predicted class
        return recognized_word

if __name__ == '__main__':
    # Define paths to the models and a sample image
    detect_model_checkpoint = '/DATA/ocr_team_2/anik/github_repo/BharatSTR/bharatSTR/East/tmp/epoch_990_checkpoint.pth.tar'  # Adjust the path
    sample_image_path = '/DATA/ocr_team_2/anik/splitonBSTD/bstd/detection/D/image_371.jpg'  # Adjust the path
    ocr = OCR(detect_model_checkpoint, sample_image_path)

    recognitions = ocr.ocr()
    print(recognitions)