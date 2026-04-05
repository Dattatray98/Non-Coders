from src.ReroutingEngine.rules import Generaterules
from src.ReroutingEngine.constraint import apply_constraints
from src.ReroutingEngine.decision import choose_best_option

def run_engine(df):
    results = []
    print(f"🔧 Engine initialized: Processing {len(df)} clashes...")

    for _, row in df.iterrows():
        try:
            # Step 1: Generate hypotheses (math offsets)
            options = Generaterules(row)

            # Step 2: Validate against project-wide geometric constraints
            valid_options = apply_constraints(options, row)

            # Step 3: Select least expensive/disruptive option
            best = choose_best_option(valid_options, row)

            results.append({
                "clash_id": row.get("clash_id", "Unknown"),
                "action": best["action"] if best else "no_solution",
                "new_position": best if best else None
            })
            
        except Exception as e:
            print(f"⚠️ Engine Error on clash {row.get('clash_id', 'Unknown')}: {e}")
            results.append({
                "clash_id": row.get("clash_id", "Unknown"),
                "action": "error",
                "new_position": None
            })

    print("✅ Engine pipeline correctly finalized.")
    return results