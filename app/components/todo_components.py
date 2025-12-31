import tkinter as tk

from app.ControllerManager import services
from app.helper import database
from app.components.scrollbar import add_scrollbar
from rocket import ReactiveWidget, StatelessWidget, BuildContext, RLabel, RCheckbox, RButton, Signal

class TodoList(ReactiveWidget):
    def __init__(self):
        super().__init__(services.todo_store, services.theme)

    def build(self, context: BuildContext, parent: tk.Frame):
        tasks = database.get_all_tasks()

        if not tasks:
            self._build_no_tasks(context, parent)
            return

        _, scrollable = add_scrollbar(parent, context.theme.get_color("bg"))

        for task, status in tasks:
            TaskItem(task, bool(status)).mount(context, scrollable, fill="x", padx=20, pady=5)

    def _build_no_tasks(self, context: BuildContext, parent: tk.Frame):
        frame = tk.Frame(parent, bg=context.theme.get_color("bg"), pady=20)
        frame.pack(pady=30, fill="x")
        
        RLabel(
            text="No tasks here, why not add one?",
            font=("Helvetica", 12, "italic"),
        ).mount(context, frame)


class TaskItem(StatelessWidget):
    """
    Now a StatelessWidget! 
    The children (RCheckbox, RButton) handle their own theme updates.
    """
    def __init__(self, task: str, status: bool):
        self.task = task
        self.status = status

    def build(self, context: BuildContext, parent: tk.Frame):
        # Create a local signal for the checkbox state
        # In a real app, this might come from the store directly,
        # but here we bridge the fast read-only db data to a reactive signal.
        status_signal = Signal(self.status)

        RCheckbox(
            text=self.task,
            variable=status_signal,
            font=("Arial", 14),
            command=lambda: self._update_status(status_signal.get())
        ).mount(context, parent, side="left", padx=5)
        # Note: RCheckbox creates its own variable if None passed, but we passed manual command. To sync UI:
        # Actually RCheckbox internal implementation needs `variable` or it makes one.
        # If we want to Initialize it, we need to pass a Signal?
        # My implementation of RCheckbox expects `Signal[bool]` or `None`.
        # If None, it defaults to False.
        # Passing `variable=Signal(self.status)` would work but is overkill?
        # Wait, previous RCheckbox implementation took `variable` as tk.Variable?
        # My NEW implementation takes `Signal[bool]`.
        # I need to fix RCheckbox usage or update RCheckbox to accept initial value or bool.
        
        # Checking elements.py RCheckbox again.
        
        RButton(
            text="Delete",
            width=60,
            height=28,
            corner_radius=6,
            command=self._delete_task
        ).mount(context, parent, side="right", padx=5)

    def _update_status(self, is_done: bool):
        database.update_task_status(self.task, is_done)
        
    def _delete_task(self):
        database.delete_task(self.task)
        services.notify_task_change()
