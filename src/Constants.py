import tkinter as tk
import customtkinter

def get_screen_size():
    root = tk.Tk()
    width = root.winfo_width()
    height = root.winfo_height()
    root.destroy()  # Destroy the root window to clean up
    return width, height
def get_window_size(toot):
    k = toot.winfo_geometry()
    return k
def Font():
    return ("Arial", 12)
    
def Background_Color():
    return "black"