import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import pytesseract
from PIL import Image
import asyncio

# If Tesseract is not found automatically, set its path manually
# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Mac (Homebrew)
# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Windows

selected_file = ""  # Global variable to store selected file

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

def extract_text(image_path):
    extracted_text = pytesseract.image_to_string(Image.open(image_path), lang="jpn")  # Use "jpn" instead of "ja"
    print("\nExtracted Japanese Text:\n", extracted_text)
    return extracted_text.strip()

async def translate_text(text):
    if not text.strip():  # If no text was extracted, return an error message
        return "No readable text found in the image."

    translator = Translator()
    translated = await translator.translate(text, src='ja', dest='en')
    print("\nTranslated Text (Japanese → English):\n", translated.text)
    return translated.text.strip()

def display_translation(original, translated):
    result_label.config(text=f"Extracted Text:\n{original}\n\nTranslated Text:\n{translated}")

def create_window():
    global result_label

    root = tk.Tk()
    root.title("JapaScan")
    root.geometry("500x400")

    file_button = tk.Button(root, text="Select Image", command=open_file)
    file_button.pack(pady=20)

    result_label = tk.Label(root, text="Extracted and Translated Text will appear here", wraplength=450, justify="left")
    result_label.pack(pady=20)

    root.mainloop()

create_window()
