import json
import pandas as pd


def preprocessing(json_path: str):

    # Load JSON
    with open(json_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # 🔹 Required columns check
    required_columns = ["clash_id", "item1_type", "item2_type", "x", "y", "z"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # 🔹 Normalize types
    df["item1_type"] = df["item1_type"].astype(str).str.capitalize()
    df["item2_type"] = df["item2_type"].astype(str).str.capitalize()

    # 🔹 Clash pair
    df["clash_pair"] = df["item1_type"] + "-" + df["item2_type"]

    # 🔹 Priority
    def assign_priority(row):
        pair = row["clash_pair"].lower()

        if "pipe" in pair and "duct" in pair:
            return "high"
        elif "cabletray" in pair:
            return "medium"
        else:
            return "low"

    df["priority"] = df.apply(assign_priority, axis=1)

    # 🔹 Zone (safe + vectorized)
    df["x"] = pd.to_numeric(df["x"], errors="coerce")

    df["zone"] = pd.cut(
        df["x"],
        bins=[-float("inf"), 2000, 4000, float("inf")],
        labels=["zone_a", "zone_b", "zone_c"]
    )


    df.to_json("output.json", orient="records",indent=4)

    print(df.head())

    return df
