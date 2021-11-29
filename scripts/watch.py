import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from build import build, delete_output
from lib.config import BASEDIR


class ChangeListener(FileSystemEventHandler):
    def __init__(self, path):
        super().__init__()

        self.path = path
        self.last_trigger = 0
        self.triggered = False
        self.observer = Observer()


    def __enter__(self):
        print("Turning on watchdog")
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()

        return self


    def __exit__(self, type, value, traceback):
        print("Turning off watchdog")
        self.observer.stop()
        self.observer.join()


    def was_modified(self, check_tick=0.1):
        now = time.time_ns()

        if self.triggered and now - self.last_trigger > check_tick:
            self.last_trigger = now
            self.triggered = False

            return True

        return False


    def on_modified(self, event):
        self.last_trigger = time.time_ns()
        self.triggered = True


def watch():
    with ChangeListener(BASEDIR) as listener:
        print("Initial building...")
        build(False)
        try:
            while True:
                if listener.was_modified():
                    print("Building...")
                    build(False)
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            delete_output()


if __name__ == "__main__":
    watch()
