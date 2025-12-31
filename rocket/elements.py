import tkinter as tk
import customtkinter as ctk
from typing import Union, Any

from rocket.widget import ReactiveWidget, StatelessWidget
from rocket.context import BuildContext
from rocket.state import Signal

class RDiv(StatelessWidget):
    """
    A theme-aware container (Frame).
    """
    def build(self, context: BuildContext, parent: tk.Frame):
        pass

class RLabel(ReactiveWidget):
    def __init__(self, text: Union[str, Signal[str]], font=None, **kwargs):
        # Identify signals
        signals = []
        if isinstance(text, Signal):
            signals.append(text)
            self._text_signal = text
            self._text_val = None
        else:
            self._text_signal = None
            self._text_val = text
            
        # Also need to listen to theme!
        # Accessing global theme is a bit dirty here if we want pure dependency injection,
        # but in our current architecture ReactiveWidget needs explicit signals in init.
        # Ideally we'd get theme from context, but context comes at mount time.
        # So we should add theme signal in mount? 
        # ReactiveWidget.mount calls subscribe. 
        # But we need the signal list in __init__.
        # We'll use the pattern of importing the service for default theme binding
        # OR we assume the user passes a theme signal if they want reactivity?
        # No, R-Components should auto-react to theme.
        from app.ControllerManager import services
        signals.append(services.theme)
        
        super().__init__(*signals)
        self.font = font
        self.kwargs = kwargs

    def build(self, context: BuildContext, parent: tk.Frame):
        current_text = self._text_signal.get() if self._text_signal else self._text_val
        
        ctk.CTkLabel(
            parent,
            text=current_text,
            font=self.font or ("Helvetica", 14),
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"),
            **self.kwargs
        ).pack(fill="both", expand=True)

class RButton(ReactiveWidget):
    def __init__(self, text: Union[str, Signal[str]], command=None, **kwargs):
        signals = []
        if isinstance(text, Signal):
            signals.append(text)
            self._text_signal = text
            self._text_val = None
        else:
            self._text_signal = None
            self._text_val = text

        from app.ControllerManager import services
        signals.append(services.theme)

        super().__init__(*signals)
        self.command = command
        self.kwargs = kwargs

    def build(self, context: BuildContext, parent: tk.Frame):
        current_text = self._text_signal.get() if self._text_signal else self._text_val

        ctk.CTkButton(
            parent,
            text=current_text,
            command=self.command,
            fg_color=context.theme.get_color("accent"),
            hover_color=context.theme.get_color("hover"),
            text_color=context.theme.get_color("text"),
            **self.kwargs
        ).pack(fill="both", expand=True)

class REntry(ReactiveWidget):
    def __init__(self, text_variable: Signal[str] = None, **kwargs):
        signals = []
        if text_variable and isinstance(text_variable, Signal):
            signals.append(text_variable)
        self._text_signal = text_variable
        
        from app.ControllerManager import services
        signals.append(services.theme)
        
        super().__init__(*signals)
        self.kwargs = kwargs
        self._entry = None

    def build(self, context: BuildContext, parent: tk.Frame):
        # Note: Rebuilding Entry on every keystroke (if using signal) is bad UX (loses focus).
        # But here signal matches text_variable. 
        # We need to bind the Tk variable to the signal.
        # This is complex for 2-way binding. 
        # For now, let's treat it as: if signal changes externally, update text.
        
        self._entry = ctk.CTkEntry(
            parent,
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"),
            **self.kwargs
        )
        self._entry.pack(fill="both", expand=True)
        
        if self._text_signal:
            self._entry.insert(0, self._text_signal.get() or "")

    def get(self):
        return self._entry.get() if self._entry else ""

    def delete(self, first, last=None):
        if self._entry:
            self._entry.delete(first, last)

class RCheckbox(ReactiveWidget):
    def __init__(self, text: str, variable: Signal[bool] = None, command=None, **kwargs):
        signals = []
        if variable and isinstance(variable, Signal):
            signals.append(variable)
        self._var_signal = variable
        
        from app.ControllerManager import services
        signals.append(services.theme)
        
        super().__init__(*signals)
        self.text = text
        self.command = command
        self.kwargs = kwargs
        self._tk_var = None

    def build(self, context: BuildContext, parent: tk.Frame):
        # We need a tk.BooleanVar to bind to the checkbox
        value = self._var_signal.get() if self._var_signal else False
        self._tk_var = tk.BooleanVar(value=value)
        
        def on_toggle():
            # Update signal if user toggles
            new_val = self._tk_var.get()
            if self._var_signal and self._var_signal.get() != new_val:
                self._var_signal.set(new_val)
            if self.command:
                self.command()

        ctk.CTkCheckBox(
            parent,
            text=self.text,
            variable=self._tk_var,
            font=self.kwargs.pop("font", ("Helvetica", 12)),
            text_color=context.theme.get_color("text"),
            hover_color=context.theme.get_color("hover"),
            fg_color=context.theme.get_color("accent"),
            bg_color=context.theme.get_color("bg"),
            command=on_toggle,
            **self.kwargs
        ).pack(fill="both", expand=True)
