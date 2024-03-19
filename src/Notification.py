import customtkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
# import DB

class EmergencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("notification")

        # Set up grid configuration for responsiveness
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Set the window geometry to fullscreen
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height-100}-1+0")
        
        
        self.create_widgets()
        
        self.column_count = 0
        self.row_count = 0
        self.count = 1
        
        # self.Notification_test()

    def create_widgets(self):
        #sidebar Frame
        self.sidebar = tk.CTkFrame(self.root,width=280)
        self.sidebar.grid_propagate(False)
        self.sidebar.grid(column=0,row=0,sticky="nsew")
            #labelframe
        self.Label_Frame = tk.CTkFrame(self.sidebar)
        self.Label_Frame.grid(column=0,row=0,padx=10,pady=10)
            #bottonfram
        self.button_Frame = tk.CTkFrame(self.sidebar,width=270,height=270)
        self.button_Frame.grid_propagate(False)
        self.button_Frame.grid(column=0,row=1,padx=5)
        #loading_cavas
        self.loading_canvas = tk.CTkCanvas(self.button_Frame)
        self.loading_canvas.grid(column=0,row=0,sticky="nsew")
        
       
        # Load the image
        self.image = Image.open("img\\Loading.gif")
        # Resize the image if necessary
        self.image = self.image.resize((540, 540))
        # Convert the Image object into a Tkinter-compatible image
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Add the image to the canvas
        self.load_image = self.loading_canvas.create_image(270, 270, image=self.tk_image)

        #Heading
        self.Heading = tk.CTkLabel(self.Label_Frame,text="Notification",font=("Arial", 24, "bold"),width=250).grid(column=0,row=0)




        #test bootn
        self.tester = tk.CTkButton(self.sidebar,text="TEST",command=self.create_button).grid(column=0,row=5)


        self.loading_canvas.rowconfigure(0,weight=1)
        self.loading_canvas.columnconfigure(0,weight=1)
        self.button_Frame.grid_rowconfigure(0, weight=1)
        self.button_Frame.grid_columnconfigure(0, weight=1)
    
    #create new button
    def create_button(self):
        self.new_button = tk.CTkButton(self.button_Frame,text=f"{self.count}",width=50,height=50,command=self.alert).grid(column=self.column_count,row=self.row_count,padx=2,pady=2)
        
        if self.column_count != 4 :
            self.column_count +=1
        else:
            self.column_count = 0
            self.row_count +=1
        self.count +=1

        self.loading_canvas.grid_forget()
        self.button_Frame.grid_rowconfigure(0, weight=0)
        self.button_Frame.grid_columnconfigure(0, weight=0)
        self.loading_canvas.rowconfigure(0,weight=0)
        self.loading_canvas.columnconfigure(0,weight=0)

    def create_alert(self):

    # press new button after alert
    def alert(self):
        messagebox.showinfo("Hi!","Fuck U!")
        

       
    # def Notification_test(self):
    #     # DBO = DB.DB()
    #     # data = DBO.Fetch_Map()

    #     self.screen_width = 800
    #     self.screen_height = 400
    #     self.map_image = Image.open(data[4][10])
        
    #     self.new_size = (self.screen_width, self.screen_height)
    #     self.resized_image = self.map_image.resize(self.new_size)
        
    #     # x1, y1 = data[4][5] * self.screen_width, data[4][6] * self.screen_height
    #     # x2, y2 = data[4][7] * self.screen_width, data[4][8] * self.screen_height
    #     # Create a square at the specified position            
    #     # Resize image
    #     # Specify the new size (width, height)
        
    #     self.map_photo = ImageTk.PhotoImage(self.resized_image)
    #     self.map_display = self.canvas.create_image(
    #         0, 0, anchor=tk.NW, image=self.map_photo)
    #     square_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", stipple="gray50")
        
    #     print(data)

def main():
    root = tk.CTk()
    app = EmergencyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()