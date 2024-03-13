import customtkinter as tk
import tkinter as TK
from PIL import ImageTk, Image
from Create_map import MapManagementApp
from Nofication import EmergencyApp


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("厠所系統")
        self.root.geometry("800x600")
        self.icon_path = "img\logo1.ico"
        self.root.iconbitmap(self.icon_path)
        self.create_sidebar()
        self.main_content()
    
    def main_content(self):
        self.main_content = tk.CTkFrame(self.root)
        self.main_content.columnconfigure(0,weight=1)
        self.main_content.columnconfigure(1,weight=1)

        #notification
        self.notif_frame = tk.CTkFrame(self.main_content)
        self.notif_label = tk.CTkLabel(self.notif_frame, text="Notification!",
                                font=("Helvetica", 20, "bold"))
        self.notif_content = tk.CTkLabel(self.notif_frame)
        
        self.notif_label.pack()
        self.notif_content.pack()
        self.notif_frame.grid(row=0, column = 0, columnspan= 2, sticky = tk.W +tk.E )


        #Analog Clock
        self.clock_frame = tk.CTkFrame(self.main_content)
        self.clock_label = tk.CTkLabel(self.clock_frame, text="Clock",
                                font=("Helvetica", 16, "bold"))
        
        self.clock_img = ImageTk.PhotoImage(Image.open('img/clock.png').resize((300,300)))
        self.clock = TK.Label(self.clock_frame, image=self.clock_img)
        
        
        self.clock_label.pack()
        self.clock.pack()
        self.clock_frame.grid(row=1, column = 0, padx = 10, pady = 10, sticky = tk.W +tk.E )

        #History
        self.history_frame = tk.CTkFrame(self.main_content)
        self.history_label = tk.CTkLabel(self.history_frame, text="History",
                                font=("Helvetica", 16, "bold"))
        
        self.history_label.pack()
        self.history_frame.grid(row=1, column = 1, sticky = tk.W +tk.E)

        #pack main content
        self.main_content.pack(fill='both')

    def create_sidebar(self):
        self.sidebar = tk.CTkFrame(self.root)
        self.sidebar.pack(fill='y', side='left')

        self.options = ['Create Map', 'Emergency Alert']
        tk.CTkLabel(self.sidebar, text="厠所系統", font=(
            "Helvetica", 16, "bold")).pack(pady="10")
        
        self.cm_btn = tk.CTkButton(
                self.sidebar, text="Create Map", command=lambda :self.open_window("Create Map"))
        self.cm_btn.pack(fill='x', padx="10", pady="10")

        self.al_btn = tk.CTkButton(
                self.sidebar, text="Add Location", command=lambda :self.open_window("Add Location"))
        self.al_btn.pack(fill='x', padx="10", pady="10")

        self.ea_btn = tk.CTkButton(
                self.sidebar, text="Emergency Alert", command=lambda : self.open_window("Emergency Alert"))
        self.ea_btn.pack(fill='x', padx="10", pady="10")        

        tk.CTkButton(self.sidebar, text="Exit", fg_color="red", command=self.close_window).pack(
            side="bottom", pady="10")

    def open_window(self, option):
        global other_window
        if option == 'Create Map':
            other_window = tk.CTkToplevel(self.root)
            other_window.title("Create Map Window")
            other_window.transient(self.root)

            self.cm_btn.configure(state="disabled")

            MapManagementApp(other_window)
            other_window.protocol("WM_DELETE_WINDOW", lambda:self.close_top('Create Map'))

        elif option == 'Add Location':
            other_window = tk.CTkToplevel(self.root)
            other_window.title("Add Toilet Location")
            other_window.transient(self.root)

            self.al_btn.configure(state="disabled")
            other_window.protocol("WM_DELETE_WINDOW", lambda:self.close_top('Add Location'))

        elif option == 'Emergency Alert':
            other_window = tk.CTkToplevel(self.root)
            other_window.transient(self.root)
            other_window.title("Alert Window")

            self.ea_btn.configure(state="disabled")

            EmergencyApp(other_window)
            other_window.protocol("WM_DELETE_WINDOW", lambda:self.close_top('Emergency Alert'))

    def close_top(self, option):
        other_window.destroy()

        if option == 'Create Map':
            self.cm_btn.configure(state="normal")
        elif option == "Add Location":
            self.al_btn.configure(state="normal")
        else:
             self.ea_btn.configure(state="normal")
           

    def close_window(self):
        self.root.destroy()


def main():
    root = tk.CTk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
