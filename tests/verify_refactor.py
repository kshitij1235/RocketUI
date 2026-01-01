import tkinter as tk
import unittest
from rocket.state import Signal
from rocket.component import StatefulComponent, StatelessComponent
from rocket.widget_core import WidgetSpec
from rocket.context import BuildContext
from rocket.renderer import Renderer
from rocket.theme.theme_manager import ThemeManager

# Mock classes
class MockWidget(tk.Frame):
    pass

class TestComponent(StatefulComponent):
    def __init__(self, signal, **kwargs):
        super().__init__(props=kwargs)
        self.register_signal(signal)
        self.build_count = 0

    def build(self, context: BuildContext):
        self.build_count += 1
        return WidgetSpec(MockWidget, props={"test": "val"})

class TestArchitecture(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.renderer = Renderer(self.root)
        self.theme = ThemeManager()
        self.context = BuildContext(self.root, self.theme)

    def tearDown(self):
        self.root.destroy()

    def test_build_purity_enforcement(self):
        """Verify that build runs and returns a spec."""
        sig = Signal(0)
        comp = TestComponent(sig)
        
        # Manually mount to test
        comp.mount(self.context)
        spec = comp.build(self.context)
        
        self.assertIsInstance(spec, WidgetSpec)
        self.assertEqual(comp.build_count, 1)

    def test_signal_propagation(self):
        """Verify that signal changes trigger update callback."""
        sig = Signal(0)
        comp = TestComponent(sig)
        comp.mount(self.context)
        
        updated = False
        def callback(c):
            nonlocal updated
            updated = True
        
        comp._request_update_callback = callback
        
        # Emit signal
        sig.set(1)
        
        self.assertTrue(updated, "Signal change should trigger update callback")

    def test_renderer_cycle(self):
        """Verify full render cycle."""
        spec = WidgetSpec(MockWidget, props={"bg": "red"})
        self.renderer.render(spec, self.context)
        
        # Check if widget created
        self.assertIsNotNone(spec._instance)
        self.assertIsInstance(spec._instance, MockWidget)

if __name__ == "__main__":
    unittest.main()
