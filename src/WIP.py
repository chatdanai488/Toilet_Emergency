import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import colorchooser
import Constants
import inspect
import DB

class EmrgFloor:
    def __init__(self, root, master_app=None):
        self.root = root
        self.master_app = master_app
        screen_height, screen_width = self.root.winfo_screenheight(), self.root.winfo_screenwidth()
        self.root.title("My New Project")
        self.root.geometry(f'{screen_height}x{screen_width}+0+0')
        self.root.update()
        self.DBO = DB.DB()

        self.dot_locations_history = {"dot": [], "line": [], "square": []}  # Dictionary to store past dot locations for each option button
        self.history_pointer = {"dot": -1, "line": -1, "square": -1}  # Pointer to track the current position in history
        self.dot_button = None
        self.square_button = None
        self.line_button = None
        self.active_button = None
        self.original_image_size = None
        self.active_dot = None
        self.active_line = None
        self.active_square = None
        self.original_image_width = None
        self.original_image_height = None
        self.selected_dot_color = "red"
        self.map_image = "img/F1.jpg"

        self.shape_data = {}

        self.create_add_location_display()  
        self.create_default_display()  
        self.add_image()

        self.default_display.bind("<Configure>",self.on_root_resize)
        self.top_widget.bind("<Configure>",self.on_root_resize)


    def on_root_resize(self, event=None):
        try:
            self.resize_canvas()
            if self.active_button == self.dot_button:
                self.resize_dot_position()
            elif self.active_button == self.line_button:
                self.resize_line_position()
            elif self.active_button == self.square_button:
                self.resize_square_position()

            self.refresh_table()
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
            
    # Other methods...
    def add_image(self):
        try:
            available_width = self.root.winfo_width() - self.default_display.winfo_reqwidth()
            available_height = self.root.winfo_height() - self.top_widget.winfo_reqheight()  # Adjusted for the top widget

            # Load the image
            image_path = self.map_image  # Use forward slashes for paths
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

            self.image_canvas = tk.CTkCanvas(self.root, width=new_width, height=new_height, borderwidth=0, highlightthickness=0)
            self.image_id = self.image_canvas.create_image(0, 0, anchor="nw", image=self.image)
            self.image_canvas.grid(row=1, column=2, padx=0, pady=0, sticky="nw")

            self.image_canvas.configure(scrollregion=(0, 0, new_width, new_height))

            self.original_image_size = (image_width, image_height)

            self.original_image_width = new_width
            self.original_image_height = new_height
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
    def resize_canvas(self):
        try:
            # Get the current dimensions of the canvas
            canvas_width = self.root.winfo_width() - self.add_location_display.winfo_reqwidth()
            canvas_height = self.root.winfo_height() - self.top_widget.winfo_reqheight()

            # Resize the canvas
            self.image_canvas.configure(width=canvas_width, height=canvas_height)

            # Resize the image if it exists
            if hasattr(self, 'image'):
                # Calculate the aspect ratio of the original image
                original_width, original_height = self.original_image_size
                aspect_ratio = original_width / original_height

                # Calculate the new dimensions of the resized image
                if aspect_ratio > 1:  # Landscape orientation
                    new_width = canvas_width
                    new_height = int(canvas_width / aspect_ratio)
                else:  # Portrait or square orientation
                    new_height = canvas_height
                    new_width = int(canvas_height * aspect_ratio)

                # Check if the new height exceeds the canvas height
                if new_height > canvas_height:
                    new_height = canvas_height
                    new_width = int(canvas_height * aspect_ratio)

                # Resize the image
                resized_image = self.original_image.resize((new_width, new_height))

                # Update the image in the canvas
                self.image = ImageTk.PhotoImage(resized_image)
                self.image_canvas.itemconfig(self.image_id, image=self.image)

                # Update the stored original image size
                self.original_image_size = (original_width, original_height)

            # Update the stored canvas dimensions for the next resize event
            self.original_image_width = new_width
            self.original_image_height = new_height
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
    def create_option_button(self, frame, image, text, active=False):
        try:
            # Create a button with the given image and text
            button = tk.CTkButton(frame, image=image, text=text, compound="top", width=35, height=35, font=("Arial", 8), fg_color="blue")

            # Bind button events to toggle active state
            button.bind("<Button-1>", lambda event, btn=button: self.toggle_active_state(btn))

            # Toggle active state if active parameter is True
            if active:
                self.toggle_active_state(button)

            return button
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
    def toggle_active_state(self, button):
        try:
            # Toggle the active state of the button
            if self.active_button == button:
                return  # Do nothing if the button is already active

            # Deactivate the currently active button (if any)
            if self.active_button:
                self.active_button.configure(fg_color="blue")
                # Unbind mouse click events from canvas if needed
                if self.active_button in (self.dot_button, self.line_button, self.square_button):
                    self.image_canvas.unbind("<Button-1>")

            # Activate the selected button
            self.active_button = button
            button.configure(fg_color="darkblue")

            # Bind mouse click events to canvas based on the selected button
            if button in (self.dot_button, self.line_button, self.square_button):
                if button == self.dot_button:
                    self.dot_button_clicked()
                    self.clear()
                elif button == self.line_button:
                    self.line_button_clicked()
                    self.clear()
                elif button == self.square_button:
                    self.square_button_clicked()
                    self.clear()
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
    def create_default_display(self):
        try:
            # Create default display frame
            self.default_display = tk.CTkFrame(self.root, fg_color="red", width=200)
            self.default_display.grid(row=0, column=1, rowspan=3, sticky="nsew")

            # Create top widget frame
            self.top_widget = tk.CTkFrame(self.root, fg_color="green", height=1)
            self.top_widget.grid(row=0, column=2, columnspan=999, sticky="nsew")
            self.top_widget.grid_columnconfigure(0, weight=1)

            # Add buttons to the default display
            self.add_return_button()
            self.add_add_location_button()
            self.add_edit_button()

            # Create table
            self.create_table()
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
    def add_return_button(self):
        # Add return button to the default display
        return_button = tk.CTkButton(self.default_display, text="Return", command=self.return_button)
        return_button.grid(row=0, column=0, padx=10, pady=2)
    def add_add_location_button(self):
        # Add add location button to the default display
        add_location_button = tk.CTkButton(self.default_display, text="Add Location", command=self.show_add_location_display)
        add_location_button.grid(row=1, column=0, padx=10, pady=2)
    def add_edit_button(self):
        # Add edit button to the default display
        edit_button = tk.CTkButton(self.default_display, text="Edit", command=self.edit_location)
        edit_button.grid(row=2, column=0, padx=10, pady=2)
    def create_table(self):
        try:
            # Create treeview widget
            self.table = ttk.Treeview(self.default_display, columns=("Location Name", "Camera IP"), show="headings")

            # Define headings
            self.table.heading("Location Name", text="Location Name")
            self.table.heading("Camera IP", text="Camera IP")

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

            # Callback to handle scrollbar visibility
            def check_scrollbar_visibility(event=None):
                if len(self.table.get_children()) > 15:  # Adjust threshold as needed
                    v_scrollbar.grid(row=3, column=2, sticky="ns")
                else:
                    v_scrollbar.grid_forget()

            # Bind the callback to configure event
            self.table.bind("<Configure>", check_scrollbar_visibility)
            self.table.bind("<<TreeviewSelect>>", self.on_row_select)
            
            # Initial check for scrollbar visibility
            check_scrollbar_visibility()

        except Exception as e:
            # Handle any errors during table creation
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def create_add_location_display(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Create add location display
            self.add_location_display = tk.CTkFrame(self.root, fg_color="lightblue")
            self.add_location_display.grid(row=0, column=1, rowspan=3, sticky="nsew")
            
            # Configure column weights for proper resizing
            self.add_location_display.columnconfigure(0, weight=1)
            
            # Add return button to the add location display
            return_button = tk.CTkButton(self.add_location_display, text="Return", command=self.show_default_display)
            return_button.grid(row=0, column=0, padx=10, pady=2, sticky="ew", columnspan=3)

            # Create option buttons frame
            option_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
            option_frame.grid(row=1, column=0, padx=1, pady=10, sticky="w")

            # Convert images to PhotoImage
            self.dot_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Dot.png"), size=(10, 10))
            self.line_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Line.png"), size=(10, 10))
            self.square_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Square.png"), size=(10, 10))

            # Create buttons with images and text
            self.dot_button = self.create_option_button(option_frame, self.dot_photo, "Dot", active=True)
            self.dot_button.grid(row=0, column=0, padx=0, pady=0)
            self.active_button = self.dot_button

            self.line_button = self.create_option_button(option_frame, self.line_photo, "Line")
            self.line_button.grid(row=0, column=1, padx=0, pady=0)

            self.square_button = self.create_option_button(option_frame, self.square_photo, "Square")
            self.square_button.grid(row=0, column=2, padx=0, pady=0)

            # Create rollback and rollforward buttons frame
            roll_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
            roll_frame.grid(row=1, column=1, padx=1, pady=10)

            # Convert images for rollback and rollforward buttons
            self.rollback_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollback.png"), size=(20, 20))
            self.rollforward_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollforward.png"), size=(20, 20))

            # Create rollback and rollforward buttons with images and text
            rollback_button = tk.CTkButton(roll_frame, image=self.rollback_photo, text="", compound="top", width=35, height=35, fg_color="blue", command=self.rollback)
            rollback_button.grid(row=0, column=0, padx=0, pady=0)

            rollforward_button = tk.CTkButton(roll_frame, image=self.rollforward_photo, text="", compound="top", width=35, height=35, fg_color="blue", command=self.rollforward)
            rollforward_button.grid(row=0, column=1, padx=0, pady=0)

            # Create color frame with button
            color_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
            color_frame.grid(row=1, column=2, padx=1, pady=10)
            color_frame.columnconfigure(0, weight=0)

            # Create a button in the color_frame
            self.color_button = tk.CTkButton(color_frame, text="", width=35, height=35, fg_color="blue", command=self.pick_color)
            self.color_button.grid(row=0, column=0, padx=1, pady=10)

            # Create a canvas for the color square
            self.color_canvas = tk.CTkCanvas(self.color_button, width=20, height=20, background="black")
            self.color_canvas.place(relx=0.5, rely=0.5, anchor="center")

            # Bind canvas events to propagate upwards
            self.color_canvas.bind("<Button-1>", lambda event: self.color_button.invoke())

            # Create a box frame to contain the location information widgets
            self.location_info_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"), border_width=2)
            self.location_info_frame.grid(row=2, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

            # Add location information labels and entries
            self.add_location_info_widgets()

            # Add save button to the add location display
            save_button = tk.CTkButton(self.location_info_frame, text="Save",command=self.save_button)
            save_button.grid(row=6, column=0, padx=10, pady=(10, 5), sticky="ew", columnspan=3)

        except Exception as e:
            # Handle any errors during creation of add location display
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def add_location_info_widgets(self):
        # Add location information labels and entries
        validate_int = self.add_location_display.register(self.validate_int)
        # Add 地點資訊 label
        location_info_label = tk.CTkLabel(self.location_info_frame, text="地點資訊", font=("Arial", 16, "bold"))
        location_info_label.grid(row=0, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        # Add 地點代號 label and entry
        location_code_label = tk.CTkLabel(self.location_info_frame, text="地點代號", font=("Arial", 12))
        location_code_label.grid(row=1, column=0, padx=(10, 2), pady=5, sticky="e")
        location_code_entry = tk.CTkEntry(self.location_info_frame, validate="key", validatecommand=(validate_int, "%P"))
        location_code_entry.grid(row=1, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        # Add 地點名稱 label and entry
        location_name_label = tk.CTkLabel(self.location_info_frame, text="地點名稱", font=("Arial", 12))
        location_name_label.grid(row=2, column=0, padx=2, pady=5, sticky="e")
        location_name_entry = tk.CTkEntry(self.location_info_frame)
        location_name_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        # Add 監視器IP label and entry
        camera_ip_label = tk.CTkLabel(self.location_info_frame, text="監視器IP", font=("Arial", 12))
        camera_ip_label.grid(row=3, column=0, padx=2, pady=5, sticky="e")
        camera_ip_entry = tk.CTkEntry(self.location_info_frame)
        camera_ip_entry.grid(row=3, column=1, columnspan=2, padx=2, pady=5, sticky="we")

        # Add 備註 label and entry
        remark_label = tk.CTkLabel(self.location_info_frame, text="備註", font=("Arial", 12))
        remark_label.grid(row=4, column=0, padx=2, pady=(5, 0), sticky="e")
        remark_entry = tk.CTkTextbox(self.location_info_frame, width=1, height=100, wrap="word")
        remark_entry.grid(row=5, column=0, columnspan=3, padx=(10, 2), pady=(0, 1), sticky="we")
    def pick_color(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Open color picker dialog
            color = colorchooser.askcolor(parent=self.add_location_display, title="Pick a color")
            if color[1]:
                print("Selected color:", color[1])  # Print selected color
                # Update the button with the selected color
                self.color_canvas.configure(background=color[1])
                # Store the selected color
                self.selected_dot_color = color[1]

                self.recolor_active_dot()
        except Exception as e:
            # Handle any errors during color picking
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def show_default_display(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            self.image_canvas.unbind("<Button-1>")
            # Show default display and hide add location display
            self.default_display.lift()
            if hasattr(self, 'add_location_display'):
                self.add_location_display.lower()

            self.on_root_resize()
            self.clear_elements()
        except Exception as e:
            # Handle any errors during display switching
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def show_add_location_display(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
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
        except Exception as e:
            # Handle any errors during display switching
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def validate_int(self, new_value):
            # Validate if the new value is an integer
            if new_value.isdigit() or new_value == "":
                return True
            else:
                return False
    def clear_elements(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Clear all entry and textbox widgets
            self.clear_entry_and_textbox()

            # Clear the dot and reset dot history
            self.clear()
        except Exception as e:
            # Handle any errors during element clearing
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise


    def clear_entry_and_textbox(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Clear all entry and textbox widgets in the add_location_display
            for widget in self.location_info_frame.winfo_children():
                if isinstance(widget, (tk.CTkEntry, tk.CTkTextbox)):
                    if isinstance(widget, tk.CTkEntry):
                        widget.delete("0", "end")  # Clear tk.CTkEntry widget
                    elif isinstance(widget, tk.CTkTextbox):
                        widget.delete("0.0", "end")  # Clear tk.CTkTextbox widget
        except Exception as e:
            # Handle any errors during clearing
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise

    def clear(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Remove the active dot from the canvas if it exists
            if self.active_dot:
                self.image_canvas.delete(self.active_dot[0])
                self.active_dot = None
                # Clear the dot history
                self.dot_locations_history["dot"] = []
                # Reset history pointer
                self.history_pointer["dot"] = -1

            # Remove the active line from the canvas if it exists
            if self.active_line:
                self.image_canvas.delete(self.active_line[0])
                self.active_line = None

            # Remove the active square from the canvas if it exists
            if self.active_square:
                self.image_canvas.delete(self.active_square[0])
                self.active_square = None

            self.dot_locations_history = {"dot": [], "line": [], "square": []}
            self.history_pointer = {"dot": -1, "line": -1, "square": -1}
        except Exception as e:
            # Handle any errors during clearing
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise

        
    def dot_button_clicked(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Bind a click event to the image_canvas
            self.image_canvas.bind("<Button-1>", self.place_or_remove_dot)
        except Exception as e:
            # Handle any errors during dot button click event
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def place_or_remove_dot(self, event):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Get the coordinates of the click event
            x, y = event.x, event.y

            # Calculate relative coordinates based on the original image size
            relative_x = x / self.original_image_width
            relative_y = y / self.original_image_height

            if self.active_dot:
                # Remove the existing dot from the canvas
                self.image_canvas.delete(self.active_dot[0])

            # Create a new dot at the clicked location
            dot_id = self.image_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.selected_dot_color)

            # Update the active dot
            self.active_dot = (dot_id, relative_x, relative_y)

            # Append the location tuple to the "dot" array in dot_locations_history
            self.update_history("dot", (relative_x, relative_y))

            # Ensure dot_locations_history["dot"] contains at most 5 locations
            if len(self.dot_locations_history["dot"]) > 5:
                self.dot_locations_history["dot"].pop(0)  # Remove the oldest entry

            print(self.dot_locations_history)
        except Exception as e:
            # Handle any errors during dot placement or removal
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def recolor_active_dot(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Check if there is an active dot or line
            if self.active_dot:
                dot_id, _, _ = self.active_dot
                # Update the fill color of the active dot with the selected color
                self.image_canvas.itemconfig(dot_id, fill=self.selected_dot_color)
            elif self.active_line:
                self.image_canvas.itemconfig(self.active_line[0], fill=self.selected_dot_color)
            elif self.active_square:
                self.image_canvas.itemconfig(self.active_square[0], fill=self.selected_dot_color)
        except Exception as e:
            # Handle any errors during dot recoloring
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def resize_dot_position(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Get the current dimensions of the image
            image_width = self.original_image_width
            image_height = self.original_image_height

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
        except Exception as e:
            # Handle any errors during dot resizing
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def rollback_dot(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Decrement the history pointer for the dot option button
            if self.history_pointer["dot"] > 0:
                self.history_pointer["dot"] -= 1
                print("History pointer decremented to:", self.history_pointer["dot"])

            # Move the dot to the previous location in history
            previous_location = self.dot_locations_history["dot"][self.history_pointer["dot"]]
            print("Previous location from history:", previous_location)
            self.move_dot_to_location(previous_location)
        except Exception as e:
            # Handle any errors during dot rollback
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def rollforward_dot(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Increment the history pointer for the dot option button
            if self.history_pointer["dot"] < len(self.dot_locations_history["dot"]) - 1:
                self.history_pointer["dot"] += 1

            # Move the dot to the next location in history
            self.move_dot_to_location(self.dot_locations_history["dot"][self.history_pointer["dot"]])
        except Exception as e:
            # Handle any errors during dot rollforward
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise
    def move_dot_to_location(self, location):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Calculate canvas coordinates based on the original image size
            canvas_x = location[0] * self.original_image_width
            canvas_y = location[1] * self.original_image_height

            # Update the coordinates of the dot on the canvas
            if self.active_dot:
                dot_id, _, _ = self.active_dot
                self.image_canvas.coords(dot_id, canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2)
        except Exception as e:
            # Handle any errors during dot movement
            print(f"An error occurred in {method_name}: {e}")
            # Optionally, raise the error to propagate it further
            raise



    def line_button_clicked(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            self.image_canvas.bind("<Button-1>", self.place_or_remove_line)
        except Exception as e:
            print(f"An error occurred in {method_name}: {e}")
            raise
    def place_or_remove_line(self, event):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Get the coordinates of the click event
            x, y = event.x, event.y

            # Calculate relative coordinates based on the original image size
            relative_x = x / self.original_image_width
            relative_y = y / self.original_image_height
                
            if not self.active_dot and not self.active_line:
                # If there's no active dot or line, create a new dot and update history
                dot_id = self.image_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.selected_dot_color)
                self.active_dot = (dot_id, x, y)
                self.update_history("line", ([relative_x, relative_y], None))
                
            elif self.active_dot:
                # If there's an active dot, connect it to the new dot with a line and update history
                x1, y1 = self.active_dot[1], self.active_dot[2]
                line_id = self.image_canvas.create_line(x1, y1, x, y, fill=self.selected_dot_color)
                self.image_canvas.delete(self.active_dot[0])  # Delete the active dot
                self.active_dot = None  # Reset active dot
                self.active_line = (line_id, x1, y1, x, y)
                relative_x1 = x1 / self.original_image_width
                relative_y1 = y1 / self.original_image_height
                self.update_history("line", ([relative_x1, relative_y1], [relative_x, relative_y]))
                
            elif self.active_line:
                # If there's an active line, delete it and connect the last dot to the new dot with a line, then update history
                self.image_canvas.delete(self.active_line[0])  # Delete the active line
                x1, y1 = self.active_line[3], self.active_line[4]  # Get the coordinates of the last dot
                line_id = self.image_canvas.create_line(x1, y1, x, y, fill=self.selected_dot_color)
                self.active_line = (line_id, x1, y1, x, y)
                relative_x1 = x1 / self.original_image_width
                relative_y1 = y1 / self.original_image_height
                self.update_history("line", ([relative_x1, relative_y1], [relative_x, relative_y]))

            print(self.dot_locations_history["line"])
        except Exception as e:
            print(f"An error occurred in {method_name}: {e}")
            raise

    def rollback_line(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            line_history = self.dot_locations_history["line"]
        
            # Check if there's any history to rollback
            if self.history_pointer["line"] > 0:
                # Get the entry to rollback
                entry = line_history[self.history_pointer["line"] - 1]
                if entry[1] is None:
                    # If the second column is None, it indicates a dot
                    dot_x, dot_y = entry[0]
                    # Calculate canvas coordinates based on the relative positions
                    canvas_x = dot_x * self.original_image_width
                    canvas_y = dot_y * self.original_image_height
                    dot_id = self.image_canvas.create_oval(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill=self.selected_dot_color)
                    self.active_dot = (dot_id, canvas_x, canvas_y)
                    # Remove the current line from the canvas
                    self.image_canvas.delete(self.active_line[0])
                    self.active_line = None  # Reset active line
                else:
                    # If the second column is not None, it indicates a line
                    # Calculate canvas coordinates based on the relative positions
                    x1, y1 = entry[0][0] * self.original_image_width, entry[0][1] * self.original_image_height
                    x2, y2 = entry[1][0] * self.original_image_width, entry[1][1] * self.original_image_height
                    line_id = self.image_canvas.create_line(x1, y1, x2, y2, fill=self.selected_dot_color)
                    # Remove the last dot from the canvas
                    self.image_canvas.delete(entry[0][0])
                    # Remove the current line from the canvas
                    self.image_canvas.delete(self.active_line[0])
                    # Update the active line
                    self.active_line = (line_id, x1, y1, x2, y2)
                    
                # Decrement the history pointer
                self.history_pointer["line"] -= 1
        except Exception as e:
            print(f"An error occurred in {method_name}: {e}")
            raise

    def rollforward_line(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            # Check if there are any lines ahead in the history
            if self.history_pointer["line"] < len(self.dot_locations_history["line"]) - 1:
                # Increment the history pointer for the line option
                self.history_pointer["line"] += 1

                # Get the next line location from history
                next_location = self.dot_locations_history["line"][self.history_pointer["line"]]

                # Check if the next location represents a dot
                if next_location[1] is None:
                    # If the next location is a dot, create a dot
                    x, y = next_location[0][0] * self.original_image_width, next_location[0][1] * self.original_image_height
                    dot_id = self.image_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.selected_dot_color)
                    self.active_dot = (dot_id, x, y)
                else:
                    # If the next location represents a line, create a line
                    if self.active_dot is not None:
                        self.image_canvas.delete(self.active_dot[0])
                        self.active_dot = None
                    else:
                        self.image_canvas.delete(self.active_line[0])
                    x1, y1 = next_location[0][0] * self.original_image_width, next_location[0][1] * self.original_image_height
                    x2, y2 = next_location[1][0] * self.original_image_width, next_location[1][1] * self.original_image_height
                    line_id = self.image_canvas.create_line(x1, y1, x2, y2, fill=self.selected_dot_color)
                    self.active_line = (line_id, x1, y1, x2, y2)
        except Exception as e:
            print(f"An error occurred in {method_name}: {e}")
            raise

    def resize_line_position(self):
        try:
            method_name = inspect.currentframe().f_code.co_name
            line_history = self.dot_locations_history["line"]
        
            # Check if there's any history to resize
            if self.history_pointer["line"] > 0:
                # Get the entry to resize
                entry = line_history[self.history_pointer["line"]]
                if entry[1] is None:
                    # If the second column is None, it indicates a dot
                    dot_x, dot_y = entry[0]
                    # Calculate canvas coordinates based on the relative positions
                    canvas_x = dot_x * self.original_image_width
                    canvas_y = dot_y * self.original_image_height
                    dot_id = self.image_canvas.create_oval(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill=self.selected_dot_color)
                    self.active_dot = (dot_id, canvas_x, canvas_y)
                    # Remove the current line from the canvas
                    if self.active_line:
                        self.image_canvas.delete(self.active_line[0])
                    self.active_line = None  # Reset active line
                else:
                    # If the second column is not None, it indicates a line
                    # Calculate canvas coordinates based on the relative positions
                    x1, y1 = entry[0][0] * self.original_image_width, entry[0][1] * self.original_image_height
                    x2, y2 = entry[1][0] * self.original_image_width, entry[1][1] * self.original_image_height
                    line_id = self.image_canvas.create_line(x1, y1, x2, y2, fill=self.selected_dot_color)
                    # Remove the last dot from the canvas
                    self.image_canvas.delete(entry[0][0])
                    # Remove the current line from the canvas
                    if self.active_line:
                        self.image_canvas.delete(self.active_line[0])
                    # Update the active line
                    self.active_line = (line_id, x1, y1, x2, y2)
                    
                # Decrement the history pointer
        except Exception as e:
            print(f"An error occurred in {method_name}: {e}")
            raise

    def square_button_clicked(self):
        try:
            # Bind the canvas to the place_or_remove_square method for square placement
            self.image_canvas.bind("<Button-1>", self.place_or_remove_square)
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

    def place_or_remove_square(self, event):
        try:
            # Get the coordinates of the click event
            x, y = event.x, event.y

            # Calculate relative coordinates based on the original image size
            relative_x = x / self.original_image_width
            relative_y = y / self.original_image_height

            if not self.active_dot and not self.active_square:
                # If there's no active dot or square, create a new dot and update history
                dot_id = self.image_canvas.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill=self.selected_dot_color)
                self.active_dot = (dot_id, x, y)
                self.update_history("square", ([relative_x, relative_y], None))
            elif self.active_dot:
                # If there's an active dot, create a square around it and update history
                x1, y1 = self.active_dot[1], self.active_dot[2]
                square_id = self.image_canvas.create_rectangle(x, y, x1, y1, fill=self.selected_dot_color, stipple="gray50")
                self.image_canvas.delete(self.active_dot[0])  # Delete the active dot
                self.active_dot = None  # Reset active dot
                self.active_square = (square_id, x, y, x1, y1)
                relative_x1 = x1 / self.original_image_width
                relative_y1 = y1 / self.original_image_height
                self.update_history("square", ([relative_x, relative_y], [relative_x1, relative_y1]))
            elif self.active_square:
                # If there's an active square, delete it and create a new square, then update history
                self.image_canvas.delete(self.active_square[0])  # Delete the active square
                x1, y1 = self.active_square[1], self.active_square[2]  # Get the coordinates of the last corner
                square_id = self.image_canvas.create_rectangle(x, y, x1, y1, fill=self.selected_dot_color, stipple="gray50")
                self.active_square = (square_id, x, y, x1, y1)
                relative_x1 = x1 / self.original_image_width
                relative_y1 = y1 / self.original_image_height
                self.update_history("square", ([relative_x, relative_y], [relative_x1, relative_y1]))
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")    
    def rollback_square(self):
        try:
            square_history = self.dot_locations_history["square"]
            
            # Check if there's any history to rollback
            if self.history_pointer["square"] > 0:
                # Get the entry to rollback
                entry = square_history[self.history_pointer["square"] - 1]
                if entry[1] is None:
                    # If the second column is None, it indicates a dot
                    dot_x, dot_y = entry[0]
                    # Calculate canvas coordinates based on the relative positions
                    canvas_x = dot_x * self.original_image_width
                    canvas_y = dot_y * self.original_image_height
                    # Create a square at the specified position
                    square_id = self.image_canvas.create_rectangle(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill=self.selected_dot_color)
                    # Remove the current square from the canvas
                    if self.active_square:
                        self.image_canvas.delete(self.active_square[0])
                    # Store the active square
                    self.active_dot = (square_id, canvas_x, canvas_y)
                    # Reset active square
                    self.active_square = None
                else:
                    # If the second column is not None, it indicates a square
                    # Calculate canvas coordinates based on the relative positions
                    x1, y1 = entry[0][0] * self.original_image_width, entry[0][1] * self.original_image_height
                    x2, y2 = entry[1][0] * self.original_image_width, entry[1][1] * self.original_image_height
                    # Create a square at the specified position
                    square_id = self.image_canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_dot_color, stipple="gray50")
                    # Remove the current square from the canvas
                    if self.active_square:
                        self.image_canvas.delete(self.active_square[0])
                    # Update the active square
                    self.active_square = (square_id, x1, y1, x2, y2)
                
                # Decrement the history pointer
                self.history_pointer["square"] -= 1
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

    def rollforward_square(self):
        try:
            # Check if there are any squares ahead in the history
            if self.history_pointer["square"] < len(self.dot_locations_history["square"]) - 1:
                # Increment the history pointer for the square option
                self.history_pointer["square"] += 1

                # Get the next square location from history
                next_location = self.dot_locations_history["square"][self.history_pointer["square"]]

                # Check if the next location represents a dot
                if next_location[1] is None:
                    # If the next location is a dot, create a dot
                    x, y = next_location[0][0] * self.original_image_width, next_location[0][1] * self.original_image_height
                    dot_id = self.image_canvas.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill=self.selected_dot_color)
                    self.active_dot = (dot_id, x, y)
                else:
                    # If the next location represents a square, create a square
                    if self.active_dot is not None:
                        self.image_canvas.delete(self.active_dot[0])
                        self.active_dot = None
                    elif self.active_square is not None:
                        self.image_canvas.delete(self.active_square[0])
                    x1, y1 = next_location[0][0] * self.original_image_width, next_location[0][1] * self.original_image_height
                    x2, y2 = next_location[1][0] * self.original_image_width, next_location[1][1] * self.original_image_height
                    square_id = self.image_canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_dot_color, stipple="gray50")
                    self.active_square = (square_id, x1, y1, x2, y2)
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
        
    def resize_square_position(self):
        try:
            square_history = self.dot_locations_history["square"]
            
            # Check if there's any history to rollback
            if self.history_pointer["square"] > 0:
                # Get the entry to resize
                entry = square_history[self.history_pointer["square"]]
                if entry[1] is None:
                    # If the second column is None, it indicates a dot
                    dot_x, dot_y = entry[0]
                    # Calculate canvas coordinates based on the relative positions
                    canvas_x = dot_x * self.original_image_width
                    canvas_y = dot_y * self.original_image_height
                    # Create a dot at the specified position
                    dot_id = self.image_canvas.create_rectangle(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill=self.selected_dot_color)
                    self.active_dot = (dot_id, canvas_x, canvas_y)
                    # Remove the current square from the canvas
                    if self.active_square:
                        self.image_canvas.delete(self.active_square[0])
                    # Reset active square
                    self.active_square = None
                else:
                    # If the second column is not None, it indicates a square
                    # Calculate canvas coordinates based on the relative positions
                    x1, y1 = entry[0][0] * self.original_image_width, entry[0][1] * self.original_image_height
                    x2, y2 = entry[1][0] * self.original_image_width, entry[1][1] * self.original_image_height
                    # Create a square at the specified position
                    square_id = self.image_canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_dot_color, stipple="gray50")
                    # Remove the last dot from the canvas
                    self.image_canvas.delete(entry[0][0])
                    # Remove the current square from the canvas
                    if self.active_square:
                        self.image_canvas.delete(self.active_square[0])
                    # Update the active square
                    self.active_square = (square_id, x1, y1, x2, y2)
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")



    def update_history(self, option, location):
        try:
            # Increment the history pointer and add the new location to the history list
            self.history_pointer[option] += 1
            self.dot_locations_history[option] = self.dot_locations_history[option][:self.history_pointer[option]] + [location]

            # Clear any forward history
            self.dot_locations_history[option] = self.dot_locations_history[option][:self.history_pointer[option] + 1]

            # Check if the number of locations exceeds the maximum allowed (5)
            if len(self.dot_locations_history[option]) > 5:
                # Clear the forward history if the maximum number of locations is exceeded
                self.dot_locations_history[option] = self.dot_locations_history[option][:5]
                self.history_pointer[option] = 4
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")


    def rollback(self):
        try:
            # Check the currently active option button
            if self.active_button == self.dot_button:
                self.rollback_dot()
            elif self.active_button == self.line_button:
                self.rollback_line()
            elif self.active_button == self.square_button:
                self.rollback_square()
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

    def rollforward(self):
        try:
            # Check the currently active option button
            if self.active_button == self.dot_button:
                self.rollforward_dot()
            elif self.active_button == self.line_button:
                self.rollforward_line()
            elif self.active_button == self.square_button:
                self.rollforward_square()
        except Exception as e:
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

    def edit_location(self):
            pass

    def save_button(self):
        save_data = []
         # Get current datetime
        current_datetime = datetime.datetime.now()

        # Format current datetime as YYYYMMDD_HHMMSS
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        save_data.append(formatted_datetime)
        for widget in self.location_info_frame.winfo_children():
                if isinstance(widget, (tk.CTkEntry, tk.CTkTextbox)):
                    if isinstance(widget, tk.CTkEntry):
                        save_data.append(widget.get())
                    elif isinstance(widget, tk.CTkTextbox):
                        save_data.append(widget.get('1.0', 'end'))  # Clear tk.CTkTextbox widget

        if self.active_button == self.dot_button:
            position = self.dot_locations_history["dot"][self.history_pointer["dot"]]
            mode = "dot"
            if not position:
                messagebox.showwarning("Incomplete Data", "Please pick a location in the map.")
                return
        elif self.active_button == self.line_button:
            position = self.dot_locations_history["line"][self.history_pointer["line"]]
            mode = "line"
            if position[0] == None or position[1] == None:
                messagebox.showwarning("Incomplete Data", "Please pick a location in the map.")
                return
        elif self.active_button == self.square_button:
            position = self.dot_locations_history["square"][self.history_pointer["square"]]
            mode = "square"
            if position[0] == None or position[1] == None:
                messagebox.showwarning("Incomplete Data", "Please pick a location in the map.")
                return
        
        save_data.append(position)
       
        save_data.append(mode)
        save_data.append(self.map_image)
        save_data.append(self.selected_dot_color)
        if save_data[3] and save_data[1] and save_data[2]:
            self.DBO.Insert_Map(save_data)
            self.show_default_display()
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")

    def return_button(self):
        if self.master_app:
            self.master_app.show_map()

    def add_table(self):
        data = self.DBO.Fetch_Map()

        for row in data:
            # Insert data into the table
            self.table.insert('', "end", values=(row[2], row[3]))

            # Create shape
            shape_id = None
            if row[9] == "square":
                x1, y1 = row[5] * self.original_image_width, row[6] * self.original_image_height
                x2, y2 = row[7] * self.original_image_width, row[8] * self.original_image_height
                shape_id = self.image_canvas.create_rectangle(x1, y1, x2, y2, fill=row[11] if row[11] is not None else "black", stipple="gray50")
            elif row[9] == "line":
                x1, y1 = row[5] * self.original_image_width, row[6] * self.original_image_height
                x2, y2 = row[7] * self.original_image_width, row[8] * self.original_image_height
                shape_id = self.image_canvas.create_line(x1, y1, x2, y2, fill=row[11] if row[11] is not None else "black")
            elif row[9] == "dot":
                x1, y1 = row[5] * self.original_image_width, row[6] * self.original_image_height
                shape_id = self.image_canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill=row[11] if row[11] is not None else "black")

            # Store shape data in shape_data dictionary
            self.shape_data.setdefault(str(row[2]), []).append({"shape_id": shape_id, "row": row})

        # Now shape_data dictionary contains all the data grouped by the location name
    def delete_table(self):
        # Delete all items from the Treeview widget
        self.table.delete(*self.table.get_children())

        # Delete all shapes on the canvas and clear shape_data dictionary
        for location_data in self.shape_data.values():
            for data in location_data:
                shape_id = data["shape_id"]
                # Delete shape from the canvas
                self.image_canvas.delete(shape_id)

        # Clear shape_data dictionary
        self.shape_data.clear()

    def refresh_table(self):
        self.delete_table()
        self.add_table()

    def on_row_select(self, event):
        selected_item = self.table.selection()
        if selected_item:
            
            item_data = self.table.item(selected_item)

            location_name = item_data['values'][0]
            self.refresh_table()
            self.highlight_shape(location_name)
        
        

    def highlight_shape(self, location_name):
        # Retrieve the data associated with the specified location name
        location_data = self.shape_data.get(str(location_name))
        if location_data:
            # Iterate through the shapes associated with the location
            for data in location_data:
                # Retrieve shape ID and row data
                shape_id = data["shape_id"]
                # Highlight the shape (you can customize this part based on your needs)
                self.image_canvas.itemconfig(shape_id, outline="red", width=10)  
                print(data["shape_id"],"selected")

def main():
    root = tk.CTk()
    app = EmrgFloor(root)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(2,weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    main()
