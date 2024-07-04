from tkinter import *
from customtkinter import *
def new_todo(window):    
    # Add padding and pack labels
    Label(window, text="new window", bg="#E4D5B8").pack(pady=10)
    CTkCheckBox(window, text="edit the app/main", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    CTkCheckBox(window, text="under the class component system", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    CTkCheckBox(window, text="edit the sequence of main.py", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    CTkCheckBox(window, text="enjoy rocket ui", text_color="black",
                hover_color="#C29130", fg_color="#C29130").pack(padx=100, pady=5, anchor="w")
    Label(window, text="", bg="#E4D5B8").pack(pady=10)
