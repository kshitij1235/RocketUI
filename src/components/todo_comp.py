from tkinter import *
from customtkinter import *
from vendor.Rocket import *
from boxdb.support import get_elements
from boxdb import *
import tkinter as tk
from src.homepages import *

# [TODO] make it more modular 
def todo_list(window ,database , table_name ):     
    """
    Creates a to-do list with checkboxes. Updates the database when a checkbox is toggled.
    """
    Label(window, text="", bg="#E4D5B8").pack(pady=10)
    
    # Fetch tasks, statuses, and IDs from the database
    task_ = get_elements(database, table_name, "task") 
    status_ = get_elements(database, table_name, "status")    
    id_ = get_elements(database, table_name, "id")        

    def update_task_status(task_id, status_var):
        """
        Updates the status of a task in the database.
        
        Args:
            task_id: The ID of the task to update.
            status_var: A tkinter BooleanVar tracking the checkbox state.
        """
        new_status = "True" if status_var.get() else "False"
        update_row(database, table_name, task_id, "status", new_status)
    
    for task, status, task_id in zip(task_, status_, id_):
        status_var = tk.BooleanVar(value=status)
        
        CTkCheckBox(
            window,
            text=task,
            text_color="black",
            hover_color="#C29130",
            fg_color="#C29130",
            variable=status_var,
            command=lambda t_id=task_id, s_var=status_var: update_task_status(t_id, s_var)
        ).pack(padx=100, pady=5, anchor="w")
    
    Label(window, text="", bg="#E4D5B8").pack(pady=10)


