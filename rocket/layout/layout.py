from collections.abc import Sequence

from rocket.core.component import StatelessComponent
from rocket.core.context import BuildContext
from rocket.core.widget import WidgetSpec
from rocket.render.native import (
    NativeColumn,
    NativeRow,
    NativeScrollableColumn,
    NativeScrollableRow,
)

# Reuse a single empty tuple to avoid repeated allocations
_EMPTY_CHILDREN: tuple[WidgetSpec, ...] = ()


def _native_props(props: dict) -> dict:
    """Return props excluding structural keys."""
    return {k: v for k, v in props.items() if k != "children"}


class _Column(StatelessComponent):
    __slots__ = ()

    def build(self, context: BuildContext) -> WidgetSpec:
        children: Sequence[WidgetSpec] = self.props["children"]
        return WidgetSpec(
            widget_class=NativeColumn,
            props=_native_props(self.props),
            children=children,
        )


def Column(
    children: list[WidgetSpec],
    spacing: int = 0,
    **kwargs,
) -> WidgetSpec:
    """Vertical layout container."""
    return WidgetSpec(
        widget_class=_Column,
        props={
            "children": tuple(children),
            "spacing": spacing,
            **kwargs,
        },
    )


class _Row(StatelessComponent):
    __slots__ = ()

    def build(self, context: BuildContext) -> WidgetSpec:
        children: Sequence[WidgetSpec] = self.props["children"]
        return WidgetSpec(
            widget_class=NativeRow,
            props=_native_props(self.props),
            children=children,
        )


def Row(
    children: list[WidgetSpec],
    spacing: int = 0,
    **kwargs,
) -> WidgetSpec:
    """Horizontal layout container."""
    return WidgetSpec(
        widget_class=_Row,
        props={
            "children": tuple(children),
            "spacing": spacing,
            **kwargs,
        },
    )


class _ScrollableColumn(StatelessComponent):
    __slots__ = ()

    def build(self, context: BuildContext) -> WidgetSpec:
        children: Sequence[WidgetSpec] = self.props["children"]
        return WidgetSpec(
            widget_class=NativeScrollableColumn,
            props=_native_props(self.props),
            children=children,
        )


def ScrollableColumn(
    children: list[WidgetSpec],
    **kwargs,
) -> WidgetSpec:
    """Scrollable vertical layout container."""
    return WidgetSpec(
        widget_class=_ScrollableColumn,
        props={
            "children": tuple(children),
            **kwargs,
        },
    )


class _ScrollableRow(StatelessComponent):
    __slots__ = ()

    def build(self, context: BuildContext) -> WidgetSpec:
        children: Sequence[WidgetSpec] = self.props["children"]
        return WidgetSpec(
            widget_class=NativeScrollableRow,
            props=_native_props(self.props),
            children=children,
        )


def ScrollableRow(
    children: list[WidgetSpec],
    **kwargs,
) -> WidgetSpec:
    """Scrollable horizontal layout container."""
    return WidgetSpec(
        widget_class=_ScrollableRow,
        props={
            "children": tuple(children),
            **kwargs,
        },
    )
