from customtkinter import *
from tkinter import Label
from vendor.Rocket import *
from Rocket import VERSION
from src.homepages import *
import tkinter as tk
from src.todopage import new_todo

def rocket_image(window) -> Tk:
    """
    Places images in rocket UI.
    """
    Label(window, text="", bg="#E4D5B8").pack(pady=100, padx=200)
    image_path = get_resource_images('rocket_ui.png')
    
    # Keep a reference to the PhotoImage object to prevent garbage collection
    image = PhotoImage(file=image_path) 
    window.image_reference = image  # Attach to the window object

    main_label = Label(window, image=image, bg="#E4D5B8")  
    main_label.pack(anchor="n")
    
    return window

def version_text(window):
        """
        text to display version of the rocket ui 
        """
        __version__ = VERSION
        CTkLabel(window, 
                text=f"Version : {__version__}",
                font=("Manrope", 15),
                text_color="black", 
                fg_color="#E4D5B8"
                  ).pack()
        return window

def next_page_button(window):
    """
    A button to move to the next window
    """
    CTkButton(
        window,
        text="Move to new page",
        border_color="#C29130",  
        hover_color="#C29130", 
        fg_color="#C29130",     
        text_color="black",     
        width=int(window.winfo_width()),
        command=lambda root=window: rerender(root, new_todo)
    ).pack(
        padx=10, 
        pady=5, 
        anchor="center",
        fill=tk.X
    )

