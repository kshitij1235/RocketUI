from rocket import Rocket
from tkinter import Label
from tkinter import PhotoImage
from app.__init_ import __version__
from customtkinter import *
from tkinter import *

class app:
    def __init__(self):
        self.window = Rocket().get_window()
        self.images = PhotoImage(file = "resources/rocket_ui.png")
    
    def get_rocket_window(self)->Tk:
        window= self.window
        window.config(bg="#E4D5B8")
        Label(window, text="",bg="#E4D5B8").pack(pady=100,padx=200)
        
        main_label = Label(window,image=self.images,bg="#E4D5B8")
        main_label.pack()
        CTkLabel(window, text="Edit app/main.py and save",font =("Manrope",20),text_color="black",fg_color="#E4D5B8").pack()
        return window
    
    def version_text(self):
        window = self.window
        CTkLabel(window ,text=f"Version : {__version__}",font =("Manrope",15),text_color="black",fg_color="#E4D5B8").pack()
        return window
    
    def todo_list(self):
        window = self.window
        Label(window, text="",bg="#E4D5B8").pack(pady=10)
        CTkCheckBox(window,text="edit the app/main",text_color="black",hover_color="#C29130",fg_color="#C29130").pack(padx=100,pady=5,anchor="w")
        CTkCheckBox(window,text="under the class component system",text_color="black",hover_color="#C29130",fg_color="#C29130").pack(padx=100,pady=5,anchor="w")
        CTkCheckBox(window,text="edit the sequence of main.py",text_color="black",hover_color="#C29130",fg_color="#C29130").pack(padx=100,pady=5,anchor="w")
        CTkCheckBox(window,text="enjoy rocket ui",text_color="black",hover_color="#C29130",fg_color="#C29130").pack(padx=100,pady=5,anchor="w")
        Label(window, text="",bg="#E4D5B8").pack(pady=10)

        return window