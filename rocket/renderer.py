from tkinter import Widget

from rocket.log import log


def _destroy_children(widget: Widget) -> None:
    """
    Destroy all direct children of a widget.

    This is layout-manager agnostic and safe for:
    - pack
    - grid
    - place

    We do NOT recurse manually and we do NOT touch
    any private Tkinter internals.
    """
    for child in widget.winfo_children():
        child.destroy()


def rerender(root, page_factory) -> None:
    """
    Replace the current page with a new one.

    This is ONLY used for page navigation
    (e.g. switching screens), not for state updates.

    Users should NEVER call this directly.
    """
    log("Renderer: page switch")

    _destroy_children(root)

    try:
        page_factory(root)
    except Exception as exc:
        log(f"Renderer error while rendering page: {exc}")
        raise


def rerender_component(parent, render_fn, *args, **kwargs) -> None:
    """
    Re-render a component inside its container.

    This function:
    - clears the container
    - calls the component's render function

    It does NOT:
    - call update()
    - force layout
    - assume pack or grid
    - touch widget internals
    """
    _destroy_children(parent)

    try:
        render_fn(parent, *args, **kwargs)
    except Exception as exc:
        log(f"Renderer error while rendering component: {exc}")
        raise
