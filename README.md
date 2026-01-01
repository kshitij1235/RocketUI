# RocketUI

RocketUI is a declarative, component-based UI framework for Tkinter that manages state, rendering, and layout predictably.

## Why It Exists

*   **Managing state without spaghetti callbacks**
*   **Avoiding manual widget recreation**
*   **Predictable re-rendering**
*   **Cleaner layout composition**

## Mental Model

*   **You describe UI by returning `WidgetSpecs`**: Your code defines *what* it should look like, not *how* to draw it.
*   **Components do not create Tk widgets directly**: They return descriptions. The framework assumes the burden of creation.
*   **State changes trigger re-renders**: Updating a `Signal` notifies the component to rebuild its description.
*   **The renderer updates existing widgets**: It differences the old and new descriptions and only applies changes (creating, destroying, or updating properties).

## Hello World

```python
from rocket.runtime.window_manager import WindowManager
from rocket.theme.manager import ThemeManager
from rocket import BasePage, StatefulComponent, Column, RLabel, RButton, Signal

class Counter(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props)
        self.count = Signal(0)
        self.register_signal(self.count)  # Auto-subscribe to changes

    def build(self, context):
        return Column(spacing=20, children=[
            RLabel(text=self.count),
            RButton(
                text="Increment",
                command=lambda: self.count.set(self.count.get() + 1)
            )
        ])

class App(BasePage):
    def build(self, context):
        return Counter()

if __name__ == "__main__":
    win = WindowManager().get("main_window")
    App(win, ThemeManager()).render()
    win.mainloop()
```

## Project Structure

*   `main.py`: Entry point for the application.
*   `app/components/`: Reusable UI components.
*   `app/pages/`: Full-screen page definitions.
*   `rocket/`: The framework source code.

## Core Concepts

### Components
All UI is built from `Component` subclasses.
*   **Stateless**: Pure render functions based on `props`.
*   **Stateful**: Can hold `Signal`s and update themselves.

### State & Signals
`Signal` is the reactive primitive.
```python
count = Signal(0)
count.set(1) # Triggers updates
print(count.get())
```

### Layout
Layouts are just components that arrange children.
*   `Column`: Vertical stack.
*   `Row`: Horizontal stack.
*   `ScrollableColumn`: Vertical stack with scrollbar.

### Pages
The root of your widget tree. Manages the window connection and global theme.

### Theme
Passed down via `BuildContext`. Allows global styling.

## Layout Basics

**Column (Vertical Stack)**
```python
Column(spacing=10, children=[
    RLabel(text="Top"),
    RLabel(text="Bottom")
])
```

**Row (Horizontal Stack)**
```python
Row(spacing=5, children=[
    RButton(text="Left"),
    RButton(text="Right")
])
```

**Nesting**
```python
Column(children=[
    Header(),
    Row(children=[SideBar(), Content()]) # Rows inside Columns
])
```

## Common Patterns

**Updating Input State**
```python
# REntry expects a Signal
self.name = Signal("")
REntry(text_variable=self.name)
```

**Conditionally Rendering Widgets**
```python
Column(children=[
    RLabel("Loading...") if self.loading.get() else Content(),
])
```

**Simple Navigation**
```python
# Replace the root component
self.current_page.set("home")
```

## What NOT To Do

*   **Don't mutate state in `build()`**: This causes infinite render loops.
*   **Don't touch Tk widgets directly**: You will break the renderer's diffing algorithm.
*   **Don't store widget instances**: Store `WidgetSpec` descriptions only.
*   **Don't subscribe to signals with lambdas without cleanup**: Use `register_signal`.

## Error Messages & Debugging

*   **"Component is already mounted"**: You are reusing a component instance in two places. Create new instances.
*   **"Unknown window"**: `WindowManager` config is missing.
*   **Silent Failures**: Check that you returned `WidgetSpec` from `build()`. Returning `None` renders nothing.

## Installation & Running

**Prerequisites**: Python 3.10+

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the app**:
    ```bash
    python main.py
    ```

## Roadmap / Status

**Status**: Experimental / Alpha.

**Subject to Change**:
*   Signal API (might move to hooks like `use_signal`)
*   Context API
*   Native Widget wrappers

This framework is for internal use and rapid prototyping.
