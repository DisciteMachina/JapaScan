import tkinter as tk

def create_window (extracted_text, translated_text):
    root = tk.Tk()
    root.title("JapaScan")
    root.geometry("400x300")
    extracted_text_label = tk.Label(root, text="Original text: " + extracted_text)
    translated_text_label = tk.Label(root, text="Translated text: " + translated_text)
    extracted_text_label.pack(pady=10)
    translated_text_label.pack(pady=10)


    root.mainloop()

