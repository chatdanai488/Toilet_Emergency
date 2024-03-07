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
        add_modal = tk.CTkToplevel(self.root)
        add_modal.title("新增地圖")
        add_modal.transient(self.root)

        #Map ID Label
        fm_map_id_label = tk.CTkLabel(add_modal, text="地圖編號")
        fm_map_id_label.grid(row=0, column=0, padx=10, pady=5)
        fm_map_id_entry = tk.CTkEntry(add_modal)
        fm_map_id_entry.grid(row=0, column=1, padx=10, pady=5)
        #Map Name Label
        fm_map_name_label = tk.CTkLabel(add_modal, text="地圖名稱")
        fm_map_name_label.grid(row=1, column=0, padx=10, pady=5)
        fm_map_name_entry = tk.CTkEntry(add_modal)
        fm_map_name_entry.grid(row=1, column=1, padx=10, pady=5)
        #Map Image Label
        fm_map_img_label = tk.CTkLabel(add_modal, text="地圖影像")
        fm_map_img_label.grid(row=2, column=0, padx=10, pady=5)
        fm_map_img_button = tk.CTkButton(
            add_modal, text="選擇檔案", command=self.Upload_Image)
        fm_map_img_button.grid(row=2, column=1, padx=10, pady=5)

        add_button = tk.CTkButton(add_modal, text="新增", command=lambda: self.save_data(
            fm_map_id_entry.get(), fm_map_name_entry.get(), self.image_path))
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def Edit_Map(self, map_id="", map_name="", map_time=""):
        add_modal = tk.CTkToplevel(self.root)
        add_modal.title("新增地圖")
        add_modal.transient(self.root)
        #Map ID Label
        fm_map_id_label = tk.CTkLabel(add_modal, text="地圖編號")
        fm_map_id_label.grid(row=0, column=0, padx=10, pady=5)
        fm_map_id_entry = tk.CTkEntry(add_modal)
        fm_map_id_entry.grid(row=0, column=1, padx=10, pady=5)
        fm_map_id_entry.insert(0, map_id)  # Fill map_id if provided
        #Map Name Label
        fm_map_name_label = tk.CTkLabel(add_modal, text="地圖名稱")
        fm_map_name_label.grid(row=1, column=0, padx=10, pady=5)
        fm_map_name_entry = tk.CTkEntry(add_modal)
        fm_map_name_entry.grid(row=1, column=1, padx=10, pady=5)
        fm_map_name_entry.insert(0, map_name)  # Fill map_name if provided
        #Map Image Label
        fm_map_img_label = tk.CTkLabel(add_modal, text="地圖影像")
        fm_map_img_label.grid(row=2, column=0, padx=10, pady=5)
        fm_map_img_button = tk.CTkButton(
            add_modal, text="選擇檔案", command=self.Upload_Image)
        fm_map_img_button.grid(row=2, column=1, padx=10, pady=5)

        # Update button to update the record
        update_button = tk.CTkButton(add_modal, text="更新", command=lambda: self.update_map(
            map_id, fm_map_id_entry.get(), fm_map_name_entry.get(), map_time, self.image_path))
        update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def Upload_Image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.png")])
        # Call a new function and pass the file_path as an argument
        if file_path:
            self.image_path = file_path
        
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
            self.add_map_window.destroy()
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all the fields.")
        print("ok")

    def Table_Add(self):
        data = DBO.Fetch_Floor()
        for i , Values in enumerate(data):

            self.table.insert("", "end", text = i+1,
                          values=Values) 
 


    def update_map(self, old_map_id, new_map_id, new_map_name, map_time, image):
        if not new_map_id or not new_map_name:
            # Display an error message if either map ID or map name is empty
            messagebox.showerror(
                "Error", "Please provide both map ID and map name.")
            return

        modified_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        selected_item = self.table.selection()

        if selected_item:
            # Update the values of the selected item in the Treeview
            self.table.item(selected_item, values=(
                new_map_id, new_map_name, map_time, modified_date, image))

            # Display a success message
            messagebox.showinfo("Success", "Map updated successfully.")

            # Close the add_modal if it's open
            self.close_add_modal()

        else:
            # If no item is selected, display an error message
            messagebox.showerror("Error", "Please select a map to update.")

    def delete_selected(self):
        selected_item = self.table.selection()

        # Check if an item is selected
        if selected_item:
            # Get the data from the selected item
            item_data = self.table.item(selected_item)
            DBO.Delete_Floor(item_data['values'][0])
        else:
            # If no item is selected, display a message or perform other actions
            messagebox.showinfo("No Item Selected",
                                "Please select an item to delete.")

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

            map_create_time = item_data['values'][2]
            # Open the add modal with the data pre-filled
            self.Edit_Map(map_id, map_name, map_create_time)


def main():
    root = tk.CTk()
    app = MapManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
