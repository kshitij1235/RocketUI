import tkinter as tk
from typing import Callable, Optional, Union

import customtkinter as ctk

from rocket.core.component import StatefulComponent, StatelessComponent
from rocket.core.context import BuildContext
from rocket.core.state import Signal
from rocket.core.widget import WidgetSpec


class _RLabel(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props=props)
        text = self.props.get("text")
        if isinstance(text, Signal):
            self.register_signal(text)

    def build(self, context: BuildContext) -> WidgetSpec:
        text_val = self.props["text"]
        if isinstance(text_val, Signal):
            text_val = text_val.get()

        text_color = context.theme.get_color("text")

        return WidgetSpec(
            widget_class=ctk.CTkLabel,
            props={
                "text": text_val,
                "font": self.props.get("font") or ("Helvetica", 14),
                "text_color": text_color,
                **{k: v for k, v in self.props.items() if k not in ["text", "font"]},
            },
        )


def RLabel(text: Union[str, Signal[str]], font=None, **kwargs) -> WidgetSpec:
    return WidgetSpec(
        widget_class=_RLabel, props={"text": text, "font": font, **kwargs}
    )


class _RButton(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props=props)
        text = self.props.get("text")
        if isinstance(text, Signal):
            self.register_signal(text)

    def build(self, context: BuildContext) -> WidgetSpec:
        text_val = self.props["text"]
        if isinstance(text_val, Signal):
            text_val = text_val.get()

        return WidgetSpec(
            widget_class=ctk.CTkButton,
            props={
                "text": text_val,
                "command": self.props.get("command"),
                "fg_color": context.theme.get_color("accent"),
                "hover_color": context.theme.get_color("hover"),
                "text_color": context.theme.get_color("text"),
                **{k: v for k, v in self.props.items() if k not in ["text", "command"]},
            },
        )


def RButton(
    text: Union[str, Signal[str]], command: Callable | None = None, **kwargs
) -> WidgetSpec:
    return WidgetSpec(
        widget_class=_RButton, props={"text": text, "command": command, **kwargs}
    )


class _REntry(StatefulComponent):
    _tk_var: Optional[tk.StringVar]

    def __init__(self, props=None):
        super().__init__(props=props)
        self._tk_var = None

    def on_mount(self) -> None:
        super().on_mount()
        signal = self.props.get("text_variable")
        if not signal:
            return

        self._tk_var = tk.StringVar(value=signal.get())
        tk_var = self._tk_var

        def on_tk_change(*args) -> None:
            val = tk_var.get()
            if signal.get() != val:
                signal.set(val)

        tk_var.trace_add("write", on_tk_change)

        def on_sig_change(val: str) -> None:
            if tk_var.get() != val:
                tk_var.set(val)

        signal.subscribe(on_sig_change)
        self.register_signal(signal)

    def build(self, context: BuildContext) -> WidgetSpec:
        props = {
            "text_color": context.theme.get_color("text"),
            "fg_color": context.theme.get_color("bg"),
            **{k: v for k, v in self.props.items() if k not in ["text_variable"]},
        }

        if self._tk_var:
            props["textvariable"] = self._tk_var

        return WidgetSpec(widget_class=ctk.CTkEntry, props=props)


def REntry(text_variable: Signal[str] | None = None, **kwargs) -> WidgetSpec:
    return WidgetSpec(
        widget_class=_REntry, props={"text_variable": text_variable, **kwargs}
    )


class _RCheckbox(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props=props)
        variable = self.props.get("variable")
        if variable:
            self.register_signal(variable)

    def build(self, context: BuildContext) -> WidgetSpec:
        return WidgetSpec(
            widget_class=ctk.CTkCheckBox,
            props={
                "text": self.props["text"],
                "command": self.props.get("command"),
                "text_color": context.theme.get_color("text"),
                **{
                    k: v
                    for k, v in self.props.items()
                    if k not in ["text", "variable", "command"]
                },
            },
        )


def RCheckbox(
    text: str, variable: Signal[bool] | None = None, command=None, **kwargs
) -> WidgetSpec:
    return WidgetSpec(
        widget_class=_RCheckbox,
        props={"text": text, "variable": variable, "command": command, **kwargs},
    )


class _RSwitch(StatelessComponent):
    def build(self, context: BuildContext) -> WidgetSpec:
        from rocket.render.native import NativeSwitch

        return WidgetSpec(widget_class=NativeSwitch, props=self.props)


def RSwitch(checked: bool = False, command=None, **kwargs) -> WidgetSpec:
    return WidgetSpec(
        widget_class=_RSwitch, props={"checked": checked, "command": command, **kwargs}
    )
