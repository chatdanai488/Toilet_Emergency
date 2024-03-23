import customtkinter as tk
from EmrgFloor import EmrgFloor
from EmrgMap import EmrgMap
from Notification import Notification
from main import MainApplication
from DB import DB
import datetime


class MasterApp:
    def __init__(self, root):
        self.root = root
        self.root.update()
        screen_height, screen_width = self.root.winfo_screenheight(), self.root.winfo_screenwidth()
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')
        self.root.title("Master Application")
        frame_color = "black"

        self.DBO = DB()
        # Create frame for EmrgFloor
        self.frame_floor = tk.CTkFrame(self.root, fg_color=frame_color)
        self.frame_floor.grid(row=0, column=0, sticky="nsew")

        # Create frame for EmrgMap
        self.frame_map = tk.CTkFrame(self.root, fg_color=frame_color)
        self.frame_map.grid(row=0, column=0, sticky="nsew")

        # Create frame for main
        self.frame_main = tk.CTkFrame(self.root, fg_color=frame_color)
        self.frame_main.grid(row=0, column=0, sticky="nsew")

        # Create frame for notification
        self.frame_notification = tk.CTkFrame(self.root, fg_color=frame_color)
        self.frame_notification.grid(row=0, column=0, sticky="nsew")

        # Instantiate EmrgFloor, EmrgMap, MainApplication, and Notification within their respective frames
        self.emrg_floor = EmrgFloor(self.frame_floor, master_app=self)
        self.emrg_map = EmrgMap(self.frame_map, master_app=self)
        self.main = MainApplication(self.frame_main, master_app=self)
        self.notification = Notification(self.frame_notification, master_app=self)

        self.frames = [self.frame_floor, self.frame_map, self.frame_main, self.frame_notification]

        # Configure row and column weights for root and frames
        for frame in self.frames:
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frames("main")

    def open_frames(self, desig_frame):
        for frame in self.frames:
            if frame == desig_frame:
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid_remove()

    def show_floor(self,value):
        # Show the frame for EmrgFloor and hide the frame for EmrgMap
        for frame in self.frames:
            if frame == self.frame_map:
                self.frame_floor.grid()
            else:
                self.frame_map.grid_remove()

        self.emrg_floor.receive_value(value)

    def show_frames(self, value):
        if value == "EmrgMap":
            self.open_frames(self.frame_map)
        elif value == "Notification":
            self.open_frames(self.frame_notification)
        elif value == "EmrgFloor":
            self.open_frames(self.frame_floor)
        elif value == "main":
            self.open_frames(self.frame_main)

    def Emergency_Alert_Called(self):
        current_datetime = datetime.datetime.now()
        # Format current datetime as YYYYMMDD_HHMMSS
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        Data = [formatted_datetime, "C108", "TEST", 1]
        self.DBO.Insert_Alert(Data)

def main():
    root = tk.CTk()
    app = MasterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
