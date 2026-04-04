import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd


def cleaner(file_path):
    print("Cleaning file:", file_path)

    df = pd.read_csv(file_path)

    # basic cleaning
    df.dropna(inplace=True)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    print(df.head())


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".csv"):
            print("File detected:", event.src_path)

            time.sleep(1)  # wait for file to finish writing
            cleaner(event.src_path)


class Watcher:
    def __init__(self, folderpath):
        self.folderpath = folderpath

    def watch(self):
        observer = Observer()
        observer.schedule(MyHandler(), self.folderpath, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()