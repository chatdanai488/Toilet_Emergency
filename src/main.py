import customtkinter as tk
import tkinter as Tk
from tkinter import ttk
from PIL import ImageTk, Image
import datetime
from DB import DB

class MainApplication:
    def __init__(self, root, master_app=None):
        try:
            self.root = root
            self.master_app = master_app
            self.DBO = DB()

            self.create_sidebar()
            self.main_content()
        except Exception as e:
            print(f"An error occurred during initialization: {e}")
            # Handle this error as needed
    
    def main_content(self):
        try:
            self.Right_Frame = tk.CTkFrame(self.root)
            self.Right_Frame.columnconfigure(0, weight=1)

            # Notification
            self.notif_frame = tk.CTkFrame(self.Right_Frame)
            self.notif_label = tk.CTkLabel(self.notif_frame, text="Notification!", font=("Helvetica", 20, "bold"))
            self.notif_content = tk.CTkLabel(self.notif_frame)

            self.notif_label.pack()
            self.notif_content.pack()
            self.notif_frame.grid(row=0, column=0, sticky=tk.E + tk.W)

            self.time_frame = tk.CTkFrame(self.Right_Frame, height=50, width=100)
            self.time_frame.grid(row=0, column=1, sticky="nsw", padx=(10, 10), pady=10)  

            # Create a sub-frame within time_frame to center the label vertically
            time_label_frame = tk.CTkFrame(self.time_frame)
            time_label_frame.pack(expand=True, fill="both")  

            # Create the time label
            self.time_label = tk.CTkLabel(time_label_frame, text="Time", font=("Helvetica", 20, "bold"))
            self.time_label.pack(expand=True)  

            # History
            self.history_frame = tk.CTkFrame(self.Right_Frame)
            self.history_label = tk.CTkLabel(self.history_frame, text="History",
                                            font=("Helvetica", 16, "bold"))

            self.history_label.pack()
            self.history_frame.grid(row=1, column=0, columnspan=2, sticky="swe")

            # Pack main content
            self.Right_Frame.pack(fill='both')

            self.create_table()
            self.update_time()
        except Exception as e:
            print(f"An error occurred while creating main content: {e}")
            # Handle this error as needed

    def create_sidebar(self):
        try:
            self.sidebar = tk.CTkFrame(self.root)
            self.sidebar.pack(fill='y', side='left')

            self.options = ['Create Map', 'Emergency Alert']
            tk.CTkLabel(self.sidebar, text="厠所系統", font=(
                "Helvetica", 16, "bold")).pack(pady="10")
            
            self.cm_btn = tk.CTkButton(
                    self.sidebar, text="Create Map", command=lambda: self.open_window("Create Map"))
            self.cm_btn.pack(fill='x', padx="10", pady="10")

            self.ea_btn = tk.CTkButton(
                    self.sidebar, text="Emergency Alert", command=lambda: self.open_window("Emergency Alert"))
            self.ea_btn.pack(fill='x', padx="10", pady="10")        

            self.Test_btn = tk.CTkButton(
                    self.sidebar, text="Test", command=self.master_app.Emergency_Alert_Called)
            self.Test_btn.pack(fill='x', padx="10", pady="10")        

            tk.CTkButton(self.sidebar, text="Exit", fg_color="red", command=self.close_window).pack(
                side="bottom", pady="10")
        except Exception as e:
            print(f"An error occurred while creating the sidebar: {e}")
            # Handle this error as needed

    def update_time(self):
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time
            self.time_label.configure(text=current_time)  # Update label text
            self.time_label.after(1000, self.update_time)  # Schedule the function to run again after 1 second
        except Exception as e:
            print(f"An error occurred while updating time: {e}")

    def create_table(self):
        try:
            style = ttk.Style()
            style.configure("Treeview", font=("Helvetica", 12))  # Adjust the font size here
            style.configure("Treeview.Heading", font=("Helvetica", 12))

            self.table = ttk.Treeview(self.history_frame, columns=("No", "Date", "Location", "IP", "Status"), show="headings", style="Treeview")
            self.table.heading("No", text="No")
            self.table.heading("Date", text="Date")
            self.table.heading("Location", text="Location")
            self.table.heading("IP", text="IP")
            self.table.heading("Status", text="Status")
            self.table.pack(side="bottom", fill="both", expand=True)  # Adjusted pack options

            # Set width for specific column
            self.table.column("No", width=50, stretch=False)  # Disable stretching for the Number column

            # Adjust the other columns to fit the content
            self.table.column("#2", width=150, stretch=True)
            self.table.column("#3", stretch=True)
            self.table.column("#4", stretch=True)
            self.table.column("#5", width=100, stretch=True)  # Disable stretching for the Status column

            # Fetch data from the database
            self.refresh_table()
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")
            # Handle this error as needed

        

    def refresh_table(self):
        try:
            self.table.delete(*self.table.get_children())
            # Insert data into the Treeview with row numbers
            data = self.DBO.Fetch_Alert_Log()
            for i, row in enumerate(data, start=1):
                # Map fAlertStatus values to display strings
                status = "Completed" if row[-1] == 0 else "In Progress"
                self.table.insert("", "end", values=[i] + row[:-1] + [status])
        except Exception as e:
            print(f"An error occurred while refreshing the table: {e}")
            # Handle this error as needed

    def open_window(self, option):
        try:
            if option == 'Create Map':
                self.master_app.show_frames('EmrgMap')
            elif option == 'Emergency Alert':
                self.master_app.show_frames('Notification')
            else:
                print(f"Unsupported option: {option}")
        except Exception as e:
            print(f"An error occurred while opening window: {e}")
            # Handle this error as needed


    def close_window(self):
        try:
            self.master_app.root.destroy()
        except Exception as e:
            print(f"An error occurred while closing the window: {e}")
            # Handle this error as needed




def main():
    root = tk.CTk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
