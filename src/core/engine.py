from src.core.rules import Generaterules
from src.core.constraint import apply_constraints
from src.core.decision import choose_best_option


def run_engine(df):
    results = []

    for _, row in df.iterrows():

        # Step 1: generate options
        options = Generaterules(row)

        # Step 2: filter constraints
        valid_options = apply_constraints(options)

        # Step 3: choose best
        best = choose_best_option(valid_options, row)

        result = {
            "clash_id": row["clash_id"],
            "action": best["action"] if best else "no_solution",
            "new_position": best if best else None
        }

        results.append(result)

    return results