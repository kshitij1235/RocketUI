from app.app_context import services
from rocket import BuildContext, RLabel, Row, RSwitch, StatefulComponent, WidgetSpec


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
                    side="left",
                ),
                RSwitch(
                    text="Dark Mode",
                    checked=is_dark,
                    command=services.theme.toggle,
                    side="right",
                ),
            ],
        )


def Header(**kwargs) -> WidgetSpec:
    return WidgetSpec(widget_class=_Header, props=kwargs)
