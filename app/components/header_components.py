import tkinter as tk
from customtkinter import CTkSwitch, CTkLabel

from rocket import ReactiveWidget, BuildContext
from app.ControllerManager import services

class Header(ReactiveWidget):
    def __init__(self):
        super().__init__(services.theme)

    def build(self, context: BuildContext, parent: tk.Frame):
        CTkLabel(
            parent,
            text="To-do List",
            font=("Helvetica", 16, "bold"),
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"), 
        ).pack(side="left", padx=10, pady=8)

        toggle = CTkSwitch(
            parent,
            text="Dark Mode",
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("accent"),
            command=context.theme.toggle,
            bg_color=context.theme.get_color("bg"),
        )
        toggle.pack(side="right", padx=10, pady=5)

        if context.theme.isdark():
            toggle.select()
        else:
            toggle.deselect()
