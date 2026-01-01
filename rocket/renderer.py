import tkinter as tk
from typing import Any, Dict, List, Optional, Type
import logging

from rocket.widget_core import WidgetSpec, GenericWidget, LayoutWidget
from rocket.component import Component, ComponentLifecycleError
from rocket.context import BuildContext

logger = logging.getLogger("rocket.renderer")

class Renderer:
    """
    The engine that turns WidgetSpecs (VNodes) into real Tkinter widgets.
    Handles mount, unmount, update cycles, and reconciliation.
    """

    def __init__(self, root: tk.Widget):
        self.root = root
        self._tree: Optional[WidgetSpec] = None # The current VNode tree

    def render(self, spec: WidgetSpec, context: BuildContext):
        """
        Public entry point. Renders the spec into self.root.
        """
        logger.debug("Renderer: render cycle start")
        # In a real implementation this would be a full tree diff.
        # For this stage, we assume we are replacing the root content 
        # or updating it.
        
        # If we have a previous tree, we should diff it.
        if self._tree:
            self._update_node(self._tree, spec, self.root, context)
        else:
            self._mount_node(spec, self.root, context)
        
        self._tree = spec
        logger.debug("Renderer: render cycle complete")

    def _mount_node(self, spec: WidgetSpec, parent: tk.Widget, context: BuildContext):
        """
        Create a new widget instance from spec and append to parent.
        """
        logger.debug(f"Mounting {spec.widget_class.__name__}")
        
        # 1. Component (Custom Widget)
        if issubclass(spec.widget_class, Component):
            self._mount_component(spec, parent, context)
        
        # 2. Native Tkinter Widget (Leaf or Container)
        else:
            self._mount_native(spec, parent, context)

    def _mount_component(self, spec: WidgetSpec, parent: tk.Widget, context: BuildContext):
        # Create instance
        instance = spec.widget_class(props=spec.props)
        spec._instance = instance
        
        # Mount lifecycle
        instance.mount(context)
        
        # Hook for re-render
        # When component calls set_state/signal changes -> it calls _request_update_callback
        # We need to bind that.
        instance._request_update_callback = lambda c: self._schedule_component_update(spec, parent)

        # Build
        child_spec = instance.build(context)
        
        # If build returns None (empty component), we stop
        if child_spec:
            # Propagate layout properties from the Component spec to the Child spec
            # This ensures that if a Component is packed with side="bottom", its root widget respects it.
            layout_props = ["side", "expand", "fill", "padx", "pady"]
            for prop in layout_props:
                if prop in spec.props and prop not in child_spec.props:
                    child_spec.props[prop] = spec.props[prop]

            # We treat the component as a logical node, so we mount its result 
            # into the SAME parent.
            instance._rendered_child = child_spec
            self._mount_node(child_spec, parent, context)

    def _mount_native(self, spec: WidgetSpec, parent: tk.Widget, context: BuildContext):
        # Instantiate Tk widget
        props = spec.props.copy()
        
        # Filter layout props that native widgets don't understand
        should_expand = props.pop("expand", False)
        side_override = props.pop("side", None)
        
        widget = spec.widget_class(parent, **props)
        spec._instance = widget
        
        # Parent layout handling
        layout_strategy = getattr(parent, "layout_strategy", "column")
        parent_spacing = getattr(parent, "spacing", 0) # Read spacing from Native wrapper
        
        pack_kwargs = {}
        if layout_strategy == "row":
            pack_kwargs = {"side": "left", "fill": "y"}
            if parent_spacing > 0:
                 pack_kwargs["padx"] = (0, parent_spacing)
        else:
            pack_kwargs = {"side": "top", "fill": "x"}
            if parent_spacing > 0:
                 pack_kwargs["pady"] = (0, parent_spacing)
            
        # Allow prop override for 'side' (e.g. for footer)
        if side_override:
            pack_kwargs["side"] = side_override

        # Add expansion
        if should_expand:
            pack_kwargs["expand"] = True
            pack_kwargs["fill"] = "both"

        try:
            widget.pack(**pack_kwargs)
        except Exception as e:
            logger.warning(f"Could not pack widget {widget}: {e}")

        # Render children
        for child_spec in spec.children:
            self._mount_node(child_spec, widget, context)

    def _update_node(self, old_spec: WidgetSpec, new_spec: WidgetSpec, parent: tk.Widget, context: BuildContext):
        # 1. Type mismatch -> Replace
        if old_spec.widget_class != new_spec.widget_class:
            self._unmount_node(old_spec)
            self._mount_node(new_spec, parent, context)
            return

        # 2. Update props
        new_spec._instance = old_spec._instance
        instance = new_spec._instance
        
        # Component update
        if issubclass(new_spec.widget_class, Component):
            self._update_component(old_spec, new_spec, parent, context)
        else:
            self._update_native(old_spec, new_spec, context)

    def _update_component(self, old_spec: WidgetSpec, new_spec: WidgetSpec, parent: tk.Widget, context: BuildContext):
        comp = new_spec._instance
        # Lifecycle
        comp.on_update(old_spec.props)
        comp.props = new_spec.props
        comp.context = context 
        
        # Re-build
        ctx = context
        new_child_spec = comp.build(ctx)
        
        old_child_spec = getattr(comp, '_rendered_child', None)
        
        if old_child_spec and new_child_spec:
            self._update_node(old_child_spec, new_child_spec, parent, context)
        elif old_child_spec and not new_child_spec:
            self._unmount_node(old_child_spec)
        elif not old_child_spec and new_child_spec:
            self._mount_node(new_child_spec, parent, context)
            
        comp._rendered_child = new_child_spec

    def _update_native(self, old_spec: WidgetSpec, new_spec: WidgetSpec, context: BuildContext):
        widget = new_spec._instance
        # Diff props
        changes = {}
        for k, v in new_spec.props.items():
            if old_spec.props.get(k) != v:
                changes[k] = v
        
        if changes:
            try:
                widget.configure(**changes)
            except Exception as e:
                logger.error(f"Failed to update native widget {widget}: {e}")

        # Diff children
        self._diff_children(old_spec.children, new_spec.children, widget, context)

    def _diff_children(self, old_children: List[WidgetSpec], new_children: List[WidgetSpec], parent: tk.Widget, context: BuildContext):
        len_old = len(old_children)
        len_new = len(new_children)
        
        for i in range(min(len_old, len_new)):
            self._update_node(old_children[i], new_children[i], parent, context)
            
        if len_new > len_old:
            for i in range(len_old, len_new):
                self._mount_node(new_children[i], parent, context)
        elif len_old > len_new:
            for i in range(len_new, len_old):
                self._unmount_node(old_children[i])

    def _unmount_node(self, spec: WidgetSpec):
        if issubclass(spec.widget_class, Component):
            comp = spec._instance
            comp.unmount()
            if hasattr(comp, '_rendered_child') and comp._rendered_child:
                self._unmount_node(comp._rendered_child)
        else:
            # Native widget
            widget = spec._instance
            widget.destroy()
            for child in spec.children:
                self._unmount_node(child)

    def _schedule_component_update(self, spec: WidgetSpec, parent: tk.Widget):
        logger.debug(f"Scheduled update for {spec}")
        comp = spec._instance
        ctx = comp.context
        new_child_spec = comp.build(ctx)
        old_child_spec = getattr(comp, '_rendered_child', None)
        
        if old_child_spec and new_child_spec:
            self._update_node(old_child_spec, new_child_spec, parent, ctx)
        elif old_child_spec and not new_child_spec:
            self._unmount_node(old_child_spec)
        elif not old_child_spec and new_child_spec:
            self._mount_node(new_child_spec, parent, ctx)
            
        comp._rendered_child = new_child_spec
