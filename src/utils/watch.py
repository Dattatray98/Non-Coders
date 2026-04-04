import time
from watchdog.observers import Observer  # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("File modified:", event.src_path)


class Watcher:
    def __init__(self, path):
        self.path = path
    def watchOn(self):
        observer = Observer()

        observer.schedule(MyHandler(), self.path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()


if __name__ == "__main__":
    path = "D:/My_Learning/Non-Coders/data"
    w = Watcher(path)
    w.watchOn()
