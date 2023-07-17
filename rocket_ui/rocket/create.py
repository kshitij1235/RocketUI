from tkinter import Tk , PhotoImage
class Rocket:
    def __init__(self,title="Rocket Window",icon = "resources/rocket_ui.png") -> None:
        
        
        self.window = Tk()
        self.title=title
        self.icon=icon

    
    def get_window(self)->Tk:
        '''
        create a window and return it 
        '''
        window = self.window
        photo = PhotoImage(file = self.icon)
        window.iconphoto(True, photo)
        window.title(self.title)
        return window