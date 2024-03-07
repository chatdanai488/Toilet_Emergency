import customtkinter as tk
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

    def create_sidebar(self):
        self.sidebar = tk.CTkFrame(self.root)
        self.sidebar.pack(fill='y', side='left')

        self.options = ['Create Map', 'Emergency Alert']
        tk.CTkLabel(self.sidebar, text="厠所系統", font=(
            "Helvetica", 16, "bold")).pack(pady="10")
        for option in self.options:
            button = tk.CTkButton(
                self.sidebar, text=option, command=lambda opt=option: self.open_window(opt))
            button.pack(fill='x', padx="10", pady="10")

        tk.CTkButton(self.sidebar, text="Exit", fg_color="red", command=self.close_window).pack(
            side="bottom", pady="10")

    def open_window(self, option):
        if option == 'Create Map':
            other_window = tk.CTkToplevel(self.root)
            other_window.title("Create Map Window")
            other_window.transient(self.root)
            MapManagementApp(other_window)
        elif option == 'Emergency Alert':
            other_window = tk.CTkToplevel(self.root)
            other_window.transient(self.root)
            other_window.title("Alert Window")
            EmergencyApp(other_window)

    def close_window(self):
        self.root.destroy()


def main():
    root = tk.CTk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
