from Rocket import *
from tkinter import Tk, Label
from tkinter import PhotoImage  
from customtkinter import *
from vendor.Rocket.resource_gather import get_resource_images
from vendor.Rocket.Rrender import *
from src.todo import *

class homescreen:
    def __init__(self, window:Tk):
        self.window = window
        window.config(bg="#E4D5B8")

    def get_rocket_window(self) -> Tk:
        window = self.window
        
        # Add padding and pack labels
        Label(window, text="", bg="#E4D5B8").pack(pady=100, padx=200)
        self.image_path = get_resource_images('rocket_ui.png')
        self.image = PhotoImage(file=self.image_path) 
        main_label = Label(window, image=self.image, bg="#E4D5B8")  # Use self.image here
        main_label.pack(anchor="n")
        
        # Add custom label with text
        CTkLabel(window, text="Edit src/Homescreen.py and save", font=("Manrope", 20),
                 text_color="black", fg_color="#E4D5B8").pack()
        return window
    
    def version_text(self):
        __version__ = VERSION
        CTkLabel(self.window, text=f"Version : {__version__}", font=("Manrope", 15),
                 text_color="black", fg_color="#E4D5B8").pack()
        return self.window
    
    def todo_list(self):
        from src.components.todo_comp import todo_list
        return todo_list(self.window)

        