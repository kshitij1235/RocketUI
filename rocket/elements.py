import tkinter as tk
from typing import Union

import customtkinter as ctk

from rocket.context import BuildContext
from rocket.state import Signal
from rocket.state_widgets.statefull import StatefullWidget
from rocket.state_widgets.stateless import StatelessWidget


class RDiv(StatelessWidget):
    """
    A theme-aware container (Frame).
    """

    def build(self, context: BuildContext, parent: tk.Frame):
        pass


class RLabel(StatefullWidget):
    def __init__(self, text: Union[str, Signal[str]], font=None, **kwargs):
        from app.ControllerManager import services

        # Identify signals
        signals = []
        if isinstance(text, Signal):
            signals.append(text)
            self._text_signal = text
            self._text_val = None
        else:
            self._text_signal = None
            self._text_val = text

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
            **self.kwargs,
        ).pack(fill="both", expand=True)


class RButton(StatefullWidget):
    def __init__(self, text: Union[str, Signal[str]], command=None, **kwargs):
        from app.ControllerManager import services

        signals = []
        if isinstance(text, Signal):
            signals.append(text)
            self._text_signal = text
            self._text_val = None
        else:
            self._text_signal = None
            self._text_val = text

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
            **self.kwargs,
        ).pack(fill="both", expand=True)


class REntry(StatefullWidget):
    def __init__(self, text_variable: Signal[str] = None, **kwargs):
        from app.ControllerManager import services

        signals = []
        if text_variable and isinstance(text_variable, Signal):
            signals.append(text_variable)
        self._text_signal = text_variable

        signals.append(services.theme)

        super().__init__(*signals)
        self.kwargs = kwargs
        self._entry = None

    def build(self, context: BuildContext, parent: tk.Frame):
        self._entry = ctk.CTkEntry(
            parent,
            text_color=context.theme.get_color("text"),
            fg_color=context.theme.get_color("bg"),
            **self.kwargs,
        )
        self._entry.pack(fill="both", expand=True)

        if self._text_signal:
            self._entry.insert(0, self._text_signal.get() or "")

    def get(self):
        return self._entry.get() if self._entry else ""

    def delete(self, first, last=None):
        if self._entry:
            self._entry.delete(first, last)


class RCheckbox(StatefullWidget):
    def __init__(
        self, text: str, variable: Signal[bool] = None, command=None, **kwargs
    ):
        from app.ControllerManager import services

        signals = []
        if variable and isinstance(variable, Signal):
            signals.append(variable)
        self._var_signal = variable

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
            **self.kwargs,
        ).pack(fill="both", expand=True)
