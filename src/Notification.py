import time
import customtkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageSequence
from tkinter import messagebox
from DB import DB
import inspect
# import DB

class Notification:
    def __init__(self, root, master_app=None):
        try:
            self.root = root
            # self.root.title("notification")
            self.master_app = master_app
            # Set up grid configuration for responsiveness
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(0, weight=1)

            # Set the window geometry to fullscreen
            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()
            # self.root.geometry(f"{self.screen_width}x{self.screen_height-100}-1+0")
            self.root.update()
            self.DBO = DB()
            
            
            self.create_widgets()
            
            self.column_count = 0
            self.row_count = 0
            self.count = 1
            self.canvases = {}
            self.messages = {}  # Dictionary to store message box references
            self.delete_buttons = {}  # Dictionary to store delete buttons
            self.canvas_image = {}
            self.canvas_shape = {}
            self.canvas_image_ids = {}  # Dictionary to store image IDs
            self.canvas_images = {}  # Dictionary to store PhotoImage objects
            self.buttons = {}
            self.LocId = {}

            self.active_button = None
            self.active_canvas = None
            self.active_canvas_image = None
            self.active_canvas_shape = None

            self.pulse_colors = ["red", "blue", "green", "yellow"]  # Add more colors as needed
            self.current_pulse_color_index = 0

            
            self.right_frame.bind("<Configure>",self.on_root_resize)
            self.Refresh_Content()
        except Exception as e:
            print(f"An error occurred during initialization: {e}")
            # Handle this error as needed


    def create_widgets(self):
        try:
            # Sidebar Frame
            self.sidebar = tk.CTkFrame(self.root, width=280)
            self.sidebar.grid_propagate(False)
            self.sidebar.grid(column=0, row=0, sticky="nsew")

            self.return_button = tk.CTkButton(self.sidebar, text="Return", fg_color="red", command=self.Return_To_Main)
            self.return_button.grid(column=0, row=0, padx=10, pady=10)

            # LabelFrame
            self.Label_Frame = tk.CTkFrame(self.sidebar)
            self.Label_Frame.grid(column=0, row=1, padx=10, pady=10)

            # ButtonFrame
            self.button_Frame = tk.CTkFrame(self.sidebar, width=270, height=270)
            self.button_Frame.grid_propagate(False)
            self.button_Frame.grid(column=0, row=2, padx=5)

            # Loading Canvas
            self.loading_canvas = tk.CTkCanvas(self.button_Frame)
            self.loading_canvas.grid(column=0, row=0, sticky="nsew")

            # Load the image and resize
            self.gif_path = "img\\Loading.gif"
            self.gif = Image.open(self.gif_path)
            self.gif_frames = []
            for frame in ImageSequence.Iterator(self.gif):
                frame = frame.resize((420, 420))
                self.gif_frames.append(ImageTk.PhotoImage(frame))
            self.frame_index = 0
            self.load_image = self.loading_canvas.create_image(200, 200, image=self.gif_frames[0])

            # Create Heading label
            self.Heading = tk.CTkLabel(self.Label_Frame, text="Notification", font=("Arial", 24, "bold"), width=250)
            self.Heading.grid(column=0, row=0)

            # Message Frame
            self.message_frame = tk.CTkFrame(self.sidebar, fg_color="lightblue")
            self.message_frame.grid(column=0, row=3, padx=5, sticky="nsew")

            # Right Side
            self.right_frame = tk.CTkFrame(self.root, fg_color="lightgreen")
            self.right_frame.grid(column=1, row=0, sticky="nsew")
            self.right_frame.grid_columnconfigure(0, weight=1)
            self.right_frame.grid_rowconfigure(0, weight=1)

            # Configure grid weight for responsiveness
            self.loading_canvas.rowconfigure(0, weight=1)
            self.loading_canvas.columnconfigure(0, weight=1)
            self.button_Frame.grid_rowconfigure(0, weight=1)
            self.button_Frame.grid_columnconfigure(0, weight=1)

            # Start animation
            self.animate()
        except Exception as e:
            print(f"An error occurred while creating widgets: {e}")
            # Handle this error as needed


    
    def animate(self):
        try:
            """Animate the GIF"""
            self.frame_index = (self.frame_index + 1) % len(self.gif_frames)
            self.loading_canvas.itemconfig(self.load_image, image=self.gif_frames[self.frame_index])
            self.root.after(50, self.animate)  # Update every 50 milliseconds
        except Exception as e:
            print(f"An error occurred during animation: {e}")
            # Handle this error as needed



    #create new button
    def create_button(self, Data, LocId):
        try:
            data = Data
            Current_Message = f"Emergency At {data[0][2]}\nPlease go there as soon as possible"
            # Create button
            new_button = tk.CTkButton(self.button_Frame, text=f"{data[0][2]}", width=50, height=50)
            new_button.grid(column=self.column_count, row=self.row_count, padx=2, pady=2)
            self.buttons[self.count] = new_button
            # Set normal color
            new_button.configure(fg_color="blue")

            # Bind click event to show_canvas method with button instance and index
            new_button.configure(command=lambda button=new_button, idx=self.count: self.show_canvas(button, idx))

            # Create associated canvas
            canvas = tk.CTkCanvas(self.right_frame, width=self.screen_width/2, height=self.screen_height)
            canvas.grid(row=0, column=0, sticky="nsew")
            self.canvases[self.count] = canvas
            canvas.grid_forget()

            # Create associated message box
            message = tk.CTkLabel(self.message_frame, text=Current_Message, width=270, height=40)
            message.grid(row=0, column=0, sticky="nsew")
            self.messages[self.count] = message
            message.grid_forget()

            delete_button = tk.CTkButton(self.right_frame, text="Delete", command=lambda idx=self.count: self.delete_item(idx))
            delete_button.grid(row=1, column=0, sticky="se")
            delete_button.grid_forget()  # Hide initially
            self.delete_buttons[self.count] = delete_button

            self.LocId[self.count] = LocId

            if self.column_count != 4:
                self.column_count += 1
            else:
                self.column_count = 0
                self.row_count += 1

            self.add_canvas_component(data[0], canvas)
            self.count += 1

            if hasattr(self, "loading_canvas"):
                self.loading_canvas.grid_forget()
            self.button_Frame.grid_rowconfigure(0, weight=0)
            self.button_Frame.grid_columnconfigure(0, weight=0)
            self.loading_canvas.rowconfigure(0, weight=0)
            self.loading_canvas.columnconfigure(0, weight=0)
            self.show_canvas(new_button, self.count-1)
        except Exception as e:
            print(f"An error occurred while creating button: {e}")
            # Handle this error as needed


        

    def show_canvas(self, button, index):
        try:
            if self.active_button:
                self.active_button.configure(fg_color="blue")
            button.configure(fg_color="darkblue")
            self.active_button = button

            self.active_canvas_image = self.canvas_image[index]
            self.active_canvas_shape = self.canvas_shape[index]
            for button_index, delete_button in self.delete_buttons.items():
                if button_index == index:
                    delete_button.grid(row=1, column=0, sticky="se")
                else:
                    delete_button.grid_forget()

            for button_index, canvas in self.canvases.items():
                if button_index == index:
                    canvas.grid(row=0, column=0, sticky="nsew")
                    self.active_canvas = canvas
                else:
                    canvas.grid_forget()
            
            for button_index, message in self.messages.items():
                if button_index == index:
                    message.grid(row=0, column=0, sticky="nsew")
                else:
                    message.grid_forget()

            self.on_root_resize()
            self.pulsate_shape()
        except Exception as e:
            print(f"An error occurred while showing canvas: {e}")
            # Handle this error as needed

        

    def delete_item(self, idx):
        try:
            self.canvases[idx].destroy()  # Remove canvas from display
            self.messages[idx].destroy()  # Remove message from display
            del self.canvases[idx]
            del self.messages[idx]
            self.delete_buttons[idx].destroy()  # Hide delete button
            del self.delete_buttons[idx]
            self.active_button.destroy()
            del self.canvas_shape[idx]
            del self.canvas_image[idx]
            self.active_button = None
            self.active_canvas = None
            self.active_canvas_image = None
            self.active_canvas_shape = None

            self.DBO.Update_Emergency_Status(self.LocId[idx])
            del self.LocId[idx]

            self.master_app.main.refresh_table()

            self.reorganize_buttons()
        except Exception as e:
            print(f"An error occurred while deleting item: {e}")
            # Handle this error as needed


    
    def reorganize_buttons(self):
        try:
            # Count the number of buttons (excluding canvases)
            button_count = sum(1 for widget in self.button_Frame.winfo_children() if isinstance(widget, tk.CTkButton))
            print(button_count)
            if button_count == 0:
                # If there are no buttons, display the loading canvas again
                self.loading_canvas.grid(row=0, column=0, sticky="nsew")
                self.button_Frame.grid_rowconfigure(0, weight=1)
                self.button_Frame.grid_columnconfigure(0, weight=1)
                self.loading_canvas.rowconfigure(0, weight=1)
                self.loading_canvas.columnconfigure(0, weight=1)
            else:
                # Remove all buttons
                for widget in self.button_Frame.winfo_children():
                    if isinstance(widget, tk.CTkButton):
                        widget.grid_remove()

                # Re-add buttons in a grid layout
                row = 0
                col = 0
                for widget in self.button_Frame.winfo_children():
                    if isinstance(widget, tk.CTkButton):
                        widget.grid(row=row, column=col, padx=2, pady=2)
                        col += 1
                        if col >= 5:  # Move to the next row after 5 columns
                            col = 0
                            row += 1

                # Update row and column counts
                self.row_count = (button_count + 4) // 5  # Add 4 to round up when there's a partial row
                self.column_count = min(button_count, 5)  # Maximum of 5 buttons per row
        except Exception as e:
            print(f"An error occurred while reorganizing buttons: {e}")
            # Handle this error as needed


    def add_canvas_component(self,data,canvas):
        try:
            current_canvas = canvas
            current_data = data

            available_width = self.root.winfo_width() - self.sidebar.winfo_reqwidth()
            available_height = self.root.winfo_height() - 20 # Adjusted for the top widget
            
            if available_width < 1 or available_height < 1:
                available_width = 1920
                available_height = 1080
            # Load the image
            image_path = current_data[10]  # Use forward slashes for paths
            self.original_image = Image.open("img\\20240321_135959.jpg")

            # Calculate the aspect ratio of the image
            image_width, image_height = self.original_image.size
            aspect_ratio = image_width / image_height

            # Calculate the dimensions of the resized image
            if aspect_ratio > 1:  # Landscape orientation
                new_width = available_width
                new_height = int(available_width / aspect_ratio)
            else:  # Portrait or square orientation
                new_height = available_height
                new_width = int(available_height * aspect_ratio)

            # Adjust height if it exceeds the available height
            if new_height > available_height:
                new_height = available_height
                new_width = int(new_height * aspect_ratio)

            # Resize the image
            resized_image = self.original_image.resize((new_width, new_height))

            # Convert image for Tkinter
            image_name = f"image_{len(self.canvas_image)}"
            self.canvas_images[image_name] = ImageTk.PhotoImage(resized_image)
            image_id = current_canvas.create_image(0, 0, anchor="nw", image=self.canvas_images[image_name])
            self.canvas_image[self.count] = image_id
            current_canvas.configure(scrollregion=(0, 0, new_width, new_height))
        
            if current_data[9] == "square":
                x1, y1 = current_data[5] * new_width, current_data[6] * new_height
                x2, y2 = current_data[7] * new_width, current_data[8] * new_height
                shape_id = current_canvas.create_rectangle(x1, y1, x2, y2, fill="red", stipple="gray50")
            elif current_data[9] == "line":
                x1, y1 = current_data[5] * new_width, current_data[6] * new_height
                x2, y2 = current_data[7] * new_width, current_data[8] * new_height
                shape_id = current_canvas.create_line(x1, y1, x2, y2, fill="red")
            elif current_data[9] == "dot":
                x1, y1 = current_data[5] * new_width, current_data[6] * new_height
                shape_id = current_canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill="red")
            self.canvas_shape[self.count] = shape_id
            
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

    def on_root_resize(self,event=None):
        self.resize_canvas_component()
        pass
        
       
    def resize_canvas_component(self):
        try:
            if self.active_canvas:
                # Get the current dimensions of the canvas
                available_width = self.root.winfo_width() - self.sidebar.winfo_reqwidth()
                available_height = self.root.winfo_height() - 20 # Adjusted for the top widget
                
                # Resize the canvas
                self.active_canvas.configure(width=available_width, height=available_height)

                # Resize the image if it exists
                image_bbox = self.active_canvas.bbox(self.active_canvas_image)

                # Calculate the size of the image
                image_width = image_bbox[2] - image_bbox[0]  # Width is the difference between the x-coordinates
                image_height = image_bbox[3] - image_bbox[1]

                aspect_ratio = image_width / image_height
                # Calculate the new dimensions of the resized image
                if aspect_ratio > 1:  # Landscape orientation
                    new_width = available_width
                    new_height = int(available_width / aspect_ratio)
                else:  # Portrait or square orientation
                    new_height = available_height
                    new_width = int(available_height * aspect_ratio)
                # Check if the new height exceeds the canvas height
                if new_height > available_height:
                    new_height = available_height
                    new_width = int(available_height * aspect_ratio)

                if new_width < 1 or new_height < 1:
                    new_width = int(1920/20)
                    new_height = int(1080/20)
                # Resize the image
                resized_image = self.original_image.resize((new_width, new_height))

                # Update the image in the canvas
                self.images = ImageTk.PhotoImage(resized_image)
                self.active_canvas.itemconfig(self.active_canvas_image, image=self.images)

                # Calculate the scaling factor for the shape
                # Calculate the scaling factor for the shape
                x_scale = new_width / image_width
                y_scale = new_height / image_height

                # Get the coordinates of the shape
                shape_bbox = self.active_canvas.bbox(self.active_canvas_shape)
                shape_x1, shape_y1, shape_x2, shape_y2 = shape_bbox

                # Calculate the new coordinates of the shape relative to the image
                new_shape_x1 = shape_x1 / image_width * new_width
                new_shape_y1 = shape_y1 / image_height * new_height
                new_shape_x2 = shape_x2 / image_width * new_width
                new_shape_y2 = shape_y2 / image_height * new_height

                # Update the shape coordinates
                self.active_canvas.coords(self.active_canvas_shape, new_shape_x1, new_shape_y1, new_shape_x2, new_shape_y2)

        
        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")

    def pulsate_shape(self):
        try:
            if self.active_canvas:
                
                """Function to pulse the active canvas shape with color change"""
                if self.current_pulse_color_index >= len(self.pulse_colors):
                    self.current_pulse_color_index = 0  # Reset index if it exceeds the list length
                color = self.pulse_colors[self.current_pulse_color_index]
                self.active_canvas.itemconfig(self.active_canvas_shape, fill=color)
                self.current_pulse_color_index += 1
                self.root.after(500, self.pulsate_shape)

        except Exception as e:
            # Add error handling to catch any exceptions
            method_name = inspect.currentframe().f_code.co_name
            print(f"An error occurred in {method_name}: {e}")


    def Search_Pending_Case(self):
        try:
            Pending = self.DBO.Fetch_Pending()
            for i in Pending:
                data = self.DBO.Fetch_Pending_Map(i[0])
                self.create_button(data, i)
        except Exception as e:
            print(f"An error occurred while searching for pending cases: {e}")
            # Handle this error as needed

    def Return_To_Main(self):
        try:
            self.master_app.show_frames("main")
            self.delete_all_items()
        except Exception as e:
            print(f"An error occurred while returning to the main frame: {e}")
            # Handle this error as needed


    def delete_all_items(self):
        try:
            # Destroy all canvases, messages, and buttons
            for canvas in self.canvases.values():
                canvas.destroy()
            for message in self.messages.values():
                message.destroy()
            for button in self.delete_buttons.values():
                button.destroy()
            for button in self.buttons.values():
                button.destroy()

            # Clear the lists
            self.canvases.clear()
            self.messages.clear()
            self.delete_buttons.clear()
            self.canvas_shape.clear()
            self.canvas_image.clear()
            self.LocId.clear()

            # Reset active attributes
            if self.active_button:
                self.active_button = None
            self.active_canvas = None
            self.active_canvas_image = None
            self.active_canvas_shape = None
        except Exception as e:
            print(f"An error occurred while deleting all items: {e}")
            # Handle this error as needed


    def Refresh_Content(self):
        try:
            self.delete_all_items()
            self.Search_Pending_Case()
            self.reorganize_buttons()
        except Exception as e:
            print(f"An error occurred while refreshing content: {e}")
            # Handle this error as needed

    def Call_Button_Frame(self):
        return self.button_Frame

def main():
    root = tk.CTk()
    app = Notification(root)
    root.mainloop()


if __name__ == "__main__":
    main()