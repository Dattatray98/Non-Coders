import os
import json
from src.processing.cleaner import cleaner
from src.preprocessing.data_preprocessing import preprocessing
from src.ReroutingEngine.engine import run_engine


def safe_get_row(df, clash_id):
    row = df[df["clash_id"] == clash_id]
    if row.empty:
        return None
    return row.iloc[0]


def run_full_pipeline(input_file: str):

    print(f"🚀 Starting Pipeline for {input_file}...")

    # --- STAGE 1: CLEAN ---
    cleaned_df = cleaner(input_file)
    if cleaned_df is None or cleaned_df.empty:
        print("❌ Cleaning failed or empty data.")
        return None

    filename = os.path.splitext(os.path.basename(input_file))[0]
    cleaned_json_path = f"output/{filename}.json"

    # --- STAGE 2: PREPROCESS ---
    print(f"🔄 Preprocessing {cleaned_json_path}...")
    preprocessed_df = preprocessing(cleaned_json_path)

    if preprocessed_df is None or preprocessed_df.empty:
        print("❌ Preprocessing failed.")
        return None

    # --- STAGE 3: ENGINE ---
    print("🧠 Running AI Decision Engine...")
    results = run_engine(preprocessed_df)

    if not results:
        print("❌ No results from engine.")
        return None

    # --- FORMAT ---
    formatted_results = []

    for item in results:
        clash_id = item.get("clash_id")
        action = item.get("action", "no_action")
        new_pos = item.get("new_position")

        row = safe_get_row(preprocessed_df, clash_id)
        if row is None:
            print(f"⚠️ Skipping missing clash_id: {clash_id}")
            continue

        orig_x, orig_y, orig_z = row["x"], row["y"], row["z"]

        if new_pos:
            nx = float(new_pos.get("x", orig_x))
            ny = float(new_pos.get("y", orig_y))
            nz = float(new_pos.get("z", orig_z))
        else:
            nx, ny, nz = orig_x, orig_y, orig_z

        dx, dy, dz = nx - orig_x, ny - orig_y, nz - orig_z

        formatted_results.append({
            "clash_id": clash_id,
            "element_id": str(row["item1_id"])
                .replace("P-", "")
                .replace("D-", "")
                .replace("CT-", ""),
            "action": action.replace("-", "_"),
            "new_position": {"x": nx, "y": ny, "z": nz},
            "offsets": {"x": dx, "y": dy, "z": dz},
        })

    # --- LOCAL SAVE ---
    os.makedirs("output", exist_ok=True)
    local_path = os.path.join("output", "ai_reroutes.json")

    try:
        with open(local_path, "w") as f:
            json.dump(formatted_results, f, indent=4)
        print(f"💾 Saved locally at {local_path}")
    except Exception as e:
        print("❌ Local save failed:", e)
        return None

    # # --- NETWORK SAVE (ROBUST VERSION) ---
    # network_path = r"\\192.168.12.90\RevitShared"
    # network_file = os.path.join(network_path, "ai_reroutes.json")

    # print("📡 Attempting network write...")

    # try:
    #     # Check if path exists
    #     if not os.path.exists(network_path):
    #         raise Exception("Network path not accessible")

    #     # Try writing
    #     with open(network_file, "w") as f:
    #         json.dump(formatted_results, f, indent=4)

    #     print("✅ Successfully written to network drive!")

    # except PermissionError:
    #     print("❌ Permission denied on network path.")

    print("✅ Pipeline complete!")
    return formatted_results


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file = os.path.join(base_dir, "data", "data.csv")

    if os.path.exists(test_file):
        print(f"--- RUNNING TEST FOR {test_file} ---")
        run_full_pipeline(test_file)
    else:
        print(f"⚠️ Test file not found: {test_file}")