import customtkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
from tkinter import messagebox
from PIL import Image, ImageTk


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
                                  command=self.show_add_modal)
        add_button.grid(row=0, column=0, padx=10, pady=10)
        edit_button = tk.CTkButton(button_frame, text="修改地圖",
                                  command= self.edit_record)
        edit_button.grid(row=0, column=1, padx=10, pady=10)
        delete_button = tk.CTkButton(
            button_frame, text="批量刪除", command=self.delete_selected)
        delete_button.grid(row=0, column=2, padx=10, pady=10)

        close_window = tk.CTkButton(
            button_frame, text="關閉", fg_color="red", command=self.close_window_).grid(row=0, column="3")

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


    def close_window_(self):
        confirm_btn = messagebox.askyesno("確認",
                            "你確定嗎？")
        if confirm_btn == True:
            self.root.destroy()

    def show_add_modal(self):
        add_modal = tk.CTkToplevel(self.root)
        add_modal.title("新增地圖")
        add_modal.transient(self.root)

        fm_map_id_label = tk.CTkLabel(add_modal, text="地圖編號")
        fm_map_id_label.grid(row=0, column=0, padx=10, pady=5)
        global fm_map_id_entry
        fm_map_id_entry = tk.CTkEntry(add_modal)
        fm_map_id_entry.grid(row=0, column=1, padx=10, pady=5)

        fm_map_name_label = tk.CTkLabel(add_modal, text="地圖名稱")
        fm_map_name_label.grid(row=1, column=0, padx=10, pady=5)
        global fm_map_name_entry
        fm_map_name_entry = tk.CTkEntry(add_modal)
        fm_map_name_entry.grid(row=1, column=1, padx=10, pady=5)

        fm_map_img_label = tk.CTkLabel(add_modal, text="地圖影像")
        fm_map_img_label.grid(row=2, column=0, padx=10, pady=5)
        global fm_map_img_button
        fm_map_img_button = tk.CTkButton(
            add_modal, text="選擇檔案", command=self.select_image)
        fm_map_img_button.grid(row=2, column=1, padx=10, pady=5)

        add_button = tk.CTkButton(add_modal, text="新增", command=lambda: self.add_map(
            fm_map_id_entry.get(), fm_map_name_entry.get(), self.image_path))
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


    def show_add_modal2(self, map_id="", map_name="", map_time=""):
        add_modal = tk.CTkToplevel(self.root)
        add_modal.title("新增地圖")
        add_modal.transient(self.root)

        fm_map_id_label = tk.CTkLabel(add_modal, text="地圖編號")
        fm_map_id_label.grid(row=0, column=0, padx=10, pady=5)
        fm_map_id_entry = tk.CTkEntry(add_modal)
        fm_map_id_entry.grid(row=0, column=1, padx=10, pady=5)
        fm_map_id_entry.insert(0, map_id)  # Fill map_id if provided

        fm_map_name_label = tk.CTkLabel(add_modal, text="地圖名稱")
        fm_map_name_label.grid(row=1, column=0, padx=10, pady=5)
        fm_map_name_entry = tk.CTkEntry(add_modal)
        fm_map_name_entry.grid(row=1, column=1, padx=10, pady=5)
        fm_map_name_entry.insert(0, map_name)  # Fill map_name if provided

        fm_map_img_label = tk.CTkLabel(add_modal, text="地圖影像")
        fm_map_img_label.grid(row=2, column=0, padx=10, pady=5)
        fm_map_img_button = tk.CTkButton(
            add_modal, text="選擇檔案", command=self.select_image)
        fm_map_img_button.grid(row=2, column=1, padx=10, pady=5)

        # Update button to update the record
        update_button = tk.CTkButton(add_modal, text="更新", command=lambda: self.update_map(
            map_id, fm_map_id_entry.get(), fm_map_name_entry.get(), map_time, self.image_path))
        update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.png")])
        # Call a new function and pass the file_path as an argument
        self.process_image(file_path)
        print("ok")

    def process_image(self, file_path):
        # Do something with the file_path
        print("ok555")
        self.image_path = file_path
        # For example, you can display the image in a label or perform other operations

    def add_map(self, map_id, map_name, image):
        created_date = modified_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Load the image
        image_path = image  # Replace with the actual image path
        image = Image.open(image_path)
        # Resize the image if needed
        image = image.resize((50, 50))  # Adjust the size as needed
        # Convert the image to Tkinter PhotoImage
        photo_image = ImageTk.PhotoImage(image)

        # Count the number of items in the table
        item_count = len(self.table.get_children())

        # Insert the data into the Treeview widget with the item count as No.
        self.table.insert("", "end", text=str(item_count + 1),
                          values=(map_id, map_name, created_date, modified_date, image_path), image=photo_image)  # Insert the image into the new column

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
            confirm_delete = messagebox.askquestion("確認提醒",
                                                    "你確定要刪除資料嗎？")
            if confirm_delete == "yes":
            # Remove the selected item from the Treeview
                self.table.delete(selected_item)
        else:
            # If no item is selected, display a message or perform other actions
            messagebox.showinfo("No Item Selected",
                                "Please select an item to delete.")

    def edit_record(self):
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
            self.show_add_modal2(map_id, map_name, map_create_time)
        else:
            messagebox.showinfo("No Item Selected",
                                "Please select an item to delete.")   


def main():
    root = tk.CTk()
    app = MapManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
