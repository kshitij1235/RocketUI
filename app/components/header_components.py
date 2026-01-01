from app.ControllerManager import services
from rocket.component import StatefulComponent
from rocket.context import BuildContext
from rocket.elements import RLabel, RSwitch
from rocket.layout import Row
from rocket.widget_core import WidgetSpec

class _Header(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props=props)
        self.register_signal(services.theme)

    def build(self, context: BuildContext) -> WidgetSpec:
        is_dark = context.theme.isdark()
        
        return Row(
            spacing=10,
            children=[
                RLabel(
                    text="To-do List",
                    font=("Helvetica", 16, "bold"),
                    # Removing fixed width to let it natural size, switch pushes right
                    side="left"
                ),
                RSwitch(
                    text="Dark Mode",
                    checked=is_dark,
                    command=services.theme.toggle,
                    side="right" # Push to right
                )
            ]
        )

def Header(**kwargs) -> WidgetSpec:
    return WidgetSpec(widget_class=_Header, props=kwargs)
