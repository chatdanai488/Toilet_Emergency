import customtkinter as tk
from EmrgMap import EmrgMap as EmrgMap
from WIP import EmrgFloor as EmrgFloor

class MainApplication(tk.CTk):
    def __init__(self, MasterRoot):
        self.MasterRoot = MasterRoot
        self.MasterRoot.title("My New Project")
        screen_width, screen_height = self.MasterRoot.winfo_screenwidth(), self.MasterRoot.winfo_screenheight()
        self.MasterRoot.geometry(f"{screen_width}x{screen_height}+0+0")
        self.MasterRoot.update()
        # Create frames for each window
        self.EmrgMap_Frame = tk.CTkFrame(self.MasterRoot)
        self.EmrgFloor_Frame = tk.CTkFrame(self.MasterRoot)

        # Create instances of window classes within their respective frames
        self.EmrgMap = EmrgMap(self.EmrgMap_Frame)
        self.EmrgFloor = EmrgFloor(self.EmrgFloor_Frame, self)

        # Show the first window by default
        self.show_window(self.EmrgMap_Frame)

    def show_window(self, window):
        # Hide the current window
        if hasattr(self, 'current_window'):
            self.current_window.pack_forget()

        # Show the new window
        window.pack(fill=tk.BOTH, expand=True)
        self.current_window = window

    def show_EmrgMap(self):
        self.show_window(self.EmrgMap_Frame)

if __name__ == "__main__":
    MasterRoot = tk.CTk()
    app = MainApplication(MasterRoot)
    app.mainloop()