import logging
import tkinter as tk
from typing import Iterable, Optional

from rocket.core.component import Component
from rocket.core.context import BuildContext
from rocket.core.widget import WidgetSpec

logger = logging.getLogger("rocket.renderer")

_LAYOUT_PROPS = ("side", "expand", "fill", "padx", "pady")


class Renderer:
    """Turns WidgetSpec trees into concrete Tkinter widgets."""

    __slots__ = ("root", "_tree")

    def __init__(self, root: tk.Widget):
        self.root = root
        self._tree: Optional[WidgetSpec] = None

    def render(self, spec: WidgetSpec, context: BuildContext) -> None:
        logger.debug("Renderer: render cycle start")

        if self._tree is None:
            self._mount_node(spec, self.root, context)
        else:
            self._update_node(self._tree, spec, self.root, context)

        self._tree = spec
        logger.debug("Renderer: render cycle complete")

    def _mount_node(
        self,
        spec: WidgetSpec,
        parent: tk.Widget,
        context: BuildContext,
    ) -> None:
        logger.debug("Mounting %s", spec.widget_class.__name__)

        if issubclass(spec.widget_class, Component):
            self._mount_component(spec, parent, context)
        else:
            self._mount_native(spec, parent, context)

    def _mount_component(
        self,
        spec: WidgetSpec,
        parent: tk.Widget,
        context: BuildContext,
    ) -> None:
        component = spec.widget_class(props=spec.props)
        spec._instance = component

        component.mount(context)
        component._request_update_callback = lambda _: self._schedule_component_update(
            spec, parent
        )

        child_spec = component.build(context)
        if child_spec is None:
            return

        self._inherit_layout_props(spec, child_spec)
        component._rendered_child = child_spec
        self._mount_node(child_spec, parent, context)

    def _mount_native(
        self,
        spec: WidgetSpec,
        parent: tk.Widget,
        context: BuildContext,
    ) -> None:
        props = spec.props
        expand = props.get("expand", False)
        side_override = props.get("side")

        native_props = {k: v for k, v in props.items() if k not in ("expand", "side")}

        widget = spec.widget_class(parent, **native_props)
        spec._instance = widget

        pack_kwargs = self._compute_pack_kwargs(
            parent=parent,
            expand=expand,
            side_override=side_override,
        )

        try:
            widget.pack(**pack_kwargs)
        except Exception as exc:
            logger.warning("Could not pack widget %s: %s", widget, exc)

        for child in spec.children:
            self._mount_node(child, widget, context)

    def _update_node(
        self,
        old: WidgetSpec,
        new: WidgetSpec,
        parent: tk.Widget,
        context: BuildContext,
    ) -> None:
        if old.widget_class is not new.widget_class:
            self._unmount_node(old)
            self._mount_node(new, parent, context)
            return

        new._instance = old._instance

        if issubclass(new.widget_class, Component):
            self._update_component(old, new, parent, context)
        else:
            self._update_native(old, new, context)

    def _update_component(
        self,
        old: WidgetSpec,
        new: WidgetSpec,
        parent: tk.Widget,
        context: BuildContext,
    ) -> None:
        component = new._instance

        component.on_update(old.props)
        component.props = new.props
        component.context = context

        new_child = component.build(context)
        old_child = getattr(component, "_rendered_child", None)

        if old_child and new_child:
            self._update_node(old_child, new_child, parent, context)
        elif old_child:
            self._unmount_node(old_child)
        elif new_child:
            self._mount_node(new_child, parent, context)

        component._rendered_child = new_child

    def _update_native(
        self,
        old: WidgetSpec,
        new: WidgetSpec,
        context: BuildContext,
    ) -> None:
        widget = new._instance
        old_props = old.props
        new_props = new.props

        changes = {k: v for k, v in new_props.items() if old_props.get(k) != v}

        if changes:
            try:
                widget.configure(**changes)
            except Exception as exc:
                logger.error("Failed to update widget %s: %s", widget, exc)

        self._diff_children(old.children, new.children, widget, context)

    def _diff_children(
        self,
        old_children: Iterable[WidgetSpec],
        new_children: Iterable[WidgetSpec],
        parent: tk.Widget,
        context: BuildContext,
    ) -> None:
        old_list = list(old_children)
        new_list = list(new_children)

        for old, new in zip(old_list, new_list):
            self._update_node(old, new, parent, context)

        if len(new_list) > len(old_list):
            for child in new_list[len(old_list) :]:
                self._mount_node(child, parent, context)
        elif len(old_list) > len(new_list):
            for child in old_list[len(new_list) :]:
                self._unmount_node(child)

    def _unmount_node(self, spec: WidgetSpec) -> None:
        if issubclass(spec.widget_class, Component):
            component = spec._instance
            component.unmount()
            child = getattr(component, "_rendered_child", None)
            if child:
                self._unmount_node(child)
            return

        widget = spec._instance
        widget.destroy()

        for child in spec.children:
            self._unmount_node(child)

    @staticmethod
    def _inherit_layout_props(parent: WidgetSpec, child: WidgetSpec) -> None:
        for prop in _LAYOUT_PROPS:
            if prop in parent.props and prop not in child.props:
                child.props[prop] = parent.props[prop]

    @staticmethod
    def _compute_pack_kwargs(
        parent: tk.Widget,
        *,
        expand: bool,
        side_override: Optional[str],
    ) -> dict:
        layout = getattr(parent, "layout_strategy", "column")
        spacing = getattr(parent, "spacing", 0)

        if layout == "row":
            kwargs = {"side": "left", "fill": "y"}
            if spacing:
                kwargs["padx"] = (0, spacing)
        else:
            kwargs = {"side": "top", "fill": "x"}
            if spacing:
                kwargs["pady"] = (0, spacing)

        if side_override:
            kwargs["side"] = side_override

        if expand:
            kwargs["expand"] = True
            kwargs["fill"] = "both"

        return kwargs

    def _schedule_component_update(
        self,
        spec: WidgetSpec,
        parent: tk.Widget,
    ) -> None:
        logger.debug("Scheduled update for %s", spec)

        component = spec._instance
        context = component.context

        new_child = component.build(context)
        old_child = getattr(component, "_rendered_child", None)

        if old_child and new_child:
            self._update_node(old_child, new_child, parent, context)
        elif old_child:
            self._unmount_node(old_child)
        elif new_child:
            self._mount_node(new_child, parent, context)

        component._rendered_child = new_child
