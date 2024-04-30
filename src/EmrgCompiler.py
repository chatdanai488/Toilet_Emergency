import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import colorchooser
import inspect
import DB
from update import InoFileEditor
from uploadesp32 import ArduinoSketchUploader

class EmrgCompiler:
    def __init__(self, root, master_app=None):
        self.root = root
        self.master_app = master_app
        screen_height, screen_width = self.root.winfo_screenheight(), self.root.winfo_screenwidth()
        # self.root.title("My New Project")
        # self.root.geometry(f'{screen_height}x{screen_width}+0+0')
        self.root.update()
        self.DBO = DB.DB()

        self.original_image_size = None
        self.active_dot = None
        self.active_line = None
        self.active_square = None
        self.original_image_width = None
        self.original_image_height = None
        self.selected_dot_color = "red"
        self.active_edit_shape = None
        self.map_image = None

        # self.uploader = ArduinoSketchUploader()

        self.shape_data = {}

        self.create_emrgCompiler_display() 
        if self.map_image: 
            self.add_image()

        self.emrgCompiler_display.bind("<Configure>",self.on_root_resize)
        self.top_widget.bind("<Configure>",self.on_root_resize)


    def on_root_resize(self, event=None):
        try:
            if self.map_image:
                self.resize_canvas()

            self.refresh_table()
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")
            
    # Other methods...
    def add_image(self):
        try:
            available_width = self.root.winfo_width() - self.emrgCompiler_display.winfo_reqwidth()
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
            if not hasattr(self, 'image_canvas'):
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
            canvas_width = self.root.winfo_width() - self.emrgCompiler_display.winfo_reqwidth()
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

    def create_emrgCompiler_display(self):
        try:
            # Create default display frame
            self.emrgCompiler_display = tk.CTkFrame(self.root, fg_color="lightgreen", width=200)
            self.emrgCompiler_display.grid(row=0, column=1, rowspan=3, sticky="nsew")

            # Create top widget frame
            self.top_widget = tk.CTkFrame(self.root, fg_color="green", height=1)
            self.top_widget.grid(row=0, column=2, columnspan=999, sticky="nsew")
            self.top_widget.grid_columnconfigure(0, weight=1)

            # Add buttons to the default display
            self.add_return_button()
            self.add_compiler_button()
            # Create table
            self.create_table()
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

            
    def add_return_button(self):
        # Add return button to the default display
        return_button = tk.CTkButton(self.emrgCompiler_display, text="Return", command=self.return_button)
        return_button.grid(row=0, column=0, padx=10, pady=2)
    def add_compiler_button(self):
        # Add add location button to the default display
        self.compiler_button = tk.CTkButton(self.emrgCompiler_display, text="Add Compiler", command=self.Compile_Arduino)
        self.compiler_button.grid(row=1, column=0, padx=10, pady=2)
        self.compiler_button.grid_forget()
    
    def create_table(self):
        try:
            style = ttk.Style()
            style.configure("Treeview", font=("Helvetica", 12))  # Adjust the font size here
            style.configure("Treeview.Heading", font=("Helvetica", 12))
            # Create treeview widget
            self.CompilerTable = ttk.Treeview(self.emrgCompiler_display, columns=("Location Name", "Camera IP"), show="headings", style="Treeview")

            # Define headings
            self.CompilerTable.heading("Location Name", text="Location Name")
            self.CompilerTable.heading("Camera IP", text="Camera IP")

            # Set column widths
            self.CompilerTable.column("Location Name", width=150)
            self.CompilerTable.column("Camera IP", width=150)
            # Create vertical scrollbar
            v_scrollbar = ttk.Scrollbar(self.emrgCompiler_display, orient="vertical", command=self.CompilerTable.yview)
            self.CompilerTable.configure(yscrollcommand=v_scrollbar.set)

            # Attach the scrollbar and the table using grid
            self.CompilerTable.grid(row=4, column=0, columnspan=2, sticky="nsew")

            # Configure row and column weights for proper resizing
            self.emrgCompiler_display.grid_rowconfigure(4, weight=1)
            self.emrgCompiler_display.grid_columnconfigure(0, weight=1)

            # Callback to handle scrollbar visibility
            def check_scrollbar_visibility(event=None):
                if len(self.CompilerTable.get_children()) > 15:  # Adjust threshold as needed
                    v_scrollbar.grid(row=3, column=2, sticky="ns")
                else:
                    v_scrollbar.grid_forget()

            # Bind the callback to configure event
            self.CompilerTable.bind("<Configure>", check_scrollbar_visibility)
            #self.CompilerTable.bind("<<TreeviewSelect>>", self.on_row_select)
            self.CompilerTable.bind("<Button-1>", self.on_row_select)
            
            # Initial check for scrollbar visibility
            check_scrollbar_visibility()

        except Exception as e:
            # Handle any errors during table creation
            method_name = inspect.currentframe().f_code.co_name
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

    def return_button(self):
        if self.master_app:
            if self.image_id:
                self.image_canvas.delete(self.image_id)
                self.map_image = None
            self.clear()
            self.delete_table()
                

            self.master_app.show_frames("EmrgMap")

    def add_table(self,map_path):
        data = self.DBO.Fetch_Map(map_path)

        for row in data:
            # Insert data into the table
            self.CompilerTable.insert('', "end", values=(row[2], row[3]))

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

            loc_map = row[2] + " " + row[10]
            # Store shape data in shape_data dictionary
            self.shape_data.setdefault(str(row[2]), []).append({"shape_id": shape_id, "row": row,"loc_map":loc_map})
            print(loc_map.split())

        # Now shape_data dictionary contains all the data grouped by the location name
    def delete_table(self):
        # Delete all items from the Treeview widget
        self.CompilerTable.delete(*self.CompilerTable.get_children())

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
        self.add_table(self.map_image)
        

    def on_row_select(self, event):
        selected_item = self.CompilerTable.selection()
        if selected_item:
            
            item_data = self.CompilerTable.item(selected_item)

            self.edit_location_name = item_data['values'][0]
            self.refresh_table()
            self.highlight_shape(self.edit_location_name)
            self.show_hidden_button()
            self.retrieve_Info(self.edit_location_name)
        
    def show_hidden_button(self):
        self.compiler_button.grid(row=1, column=0, padx=10, pady=2)

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



        
    
        
   

    def create_current_active_shape(self):
        coordinates = [self.edit_shape_data[0][0][0],self.edit_shape_data[0][0][1],self.edit_shape_data[0][1][0],self.edit_shape_data[0][1][1]]
        print(coordinates)
        if self.edit_shape_data[1] == "square":
            x1, y1 = coordinates[0] * self.original_image_width, coordinates[1] * self.original_image_height
            x2, y2 = coordinates[2] * self.original_image_width, coordinates[3] * self.original_image_height
            self.active_edit_shape = self.image_canvas.create_rectangle(x1, y1, x2, y2, fill=self.edit_shape_data[3] if self.edit_shape_data[3] is not None else "black", stipple="gray50")
        elif self.edit_shape_data[1] == "line":
            x1, y1 = coordinates[0] * self.original_image_width, coordinates[1] * self.original_image_height
            x2, y2 = coordinates[2] * self.original_image_width, coordinates[3] * self.original_image_height
            self.active_edit_shape = self.image_canvas.create_line(x1, y1, x2, y2, fill=self.edit_shape_data[3] if self.edit_shape_data[3] is not None else "black")
        elif self.edit_shape_data[1] == "dot":
            x1, y1 = coordinates[0] * self.original_image_width, coordinates[1] * self.original_image_height
            self.active_edit_shape = self.image_canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill=self.edit_shape_data[3] if self.edit_shape_data[3] is not None else "black")

    def receive_value(self,value):
        self.map_image = value
        self.add_image()
        self.on_root_resize()

    def retrieve_Info(self,value):
        # Retrieve the data associated with the specified location name
        location_data = self.shape_data.get(str(value))
        if location_data:
            # Iterate through the shapes associated with the location
            for data in location_data:
                # Retrieve shape ID and row data
                self.location_and_map = data["loc_map"]
                print(self.location_and_map)

    def Compile_Arduino(self):
        # file_path = "sketch_test1\sketch_test1.ino"
        
        ino_editor = InoFileEditor()
        # data = ino_editor.update_code(wifi_name, mycom_ip, my_port)
        data = ino_editor.auto_update(self.location_and_map)
        ino_editor.write_code(data)
        print(self.location_and_map)

        
        if self.uploader.compile_sketch():
            if self.uploader.upload_sketch():
                # uploader.communicate_serial()
                print("ok")


        

def main():
    root = tk.CTk()
    app = EmrgCompiler(root)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(2,weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    main()
