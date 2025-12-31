from app.homepages import Homepage
from rocket.runtime.window_manager import WindowManager


def main():
    windows = WindowManager()
    main_window = windows.get("main_window")
    Homepage(main_window).render()
    main_window.mainloop()


if __name__ == "__main__":
    main()
