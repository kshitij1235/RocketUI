import tkinter as tk
from customtkinter import CTkCheckBox, CTkButton, CTkLabel

from app.ControllerManager import todo_store
from app.helper import database
from app.components.scrollbar import add_scrollbar
from rocket import Widget, StatelessWidget, StatefulWidget, State, BuildContext

class TodoList(StatefulWidget):
    def create_state(self) -> "State":
        return _TodoListState()

class _TodoListState(State):
    def init_state(self):
        # Subscribe to the todo store to trigger updates
        todo_store.subscribe(self)

    def invalidate(self):
        # Called by todo_store when it notifies subscribers
        self.set_state()

    def build(self, context: BuildContext, parent: tk.Frame):
        container = tk.Frame(parent, bg=context.theme.get_color("bg"))
        container.pack(fill="both", expand=True)

        tasks = database.get_all_tasks()

        if not tasks:
            self._build_no_tasks(context, container)
            return

        _, scrollable = add_scrollbar(container, context.theme.get_color("bg"))

        for task, status in tasks:
            TaskItem(task, bool(status)).build(context, scrollable)

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


class TaskItem(StatelessWidget):
    def __init__(self, task: str, status: bool):
        self.task = task
        self.status = status

    def build(self, context: BuildContext, parent: tk.Frame):
        container = tk.Frame(parent, bg=context.theme.get_color("bg"))
        container.pack(fill="x", padx=20, pady=5)
        
        status_var = tk.BooleanVar(value=self.status)

        CTkCheckBox(
            container,
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
            container,
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
        todo_store.notify()

