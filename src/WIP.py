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
        self.root.geometry("400x400")
        self.root.update()


        self.dot_locations_history = {"dot": [], "line": [], "square": []}  # Dictionary to store past dot locations for each option button
        self.history_pointer = {"dot": -1, "line": -1, "square": -1}  # Pointer to track the current position in history
        self.dot_button = None
        self.square_button = None
        self.line_button = None
        self.active_button = None
        self.original_image_size = None
        self.active_dot = None
        self.original_image_width = None
        self.original_image_height = None
        self.selected_dot_color = "black"

        self.create_add_location_display()  
        self.create_default_display()  
        self.add_image()

        self.default_display.bind("<Configure>",self.on_root_resize)
        self.top_widget.bind("<Configure>",self.on_root_resize)


    def on_root_resize(self,event=None):
        self.resize_canvas()
        self.resize_dot_position()
            
    # Other methods...
    def add_image(self):
        available_width = self.root.winfo_width() - self.default_display.winfo_reqwidth()
        available_height = self.root.winfo_height() - self.top_widget.winfo_reqheight()  # Adjusted for the top widget

        # Load the image
        image_path = "img\\F1.jpg"  # Replace with the path to your image
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

    def resize_canvas(self):
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
            return  # Do nothing if the button is already active

        # Deactivate the currently active button (if any)
        if self.active_button:
            self.active_button.configure(fg_color="blue")
            # Remove binding from the dot button if it's not active
            if self.active_button == self.dot_button:
                self.image_canvas.unbind("<Button-1>")
            # Remove binding from the line button if it's not active
            elif self.active_button == self.line_button:
                self.image_canvas.unbind("<Button-1>")
            # Remove binding from the square button if it's not active
            elif self.active_button == self.square_button:
                self.image_canvas.unbind("<Button-1>")

        # Activate the selected button
        self.active_button = button
        button.configure(fg_color="darkblue")
        
        # Bind the dot_button_clicked method when dot button is active
        if button == self.dot_button:
            self.dot_button_clicked()
        # Bind the line_button_clicked method when line button is active
        elif button == self.line_button:
            self.line_button_clicked()
            self.clear_dot()
        # Bind the square_button_clicked method when square button is active
        elif button == self.square_button:
            self.square_button_clicked()
            self.clear_dot()

    def create_default_display(self):
        # Create default display
        self.default_display = tk.CTkFrame(self.root, fg_color="red", width=200+self.root.winfo_width()*0.1)
        self.default_display.grid(row=0, column=1, rowspan = 3,sticky="nsew")

        self.top_widget = tk.CTkFrame(self.root, fg_color="green",height=1)
        self.top_widget.grid(row=0, column=2,columnspan = 999, sticky="nsew")
        self.top_widget.grid_columnconfigure(0, weight=1)

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
        self.add_location_display.grid(row=0, column=1, rowspan=3,sticky="nsew")
        
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
        self.dot_button = self.create_option_button(option_frame, self.dot_photo, "點", active=True)
        self.dot_button.grid(row=0, column=0, padx=0, pady=0)
        self.active_button = self.dot_button

        self.line_button = self.create_option_button(option_frame, self.line_photo, "線")
        self.line_button.grid(row=0, column=1, padx=0, pady=0)

        self.square_button = self.create_option_button(option_frame, self.square_photo, "區域")
        self.square_button.grid(row=0, column=2, padx=0, pady=0)
        

        # Create rollback and rollforward buttons frame
        roll_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        roll_frame.grid(row=1, column=1, padx=1, pady=10)  # Adjust padx to 1

        # Convert images for rollback and rollforward buttons
        self.rollback_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollback.png"), size=(20, 20))
        self.rollforward_photo = tk.CTkImage(light_image=Image.open("img\\symbol\\Rollforward.png"), size=(20, 20))
        
        # Create rollback and rollforward buttons with images and text
        rollback_button = tk.CTkButton(roll_frame, image=self.rollback_photo, text="", compound="top", width=35, height=35,fg_color="blue",command=self.rollback)
        rollback_button.grid(row=0, column=0, padx=0, pady=0)
        
        rollforward_button = tk.CTkButton(roll_frame, image=self.rollforward_photo, text="", compound="top", width=35, height=35,fg_color="blue", command=self.rollforward)
        rollforward_button.grid(row=0, column=1, padx=0, pady=0)
        
        # Create color frame with button
        color_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"))
        color_frame.grid(row=1, column=2, padx=1, pady=10)  # Adjust padx to 1
        color_frame.columnconfigure(0, weight=0)  # Set weight of column to 0
        
        # Create a button in the color_frame
        self.color_button = tk.CTkButton(color_frame, text="", width=35, height=35, fg_color="blue",command=self.pick_color)
        self.color_button.grid(row=0, column=0, padx=1, pady=10)

        # Create a canvas for the color square
        self.color_canvas = tk.CTkCanvas(self.color_button, width=20, height=20,background="black")
        self.color_canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Bind canvas events to propagate upwards
        self.color_canvas.bind("<Button-1>", lambda event: self.color_button.invoke())

        # Create a box frame to contain the location information widgets
        self.location_info_frame = tk.CTkFrame(self.add_location_display, fg_color=self.add_location_display.cget("fg_color"),border_width=2)
        self.location_info_frame.grid(row=2, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        # Add 地點資訊 label
        location_info_label = tk.CTkLabel(self.location_info_frame, text="地點資訊", font=("Arial", 16, "bold"))
        location_info_label.grid(row=0, column=0, columnspan=3, padx=1, pady=10, sticky="nsew")

        # Add 地點代號 label and entry
        location_code_label = tk.CTkLabel(self.location_info_frame, text="地點代號", font=("Arial", 12))
        location_code_label.grid(row=1, column=0, padx=(10, 2), pady=5, sticky="e")
        location_code_entry = tk.CTkEntry(self.location_info_frame)
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
        remark_label.grid(row=4, column=0, padx=2, pady=(5,0), sticky="e")
        remark_entry = tk.CTkTextbox(self.location_info_frame, width=1, height=100, wrap="word")
        remark_entry.grid(row=5, column=0, columnspan=3, padx=(10, 2), pady=(0,1), sticky="we")

        # Add return button to the add location display
        save_button = tk.CTkButton(self.location_info_frame, text="Save")
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
            # Store the selected color
            self.selected_dot_color = color[1]

            self.recolor_active_dot()

    def show_default_display(self):
        self.image_canvas.unbind("<Button-1>")
        # Show default display and hide add location display
        self.default_display.lift()
        if hasattr(self, 'add_location_display'):
            self.add_location_display.lower()

        self.on_root_resize()
        self.clear_elements()

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

    def clear_elements(self):
        # Clear all entry and textbox widgets
        self.clear_entry_and_textbox()

        # Clear the dot and reset dot history
        self.clear_dot()

    def clear_entry_and_textbox(self):
        # Clear all entry and textbox widgets in the add_location_display
        for widget in self.location_info_frame.winfo_children():
            if isinstance(widget, (tk.CTkEntry, tk.CTkTextbox)):
                if isinstance(widget, tk.CTkEntry):
                    widget.delete("0", "end")  # Clear tk.CTkEntry widget
                elif isinstance(widget, tk.CTkTextbox):
                    widget.delete("0.0", "end")  # Clear tk.CTkTextbox widget

    def clear_dot(self):
        # Remove the active dot from the canvas if it exists
        if self.active_dot:
            self.image_canvas.delete(self.active_dot[0])
            self.active_dot = None
            # Clear the dot history
            self.dot_locations_history["dot"] = []
            # Reset history pointer
            self.history_pointer["dot"] = -1
        
    def edit_location(self):
        pass

    def dot_button_clicked(self):
        # Bind a click event to the image_canvas
        self.image_canvas.bind("<Button-1>", self.place_or_remove_dot)
    def place_or_remove_dot(self, event):
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
    def recolor_active_dot(self):
            # Check if there is an active dot
            if self.active_dot:
                dot_id, _, _ = self.active_dot
                # Update the fill color of the active dot with the selected color
                self.image_canvas.itemconfig(dot_id, fill=self.selected_dot_color)
    def resize_dot_position(self):
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
    def rollback_dot(self):
        # Decrement the history pointer for the dot option button
        if self.history_pointer["dot"] > 0:
            self.history_pointer["dot"] -= 1
            print("History pointer decremented to:", self.history_pointer["dot"])

        # Move the dot to the previous location in history
        previous_location = self.dot_locations_history["dot"][self.history_pointer["dot"]]
        print("Previous location from history:", previous_location)
        self.move_dot_to_location(previous_location)
    def rollforward_dot(self):
        # Increment the history pointer for the dot option button
        if self.history_pointer["dot"] < len(self.dot_locations_history["dot"]) - 1:
            self.history_pointer["dot"] += 1

        # Move the dot to the next location in history
        self.move_dot_to_location(self.dot_locations_history["dot"][self.history_pointer["dot"]])
    def move_dot_to_location(self, location):



        # Calculate canvas coordinates based on the original image size
        canvas_x = location[0] * self.original_image_width
        canvas_y = location[1] * self.original_image_height

        # Update the coordinates of the dot on the canvas
        if self.active_dot:
            dot_id, _, _ = self.active_dot
            self.image_canvas.coords(dot_id, canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2)

    def line_button_clicked(self):
        self.image_canvas.bind("<Button-1>", self.place_or_remove_line)
    def place_or_remove_line(self, event):
        # Get the coordinates of the click event
        x, y = event.x, event.y

        # Check if there are already two dots present
        if len(self.dot_locations_history["line"]) >= 2:
            # Remove the oldest dot and the line connected to it
            oldest_dot = self.dot_locations_history["line"].pop(0)
            self.image_canvas.delete(self.active_line)
            # Clear the active_line attribute
            del self.active_line
        else:
            # Create a new dot at the clicked location
            dot_id = self.image_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.selected_dot_color)
            # Set the active_line attribute to the dot ID
            self.active_line = dot_id

        # Update the dot location in the dot_locations_history dictionary
        self.dot_locations_history["line"].append((x, y))

        # Draw the line connecting the dots
        if len(self.dot_locations_history["line"]) >= 2:
            # Get the coordinates of the last two dots
            x1, y1 = self.dot_locations_history["line"][-2]
            x2, y2 = self.dot_locations_history["line"][-1]
            # Draw a line between the last two dots
            line_id = self.image_canvas.create_line(x1, y1, x2, y2, fill=self.selected_dot_color, width=2)
            # Set the active_line attribute to the line ID
            self.active_line = line_id

        # Update the history for the line option
        self.update_history("line", (x, y))




        def rollback_line(self):
            # Remove the last dot from the canvas
            self.image_canvas.delete(self.dot_locations_history["line"].pop())

            # Remove the last line from the canvas
            self.image_canvas.delete(self.active_line)
            # Clear the active_line attribute
            del self.active_line

            # Update the history pointer for the line option
            self.history_pointer["line"] -= 1

    def rollforward_line(self):
        # Add the dot back to the canvas
        x, y = self.dot_locations_history["line"][self.history_pointer["line"]]
        dot_id = self.image_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        # Set the active_line attribute to the dot ID
        self.active_line = dot_id

        # Draw the line connecting the dots
        if len(self.dot_locations_history["line"]) >= 2:
            # Get the coordinates of the last two dots
            x1, y1 = self.dot_locations_history["line"][-2]
            x2, y2 = self.dot_locations_history["line"][-1]
            # Draw a line between the last two dots
            line_id = self.image_canvas.create_line(x1, y1, x2, y2, fill=self.line_color, width=2)
            # Set the active_line attribute to the line ID
            self.active_line = line_id

        # Update the history pointer for the line option
        self.history_pointer["line"] += 1


    def square_button_clicked(self):
        pass  # Temporary empty method for square button


    def update_history(self, option, location):
        # Increment the history pointer and add the new location to the history list
        self.history_pointer[option] += 1
        self.dot_locations_history[option] = self.dot_locations_history[option][:self.history_pointer[option]] + [location]

        # Clear any forward history
        self.dot_locations_history[option] = self.dot_locations_history[option][:self.history_pointer[option] + 1]

        # Check if the number of locations exceeds the maximum allowed (5)
        if len(self.dot_locations_history[option]) > 5:
            # Clear the forward history if the maximum number of locations is exceeded
            self.dot_locations_history[option] = self.dot_locations_history[option][:5]

    def rollback(self):
        # Check the currently active option button
        if self.active_button == self.dot_button:
            self.rollback_dot()
        elif self.active_button == self.line_button:
            self.rollback_line()
        elif self.active_button == self.square_button:
            self.rollback_square()
    def rollforward(self):
        # Check the currently active option button
        if self.active_button == self.dot_button:
            self.rollforward_dot()
        elif self.active_button == self.line_button:
            self.rollforward_line()
        elif self.active_button == self.square_button:
            self.rollforward_square()




def main():
    root = tk.CTk()
    app = MyApplication(root)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(2,weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    main()
