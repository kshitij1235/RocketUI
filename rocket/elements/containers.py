from rocket.core.component import Component
from rocket.core.context import BuildContext
from rocket.core.widget import WidgetSpec
from rocket.render.native import NativeColumn


class _RDiv(Component):
    def build(self, context: BuildContext):
        return WidgetSpec(
            widget_class=NativeColumn, props=self.props, children=self.props["children"]
        )


def RDiv(children=None, **kwargs) -> WidgetSpec:
    return WidgetSpec(widget_class=_RDiv, props={"children": children or [], **kwargs})
