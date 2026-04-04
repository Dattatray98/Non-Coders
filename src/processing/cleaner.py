import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# CLEANER FUNCTION
def cleaner(file_path):
    print("Cleaning file:", file_path)

    try:
        df = pd.read_csv(file_path)

        # Normalize column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Column mapping
        column_map = {
            "clash_id": ["clash_id", "clashname", "clash_name"],
            "item1_id": ["item1_id", "item_1_id", "element1_id"],
            "item1_type": ["item1_type", "item_1_type", "element1_type"],
            "item2_id": ["item2_id", "item_2_id", "element2_id"],
            "item2_type": ["item2_type", "item_2_type", "element2_type"],
            "x": ["x"],
            "y": ["y"],
            "z": ["z"]
        }

        # Resolve columns
        resolved_cols = {}
        for key, options in column_map.items():
            for opt in options:
                if opt in df.columns:
                    resolved_cols[key] = opt
                    break

        # Check required fields
        required_keys = ["clash_id", "item1_id", "item2_id", "x", "y", "z"]
        for key in required_keys:
            if key not in resolved_cols:
                raise ValueError(f"Missing required column: {key}")

        # Select + rename
        cdf = df[[resolved_cols[k] for k in resolved_cols]].copy()
        cdf.columns = list(resolved_cols.keys())

        # Drop invalid rows
        cdf.dropna(subset=["clash_id", "item1_id", "item2_id"], inplace=True)

        # Convert coordinates
        for coord in ["x", "y", "z"]:
            cdf[coord] = pd.to_numeric(cdf[coord], errors="coerce")

        cdf.dropna(subset=["x", "y", "z"], inplace=True)

        # Normalize types
        if "item1_type" in cdf.columns:
            cdf["item1_type"] = cdf["item1_type"].astype(str).str.capitalize()

        if "item2_type" in cdf.columns:
            cdf["item2_type"] = cdf["item2_type"].astype(str).str.capitalize()

        # Output folder
        os.makedirs("output", exist_ok=True)

        # Unique file naming
        filename = os.path.basename(file_path).replace(".csv", "")
        json_path = f"output/{filename}.json"
        csv_path = f"output/{filename}.csv"

        # Save
        cdf.to_json(json_path, orient="records", indent=4)
        cdf.to_csv(csv_path, index=False)

        print("Saved:", json_path, "and", csv_path)

        return cdf

    except Exception as e:
        print("Cleaner Error:", e)


# WATCHDOG CLASS
last_processed = {}


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        if not event.src_path.endswith(".csv"):
            return

        current_time = time.time()

        # Debounce (avoid duplicate triggers)
        if event.src_path in last_processed:
            if current_time - last_processed[event.src_path] < 2:
                return

        last_processed[event.src_path] = current_time

        print("File detected:", event.src_path)

        time.sleep(1)  # wait for file write completion

        try:
            cleaner(event.src_path)
        except Exception as e:
            print("Handler Error:", e)


# WATCHER CLASS
class Watcher:
    def __init__(self, folderpath):
        self.folderpath = folderpath

    def watch(self):
        observer = Observer()
        observer.schedule(MyHandler(), self.folderpath, recursive=True)
        observer.start()

        print("Watching folder:", self.folderpath)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
