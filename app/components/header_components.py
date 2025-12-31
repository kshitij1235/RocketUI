import tkinter as tk
from customtkinter import CTkSwitch, CTkLabel

from rocket import StatelessWidget, BuildContext

class Header(StatelessWidget):
    def build(self, context: BuildContext, parent: tk.Frame):
        # Container for the header
        container = tk.Frame(parent, bg=context.theme.get_color("bg"))
        container.pack(fill="x", anchor="n")

        # Title
        CTkLabel(
            container,
            text="To-do List",
            font=("Helvetica", 16, "bold"),
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"), 
        ).pack(side="left", padx=10, pady=8)

        # Theme Toggle
        toggle = CTkSwitch(
            container,
            text="Dark Mode",
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("accent"),
            command=context.theme.toggle,
            bg_color=context.theme.get_color("bg"),
        )
        toggle.pack(side="right", padx=10, pady=5)

        # Initialize toggle state
        if context.theme.isdark():
            toggle.select()
        else:
            toggle.deselect()
