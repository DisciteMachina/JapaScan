import os
from PIL import Image

def is_valid_image(image_name):
    # Checking if image exists
    if not os.path.exists(image_name):
        print("Image does not exist.")
        return False

    # Checking if the image has a valid extension
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', 'tiff')
    if not image_name.lower().endswith(valid_extensions):
        print("File is not a valid image file (valid extensions: .jpg, .jpeg, .png, .gif, .bmp, .tiff).")
        return False

    # Try to open the image
    try:
        with Image.open(image_name) as img:
            img.verify()
        return True
    except (IOError, SyntaxError):
        print("File is not a valid image")
        return False