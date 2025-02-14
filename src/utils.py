import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import pytesseract
from PIL import Image, ImageTk
import asyncio
import time
import requests
import re

# Global variables for selected file, manual input, and debouncing
selected_file = ""
manual_input_text = ""
last_typed_time = 0
debounce_delay = 0.5  # 500ms delay before triggering the translation
img_label = None
root = None 
kanji_info_label = None


# Function to open a file dialog and select an image

def open_file():
    global selected_file
    selected_file = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")]
    )
    if selected_file:
        print("Selected file:", selected_file)
        extracted_text = extract_text(selected_file)
        
        # Run translation asynchronously
        asyncio.create_task(handle_translation(extracted_text))
        
        display_image(selected_file)
        
        # Look for kanji characters in the extracted text and display info
        kanji_chars = re.findall(r'[一-龯]', extracted_text)
        if kanji_chars:
            kanji = kanji_chars[0] 
            kanji_info = get_kanji_info(kanji)
            display_kanji_info(kanji_info)

async def handle_translation(text):
    translated_text = await translate_text(text)
    display_translation(text, translated_text)


# Function to extract text from an image
def extract_text(image_path):
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    img = img.resize((img.width // 2, img.height // 2))  # Reduce image size
    extracted_text = pytesseract.image_to_string(img, lang="jpn")
    print("\nExtracted Japanese Text:\n", extracted_text)
    return extracted_text.strip()


# Asynchronous function to translate the text
async def translate_text(text):
    if not text.strip():  # If no text was extracted or entered, return an error message
        return "No readable text found."

    translator = Translator()
    try:
        translated = await asyncio.to_thread(translator.translate, text, src='ja', dest='en')
        fixed_translation = fix_translation_spacing(translated.text)
        
        print("\nTranslated Text (Japanese → English):\n", fixed_translation)
        return fixed_translation.strip()
    except Exception as e:
        print("Error during translation:", e)
        return "Translation Error"


# Function to display the extracted and translated text
def display_translation(original, translated):
    result_label.config(text=f"Extracted Text:\n{original}\n\nTranslated Text:\n{translated}")


# Function to display the selected image in the GUI
def display_image(image_path):
    global img_label
    img = Image.open(image_path)
    img.thumbnail((300, 300))  # Resize the image
    img_tk = ImageTk.PhotoImage(img)
    
    # If an image was already displayed, replace it
    if img_label:
        img_label.config(image=img_tk)
        img_label.image = img_tk
    else:
        img_label = tk.Label(root, image=img_tk)
        img_label.image = img_tk
        img_label.pack(pady=10)


# Function to auto-translate the manual input text
def auto_translate(event=None):
    global manual_input_text, last_typed_time

    # Get the current time
    current_time = time.time()

    # if the time since the last typed time is greater than the debounce delay
    if current_time - last_typed_time > debounce_delay:
        manual_input_text = text_box.get("1.0", tk.END).strip()  
        if manual_input_text:
            print("Manual Input Text:", manual_input_text)
            translated_text = asyncio.run(translate_text(manual_input_text))
            display_translation(manual_input_text, translated_text)

        # Look for kanji characters in the manual input and display info
        kanji_chars = re.findall(r'[一-龯]', manual_input_text)
        if kanji_chars:
            kanji = kanji_chars[0]  # Show info for the first kanji found
            kanji_info = get_kanji_info(kanji)
            display_kanji_info(kanji_info)
            
    last_typed_time = current_time

# Add a space after periods
def fix_translation_spacing(text):
    return re.sub(r'(?<!\s)([.])', r'\1 ', text)


# Function to clear the text box and results
def clear_all():
    text_box.delete("1.0", tk.END)
    result_label.config(text="Extracted and Translated Text will appear here")
    if img_label:
        img_label.config(image=None)
        img_label.image = None

def get_kanji_info(kanji):
    url = f'https://kanjiapi.dev/v1/kanji/{kanji}'
    
    headers = {
        'Accept-Encoding': 'gzip, deflate',
    }
    
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Set encoding to utf-8
            response.encoding = 'utf-8'

            # Try to parse the JSON
            data = response.json()

            kanji_data = {
                'kanji': data.get('kanji', ''),
                'readings': data.get('readings', []),
                'meanings': data.get('meanings', []),
                'strokes': data.get('strokes', 0),
                'jlpt': data.get('jlpt', 'N/A')
            }
            
            return kanji_data
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print(f"Error: Failed to retrieve data (Status Code: {response.status_code})")
        return None
          
# Function to display Kanji information on the GUI
def display_kanji_info(kanji_info):
    if kanji_info and kanji_info_label:
        kanji_info_label.config(
            text=f"Kanji: {kanji_info['ka