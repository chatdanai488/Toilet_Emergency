import tkinter as tk
from PIL import ImageTk, Image

# Create the main application window
root = tk.Tk()
root.title("Canvas with Full Frame Image")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Load the image
image = Image.open("Loading_icon.gif")
# Resize the image to match the canvas size
image = image.resize((800, 600))
# Convert the Image object into a Tkinter-compatible image
tk_image = ImageTk.PhotoImage(image)

# Add the image to the canvas at the center
canvas.create_image(400, 300, image=tk_image)

# Run the Tkinter event loop
root.mainloop()
