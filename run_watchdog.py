import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pipeline import run_full_pipeline

last_processed = {}

class ClashDataHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        # -------------------------
        # FILE TYPE FILTER
        # -------------------------
        if not (event.src_path.endswith(".csv") or event.src_path.endswith(".xml")):
            return

        current_time = time.time()

        # Debounce
        if event.src_path in last_processed:
            if current_time - last_processed[event.src_path] < 2:
                return

        last_processed[event.src_path] = current_time

        print(f"\n[WATCHDOG] New clash file detected: {event.src_path}")
        time.sleep(1)

        try:
            # Trigger full AI pipeline processing instead of just cleaning
            run_full_pipeline(event.src_path)
        except Exception as e:
            print(f"[WATCHDOG] Handler Error: {e}")


def start_watchdog(folderpath="data"):
    os.makedirs(folderpath, exist_ok=True)
    
    observer = Observer()
    observer.schedule(ClashDataHandler(), folderpath, recursive=True)
    observer.start()

    print(f"👁️ Watchdog active... Monitoring '{folderpath}' directory for new clash files.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Watchdog.")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    # Monitor the root 'data' directory for incoming naviswork XML/CSV exports
    start_watchdog("data")
