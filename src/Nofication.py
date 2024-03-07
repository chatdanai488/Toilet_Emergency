import customtkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class EmergencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("--緊急求助--")

        # Set up grid configuration for responsiveness
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Set the window geometry to fullscreen
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height-100}-1+0")
        self.icon_path = "img\logo1.ico"
        self.root.iconbitmap(self.icon_path)

        self.create_widgets()

    def create_widgets(self):

        # Create frame for emergency information
        self.emergency_frame = ttk.Frame(self.root)
        self.emergency_frame.grid(
            row=0, column=0, sticky="nsew")

        # Create canvas for displaying map
        self.canvas = tk.CTkCanvas(self.root)
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.symbol = tk.CTkCanvas(self.emergency_frame, width=300)
        self.symbol.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.input_symbol = Image.open(
            "img\symbol\warning_sign_gradient_shine.jpg")
        self.symbol_new_size = (300, 300)
        self.resized_symbol = self.input_symbol.resize(
            self.symbol_new_size)

        self.map_symbol = ImageTk.PhotoImage(self.resized_symbol)
        self.show_alert = self.symbol.create_image(
            0, 0, anchor=tk.NW, image=self.map_symbol)
        # Load initial map image
        # Provide default map image
        self.map_image = Image.open("img\map\F1.jpg")
        # Resize image
        # Specify the new size (width, height)
        self.new_size = (self.screen_width, self.screen_height)
        self.resized_image = self.map_image.resize(
            self.new_size)
        self.map_photo = ImageTk.PhotoImage(self.resized_image)
        self.map_display = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.map_photo)

        # Emergency alert
        self.alert_label = ttk.Label(
            self.emergency_frame, text="***等待連線***", foreground="blue")
        self.alert_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Pagination combobox
        self.page_label = ttk.Label(self.emergency_frame, text="選擇求助者:")
        self.page_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.page_combobox = tk.CTkComboBox(
            self.emergency_frame, state="readonly", width=10)
        self.page_combobox.grid(row=1, column=1)
        self.page_combobox.bind("<<ComboboxSelected>>", self.show_emergency)

        # Cancel emergency button
        self.cancel_button = tk.CTkButton(
            self.root, text="關閉緊急求助", fg_color="red", command=self.cancel_emergency)
        self.cancel_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # Configure grid weights to make the emergency frame and canvas resize properly
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Bind window resize event to update canvas size
        self.root.bind("<Configure>", self.update_canvas_size)

    def show_emergency(self, event=None):
        selected_page = int(self.page_combobox.get()) - 1
        # Fetch and display emergency information for the selected page
        # Use selected_page variable to determine which page is selected
        pass

    def cancel_emergency(self):
        # Perform actions to cancel the emergency
        self.root.destroy()

    def update_canvas_size(self, event):
        # Update the canvas size to fit the remaining space in the window
        canvas_width = event.width - self.emergency_frame.winfo_width()
        canvas_height = event.height
        self.canvas.config(width=canvas_width, height=canvas_height)


def main():
    root = tk.CTk()
    app = EmergencyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
