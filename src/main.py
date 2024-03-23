import customtkinter as tk
import tkinter as Tk
from tkinter import ttk
from PIL import ImageTk, Image
from Create_map import MapManagementApp
import datetime
from DB import DB

class MainApplication:
    def __init__(self, root,master_app=None):
        self.root = root
        self.master_app = master_app
        self.DBO = DB()
        
        self.create_sidebar()
        self.main_content()
    
    def main_content(self):
        self.Right_Frame = tk.CTkFrame(self.root)
        self.Right_Frame.columnconfigure(0,weight=1)

        #notification
        self.notif_frame = tk.CTkFrame(self.Right_Frame)
        self.notif_label = tk.CTkLabel(self.notif_frame, text="Notification!", font=("Helvetica", 20, "bold"))
        self.notif_content = tk.CTkLabel(self.notif_frame)

        self.notif_label.pack()
        self.notif_content.pack()
        self.notif_frame.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.time_frame = tk.CTkFrame(self.Right_Frame, height=50, width=100)
        self.time_frame.grid(row=0, column=1, sticky="nsw", padx=(10, 10), pady=10)  # Add padx and pady for padding

        # Create a sub-frame within time_frame to center the label vertically
        time_label_frame = tk.CTkFrame(self.time_frame)
        time_label_frame.pack(expand=True, fill="both")  # Ensure the sub-frame fills the available space

        # Create the time label
        self.time_label = tk.CTkLabel(time_label_frame, text="Time", font=("Helvetica", 20, "bold"))
        self.time_label.pack(expand=True)  # Center the label vertically within the sub-frame

        
        #History
        self.history_frame = tk.CTkFrame(self.Right_Frame)
        self.history_label = tk.CTkLabel(self.history_frame, text="History",
                                font=("Helvetica", 16, "bold"))
        
        self.history_label.pack()
        self.history_frame.grid(row=1, column = 0, columnspan = 2, sticky = "swe")

        
        #pack main content
        self.Right_Frame.pack(fill='both')

        self.create_table()
        self.update_time()

    def create_sidebar(self):
        self.sidebar = tk.CTkFrame(self.root)
        self.sidebar.pack(fill='y', side='left')

        self.options = ['Create Map', 'Emergency Alert']
        tk.CTkLabel(self.sidebar, text="厠所系統", font=(
            "Helvetica", 16, "bold")).pack(pady="10")
        
        self.cm_btn = tk.CTkButton(
                self.sidebar, text="Create Map", command=lambda :self.open_window("Create Map"))
        self.cm_btn.pack(fill='x', padx="10", pady="10")

        self.ea_btn = tk.CTkButton(
                self.sidebar, text="Emergency Alert", command=lambda : self.open_window("Emergency Alert"))
        self.ea_btn.pack(fill='x', padx="10", pady="10")        

        tk.CTkButton(self.sidebar, text="Exit", fg_color="red", command=self.close_window).pack(
            side="bottom", pady="10")

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time
        self.time_label.configure(text=current_time)  # Update label text
        self.time_label.after(1000, self.update_time)  # Schedule the function to run again after 1 second

    def create_table(self):
        
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 12))  # Adjust the font size here
        style.configure("Treeview.Heading", font=("Helvetica", 12))

        self.tree = ttk.Treeview(self.history_frame, columns=("No", "Date", "Location", "IP", "Status"), show="headings", style="Treeview")
        self.tree.heading("No", text="No")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Location", text="Location")
        self.tree.heading("IP", text="IP")
        self.tree.heading("Status", text="Status")
        self.tree.pack(side="top", fill="both", expand=True)  # Adjusted pack options

        # Set width for specific column
        self.tree.column("No", width=50, stretch=False)  # Disable stretching for the Number column

        # Adjust the other columns to fit the content
        self.tree.column("#2", width=150, stretch=True)
        self.tree.column("#3", stretch=True)
        self.tree.column("#4", stretch=True)
        self.tree.column("#5", width=100, stretch=True)  # Disable stretching for the Status column

        # Fetch data from the database
        data = self.DBO.Fetch_Alert_Log()

        # Insert data into the Treeview with row numbers
        for i, row in enumerate(data, start=1):
            # Map fAlertStatus values to display strings
            status = "Completed" if row[-1] == 0 else "In Progress"
            self.tree.insert("", "end", values=[i] + row[:-1] + [status])


    def open_window(self, option):
        if option == 'Create Map':
            self.master_app.show_frames('EmrgMap')
        elif option == 'Emergency Alert':
            self.master_app.show_frames('Notification')

    def close_window(self):
        self.master_app.root.destroy()



def main():
    root = tk.CTk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
