import tkinter as tk
import pyautogui
import time
import tkinter.simpledialog as simpledialog
from tkinter import filedialog

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, button):
        self.button = button
        super().__init__(parent, title="Edit Button")

    def body(self, parent):
        tk.Label(parent, text="Label:").grid(row=0, column=0)
        self.label_entry = tk.Entry(parent)
        self.label_entry.grid(row=0, column=1)
        self.label_entry.insert(0, self.button.cget("text"))

        tk.Label(parent, text="Text (use {Enter} for Enter key):").grid(row=1, column=0)
        self.text_entry = tk.Entry(parent)
        self.text_entry.grid(row=1, column=1)
        self.text_entry.insert(0, self.button.text.replace('\n', '{Enter}'))

        return self.label_entry

    def apply(self):
        new_label = self.label_entry.get()
        new_text = self.text_entry.get()
        self.button.config(text=new_label)
        self.button.text = new_text

def on_button_click(button):
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)
    text_to_type = button.text.replace('{Enter}', '\n')
    pyautogui.typewrite(text_to_type)

def on_button_right_click(event, button):
    CustomDialog(root, button)

def save_settings():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            for button in buttons:
                file.write(f"{button.cget('text')};{button.text}\n")

def load_settings():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            for button, line in zip(buttons, file):
                label, text = line.strip().split(';')
                button.config(text=label)
                button.text = text

root = tk.Tk()
root.title("3x3 Matrix of Buttons")
root.attributes('-topmost', True)

buttons = []
for i in range(3):
    for j in range(3):
        button = tk.Button(root, text="Button")
        button.text = 'Hello World' # Default text
        button.grid(row=i, column=j)
        button.config(command=lambda b=button: on_button_click(b))
        button.bind('<Button-3>', lambda event, b=button: on_button_right_click(event, b))
        buttons.append(button)

save_button = tk.Button(root, text="Save", command=save_settings)
save_button.grid(row=3, column=0)

load_button = tk.Button(root, text="Load", command=load_settings)
load_button.grid(row=3, column=1)

root.mainloop()
