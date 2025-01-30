import cv2
import pytesseract
import os
import asyncio

from utils import is_valid_image, translate_text

image_name = input("Enter the image file name: ")
image_path = os.path.join("images", image_name)

if is_valid_image(image_name):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        print("Error: OpenCV could not read the image. Check the file path.")
    else:
        # Preprocessing to improve OCR accuracy
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh = cv2.medianBlur(thresh, 5)

        extracted_text = pytesseract.image_to_string(thresh, lang='jpn')

        print("Extracted Text: " + extracted_text)

        asyncio.run(translate_text(extracted_text))
else:
    print("Image is not valid.")








