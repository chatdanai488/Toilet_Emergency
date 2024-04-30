import customtkinter as tk
from EmrgFloor import EmrgFloor
from EmrgMap import EmrgMap
from Notification import Notification
from main import MainApplication
from EmrgCompiler import EmrgCompiler
from DB import DB
from Alert_Function import Alert_Function as AF
import datetime
import os
import shutil
import sys

class MasterApp:
    def __init__(self, root):
        self.root = root
        self.root.update()
        screen_height, screen_width = self.root.winfo_screenheight(), self.root.winfo_screenwidth()
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')
        self.root.title("Master Application")
        frame_color = "black"

        self.DBO = DB()
        self.AF = AF(master_app=self)
        
        self.active_frame = None

        
        # self.add_to_startup()

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

        # Create frame for Compiler
        self.frame_compiler = tk.CTkFrame(self.root, fg_color=frame_color)
        self.frame_compiler.grid(row=0, column=0, sticky="nsew")

        # Instantiate EmrgFloor, EmrgMap, MainApplication, and Notification within their respective frames
        self.emrg_floor = EmrgFloor(self.frame_floor, master_app=self)
        self.emrg_map = EmrgMap(self.frame_map, master_app=self)
        self.main = MainApplication(self.frame_main, master_app=self)
        self.notification = Notification(self.frame_notification, master_app=self)
        self.emrg_compiler = EmrgCompiler(self.frame_compiler, master_app=self)
        
        self.frames = [self.frame_floor, self.frame_map, self.frame_main, self.frame_notification, self.frame_compiler]

        # Configure row and column weights for root and frames
        for frame in self.frames:
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frames("main")
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_and_exit)

    def open_frames(self, desig_frame):
        try:
            for frame in self.frames:
                if frame == desig_frame:
                    frame.grid(row=0, column=0, sticky="nsew")
                    self.active_frame = frame
                else:
                    frame.grid_remove()
        except Exception as e:
            print("An error occurred while opening frames:", e)
            # Handle this error as needed

        

    def show_frames(self, value, attribute=None):
        try:
            if value == "EmrgMap":
                self.open_frames(self.frame_map)
            elif value == "Notification":
                self.open_frames(self.frame_notification)
                self.notification.Refresh_Content()
            elif value == "EmrgFloor":
                self.open_frames(self.frame_floor)
                self.emrg_floor.receive_value(attribute)
            elif value == "main":
                self.open_frames(self.frame_main)
            elif value == "EmrgCompiler":
                self.open_frames(self.frame_compiler)
                self.emrg_compiler.receive_value(attribute)
        except Exception as e:
            print("An error occurred while showing frames:", e)
            # Handle this error as needed

    def Emergency_Alert_Called(self, Value='B105'):
        try:
            current_datetime = datetime.datetime.now()
            # Format current datetime as YYYYMMDD_HHMMSS
            formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            formatted_datetime2 = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            check = self.DBO.Active_Emergency_Check()

            active = any(i[0].strip() == Value[0] for i in check)

            if not active:
                alert_id = current_datetime.strftime("%Y%m%d%H%M%S")
                Data = [formatted_datetime, Value[0], alert_id, 1]
                self.DBO.Insert_Alert(Data)

            message = f"""There is an Emergency at: {Value[0]}\nEmergency Occurred at: {formatted_datetime2}\nPlease Go There Immediately"""
            self.AF.Send_Line_Message(message)
            self.AF.Alert_Sound()
            self.AF.show_notification(message)

            if self.active_frame != self.frame_notification:
                # Open a new notification window
                print("okay")
                self.show_frames('Notification')
            self.main.refresh_table()

            button_exist = 0

            # button_frame = self.notification.Call_Button_Frame()
            for widget in self.notification.button_Frame.winfo_children():
                if isinstance(widget,tk.CTkButton) and widget.cget('text') == Value:
                    button_exist +=1
            
            if button_exist == 0:
                self.notification.Refresh_Content()
        except Exception as e:
            print("An error occurred during emergency alert:", e)
            # Handle this error as needed

        


    def add_to_startup(self):
        try:
            file_path = sys.argv[0]
            file_path = os.path.abspath(file_path)
            # Get the path to the user's Startup folder
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

            # Check if the executable has been added to startup before
            startup_flag_file = os.path.join(startup_folder, "startup_flag.txt")
            if os.path.exists(startup_flag_file):
                print("Executable has already been added to startup.")
                return

            # Copy the executable file to the Startup folder
            shutil.copy(file_path, startup_folder)
            # Create a flag file to indicate that the executable has been added to startup
            with open(startup_flag_file, "w") as flag_file:
                flag_file.write("Added to startup")
            print("Successfully added to startup!")
        except Exception as e:
            print(f"Error: {e}")      

    def cleanup_and_exit(self):
        # Add any cleanup tasks here before exiting the program
        self.AF.cleanup()  # Call the cleanup method of the Alert_Function object
        self.root.destroy()  # Destroy the main Tkinter window
    

def main():
    root = tk.CTk()
    app = MasterApp(root)
    
    root.mainloop()



if __name__ == "__main__":
    main()
