import functools
import sys
import threading
import traceback


def threaded(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def run():
            try:
                func(*args, **kwargs)
            except Exception:
                traceback.print_exc(file=sys.stderr)

        thread = threading.Thread(
            target=run, daemon=True, name=f"{func.__name__}-thread"
        )
        thread.start()
        return thread

    return wrapper
