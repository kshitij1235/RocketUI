from app.homepages import Homepage
from rocket.runtime.window_manager import WindowManager


def main():
    window = WindowManager().get_runtime()
    page = Homepage(window)
    page.render()
    window.mainloop()


if __name__ == "__main__":
    main()
