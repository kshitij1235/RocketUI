import tkinter as tk
from customtkinter import CTkSwitch

from rocket import StatelessWidget, BuildContext, RLabel
from app.ControllerManager import services


from rocket import ReactiveWidget

class Header(ReactiveWidget):
    def __init__(self):
        super().__init__(services.theme)

    def build(self, context: BuildContext, parent: tk.Frame):
        RLabel(
            text="To-do List",
            font=("Helvetica", 16, "bold"),
        ).mount(context, parent, side="left", padx=10, pady=8)

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
