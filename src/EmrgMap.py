import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import Constants
import Style
import datetime
import os
import shutil
import DB

DBO = DB.DB()

class MapManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Management")
        self.add_map_window = None
        self.root.configure(background=Constants.Background_Color())

        self.width, self.height = Constants.get_screen_size()
        self.root.geometry(f"{self.width}x{self.height}")

        Style.button_style()
        Style.checkbox_style()
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Navigation frame
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(fill="x")
        
        tk.Label(self.nav_frame, text="地圖管理", font=Constants.Font()).pack(side="left", padx=10)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)

        self.new_map_button = ttk.Button(self.buttons_frame, text="新增地圖", command=self.add_map_window_function, style='New_Map_Btn.TButton')
        self.new_map_button.pack(side="left", padx=5)
        
        self.delete_button = ttk.Button(self.buttons_frame, text="批量刪除", command=self.delete_maps, style="Del_Map_Btn.TButton")
        self.delete_button.pack(side="left", padx=5)
        
        # Map table
        Style.table_style()

        # Create the LabelFrame with a border
        self.map_table = ttk.LabelFrame(self.root, text="地圖資料表", borderwidth=2, relief="groove")
        self.map_table.pack(fill="both", expand=True, padx=10, pady=5)

        # Apply the font to the text inside the LabelFrame
        label_font = Constants.Font()  # Assuming Constants.Font() returns the desired font
        self.map_table.config(labelwidget=tk.Label(self.map_table, font=label_font))

        # Define headers and column widths
        headers = ['序', '地圖編號', '地圖名稱', '創建日期', '修改日期', '操作', '']
        col_widths = [5, 10, 20, 20, 20, 10, 5]

        # Create a dictionary to store checkbox variables
        self.checkbox_vars = {}

        # Create labels for headers
        for col, header in enumerate(headers):
            background_color = "lightblue"
            label = ttk.Label(self.map_table, text=header, width=col_widths[col], style='Table.TLabel', borderwidth=1, relief="solid", background=background_color)
            label.grid(row=0, column=col, sticky="ew")

        data = DBO.Fetch_Floor()
        # Populate table with data
        for row, row_data in enumerate(data, start=1):
            for col, value in enumerate(row_data):
                if col == 6:  # Check if it's the 7th column
                    background_color = "lightblue" if row % 2 == 0 else "lightgrey"
                    checkbox_var = tk.BooleanVar(value=False)  # Start with unchecked state
                    checkbox = ttk.Checkbutton(self.map_table, variable=checkbox_var, style="TableBlue.TCheckbutton" if row % 2 == 0 else "TableGrey.TCheckbutton")
                    checkbox.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
                    # Store checkbox variable with corresponding value of 1st column
                    self.checkbox_vars[row_data[1]] = checkbox_var
                else:
                    background_color = "lightblue" if row % 2 == 0 else "lightgrey"
                    label = ttk.Label(self.map_table, text=value, width=col_widths[col], style='Table.TLabel', borderwidth=1, relief="solid", background=background_color)
                    label.grid(row=row, column=col, sticky="ew")

        # Center the table horizontally within its parent widget
        for i in range(len(headers)):
            self.map_table.grid_columnconfigure(i, weight=1)

        # Add an empty row at the bottom with a border
        border_frame = ttk.Frame(self.map_table, height=2, relief="groove")
        border_frame.grid(row=len(data) + 1, column=0, columnspan=len(headers), sticky="ew")

        
    def add_map_window_function(self):
        self.add_map_window = tk.Toplevel(root)
        self.add_map_window.title("Add Map")
        self.add_map_window.geometry("300x300+100+100")
        self.add_map_window.transient(self.root)

        # First field with label and textbox
        label1 = ttk.Label(self.add_map_window, text="Field 1:")
        label1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        # Entry widget with validation to allow only integers
        validate_int = self.add_map_window.register(self.validate_int)
        textbox1 = ttk.Entry(self.add_map_window, validate="key", validatecommand=(validate_int, "%P"))
        textbox1.grid(row=0, column=1, padx=5, pady=5)

        # Second field with label and textbox
        label2 = ttk.Label(self.add_map_window, text="Field 2:")
        label2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        textbox2 = ttk.Entry(self.add_map_window)
        textbox2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Upload button
        upload_button = ttk.Button(self.add_map_window, text="Upload", command=self.upload_file)
        upload_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Label beside the button
        label = ttk.Label(self.add_map_window, text="Upload Picture:", anchor="w")
        label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Label for the picture path
        self.picture_label = ttk.Label(self.add_map_window, text="", anchor="w")
        self.picture_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Another button
        save_button = ttk.Button(self.add_map_window, text="Save", command=lambda: self.save_data(textbox1.get(), textbox2.get(), self.picture_label.cget("text")))
        save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def validate_int(self, new_value):
        # Validate if the new value is an integer
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False
        
    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print("Selected file:", file_path)
            self.picture_label.config(text=file_path)

    def save_data(self, field1, field2, picture_path):
        # Check if all fields are filled
        if field1 and field2 and picture_path:
            # Get current datetime
            current_datetime = datetime.datetime.now()

            # Format current datetime as YYYYMMDD_HHMMSS
            formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")

            # Define target folder for copied picture
            #current_directory = os.getcwd()
            #target_folder = os.path.join(current_directory, "img")
            target_folder = "img\\"
            
            # Create target folder if it doesn't exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            _, picture_filename = os.path.split(picture_path)
            picture_name, picture_ext = os.path.splitext(picture_filename)
            picture_name = current_datetime.strftime("%Y%m%d_%H%M%S")
            # Generate new picture file name based on current datetime
            new_picture_filename = f"{picture_name}{picture_ext}"
            new_picture_path = os.path.join(target_folder, new_picture_filename)

            # Copy picture to target folder with new file name
            shutil.copy(picture_path, new_picture_path)

            # Create an array and push the data
            data = [field1, field2, formatted_datetime,formatted_datetime,new_picture_path]
            print("Data:", data)
            # You can perform further actions with the data, such as saving it to a file or database

            DBO.Insert_Floor(data)
            # Close the add_map_window
            self.add_map_window.destroy()
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")
        
    def delete_maps(self):
        # Iterate through the checkbox_vars dictionary
        for key, checkbox_var in self.checkbox_vars.items():
            # Check if the checkbox is checked
            if checkbox_var.get():
                # Delete the row from the database based on the key associated with the checkbox
                DBO.Delete_Floor(key)


if __name__ == "__main__":
    root = tk.Tk()
    app = MapManagementApp(root)
   
    root.mainloop()