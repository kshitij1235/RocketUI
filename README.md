# Rocket UI Framework

Rocket is a **state-driven UI framework built on top of Tkinter**, designed to give you a **React-like rendering model** without forcing you to write boilerplate, lifecycle code, or manual refresh logic.

Rocket separates **framework code** from **application code**, provides a **clean CLI**, and supports **hot reload**, **theme updates**, and **automatic UI re-rendering**.

---

## Key Concepts

### 1. Declarative Rendering

You describe *what* the UI should look like. Rocket decides *when* to re-render.

You never manually refresh widgets.

---

### 2. State-Driven UI

Rocket uses a simple `State` object.

When state changes:

* All subscribed components re-render automatically
* No callbacks, no manual redraws

---

### 3. Component Ownership

Each component:

* Owns its container
* Re-renders only its subtree
* Never destroys unrelated widgets

---

### 4. Theme Reactivity

Changing the theme:

* Automatically re-renders all subscribed components
* No widget-by-widget updates

---

## Project Structure

```
.
├── app/                  # Your application code
│   ├── components/       # UI components
│   ├── helper/           # Database, utilities
│   ├── homepages.py      # Page composition
│   └── ControllerManager.py
│
├── rocket/               # Rocket framework (DO NOT EDIT)
│   ├── components.py
│   ├── renderer.py
│   ├── state.py
│   ├── theme/
│   ├── runtime/
│   └── cli/
│
├── main.py               # App entry point
├── project_config.py     # App configuration
└── requirements.txt
```

---

## Core APIs

### `Components`

Used to create themed widgets and bind state.

```python
from rocket import Components
```

Provides:

* `Rframe`
* `Rlabels`
* `Rbutton`
* `Rcheckbox`
* `Rentry`
* `use_state(...)`

---

### `State`

Represents reactive state.

```python
from rocket import State

todo_store = State()
```

When you call:

```python
todo_store.notify()
```

All subscribed components re-render automatically.

---

### `ThemeManager`

Controls light/dark themes.

```python
from rocket import ThemeManager

app_theme = ThemeManager()
```

Toggling the theme automatically re-renders all components using it.

---

## Writing Components (Example)

### Todo List Component

```python
def todo_list(window):
    comp = Components(window, app_theme)

    container = comp.Rframe(window)
    container.pack(fill="both", expand=True)

    def render(parent):
        for child in parent.winfo_children():
            child.destroy()

        tasks = get_all_tasks()

        if not tasks:
            no_tasks_message(parent)
            return

        _, scrollable = add_scrollbar(parent, app_theme.get_color("bg"))

        for task, status in tasks:
            task_frame(scrollable, task, bool(status))

    comp.use_state(todo_store, container, render)
```

You never call `render()` manually.
Rocket does it automatically when state changes.

---

## Single Row Component

```python
def task_frame(parent, task: str, status: bool):
    comp = Components(parent, app_theme)

    frame = comp.Rframe(parent)
    frame.pack(fill="x", padx=20, pady=5)

    status_var = tk.BooleanVar(value=status)

    comp.Rcheckbox(
        frame,
        text=task,
        variable=status_var,
        command=lambda: update_task_status(task, status_var),
    ).pack(side="left")

    comp.Rbutton(
        frame,
        text="Delete",
        command=lambda: delete_task(task),
    ).pack(side="right")
```

---

## Pages

Pages are just functions that compose components.

```python
def homepage(window):
    todo_header(window)
    todo_list(window)
    task_entry(window)
```

No router. No lifecycle. Just functions.

---

## App Entry Point

```python
from rocket.runtime.window_manager import WindowManager
from app.homepages import homepage

def main():
    windows = WindowManager()
    main_window = windows.get("main_window")

    homepage(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()
```

Rocket manages the window.
Your app decides what to render.

---

## Configuration (`project_config.py`)

This file is owned by the **app**, not the framework.

```python
PROJECT_NAME = "demo_app"
VERSION = "0.0"
RELEASE = False

class MainWindowConfig:
    title = "Todo List"
    geometry = "500x700"
    resizable = False
    icon = "rocket_ui.png"
```

Rocket loads this automatically at runtime.

---

## CLI Usage

After installation:

```bash
pip install -e .
```

Available commands:

```bash
rocket --help
rocket run
rocket run --hotreload
rocket build
rocket clean
rocket version
```

### Hot Reload

Automatically restarts the app on `.py` file changes:

```bash
rocket run --hotreload
```

---

##  Build (PyInstaller)

```bash
rocket build
```

Output:

```
build/
└── linux/
    ├── dist/
    └── work/
```

OS is auto-detected.

---

## 🚫 What Rocket Does NOT Do

* No virtual DOM
* No diffing
* No magic imports
* No global widget registry
* No hidden side effects

Rocket is **simple by design**.

---

## 🎯 When to Use Rocket

✔ Desktop apps
✔ Internal tools
✔ Prototypes
✔ Small to medium UI projects
✔ Tkinter apps that need structure

❌ Web apps
❌ High-frequency animations
❌ Massive widget trees

---

## Philosophy

> UI should re-render because **state changed**,
> not because you remembered to call a function.

Rocket enforces that rule.

---

## Final Notes

* Framework code lives in `rocket/`
* App code lives in `app/`
* Never import app code from the framework
* State changes drive UI updates
* Themes are reactive by default
