import customtkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import PhotoImage
from PIL import Image, ImageTk

class MyApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("My New Project")
        self.root.geometry("400x400")
        self.root.update()

        self.dot_locations = []
        self.active_button = None
        self.original_image_size = None
        self.active_dot = None
        self.original_image_width = None
        self.original_image_height = None

        self.create_default_display()  
        self.add_image()

        self.default_display.bind("<Configure>", self.on_root_resize)
        self.root.bind("<Configure>", self.on_root_resize)

    def on_root_resize(self, event=None):
        self.resize_canvas()
        self.resize_dot_position()
        self.resize_bottom_frame()

    def add_image(self):
        available_width = self.root.winfo_width() - self.default_display.winfo_reqwidth()
        available_height = self.root.winfo_height() - self.top_widget.winfo_reqheight()

        # Load the image
        image_path = "img\\F1.jpg"
        self.original_image = Image.open(image_path)

        # Calculate the aspect ratio of the image
        image_width, image_height = self.original_image.size
        aspect_ratio = image_width / image_height

        # Calculate the dimensions of the resized image
        if aspect_ratio > 1:  # Landscape orientation
            new_width = available_width
            new_height = int(available_width / aspect_ratio)
        else:  # Portrait or square orientation
            new_height = available_height
            new_width = int(available_height * aspect_ratio)

        # Adjust height if it exceeds the available height
        if new_height > available_height:
            new_height = available_height
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        resized_image = self.original_image.resize((new_width, new_height))

        # Convert image for Tkinter
        self.image = ImageTk.PhotoImage(resized_image)

        # Create a Canvas widget to display the image
        self.image_canvas = tk.CTkCanvas(self.root, width=new_width, height=new_height, borderwidth=0, highlightthickness=0)
        self.image_id = self.image_canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.image_canvas.grid(row=1, column=2, sticky="nsew") 

        self.bottom_frame = tk.CTkFrame(self.root)
        self.bottom_frame.grid(row=2, column=2, sticky="nsew")

        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.image_canvas.configure(scrollregion=(0, 0, new_width, new_height))

        self.original_image_size = (image_width, image_height)
        self.original_image_width = new_width
        self.original_image_height = new_height

    def resize_canvas(self):
        canvas_width = self.root.winfo_width() - self.default_display.winfo_reqwidth()
        canvas_height = self.root.winfo_height() - self.top_widget.winfo_reqheight()

        self.image_canvas.configure(width=canvas_width, height=canvas_height)

        if hasattr(self, 'image'):
            original_width, original_height = self.original_image_size
            aspect_ratio = original_width / original_height

            if aspect_ratio > 1:
                new_width = canvas_width
                new_height = int(canvas_width / aspect_ratio)
            else:
                new_height = canvas_height
                new_width = int(canvas_height * aspect_ratio)

            resized_image = self.original_image.resize((new_width, new_height))

            self.image = ImageTk.PhotoImage(resized_image)
            self.image_canvas.itemconfig(self.image_id, image=self.image)

            self.original_image_size = (original_width, original_height)

    def resize_bottom_frame(self):
        canvas_height = self.root.winfo_height() - self.top_widget.winfo_reqheight()

        self.bottom_frame.configure(height=canvas_height)

    def resize_dot_position(self):
        image_width = self.original_image_size[0]
        image_height = self.original_image_size[1]

        if self.active_dot:
            dot_id, relative_x, relative_y = self.active_dot

            new_x = relative_x * image_width
            new_y = relative_y * image_height

            self.image_canvas.coords(dot_id, new_x - 2, new_y - 2, new_x + 2, new_y + 2)

    def create_default_display(self):
        self.default_display = tk.CTkFrame(self.root, fg_color="red", width=200+self.root.winfo_width()*0.1)
        self.default_display.grid(row=0, column=1, rowspan=3, sticky="nsew")

        self.top_widget = tk.CTkFrame(self.root, fg_color="green", height=1)
        self.top_widget.grid(row=0, column=2, columnspan=999, sticky="nsew")
        self.top_widget.grid_columnconfigure(0, weight=1)

        return_button = tk.CTkButton(self.default_display, text="Return", command=self.show_default_display)
        return_button.grid(row=0, column=0, padx=10, pady=2)

        add_location_button = tk.CTkButton(self.default_display, text="Add Location", command=self.show_add_location_display)
        add_location_button.grid(row=1, column=0, padx=10, pady=2)

        edit_button = tk.CTkButton(self.default_display, text="Edit", command=self.edit_location)
        edit_button.grid(row=2, column=0, padx=10, pady=2)

        self.create_table()

    def create_table(self):
        self.table = ttk.Treeview(self.default_display, columns=("Location Name", "Camera IP"), show="headings")
        self.table.heading("Location Name", text="地點名稱")
        self.table.heading("Camera IP", text="監視器IP")
        self.table.column("Location Name", width=150)
        self.table.column("Camera IP", width=150)

        v_scrollbar = ttk.Scrollbar(self.default_display, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=v_scrollbar.set)
        self.table.grid(row=3, column=0, columnspan=2, sticky="nsew")
        
        self.default_display.grid_rowconfigure(3, weight=1)
        self.default_display.grid_columnconfigure(0, weight=1)

        def check_scrollbar_visibility():
            if len(self.table.get_children()) > 15:
                v_scrollbar.grid(row=3, column=2, sticky="ns")
            else:
                v_scrollbar.grid_forget()

        self.table.bind("<Configure>", lambda event: check_scrollbar_visibility())

    def create_add_location_display(self):
        self.add_location_display = tk.CTkFrame(self.root, fg_color="lightblue")
        self.add_location_display.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.add_location_display.columnconfigure(0, weight=1)
        
        return_button = tk.CTkButton(self.add_location_display, text="Return", command=self.show_default_display)
        return_button.grid(row=0, column=0, padx=10, pady=2, sticky="ew", columnspan=3)
 
        option_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        option_frame.grid(row=1, column=0, padx=1, pady=10, sticky="w")

        self.dot_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Dot.png"), size=(10, 10))
        self.line_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Line.png"), size=(10, 10))
        self.square_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Square.png"), size=(10, 10))
        
        self.dot_button = self.create_option_button(option_frame, self.dot_photo, "點", active=True)
        self.dot_button.grid(row=0, column=0, padx=0, pady=0)
        self.active_button = self.dot_button

        self.line_button = self.create_option_button(option_frame, self.line_photo, "線")
        self.line_button.grid(row=0, column=1, padx=0, pady=0)

        self.square_button = self.create_option_button(option_frame, self.square_photo, "區域")
        self.square_button.grid(row=0, column=2, padx=0, pady=0)
        
        roll_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        roll_frame.grid(row=1, column=1, padx=1, pady=10)

        self.rollback_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollback.png"), size=(20, 20))
        self.rollforward_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollforward.png"), size=(20, 20))
        
        rollback_button = tk.CTkButton(roll_frame, image=self.rollback_photo, text="", compound="top", width=35, height=35, fg_color="blue")
        rollback_button.grid(row=0, column=0, padx=0, pady=0)
        
        rollforward_button = tk.CTkButton(roll_frame, image=self.rollforward_photo, text="", compound="top", width=35, height=35, fg_color="blue")
        rollforward_button.grid(row=0, column=1, padx=0, pady=0)
        
        color_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        color_frame.grid(row=1, column=2, padx=1, pady=10)
        color_frame.columnconfigure(0, weight=0)
        
        self.color_button = tk.CTkButton(color_frame, text="", width=35, height=35, fg_color="blue", command=self.pick_color)
        self.color_button.grid(row=0, column=0, padx=1, pady=10)

        self.color_canvas = tk.CTkCanvas(self.color_button, width=20, height=20)
        self.color_canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.color_canvas.bind("<Button-1>", lambda event: self.color_button.invoke())

        location_info_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"), border_width=2)
        location_info_frame.grid(row=2, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        location_info_label = tk.CTkLabel(location_info_frame, text="地點資訊", font=("Arial", 16, "bold"))
        location_info_label.grid(row=0, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        location_code_label = tk.CTkLabel(location_info_frame, text="地點代號", font=("Arial", 12))
        location_code_label.grid(row=1, column=0, padx=(10, 2), pady=5, sticky="e")
        location_code_entry = tk.CTkEntry(location_info_frame)
        location_code_entry.grid(row=1, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        location_name_label = tk.CTkLabel(location_info_frame, text="地點名稱", font=("Arial", 12))
        location_name_label.grid(row=2, column=0, padx=2, pady=5, sticky="e")
        location_name_entry = tk.CTkEntry(location_info_frame)
        location_name_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        camera_ip_label = tk.CTkLabel(location_info_frame, text="監視器IP", font=("Arial", 12))
        camera_ip_label.grid(row=3, column=0, padx=2, pady=5, sticky="e")
        camera_ip_entry = tk.CTkEntry(location_info_frame)
        camera_ip_entry.grid(row=3, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        remark_label = tk.CTkLabel(location_info_frame, text="備註", font=("Arial", 12))
        remark_label.grid(row=4, column=0, padx=2, pady=(5, 0), sticky="e")
        remark_entry = tk.CTkTextbox(location_info_frame, width=1, height=100, wrap="word")
        remark_entry.grid(row=5, column=0, columnspan=3, padx=(10, 2), pady=(0, 1), sticky="we")

        save_button = tk.CTkButton(location_info_frame, text="Save")
        save_button.grid(row=6, column=0, padx=10, pady=(10, 5), sticky="ew", columnspan=3)

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
        self.image_canvas.unbind("<Button-1>")
        # Show default display and hide add location display
        self.default_display.lift()
        if hasattr(self, 'add_location_display'):
            self.add_location_display.lower()

        self.on_root_resize()

    def show_add_location_display(self):
        # Check if add_location_display already exists
        if not hasattr(self, 'add_location_display'):
            # Create add location display if it doesn't exist
            self.create_add_location_display()

        # Show add location display and hide default display
        self.add_location_display.lift()
        self.default_display.lower()

        if self.active_button:
            if self.active_button == self.dot_button:
                self.dot_button_clicked()
            elif self.active_button == self.line_button:
                self.line_button_clicked()
            elif self.active_button == self.square_button:
                self.square_button_clicked()
        
        self.on_root_resize()

    def edit_location(self):
        pass


    def dot_button_clicked(self):
        # Bind a click event to the image_canvas
        self.image_canvas.bind("<Button-1>", self.place_or_remove_dot)

    def line_button_clicked(self):
        pass  # Temporary empty method for line button

    def square_button_clicked(self):
        pass  # Temporary empty method for square button

    def place_or_remove_dot(self, event):
        # Get the coordinates of the click event
        x, y = event.x, event.y

        # Calculate relative coordinates based on the original image size
        relative_x = x / self.original_image_size[0]
        relative_y = y / self.original_image_size[1]

        if self.active_dot:
            # Remove the existing dot from the canvas
            self.image_canvas.delete(self.active_dot[0])

        # Create a new dot at the clicked location
        dot_id = self.image_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        # Update the active dot
        self.active_dot = (dot_id, relative_x, relative_y)

        # Update the dot location in the dot_locations list
        self.dot_locations.append((relative_x, relative_y))

        print(self.dot_locations)

    def resize_dot_position(self):
        # Get the current dimensions of the image
        image_width = self.original_image_size[0]
        image_height = self.original_image_size[1]

        # Check if there is an active dot
        if self.active_dot:
            dot_id, relative_x, relative_y = self.active_dot

            # Calculate the new coordinates based on the resized image dimensions
            new_x = relative_x * image_width
            new_y = relative_y * image_height

            # Update the coordinates of the dot on the canvas
            self.image_canvas.coords(dot_id, new_x - 2, new_y - 2, new_x + 2, new_y + 2)

        # Update the stored image dimensions for the next resize event
        self.image_width = image_width
        self.image_height = image_height


    def rollback_button_clicked(self):
        if self.dot_locations:
            # Remove the most recent dot from the canvas
            self.image_canvas.delete(self.dot_locations.pop())

    def rollforward_button_clicked(self):
        # Reapply the next undone change (if any) by restoring the dot
        pass


def main():
    root = tk.CTk()
    app = MyApplication(root)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    main()
