from vendor.Rocket.BaseImports import *
from vendor.Rocket.Log import *

# This file make sure the work of how render is 
# going to take palce in the rocket window 
# It contains all the basic function that help 
# rocket window to render components on the screen 

def get_all_widgets(root : Tk)->list[Tk]:
    """
    It return you all the list of componets in the root 
    """
    widgets = root.winfo_children()
    for widget in widgets:
        if widget.winfo_children():
            widgets.extend(widget.winfo_children())
    return widgets

def rerender(root : Tk, new_page)->None:
    """
    It destorys all the components on the root and 
    renders new_page components 
    new_page should be written in function
    """
    log("re-rendered root")
    for widget in get_all_widgets(root):
        widget.destroy()
    new_page(root)
