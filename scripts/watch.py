import time
from datetime import datetime

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from build import build_test, get_config


class EventHandler(FileSystemEventHandler):
  def __init__(self):
      super().__init__()

      self.last_trigger = 0
      self.triggered = False

  def on_modified(self, event):
        self.last_trigger = time.time_ns()
        self.triggered = True


if __name__ == "__main__":
    path = "./src"
    config = get_config()
    event_handler = EventHandler()
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    build_test(config, False)

    try:
        while True:
            now = time.time_ns()

            if event_handler.triggered and now - event_handler.last_trigger > 50:
                event_handler.last_trigger = now
                event_handler.triggered = False
                
                build_test(config, False)

            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
