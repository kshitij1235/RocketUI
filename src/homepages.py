from src.components.homepage_components import *
from src.components.todo_comp import *

def homepage(window): 
    rocket_image(window)
    version_text(window)
    todo_list(window,"rocketdb","tasks")
    next_page_button(window)