import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import colorchooser
import Constants
import pyautogui


class MyApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("My New Project")
        self.root.geometry("800x800")
        self.root.update()
        self.create_default_display()
        # Initialize active button variable
        self.active_button = None
        
        self.add_image()


    def on_root_resize(self, event):
        self.add_image()
    # Other methods...


    def add_image(self):
        available_width = self.root.winfo_width()-self.default_display.winfo_reqwidth()
        available_height = self.root.winfo_height()

        
        # Load the image
        image_path = "img\\F1.jpg"  # Replace with the path to your image
        image = Image.open(image_path)

        # Calculate the aspect ratio of the image
        image_width, image_height = image.size
        aspect_ratio = image_width / image_height

        # Calculate the dimensions of the resized image
        if aspect_ratio > 1:  # Landscape orientation
            new_width = available_width
            new_height = int(available_width / aspect_ratio)
        else:  # Portrait or square orientation
            new_height = available_height
            new_width = int(available_height * aspect_ratio)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Convert image for Tkinter
        self.image = ImageTk.PhotoImage(resized_image)

        # Create a Canvas widget to display the image
        self.image_canvas = tk.CTkCanvas(self.root, width=new_width, height=new_height)
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.image_canvas.grid(row=0, column=2, sticky="nsew")

    # Create add location display and other methods...

    def create_option_button(self, frame, image, text, active=False):
        # Create a button with given image and text
        button = tk.CTkButton(frame, image=image, text=text, compound="top", width=35, height=35, font=("Arial", 8), fg_color="blue")

        # Bind button events to toggle active state
        button.bind("<Button-1>", lambda event, btn=button: self.toggle_active_state(btn))

        if active:
            self.toggle_active_state(button)

        return button

    def toggle_active_state(self, button):
        # Toggle the active state of the button
        if self.active_button == button:
            self.active_button = None
            button.configure(fg_color="blue")
        else:
            if self.active_button:
                self.active_button.configure(fg_color="blue")
            self.active_button = button
            button.configure(fg_color="darkblue")

    def create_default_display(self):
        # Create default display
        self.default_display = tk.CTkFrame(self.root, fg_color="red", width=200+self.root.winfo_width()*0.1)
        self.default_display.grid(row=0, column=1, sticky="nsew")

        
        # Add return button to the default display
        return_button = tk.CTkButton(self.default_display, text="Return", command=self.show_default_display)
        return_button.grid(row=0, column=0, padx=10, pady=2)

        # Add add location button to the default display
        add_location_button = tk.CTkButton(self.default_display, text="Add Location", command=self.show_add_location_display)
        add_location_button.grid(row=1, column=0, padx=10, pady=2)

        # Add edit button to the default display
        edit_button = tk.CTkButton(self.default_display, text="Edit", command=self.edit_location)
        edit_button.grid(row=2, column=0, padx=10, pady=2)

        # Create table
        self.create_table()

    def create_table(self):
        # Create treeview widget
        self.table = ttk.Treeview(self.default_display, columns=("Location Name", "Camera IP"), show="headings")

        # Define headings
        self.table.heading("Location Name", text="地點名稱")
        self.table.heading("Camera IP", text="監視器IP")

        # Set column widths
        self.table.column("Location Name", width=150)
        self.table.column("Camera IP", width=150)

        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self.default_display, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=v_scrollbar.set)

        # Attach the scrollbar and the table using grid
        self.table.grid(row=3, column=0, columnspan=2, sticky="nsew")
        
        # Configure row and column weights for proper resizing
        self.default_display.grid_rowconfigure(3, weight=1)
        self.default_display.grid_columnconfigure(0, weight=1)

        def check_scrollbar_visibility():
            # Update scrollbar visibility based on table content
            if len(self.table.get_children()) > 15:  # Change the threshold as needed
                v_scrollbar.grid(row=3, column=2, sticky="ns")
            else:
                v_scrollbar.grid_forget()  # Hide scrollbar if not needed

        self.table.bind("<Configure>", lambda event: check_scrollbar_visibility())


    def create_add_location_display(self):
   
        # Create add location display
        self.add_location_display = tk.CTkFrame(self.root, fg_color="lightblue")
        self.add_location_display.grid(row=0, column=1, sticky="nsew")
        
        # Configure column weights for proper resizing
        self.add_location_display.columnconfigure(0, weight=1)
        
        # Add return button to the add location display
        return_button = tk.CTkButton(self.add_location_display, text="Return", command=self.show_default_display)
        return_button.grid(row=0, column=0, padx=10, pady=2, sticky="ew", columnspan=3)  # Adjust columnspan to 3
 
        # Create option buttons frame
        option_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        option_frame.grid(row=1, column=0, padx=1, pady=10, sticky="w")  # Adjust padx to 1

        # Convert images to PhotoImage
        self.dot_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Dot.png"), size=(10, 10))
        self.line_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Line.png"), size=(10, 10))
        self.square_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Square.png"), size=(10, 10))
        
        # Create buttons with images and text
        dot_button = self.create_option_button(option_frame, self.dot_photo, "點", active=True)
        dot_button.grid(row=0, column=0, padx=0, pady=0)

        line_button = self.create_option_button(option_frame, self.line_photo, "線")
        line_button.grid(row=0, column=1, padx=0, pady=0)

        square_button = self.create_option_button(option_frame, self.square_photo, "區域")
        square_button.grid(row=0, column=2, padx=0, pady=0)

        # Create rollback and rollforward buttons frame
        roll_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        roll_frame.grid(row=1, column=1, padx=1, pady=10)  # Adjust padx to 1

        # Convert images for rollback and rollforward buttons
        self.rollback_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollback.png"), size=(20, 20))
        self.rollforward_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollforward.png"), size=(20, 20))
        
        # Create rollback and rollforward buttons with images and text
        rollback_button = tk.CTkButton(roll_frame, image=self.rollback_photo, text="", compound="top", width=35, height=35,fg_color="blue")
        rollback_button.grid(row=0, column=0, padx=0, pady=0)
        
        rollforward_button = tk.CTkButton(roll_frame, image=self.rollforward_photo, text="", compound="top", width=35, height=35,fg_color="blue")
        rollforward_button.grid(row=0, column=1, padx=0, pady=0)
        
        # Create color frame with button
        color_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        color_frame.grid(row=1, column=2, padx=1, pady=10)  # Adjust padx to 1
        color_frame.columnconfigure(0, weight=0)  # Set weight of column to 0
        
        # Create a button in the color_frame
        self.color_button = tk.CTkButton(color_frame, text="", width=35, height=35, fg_color="blue",command=self.pick_color)
        self.color_button.grid(row=0, column=0, padx=1, pady=10)

        # Create a canvas for the color square
        self.color_canvas = tk.CTkCanvas(self.color_button, width=20, height=20)
        self.color_canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Bind canvas events to propagate upwards
        self.color_canvas.bind("<Button-1>", lambda event: self.color_button.invoke())

        # Create a box frame to contain the location information widgets
        location_info_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"),border_width=2)
        location_info_frame.grid(row=2, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        # Add 地點資訊 label
        location_info_label = tk.CTkLabel(location_info_frame, text="地點資訊", font=("Arial", 16, "bold"))
        location_info_label.grid(row=0, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        # Add 地點代號 label and entry
        location_code_label = tk.CTkLabel(location_info_frame, text="地點代號", font=("Arial", 12))
        location_code_label.grid(row=1, column=0, padx=(10, 2), pady=5, sticky="e")
        location_code_entry = tk.CTkEntry(location_info_frame)
        location_code_entry.grid(row=1, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        # Add 地點名稱 label and entry
        location_name_label = tk.CTkLabel(location_info_frame, text="地點名稱", font=("Arial", 12))
        location_name_label.grid(row=2, column=0, padx=2, pady=5, sticky="e")
        location_name_entry = tk.CTkEntry(location_info_frame)
        location_name_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        # Add 監視器IP label and entry
        camera_ip_label = tk.CTkLabel(location_info_frame, text="監視器IP", font=("Arial", 12))
        camera_ip_label.grid(row=3, column=0, padx=2, pady=5, sticky="e")
        camera_ip_entry = tk.CTkEntry(location_info_frame)
        camera_ip_entry.grid(row=3, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        # Add 備註 label and entry
        remark_label = tk.CTkLabel(location_info_frame, text="備註", font=("Arial", 12))
        remark_label.grid(row=4, column=0, padx=2, pady=(5,0), sticky="e")
        remark_entry = tk.CTkTextbox(location_info_frame, width=1, height=100, wrap="word")
        remark_entry.grid(row=5, column=0, columnspan=3, padx=(10, 2), pady=(0,1), sticky="we")

        # Add return button to the add location display
        save_button = tk.CTkButton(location_info_frame, text="Save")
        save_button.grid(row=6, column=0, padx=10, pady=(10,5), sticky="ew", columnspan=3)  # Adjust columnspan to 3
 



    def select_dot(self):
        # Handle dot option selection
        pass

    def select_line(self):
        # Handle line option selection
        pass

    def select_square(self):
        # Handle square option selection
        pass
    
    def pick_color(self):
        # Open color picker dialog
        color = colorchooser.askcolor(parent=self.add_location_display, title="Pick a color")
        if color[1]:
            print("Selected color:", color[1])  # Print selected color
            # Update the button with the selected color
            self.color_canvas.configure(background=color[1])

    def show_default_display(self):
        # Show default display and hide add location display
        self.default_display.lift()
        if hasattr(self, 'add_location_display'):
            self.add_location_display.lower()

    def show_add_location_display(self):
        # Show add location display and hide default display
        self.create_add_location_display()
        if hasattr(self, 'add_location_display'):
            self.add_location_display.lift()
        self.default_display.lower()

        self.get_window_size()

    def edit_location(self):
        pass

def main():
    root = tk.CTk()
    app = MyApplication(root)
    root.rowconfigure(0, weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    main()
