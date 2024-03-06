import tkinter as tk

def get_screen_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()  # Destroy the root window to clean up
    return width, height

def Font():
    return ("Arial", 12)
    
def Background_Color():
    return "black"