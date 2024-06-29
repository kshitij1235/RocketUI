from tkinter import *
from vendor.json_extractor.extract_values import *

class Rocket:
    def __init__(self) -> None:
        self.window = Tk()
        self.data = json_extractor("Project.json").get_json()
    
    def get_window(self , 
                   title=json_extractor("Project.json").get_value("project_name") , 
                   icon=json_extractor("Project.json").get_value("icon")
                   )->Tk:
        '''
        create a window and return it 
        '''
        window = self.window
        photo = PhotoImage(file=icon)
        window.iconphoto(True, photo)
        window.title(title)
        return window