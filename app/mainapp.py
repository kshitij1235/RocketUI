from app.Window_managment import *

#page files that contains everything 
from src.Homescreen import*


# this is the file where all the main application is strcutured 
# this is the only file which gets all the window acess 

class APP:
    def __init__(self) -> None:
        self.windows = windowManager().get_all_rwindows()  



    # make function in the class  where you club all the components  
    
    def homescreen(self):
        homescreen_ = homescreen(self.windows["main_window"])
        homescreen_.get_rocket_window()
        homescreen_.version_text()
        homescreen_.todo_list()

        self.windows["main_window"].mainloop()


