import sys
# sys.path.insert(1, '/DATA/ocr_team_2/anik/github_repo/bharatSTR/bharatSTR') 
import os
import torch
from PIL import Image
from east_infer_detect import predict as detect_text
from infer_script import predict as identify_script
from infer import recogniser

class OCR:
    def __init__(self, detect_model_checkpoint, image_path, device='cuda:0'):
        self.detect_model_checkpoint = detect_model_checkpoint
        self.device = device
        self.image_path = image_path

    def run_detection(self, image_path):
        """Run the detection model to get bounding boxes of text areas."""
        print("Running text detection...")
        detections = detect_text(image_path, self.device, self.detect_model_checkpoint)
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

        os.makedirs("images", exist_ok=True)
        # Temporarily save the cropped image to pass to the script model
        cropped_path = f'images/temp_crop_{x_min}_{y_min}.jpg'
        cropped_image.save(cropped_path)

        # Predict script language, here we assume "hindi" as the model name
        print("Identifying script for the cropped area...")
        script_lang = identify_script(cropped_path, "hindi")  # Use "hindi" as the model name
        print(script_lang)

        # Clean up temporary file
        # os.remove(cropped_path)

        return script_lang, cropped_path

    def recognize_text_in_area(self, cropped_image_path, script_lang):
        """Recognize text in a cropped image area using the identified script."""
        print("Recognizing text in detected area...")
        recognized_text = recogniser(script_lang, cropped_image_path, script_lang)
        return recognized_text

    def ocr(self, image_path):
        """Process the image by detecting text areas, identifying script, and recognizing text."""
        recognized_words = []
        image = Image.open(image_path)
        
        # Run detection
        detections = self.run_detection(image_path)

        # Process each detected text area
        for bbox in detections:
            # Crop and identify script language
            script_lang, cropped_path = self.crop_and_identify_script(image, bbox)

            # Check if the script language is valid
            if script_lang:
                # cropped_path = f'temp_crop_{bbox[0]}_{bbox[1]}.jpg'

                # Recognize text
                recognized_word = self.recognize_text_in_area(cropped_path, script_lang)
                recognized_words.append(recognized_word)
                print(f"Recognized word: {recognized_word}")

        return recognized_words

if __name__ == '__main__':
    detect_model_checkpoint = '/DATA1/ocrteam/anik/git/BharatSTR/bharatSTR/East/tmp/epoch_990_checkpoint.pth.tar'
    sample_image_path = '/DATA1/ocrteam/anik/git/BharatSTR/bharatSTR/demo_images/image_141.jpg'
    ocr = OCR(detect_model_checkpoint, sample_image_path)

    recognitions = ocr.ocr(sample_image_path)
    print(recognitions)
