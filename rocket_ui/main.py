from app.main import * 

if __name__=='__main__':

    window = app()

    windows = window.get_rocket_window()
    windows = window.version_text()
    windows = window.todo_list()    
    windows.mainloop()