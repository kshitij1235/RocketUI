import tkinter as tk
from customtkinter import CTkEntry, CTkButton

from app.ControllerManager import services
from app.helper.database import add_task
from rocket import ReactiveWidget, BuildContext

class TaskEntry(ReactiveWidget):
    def __init__(self):
        # Responsive to theme
        super().__init__(services.theme)

    def build(self, context: BuildContext, parent: tk.Frame):
        inner_frame = tk.Frame(parent, bg=context.theme.get_color("bg"))
        inner_frame.pack(fill="x", padx=16, pady=16)

        entry = CTkEntry(
            inner_frame,
            placeholder_text="Add task",
            height=32,
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"),
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        def on_add():
            text = entry.get().strip()
            if not text:
                return
            
            add_task(text)
            entry.delete(0, "end")
            
            # Notify the store so TodoList updates
            services.notify_task_change()

        CTkButton(
            inner_frame,
            text="Add Task",
            width=80,
            height=32,
            corner_radius=6,
            font=("Helvetica", 11),
            fg_color=context.theme.get_color("accent"),
            hover_color=context.theme.get_color("hover"),
            text_color=context.theme.get_color("text"),
            command=on_add,
        ).pack(side="right")
