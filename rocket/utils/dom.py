def get_element_by_name(parent, name: str):
    for widget in parent.winfo_children():
        if widget.winfo_name() == name:
            return widget
        result = get_element_by_name(widget, name)
        if result is not None:
            return result
    return None
