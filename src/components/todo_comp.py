from tkinter import *
from customtkinter import *
from vendor.Rocket import *
from src.todo import new_todo

# [TODO] make it more modular 
def todo_list(window):     
        Label(window, text="", bg="#E4D5B8").pack(pady=10)
        for option in ["edit the src/Homescreen.py",
                       "under the class component system","edit the sequence of main.py","enjoy rocket ui"] : 
            CTkCheckBox(window, text=option, text_color="black",
                    hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")

        Label(window, text="", bg="#E4D5B8").pack(pady=10)

        CTkButton(window,text="re-render",
                  command = lambda root = window : rerender(root,  new_todo)
                  ).pack(
                    padx=100, 
                    pady=5, 
                    anchor="center"
                )
        return window