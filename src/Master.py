import customtkinter as tk
from EmrgFloor import EmrgFloor
from EmrgMap import EmrgMap

class MasterApp:
    def __init__(self, root):
        self.root = root
        self.root.update()
        screen_height, screen_width = self.root.winfo_screenheight(), self.root.winfo_screenwidth()
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')
        self.root.title("Master Application")
        frame_color = "black"
        # Create frame for EmrgFloor
        self.frame_floor = tk.CTkFrame(self.root,fg_color=frame_color)
        self.frame_floor.grid(row=0, column=0, sticky="nsew")

        # Create frame for EmrgMap
        self.frame_map = tk.CTkFrame(self.root,fg_color=frame_color)
        self.frame_map.grid(row=0, column=0, sticky="nsew")

        # Instantiate EmrgFloor and EmrgMap within their respective frames
        self.emrg_floor = EmrgFloor(self.frame_floor, master_app=self)
        self.emrg_map = EmrgMap(self.frame_map,master_app=self)

        # Hide the frame for EmrgMap initially
        self.frame_floor.grid_remove()

        # Configure row and column weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frame_floor.grid_rowconfigure(0, weight=1)
        self.frame_floor.grid_columnconfigure(0, weight=1)
        self.frame_map.grid_rowconfigure(0, weight=1)
        self.frame_map.grid_columnconfigure(0, weight=1)

    def show_floor(self,value):
        # Show the frame for EmrgFloor and hide the frame for EmrgMap
        self.frame_floor.grid()
        self.frame_map.grid_remove()

        self.emrg_floor.receive_value(value)

    def show_map(self):
        # Show the frame for EmrgMap and hide the frame for EmrgFloor
        self.frame_map.grid()
        self.frame_floor.grid_remove()


def main():
    root = tk.CTk()
    app = MasterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
