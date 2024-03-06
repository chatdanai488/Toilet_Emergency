import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import Constants
import Style

class MapManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Management")
        
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

        self.new_map_button = ttk.Button(self.buttons_frame, text="新增地圖", command=self.add_map, style='New_Map_Btn.TButton')
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
        
    def add_map(self):
        # Functionality for adding a new map
        pass
        
    def delete_maps(self):
        # Functionality for deleting maps
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MapManagementApp(root)
   
    root.mainloop()