from app.homepages import Homepage
from rocket.runtime.window_manager import WindowManager


def main():
    windows = WindowManager()
    main_window = windows.get("main_window")
    page = Homepage(main_window)
    page.render()
    main_window.mainloop()


if __name__ == "__main__":
    main()
