import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import shutil
import DB 
import Constants

DBO = DB.DB()

class MapManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("地圖管理")
        self.root.geometry("800x600")
        self.icon_path = "img\logo1.ico"
        self.root.iconbitmap(self.icon_path)

        self.create_widgets()
        self.image_path = None

    def create_widgets(self):
        # Navigation bar
        nav_frame = tk.CTkFrame(self.root)
        nav_frame.pack(fill=tk.X)
        nav_label = tk.CTkLabel(nav_frame, text="地圖管理",
                                font=("Helvetica", 16, "bold"))
        nav_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Buttons
        button_frame = tk.CTkFrame(self.root)
        button_frame.pack(fill=tk.X)
        add_button = tk.CTkButton(button_frame, text="新增地圖",
                                  command=self.open_add_map)
        add_button.grid(row=0, column=0, padx=10, pady=10)
        delete_button = tk.CTkButton(
            button_frame, text="批量刪除", command=self.delete_selected)
        delete_button.grid(row=0, column=1, padx=10, pady=10)

        close_window = tk.CTkButton(
            button_frame, text="關閉", fg_color="red", command=self.close_window_).grid(row=0, column="2")

        # Map data table
        table_frame = tk.CTkFrame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)
        self.table = ttk.Treeview(table_frame, columns=(
            "Map ID", "Map Name", "Created Date", "Modified Date", "Image"))
        self.table.heading("#0", text="序")
        self.table.heading("Map ID", text="地圖編號")
        self.table.heading("Map Name", text="地圖名稱")
        self.table.heading("Created Date", text="創建日期")
        self.table.heading("Modified Date", text="修改日期")
        self.table.heading("Image", text="地圖影像")
        self.table.pack(fill=tk.BOTH, expand=True)

        # Bind double click event to edit record
        self.table.bind("<Double-1>", self.edit_record)
        self.Table_Add()

    def close_window_(self):
        self.root.destroy()
        
    def open_add_map(self):
        self.add_modal = tk.CTkToplevel(self.root)
        self.add_modal.title("新增地圖")
        self.add_modal.transient(self.root)

        #Map ID Label
        map_id_label = tk.CTkLabel(self.add_modal, text="地圖編號")
        map_id_label.grid(row=0, column=0, padx=10, pady=5)
        validate_int = self.add_modal.register(self.validate_int)
        map_id_entry = tk.CTkEntry(self.add_modal,validate="key", validatecommand=(validate_int, "%P"))
        map_id_entry.grid(row=0, column=1, padx=10, pady=5)

        #Map Name Label
        map_name_label = tk.CTkLabel(self.add_modal, text="地圖名稱")
        map_name_label.grid(row=1, column=0, padx=10, pady=5)
        map_name_entry = tk.CTkEntry(self.add_modal)
        map_name_entry.grid(row=1, column=1, padx=10, pady=5)

        #Map Image Label
        map_img_label = tk.CTkLabel(self.add_modal, text="地圖影像")
        map_img_label.grid(row=2, column=0, padx=10, pady=5)
        map_img_button = tk.CTkButton(self.add_modal, text="選擇檔案", command=self.Upload_Image)
        map_img_button.grid(row=2, column=1, padx=10, pady=5)
        self.map_img_path = tk.CTkLabel(self.add_modal, text="")
        self.map_img_path.grid(row=3,column=0, padx=10, pady=5)

        add_button = tk.CTkButton(self.add_modal, text="新增", command=lambda: self.save_data(
            map_id_entry.get(), map_name_entry.get(), self.image_path))
        add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def save_data(self,ID,Name,Image):
        if ID and Name and Image:
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

            _, picture_filename = os.path.split(Image)
            picture_name, picture_ext = os.path.splitext(picture_filename)
            picture_name = current_datetime.strftime("%Y%m%d_%H%M%S")
            # Generate new picture file name based on current datetime
            new_picture_filename = f"{picture_name}{picture_ext}"
            new_picture_path = os.path.join(target_folder, new_picture_filename)

            # Copy picture to target folder with new file name
            shutil.copy(Image, new_picture_path)

            # Create an array and push the data
            data = [ID, Name, formatted_datetime,formatted_datetime,new_picture_path]
            print("Data:", data)
            # You can perform further actions with the data, such as saving it to a file or database

            DBO.Insert_Floor(data)
            # Close the add_map_window
            self.Clear_Table()
            self.add_modal.destroy()
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")
        print("ok")

    def Edit_Map(self, map_id, map_name, map_path):
        self.edit_modal = tk.CTkToplevel(self.root)
        self.edit_modal.title("新增地圖")
        self.edit_modal.transient(self.root)

        #Map ID Label
        map_id_label = tk.CTkLabel(self.edit_modal, text="地圖編號")
        map_id_label.grid(row=0, column=0, padx=10, pady=5)
        validate_int = self.edit_modal.register(self.validate_int)
        map_id_entry = tk.CTkEntry(self.edit_modal,validate="key", validatecommand=(validate_int, "%P"))
        map_id_entry.grid(row=0, column=1, padx=10, pady=5)
        map_id_entry.insert(0, map_id)  # Fill map_id if provided

        #Map Name Label
        map_name_label = tk.CTkLabel(self.edit_modal, text="地圖名稱")
        map_name_label.grid(row=1, column=0, padx=10, pady=5)
        map_name_entry = tk.CTkEntry(self.edit_modal)
        map_name_entry.grid(row=1, column=1, padx=10, pady=5)
        map_name_entry.insert(0, map_name)  # Fill map_name if provided

        #Map Image Label
        map_img_label = tk.CTkLabel(self.edit_modal, text="地圖影像")
        map_img_label.grid(row=2, column=0, padx=10, pady=5)
        map_img_button = tk.CTkButton(self.edit_modal, text="選擇檔案", command=self.Upload_Image)
        map_img_button.grid(row=2, column=1, padx=10, pady=5)
        self.map_img_path = tk.CTkLabel(self.edit_modal, text="")
        self.map_img_path.grid(row=3,column=0, padx=10, pady=5)
        self.map_img_path.configure(text=map_path)

        # Update button to update the record
        update_button = tk.CTkButton(self.edit_modal, text="更新", command=lambda: self.update_data(
            map_path, map_id_entry.get(), map_name_entry.get(), self.image_path))
        update_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def edit_record(self, event):
        # Get the selected item from the treeview
        selected_item = self.table.selection()
        if selected_item:
            # Get the data from the selected item
            item_data = self.table.item(selected_item)
            # Assuming the map ID is the first column
            map_id = item_data['values'][0]
            # Assuming the map name is the second column
            map_name = item_data['values'][1]

            map_path = item_data['values'][4]
            # Open the add modal with the data pre-filled
            self.Edit_Map(map_id, map_name, map_path)
 
    def update_data(self,OldImagePath,ID,Name,Image):
        if ID and Name and Image:
            # Get current datetime
            current_datetime = datetime.datetime.now()

            # Format current datetime as YYYYMMDD_HHMMSS
            formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")

            if Image != OldImagePath:
                os.remove(OldImagePath)
                # Define target folder for copied picture
                #current_directory = os.getcwd()
                #target_folder = os.path.join(current_directory, "img")
                target_folder = "img\\"
                
                # Create target folder if it doesn't exist
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                _, picture_filename = os.path.split(Image)
                picture_name, picture_ext = os.path.splitext(picture_filename)
                picture_name = current_datetime.strftime("%Y%m%d_%H%M%S")
                # Generate new picture file name based on current datetime
                new_picture_filename = f"{picture_name}{picture_ext}"
                new_picture_path = os.path.join(target_folder, new_picture_filename)

                # Copy picture to target folder with new file name
                shutil.copy(Image, new_picture_path)
            
            else:
                new_picture_path = Image

            # Create an array and push the data
            data = [ID, Name, formatted_datetime,new_picture_path,OldImagePath]
            # You can perform further actions with the data, such as saving it to a file or database
            
            
            DBO.Edit_Floor(data)
            # Close the add_map_window
            self.Clear_Table()
            self.edit_modal.destroy()

        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")
        print("ok")

    def Upload_Image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.png")])
        # Call a new function and pass the file_path as an argument
        if file_path:
            self.image_path = file_path
            self.map_img_path.configure(text=self.image_path)
        
    def Table_Add(self):
        data = DBO.Fetch_Floor()
        for i , Values in enumerate(data):

            self.table.insert("", "end", text = i+1,
                          values=Values) 

    def Clear_Table(self):
        self.table.delete(*self.table.get_children())
        self.Table_Add()

    def delete_selected(self):
        selected_item = self.table.selection()

        # Check if an item is selected
        if selected_item:
            # Get the data from the selected item
            item_data = self.table.item(selected_item)
            if os.path.exists(item_data['values'][4]):
                os.remove(item_data['values'][4])
            DBO.Delete_Floor(item_data['values'][0])
            
            self.Clear_Table()

        else:
            # If no item is selected, display a message or perform other actions
            messagebox.showinfo("No Item Selected",
                                "Please select an item to delete.")

    def validate_int(self, new_value):
        # Validate if the new value is an integer
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False


def main():
    root = tk.CTk()
    app = MapManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
