from Rocket import *
import sys
from tkinter import Tk, Label,Button
from tkinter import PhotoImage  # Import PhotoImage for loading images
from customtkinter import *
from vendor.json_extractor.extract_values import json_extractor
from vendor.Rocket.resource_gather import get_resource_images
from vendor.Rocket.Rrender import *
from src.todo import *

class homescreen:
    def __init__(self, window:Tk):
        self.window = window
        try:
            self.image_path = get_resource_images('rocket_ui.png')
            self.image = PhotoImage(file=self.image_path)  # Load image using PhotoImage
        except:
            print("error loading image")
    def get_rocket_window(self) -> Tk:
        window = self.window
        window.config(bg="#E4D5B8")
        
        # Add padding and pack labels
        Label(window, text="", bg="#E4D5B8").pack(pady=100, padx=200)
        main_label = Label(window, image=self.image, bg="#E4D5B8")  # Use self.image here
        main_label.pack()
        
        # Add custom label with text
        CTkLabel(window, text="Edit app/main.py and save", font=("Manrope", 20),
                 text_color="black", fg_color="#E4D5B8").pack()
        
        return window
    
    def version_text(self):
        __version__ = rocket["version"];
        CTkLabel(self.window, text=f"Version : {__version__}", font=("Manrope", 15),
                 text_color="black", fg_color="#E4D5B8").pack()
        return self.window
    
    def todo_list(self):
        window = self.window
        
        # Add padding and pack labels
        Label(window, text="", bg="#E4D5B8").pack(pady=10)
        CTkCheckBox(window, text="edit the app/main", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
        CTkCheckBox(window, text="under the class component system", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
        CTkCheckBox(window, text="edit the sequence of main.py", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
        CTkCheckBox(window, text="enjoy rocket ui", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
        Label(window, text="", bg="#E4D5B8").pack(pady=10)

        CTkButton(window,text="re-render",command= lambda root = self.window : rerender(root,  new_todo)).pack()
        return window
