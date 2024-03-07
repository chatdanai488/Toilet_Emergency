import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import Constants
import Style
import datetime

class MapManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Management")
        self.add_map_window = None
        self.root.configure(background=Constants.Background_Color())

        self.width, self.height = Constants.get_screen_size()
        self.root.geometry(f"{self.width}x{self.height}")

        Style.button_style()
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

        self.map_table = tk.LabelFrame(self.root, text="地圖資料表",font=Constants.Font())
        self.map_table.pack(fill="both", expand=True, padx=10, pady=5)
        
        headers = ['序',	'地圖編號',	'地圖名稱',	'創建日期',	'修改日期',	'操作', '']
        Col_width = [10,20,40,40,40,20,10]
        for col, header in enumerate(headers):
            label = ttk.Label(self.map_table, text=header, relief=tk.RIDGE, width=Col_width[col],style='Table.TLabel')
            label.grid(row=0, column=col, sticky="ew")

        data = [
        ]
        
        # Populate table with data
        for row, row_data in enumerate(data, start=1):
            for col, value in enumerate(row_data):
                label = ttk.Label(self.map_table, text=value, relief=tk.RIDGE, width=Col_width[col])
                label.grid(row=row, column=col)
        
        # Center the table horizontally within its parent widget
        for i in range(1,8):
            self.map_table.grid_columnconfigure(i, weight=Col_width[i-1])
        
        
        
        # Center the table horizontally within its parent widget
        empty_label = ttk.Label(self.map_table, text="")
        empty_label.grid(row=1, column=0, columnspan=len(headers))
        
    def add_map_window_function(self):
        self.add_map_window = tk.Toplevel(root)
        self.add_map_window.title("Add Map")
        self.add_map_window.geometry("300x300+100+100")
        self.add_map_window.transient(self.root)

        # First field with label and textbox
        label1 = ttk.Label(self.add_map_window, text="Field 1:")
        label1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        textbox1 = ttk.Entry(self.add_map_window)
        textbox1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

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

            # Format current datetime as YYYY/MM/DD HH:MM:SS
            formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
            # Create an array and push the data
            data = [field1, field2, picture_path, formatted_datetime,formatted_datetime]
            print("Data:", data)
            # You can perform further actions with the data, such as saving it to a file or database

            # Close the add_map_window
            self.add_map_window.destroy()
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")
        
    def delete_maps(self):
        # Functionality for deleting maps
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MapManagementApp(root)
   
    root.mainloop()