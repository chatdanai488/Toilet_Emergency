import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
from tkinter import messagebox


class MapManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("地圖管理")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Navigation bar
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(fill=tk.X)
        nav_label = ttk.Label(nav_frame, text="地圖管理",
                              font=("Helvetica", 16, "bold"))
        nav_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X)
        add_button = ttk.Button(button_frame, text="新增地圖",
                                command=self.show_add_modal)
        add_button.grid(row=0, column=0, padx=10, pady=10)
        delete_button = ttk.Button(
            button_frame, text="批量刪除", command=self.delete_selected)
        delete_button.grid(row=0, column=1, padx=10, pady=10)

        # Map data table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True)
        self.table = ttk.Treeview(table_frame, columns=(
            "Map ID", "Map Name", "Created Date", "Modified Date"))
        self.table.heading("#0", text="序")
        self.table.heading("Map ID", text="地圖編號")
        self.table.heading("Map Name", text="地圖名稱")
        self.table.heading("Created Date", text="創建日期")
        self.table.heading("Modified Date", text="修改日期")
        self.table.pack(fill=tk.BOTH, expand=True)

        # Bind double click event to edit record
        self.table.bind("<Double-1>", self.edit_record)

    def show_add_modal(self):
        add_modal = tk.Toplevel(self.root)
        add_modal.title("新增地圖")

        fm_map_id_label = ttk.Label(add_modal, text="地圖編號")
        fm_map_id_label.grid(row=0, column=0, padx=10, pady=5)
        fm_map_id_entry = ttk.Entry(add_modal)
        fm_map_id_entry.grid(row=0, column=1, padx=10, pady=5)

        fm_map_name_label = ttk.Label(add_modal, text="地圖名稱")
        fm_map_name_label.grid(row=1, column=0, padx=10, pady=5)
        fm_map_name_entry = ttk.Entry(add_modal)
        fm_map_name_entry.grid(row=1, column=1, padx=10, pady=5)

        fm_map_img_label = ttk.Label(add_modal, text="地圖影像")
        fm_map_img_label.grid(row=2, column=0, padx=10, pady=5)
        fm_map_img_button = ttk.Button(
            add_modal, text="選擇檔案", command=self.select_image)
        fm_map_img_button.grid(row=2, column=1, padx=10, pady=5)

        add_button = ttk.Button(add_modal, text="新增", command=lambda: self.add_map(
            fm_map_id_entry.get(), fm_map_name_entry.get()))
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def show_add_modal2(self, map_id="", map_name=""):
        add_modal = tk.Toplevel(self.root)
        add_modal.title("新增地圖")

        fm_map_id_label = ttk.Label(add_modal, text="地圖編號")
        fm_map_id_label.grid(row=0, column=0, padx=10, pady=5)
        fm_map_id_entry = ttk.Entry(add_modal)
        fm_map_id_entry.grid(row=0, column=1, padx=10, pady=5)
        fm_map_id_entry.insert(0, map_id)  # Fill map_id if provided

        fm_map_name_label = ttk.Label(add_modal, text="地圖名稱")
        fm_map_name_label.grid(row=1, column=0, padx=10, pady=5)
        fm_map_name_entry = ttk.Entry(add_modal)
        fm_map_name_entry.grid(row=1, column=1, padx=10, pady=5)
        fm_map_name_entry.insert(0, map_name)  # Fill map_name if provided

        fm_map_img_label = ttk.Label(add_modal, text="地圖影像")
        fm_map_img_label.grid(row=2, column=0, padx=10, pady=5)
        fm_map_img_button = ttk.Button(
            add_modal, text="選擇檔案", command=lambda: self.select_image(add_modal))
        fm_map_img_button.grid(row=2, column=1, padx=10, pady=5)

        # Update button to update the record
        update_button = ttk.Button(add_modal, text="更新", command=lambda: self.update_map(
            map_id, fm_map_id_entry.get(), fm_map_name_entry.get()))
        update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.png")])
        # You can do something with the selected image file path here

    def add_map(self, map_id, map_name):
        created_date = modified_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Count the number of items in the table
        item_count = len(self.table.get_children())

        # Insert the data into the Treeview widget with the item count as No.
        self.table.insert("", "end", text=str(item_count + 1),
                          values=(map_id, map_name, created_date, modified_date))

    def delete_selected(self):
        selected_item = self.table.selection()

        # Check if an item is selected
        if selected_item:
            # Remove the selected item from the Treeview
            self.table.delete(selected_item)
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
            # Open the add modal with the data pre-filled
            self.show_add_modal2(map_id, map_name)


def main():
    root = tk.Tk()
    app = MapManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
