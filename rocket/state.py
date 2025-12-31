from typing import Generic, TypeVar, Callable, List
import weakref

T = TypeVar("T")

class Signal(Generic[T]):
    """
    A simple observable state container.
    Uses weak references to avoid memory leaks.
    """
    def __init__(self, initial_value: T = None):
        self._value: T = initial_value
        # List of weak references to subscribers
        self._subscribers: List[weakref.WeakMethod] = []

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        if self._value != value:
            self._value = value
            self.notify()

    def notify(self) -> None:
        # Clean up dead references while iterating
        dead_refs = []
        for ref in self._subscribers:
            subscriber = ref()
            if subscriber is not None:
                try:
                    subscriber(self._value)
                except Exception as e:
                    print(f"Error in signal subscriber: {e}")
            else:
                dead_refs.append(ref)
        
        for ref in dead_refs:
            self._subscribers.remove(ref)

    def subscribe(self, callback: Callable[[T], None]) -> None:
        """
        Register a callback to be called when value changes.
        Callback must be a bound method (method of an object).
        """
        # We assume callback is a bound method for now (all our usage is self.method)
        # If it's a plain function, WeakMethod might fail or not be appropriate.
        try:
            ref = weakref.WeakMethod(callback)
            
            # Check if already subscribed (simple linear scan)
            for existing_ref in self._subscribers:
                if existing_ref() == callback:
                    return

            self._subscribers.append(ref)
        except TypeError:
            # Fallback for non-method callables (lambdas, functions) - use strong ref or WeakRef?
            # For simplicity and our specific use case (ReactiveWidget), avoiding complexity.
            # But if a user passes a lambda, WeakMethod fails.
            # Let's just warn or handle?
            # Our ReactiveWidget passes self._on_signal_change, which is a method.
            print(f"Warning: Could not create weak reference for {callback}. Subscription ignored to prevent leaks.")

    def unsubscribe(self, callback: Callable[[T], None]) -> None:
        # Harder with weakrefs to find exact match without resolving
        to_remove = []
        for ref in self._subscribers:
            resolved = ref()
            if resolved == callback or resolved is None:
                to_remove.append(ref)
        
        for ref in to_remove:
            self._subscribers.remove(ref)
