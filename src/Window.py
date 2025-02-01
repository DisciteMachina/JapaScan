import tkinter as tk

from utils import open_file

def create_window (extracted_text, translated_text):
    root = tk.Tk()
    root.title("JapaScan")
    root.geometry("400x300")
    file_button = tk.Button(root, text = "Enter File", command= open_file)
    extracted_text_label = tk.Label(root, text="Original text: " + extracted_text)
    translated_text_label = tk.Label(root, text="Translated text: " + translated_text)

    file_button.pack(pady=20)
    extracted_text_label.pack(pady=10)
    translated_text_label.pack(pady=10)



    root.mainloop()

