import tkinter as tk
from tkinter import filedialog
import sys

def select_folder():
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', True)  # Make dialog appear on top
        folder_path = filedialog.askdirectory(title="Select Download Folder")
        root.destroy()
        if folder_path:
            print(folder_path)
        else:
            print("")
    except Exception as e:
        print("")

if __name__ == "__main__":
    select_folder()
