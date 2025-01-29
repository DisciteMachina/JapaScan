import cv2

from utils import is_valid_image

image_name = input("Enter the image file name: ")

if is_valid_image(image_name):
    print("Valid")
else:
    print("Not valid")





