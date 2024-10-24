import sys
import os
import torch
from PIL import Image


from bharatOCR.detection.east_detector import EASTdetector
from bharatOCR.script_identification.CLIP_identifier import CLIPidentifier
from bharatOCR.recognition.parseq_recogniser import PARseqrecogniser
import bharatOCR.detection.east_config as cfg


class OCR:
    def __init__(self, device='cuda:0'):
        # self.detect_model_checkpoint = detect_model_checkpoint
        self.device = device
        # self.image_path = image_path
        self.detector = EASTdetector()
        self.recogniser = PARseqrecogniser()
        self.identifier = CLIPidentifier()

    def detect(self, image_path, detect_model_checkpoint=cfg.checkpoint):
        """Run the detection model to get bounding boxes of text areas."""
        print("Running text detection...")
        detections = self.detector.detect(image_path, detect_model_checkpoint, self.device)
        # print(detections)
        return detections['detections']

    def crop_and_identify_script(self, image, bbox):
        """
        Crop a text area from the image and identify its script language.

        Args:
            image (PIL.Image): The full image.
            bbox (list): List of four corner points, each a [x, y] pair.

        Returns:
            str: Identified script language.
        """
        # Extract x and y coordinates from the four corner points
        x_coords = [point[0] for point in bbox]
        y_coords = [point[1] for point in bbox]

        # Get the bounding box coordinates (min and max)
        x_min, y_min = min(x_coords), min(y_coords)
        x_max, y_max = max(x_coords), max(y_coords)

        # Crop the image based on the bounding box
        cropped_image = image.crop((x_min, y_min, x_max, y_max))
        root_image_dir = "bharatOCR/script_identification"
        os.makedirs(f"{root_image_dir}/images", exist_ok=True)
        # Temporarily save the cropped image to pass to the script model
        cropped_path = f'{root_image_dir}/images/temp_crop_{x_min}_{y_min}.jpg'
        cropped_image.save(cropped_path)

        # Predict script language, here we assume "hindi" as the model name
        print("Identifying script for the cropped area...")
        script_lang = self.identifier.identify(cropped_path, "hindi")  # Use "hindi" as the model name
        # print(script_lang)

        # Clean up temporary file
        # os.remove(cropped_path)

        return script_lang, cropped_path

    def recognise(self, cropped_image_path, script_lang):
        """Recognize text in a cropped image area using the identified script."""
        print("Recognizing text in detected area...")
        recognized_text = self.recogniser.recognise(script_lang, cropped_image_path, script_lang)
        # print(recognized_text)
        return recognized_text

    def ocr(self, image_path):
        """Process the image by detecting text areas, identifying script, and recognizing text."""
        recognized_words = []
        image = Image.open(image_path)
        
        # Run detection
        detections = self.detect(image_path)

        # Process each detected text area
        for bbox in detections:
            # Crop and identify script language
            script_lang, cropped_path = self.crop_and_identify_script(image, bbox)

            # Check if the script language is valid
            if script_lang:

                # Recognize text
                recognized_word = self.recognise(cropped_path, script_lang)
                recognized_words.append(recognized_word)
                print(f"Recognized word: {recognized_word}")

        return recognized_words

if __name__ == '__main__':
    # detect_model_checkpoint = '/DATA1/ocrteam/anik/git/BharatSTR/bharatSTR/East/tmp/epoch_990_checkpoint.pth.tar'
    sample_image_path = '/DATA1/ocrteam/anik/git/BharatSTR/demo_images/image_141.jpg'
    cropped_image_path = '/DATA1/ocrteam/anik/git/BharatSTR/demo_images/cropped_image/image_141_0.jpg'

    ocr = OCR()

    detections = ocr.detect(sample_image_path)
    print(detections)

    recognition = ocr.recognise(cropped_image_path, "hindi")
    print(recognition)

    recognised_words = ocr.ocr(sample_image_path)
    print(recognised_words)