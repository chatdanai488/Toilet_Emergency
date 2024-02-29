import tkinter as tk
from Create_map import MapManagementApp
from Nofication import EmergencyApp


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")

        self.create_widgets_map()
        self.create_widgets_alert()

    def create_widgets_map(self):
        self.open_window_button = tk.Button(
            self.root, text="Open Create Map Window", command=self.open_other_window_map)
        self.open_window_button.pack(pady=20)

    def create_widgets_alert(self):
        self.open_window_button = tk.Button(
            self.root, text="Open Alert Window", command=self.open_other_window_alert)
        self.open_window_button.pack(pady=20)

    def open_other_window_map(self):
        other_window = tk.Toplevel(self.root)
        other_window.title("Other Window")
        MapManagementApp(other_window)

    def open_other_window_alert(self):
        other_window = tk.Toplevel(self.root)
        other_window.title("Other Window")
        EmergencyApp(other_window)


def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
