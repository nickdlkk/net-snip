import threading
import time

from pywebio.session import register_thread


class Debounce:
    """
    连续输入防抖,合并保存
    """
    def __init__(self, interval):
        self.interval = interval
        self.timer = None
        self.args = None
        self.kwargs = None

    def debounce(self, func):
        def wrapper(*args, **kwargs):
            def thread_func():
                time.sleep(self.interval)
                if not self.timer.is_alive():
                    # Timer has been cancelled.
                    return
                func(*self.args, **self.kwargs)

            if self.timer is not None:
                self.timer.cancel()

            self.args = args
            self.kwargs = kwargs
            self.timer = threading.Timer(self.interval, thread_func)
            register_thread(self.timer)
            self.timer.start()

        return wrapper

    def cancel(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
