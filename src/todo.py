from tkinter import *
from customtkinter import *
from vendor.Rocket import rerender

## TODO modify window var as a reference so it does not have to be returned everytime.

def new_todo(window):    
    from src.components.todo_comp import todo_list
    '''
    This is a different todo list 
    '''
    CTkCheckBox(window, text="under the class component system", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    CTkCheckBox(window, text="edit the sequence of main.py", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    CTkCheckBox(window, text="enjoy rocket ui", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    CTkButton(window,text="re-render",
                  command = lambda root = window : rerender(root, todo_list)
                  ).pack(
                    padx=100, 
                    pady=5, 
                    anchor="center")

