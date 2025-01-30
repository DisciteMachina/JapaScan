import os
from PIL import Image
from googletrans import Translator

def is_valid_image(image_name):
    file_dir = "images"
    full_path = os.path.join(file_dir, image_name)

    print (f"Checking: {full_path}")

    # Checking if image exists
    if not os.path.exists(full_path):
        print(f"❌ Image '{full_path}' does not exist.")
        return False

    # Checking if the image has a valid extension
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', 'tiff')
    if not image_name.lower().endswith(valid_extensions):
        print("❌ File is not a valid image file (valid extensions: .jpg, .jpeg, .png, .gif, .bmp, .tiff).")
        return False

    # Try to open the image
    try:
        with Image.open(full_path) as img:
            img.verify()
            print("✅ Image is valid.")
        return True
    except (IOError, SyntaxError) as e:
        print(f"❌ Image file error: {e}")
        return False

async def translate_text(text):
    translator = Translator()
    translated = await translator.translate(text, src='ja', dest='en')

    print("Original Text:", text)
    print("Translated Text:", translated.text)