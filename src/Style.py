import tkinter as tk
from tkinter import ttk
import Constants as Cons

def button_style():
    style = ttk.Style()
    style.configure('New_Map_Btn.TButton', 
                    background='blue', 
                    foreground='blue', 
                    font=Cons.Font(),
                    borderwidth=0)
    
    style.configure('Del_Map_Btn.TButton', 
                    background='orange', 
                    foreground='orange', 
                    font=Cons.Font(),
                    borderwidth=0)

def table_style():
    style = ttk.Style()
    style.configure('Table.TLabel',
                    background='white',
                    font=Cons.Font(),
                    padding=(5,5)
                    )
    
def checkbox_style():
    style = ttk.Style()
    style.configure("TableBlue.TCheckbutton", background="lightblue", borderwidth=1, relief="solid")
    style.configure("TableGrey.TCheckbutton", background="lightgrey", borderwidth=1, relief="solid")