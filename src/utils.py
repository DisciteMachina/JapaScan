import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import pytesseract
from PIL import Image
import asyncio

# Global variable to store selected file and text input
selected_file = ""
manual_input_text = ""

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
    translated = await translator.translate(text, src='ja', dest='en')
    print("\nTranslated Text (Japanese → English):\n", translated.text)
    return translated.text.strip()

# Function to display the extracted and translated text
def display_translation(original, translated):
    result_label.config(text=f"Extracted Text:\n{original}\n\nTranslated Text:\n{translated}")

# Function to get the manual text input and process it
def process_manual_input():
    global manual_input_text
    manual_input_text = text_box.get("1.0", tk.END).strip()  # Get text from the input box
    if manual_input_text:
        print("Manual Input Text:", manual_input_text)
        translated_text = asyncio.run(translate_text(manual_input_text))
        display_translation(manual_input_text, translated_text)

# Create the main window
def create_window():
    global result_label, text_box

    root = tk.Tk()
    root.title("JapaScan")
    root.geometry("600x500")

    # Button to select an image file
    file_button = tk.Button(root, height=2, width=10, text="Select Image", command=open_file)
    file_button.pack(pady=10)

    input_label = tk.Label(root, text="Enter Japanese Text:", font=("Arial", 25))
    input_label.pack(pady=5)
    
    # Text box for manual Japanese input
    text_box = tk.Text(root, height=5, width=20, font=("Arial", 25))  # Change font size to 14
    text_box.pack(pady=10)

    # Button to process the manual input
    manual_button = tk.Button(root, text="Translate Text", command=process_manual_input)
    manual_button.pack(pady=10)

    # Label to display the results
    result_label = tk.Label(root, text="Extracted and Translated Text will appear here", wraplength=450, justify="left",font=("Arial", 15))
    result_label.pack(pady=0)

    root.mainloop()

create_window()