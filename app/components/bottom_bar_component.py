import tkinter as tk

from app.ControllerManager import services
from app.helper.database import add_task
from rocket import ReactiveWidget, BuildContext, REntry, RButton

class TaskEntry(ReactiveWidget):
    def __init__(self):
        super().__init__(services.theme)

    def build(self, context: BuildContext, parent: tk.Frame):
        inner_frame = tk.Frame(parent, bg=context.theme.get_color("bg"))
        inner_frame.pack(fill="x", padx=16, pady=16)

        entry = REntry(
            placeholder_text="Add task",
            height=32,
        )
        entry.mount(context, inner_frame, side="left", fill="x", expand=True, padx=(0, 8))

        def on_add():
            text = entry.get().strip()
            if not text:
                return
            
            add_task(text)
            entry.delete(0, "end")
            services.notify_task_change()

        RButton(
            text="Add Task",
            width=80,
            height=32,
            corner_radius=6,
            font=("Helvetica", 11),
            command=on_add,
        ).mount(context, inner_frame, side="right")
