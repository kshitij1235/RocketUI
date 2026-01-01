from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from rocket.core.context import BuildContext
from rocket.core.state import Signal
from rocket.core.widget import WidgetSpec


class ComponentLifecycleError(Exception):
    """Raised when component lifecycle rules are violated."""

    pass


class Component(ABC):
    """
    Base class for all RocketUI components.
    Enforces strict lifecycle: init -> mount -> build -> unmount.
    """

    def __init__(self, props: Optional[dict[str, Any]] = None):
        self.props = props or {}
        self.context: Optional[BuildContext] = None
        self._mounted = False
        self._node: Optional[WidgetSpec] = (
            None  # The VNode that produced this component
        )

    def mount(self, context: BuildContext):
        """Called by the renderer when the component is added to the tree."""
        if self._mounted:
            raise ComponentLifecycleError(f"Component {self} is already mounted.")
        self.context = context
        self._mounted = True
        self.on_mount()

    def unmount(self):
        """Called by the renderer when the component is removed."""
        if not self._mounted:
            return
        self.on_unmount()
        self._mounted = False
        self.context = None

    def on_mount(self):
        """Lifecycle hook: Called once when component is mounted."""
        pass

    def on_unmount(self):
        """Lifecycle hook: Called once when component is unmounted."""
        pass

    def on_update(self, prev_props: Dict[str, Any]):
        """Lifecycle hook: Called when props change."""
        pass

    @abstractmethod
    def build(self, context: BuildContext) -> Union[WidgetSpec, None]:
        """
        Pure function to describe the UI.
        MUST NOT mutate state or touch Tkinter directly.
        """
        pass


class StatelessComponent(Component):
    """A component that is a pure function of its props."""

    pass


class StatefulComponent(Component):
    """
    A component that owns internal state.
    State mutations must happen via set_state.
    """

    def __init__(self, props: Dict[str, Any] = None):
        super().__init__(props)
        self._signals: list[Signal] = []

    def register_signal(self, signal: Signal):
        """
        Register a signal to automatically unsubscribe on unmount.
        This framework calls this automatically if you use `use_signal` (future)
        or pass signals to __init__ (legacy compatibility).
        """
        self._signals.append(signal)
        # Helper to force update on signal change
        signal.subscribe(self._on_signal_change)

    def _on_signal_change(self, value):
        if not self._mounted:
            return
        # In a real implementation, this would schedule a render.
        # For now, we rely on the renderer to handle 'invalidate'.
        # We need a way to tell the renderer "I am dirty".
        # This requires the component to have a reference to its 'owner' or 'updater'.
        if hasattr(self, "_request_update_callback"):
            self._request_update_callback(self)

    def on_unmount(self):
        for sig in self._signals:
            sig.unsubscribe(self._on_signal_change)
        super().on_unmount()

    def set_state(self, fn):
        """
        Update state and schedule a re-render.
        fn: (current_state) -> new_state (or just mutate inplace and return)
        """
        # In this simplistic version, we assume state is just signals or direct attributes.
        # This method is a placeholder for stricter state management if we introduce a `State` object.
        raise NotImplementedError("Use Signals for state management for now.")
