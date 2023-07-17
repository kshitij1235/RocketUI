import weakref
from typing import Callable, Generic, List, TypeVar

from rocket.log import log

T = TypeVar("T")


class Signal(Generic[T]):
    """
    A simple observable state container.
    Uses weak references to avoid memory leaks.
    Synchronous and traceable.
    """

    def __init__(self, initial_value: T = None, name: str = "Signal"):
        self._value: T = initial_value
        self._name = name
        # List of weak references to subscribers
        self._subscribers: List[weakref.WeakMethod] = []
        self._debug_mode = False

    def set_debug(self, enabled: bool):
        self._debug_mode = enabled

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        if self._value != value:
            old = self._value
            self._value = value
            if self._debug_mode:
                log(f"Signal[{self._name}] changed: {old} -> {value}")
            self.notify()

    def notify(self) -> None:
        # Clean up dead references while iterating
        dead_refs = []
        notified_count = 0

        for ref in self._subscribers:
            subscriber = ref()
            if subscriber is not None:
                try:
                    if self._debug_mode:
                        log(f"Signal[{self._name}] notifying {subscriber}")
                    subscriber(self._value)
                    notified_count += 1
                except Exception as e:
                    log(f"Error in signal subscriber {subscriber}: {e}")
                    # We might want to re-raise here if we want "Fail Fast"
                    raise e
            else:
                dead_refs.append(ref)

        for ref in dead_refs:
            self._subscribers.remove(ref)

    def subscribe(self, callback: Callable[[T], None]) -> None:
        """
        Register a callback to be called when value changes.
        Callback must be a bound method (method of an object).
        """
        try:
            ref = weakref.WeakMethod(callback)

            # Check if already subscribed
            for existing_ref in self._subscribers:
                if existing_ref() == callback:
                    return

            self._subscribers.append(ref)
            if self._debug_mode:
                log(f"Signal[{self._name}] subscribed: {callback}")

        except TypeError:
            log(
                f"Signal[{self._name}]: Could not create weak reference for {callback}. Subscription ignored to prevent leaks."
            )

    def unsubscribe(self, callback: Callable[[T], None]) -> None:
        to_remove = []
        for ref in self._subscribers:
            resolved = ref()
            if resolved == callback or resolved is None:
                to_remove.append(ref)

        for ref in to_remove:
            self._subscribers.remove(ref)

    def __repr__(self):
        return f"Signal<{self._name}>({self._value})"
