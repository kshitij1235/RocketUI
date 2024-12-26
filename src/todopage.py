from tkinter import *
from customtkinter import *
from vendor.Rocket import rerender
from boxdb.support import *
## TODO modify window var as a reference so it does not have to be returned everytime.

def new_todo(window):    
    from src.components.todo_comp import todo_list
    '''
    This is a different todo list 
    '''
    from src.homepages import homepage

    todo_list(window,"rocketdb","demo")
      
    CTkButton(window,text="go to Home",
                  command = lambda root = window : rerender(root, homepage)
                  ).pack(
                    padx=100, 
                    pady=5, 
                    anchor="center")

