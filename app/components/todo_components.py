import tkinter as tk
from customtkinter import CTkCheckBox, CTkButton, CTkLabel

from app.ControllerManager import services
from app.helper import database
from app.components.scrollbar import add_scrollbar
from rocket import ReactiveWidget, StatelessWidget, BuildContext

class TodoList(ReactiveWidget):
    def __init__(self):
        # Subscribe to todo_store changes and theme changes
        super().__init__(services.todo_store, services.theme)

    def build(self, context: BuildContext, parent: tk.Frame):
        tasks = database.get_all_tasks()

        if not tasks:
            self._build_no_tasks(context, parent)
            return

        _, scrollable = add_scrollbar(parent, context.theme.get_color("bg"))

        for task, status in tasks:
            # Mount task items into the scrollable area
            # They need to be reactive to theme changes too
            TaskItem(task, bool(status)).mount(context, scrollable, fill="x", padx=20, pady=5)

    def _build_no_tasks(self, context: BuildContext, parent: tk.Frame):
        frame = tk.Frame(parent, bg=context.theme.get_color("bg"), pady=20)
        frame.pack(pady=30, fill="x")
        
        CTkLabel(
            frame,
            text="No tasks here, why not add one?",
            font=("Helvetica", 12, "italic"),
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"),
        ).pack()


class TaskItem(ReactiveWidget):
    def __init__(self, task: str, status: bool):
        # Responsive to theme changes
        super().__init__(services.theme)
        self.task = task
        self.status = status

    def build(self, context: BuildContext, parent: tk.Frame):
        status_var = tk.BooleanVar(value=self.status)

        CTkCheckBox(
            parent,
            text=self.task,
            variable=status_var,
            font=("Arial", 14),
            text_color=context.theme.get_color("text"),
            hover_color=context.theme.get_color("hover"),
            fg_color=context.theme.get_color("accent"),
            bg_color=context.theme.get_color("bg"),
            command=lambda: self._update_status(status_var.get())
        ).pack(side="left", padx=5)

        CTkButton(
            parent,
            text="Delete",
            width=60,
            height=28,
            corner_radius=6,
            fg_color=context.theme.get_color("accent"),
            hover_color=context.theme.get_color("hover"),
            text_color=context.theme.get_color("text"),
            command=self._delete_task
        ).pack(side="right", padx=5)

    def _update_status(self, is_done: bool):
        database.update_task_status(self.task, is_done)
        
    def _delete_task(self):
        database.delete_task(self.task)
        # Notify store to refresh list
        services.notify_task_change()
