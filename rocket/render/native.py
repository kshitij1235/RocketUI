from customtkinter import CTkFrame, CTkScrollableFrame, CTkSwitch


class NativeColumn(CTkFrame):
    layout_strategy = "column"

    def __init__(self, *args, **kwargs):
        self.spacing = kwargs.pop("spacing", 0)
        # Ensure children aren't passed even if filtering fails upstream
        kwargs.pop("children", None)
        super().__init__(*args, **kwargs)


class NativeRow(CTkFrame):
    layout_strategy = "row"

    def __init__(self, *args, **kwargs):
        self.spacing = kwargs.pop("spacing", 0)
        kwargs.pop("children", None)
        super().__init__(*args, **kwargs)


class NativeScrollableColumn(CTkScrollableFrame):
    layout_strategy = "column"

    def __init__(self, *args, **kwargs):
        self.spacing = kwargs.pop("spacing", 0)
        kwargs.pop("children", None)
        super().__init__(*args, **kwargs)


class NativeScrollableRow(CTkScrollableFrame):
    layout_strategy = "row"

    def __init__(self, *args, **kwargs):
        self.spacing = kwargs.pop("spacing", 0)
        kwargs.pop("children", None)

        # Force horizontal scrolling
        kwargs.setdefault("orientation", "horizontal")

        super().__init__(*args, **kwargs)


class NativeSwitch(CTkSwitch):
    def __init__(self, *args, **kwargs):
        checked = kwargs.pop("checked", False)
        kwargs.pop("children", None)  # Just in case
        super().__init__(*args, **kwargs)
        if checked:
            self.select()
        else:
            self.deselect()

    def configure(self, require_redraw=False, **kwargs):
        if "checked" in kwargs:
            checked = kwargs.pop("checked")
            if checked:
                self.select()
            else:
                self.deselect()
        super().configure(require_redraw=require_redraw, **kwargs)
