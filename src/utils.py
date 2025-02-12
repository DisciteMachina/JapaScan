import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import pytesseract
from PIL import Image, ImageTk
import asyncio
import time
import requests


# Global variables for selected file, manual input, and debouncing
selected_file = ""
manual_input_text = ""
last_typed_time = 0
debounce_delay = 0.5  # 500ms delay before triggering the translation
img_label = None
root = None 

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
        translated_text = asyncio.run(translate_text(extracted_text))
        display_translation(extracted_text, translated_text)
        display_image(selected_file)


# Function to extract text from an image
def extract_text(image_path):
    extracted_text = pytesseract.image_to_string(Image.open(image_path), lang="jpn")
    print("\nExtracted Japanese Text:\n", extracted_text)
    return extracted_text.strip()


# Asynchronous function to translate the text
async def translate_text(text):
    if not text.strip():  # If no text was extracted or entered, return an error message
        return "No readable text found."

    translator = Translator()
    try:
        translated = await translator.translate(text, src='ja', dest='en')
        print("\nTranslated Text (Japanese → English):\n", translated.text)
        return translated.text.strip()
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

    last_typed_time = current_time


# Function to clear the text box and results
def clear_all():
    text_box.delete("1.0", tk.END)
    result_label.config(text="Extracted and Translated Text will appear here")
    if img_label:
        img_label.config(image=None)
        img_label.image = None


# Create the main window
def create_window():
    global result_label, text_box, root

    root = tk.Tk()
    root.title("JapaScan")
    root.geometry("600x600")

    # Button to select an image file
    file_button = tk.Button(root, height=2, width=10, text="Select Image", command=open_file)
    file_button.pack(pady=10)

    input_label = tk.Label(root, text="Enter Japanese Text:", font=("Arial", 20))
    input_label.pack(pady=5)
    
    # Text box for manual Japanese input
    text_box = tk.Text(root, height=5, width=30, font=("Arial", 16))  # Adjust font size for better fit
    text_box.pack(pady=10)

    text_box.bind("<KeyRelease>", auto_translate)

    # Label to display the results
    result_label = tk.Label(root, text="Extracted and Translated Text will appear here", wraplength=450, justify="left", font=("Arial", 15))
    result_label.pack(pady=10)

    # Button to clear the text box and results
    clear_button = tk.Button(root, height=2, width=10, text="Clear", command=clear_all)
    clear_button.pack(pady=10)

    root.mainloop()

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

            readings = data.get('readings', [])
            meanings = data.get('meanings', [])
            strokes = data.get('strokes', 0)
            jlpt = data.get('jlpt', 'N/A')
            kanji_unicode = data.get('kanji', '')

            # Print the Kanji info
            print(f"Kanji: {kanji_unicode}")
            print(f"Readings: {', '.join(readings)}")
            print(f"Meanings: {', '.join(meanings)}")
            print(f"Strokes: {strokes}")
            print(f"JLPT Level: {jlpt}")
            
            
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print(f"Error: Failed to retrieve data (Status Code: {response.status_code})")
        print("Response Content:", response.content)  # Print raw content for inspection

# Example usage
kanji = '人'
get_kanji_info(kanji)