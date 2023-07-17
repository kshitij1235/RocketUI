from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Type


@dataclass
class WidgetSpec:
    """
    Intermediate representation of a UI component (VNode).
    This class is purely data and should be immutable-ish.
    """

    widget_class: Type
    props: Dict[str, Any] = field(default_factory=dict)
    children: Sequence["WidgetSpec"] = ()
    key: Optional[str] = None

    # Internal usage by the Renderer - do not touch in user code
    _instance: Any = None

    def __repr__(self):
        return (
            f"<{self.widget_class.__name__} key={self.key} props={self.props.keys()}>"
        )


class GenericWidget:
    """Marker interface for widgets that wrap Tkinter widgets directly."""

    pass


class LayoutWidget:
    """Marker interface for widgets that handle layout (Row, Column, etc)."""

    pass
