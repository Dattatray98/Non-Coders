import time
import os
import pandas as pd
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def _get_element_id(clashobj):
    for attr in clashobj.findall('.//objectattribute'):
        name = attr.findtext('name')
        if name == 'Element ID':
            return attr.findtext('value')
    return "Unknown"

def _get_item_name(clashobj):
    for tag in clashobj.findall('.//smarttag'):
        name = tag.findtext('name')
        if name == 'Item Name':
            val = tag.findtext('value') or ''
            val_lower = val.lower()
            if 'pipe' in val_lower or 'water' in val_lower:
                return 'Pipe'
            elif 'duct' in val_lower:
                return 'Duct'
            elif 'tray' in val_lower:
                return 'CableTray'
            else:
                return val
    return "Unknown"

def parse_navisworks_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    data = []
    
    for clashtest in root.iter('clashtest'):
        clash_type = (clashtest.attrib.get('test_type') or 'Hard').capitalize()
        
        for result in clashtest.iter('clashresult'):
            clash_id = result.attrib.get('name')
            
            distance = result.attrib.get('distance', '0')
            severity = "Medium"
            try:
                dist_val = abs(float(distance))
                if dist_val > 0.05:
                    severity = "High"
                elif dist_val < 0.01:
                    severity = "Low"
            except:
                pass
            
            x, y, z = None, None, None
            clashpoint = result.find('clashpoint')
            if clashpoint is not None:
                pos = clashpoint.find('pos3f')
                if pos is not None:
                    x = pos.attrib.get('x')
                    y = pos.attrib.get('y')
                    z = pos.attrib.get('z')
            
            objects = list(result.find('clashobjects') or [])
            item1_id, item1_type = "Unknown", "Unknown"
            item2_id, item2_type = "Unknown", "Unknown"
            
            if len(objects) > 0:
                item1_id = _get_element_id(objects[0])
                item1_type = _get_item_name(objects[0])
            if len(objects) > 1:
                item2_id = _get_element_id(objects[1])
                item2_type = _get_item_name(objects[1])
                
            data.append({
                "clash_id": clash_id,
                "item1_id": item1_id,
                "item1_type": item1_type,
                "item2_id": item2_id,
                "item2_type": item2_type,
                "clash_type": clash_type,
                "severity": severity,
                "x": x,
                "y": y,
                "z": z
            })
            
    return pd.DataFrame(data)

# CLEANER FUNCTION
def cleaner(file_path):
    print("Cleaning file:", file_path)

    try:
        # -------------------------
        # 1. READ FILE (CSV or XML)
        # -------------------------
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith(".xml"):
            try:
                df = parse_navisworks_xml(file_path)
            except Exception as e:
                print(f"Failed to parse XML: {e}")
                return

        else:
            print("Unsupported file format")
            return

        # -------------------------
        # 2. NORMALIZE COLUMNS
        # -------------------------
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        column_map = {
            "clash_id": ["clash_id", "clashname", "clash_name"],
            "item1_id": ["item1_id", "item_1_id", "element1_id"],
            "item1_type": ["item1_type", "item_1_type", "element1_type"],
            "item2_id": ["item2_id", "item_2_id", "element2_id"],
            "item2_type": ["item2_type", "item_2_type", "element2_type"],
            "clash_type": ["clash_type"],
            "severity": ["severity"],
            "x": ["x"],
            "y": ["y"],
            "z": ["z"],
        }

        resolved_cols = {}

        for key, options in column_map.items():
            for opt in options:
                if opt in df.columns:
                    resolved_cols[key] = opt
                    break

        # -------------------------
        # 3. VALIDATION
        # -------------------------
        required_keys = ["clash_id", "item1_id", "item2_id", "x", "y", "z"]
        for key in required_keys:
            if key not in resolved_cols:
                raise ValueError(f"Missing required column: {key}")

        # -------------------------
        # 4. CLEAN DATA
        # -------------------------
        cdf = df[[resolved_cols[k] for k in resolved_cols]].copy()
        cdf.columns = list(resolved_cols.keys())

        cdf.dropna(subset=["clash_id", "item1_id", "item2_id"], inplace=True)

        for coord in ["x", "y", "z"]:
            cdf[coord] = pd.to_numeric(cdf[coord], errors="coerce")

        cdf.dropna(subset=["x", "y", "z"], inplace=True)

        if "item1_type" in cdf.columns:
            cdf["item1_type"] = cdf["item1_type"].astype(str).str.capitalize()

        if "item2_type" in cdf.columns:
            cdf["item2_type"] = cdf["item2_type"].astype(str).str.capitalize()

        # -------------------------
        # 5. SAVE OUTPUT
        # -------------------------
        os.makedirs("output", exist_ok=True)

        filename = os.path.splitext(os.path.basename(file_path))[0]

        json_path = f"output/{filename}.json"
        csv_path = f"output/{filename}.csv"

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

        # -------------------------
        # 6. FILE TYPE FILTER
        # -------------------------
        if not (event.src_path.endswith(".csv") or event.src_path.endswith(".xml")):
            return

        current_time = time.time()

        # Debounce
        if event.src_path in last_processed:
            if current_time - last_processed[event.src_path] < 2:
                return

        last_processed[event.src_path] = current_time

        print("File detected:", event.src_path)

        time.sleep(1)

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