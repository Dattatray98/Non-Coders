def Generaterules(row):
    pair = row.get("clash_pair", "").lower()

    options = []
    
    # Base coordinates (safe float conversion)
    try:
        x = float(row.get("x", 0))
        y = float(row.get("y", 0))
        z = float(row.get("z", 0))
    except (ValueError, TypeError):
        x, y, z = 0.0, 0.0, 0.0

    # Auto-detect units: if coordinates are very small, it's likely exported in Meters
    unit_scale = 0.001 if (abs(x) < 200 and abs(y) < 200 and abs(z) < 200) else 1.0

    # Dynamic Scaling based on Severity
    # This solves the issue of sometimes needing a large jump vs a slight nudge
    severity = row.get("severity", "Medium").lower()
    
    if severity == "high":
        offset_multiplier = 2.5
    elif severity == "low":
        offset_multiplier = 0.5 
    else:
        offset_multiplier = 1.0

    # Define standard offset magnitudes scaled by the multiplier and unit scale
    VERTICAL_OFFSET = 100.0 * offset_multiplier * unit_scale
    HORIZONTAL_OFFSET = 100.0 * offset_multiplier * unit_scale

    if "pipe" in pair and "duct" in pair:
        # Best Practice: Pipes are more flexible and easier to reroute than bulky ducts.
        # Prefer moving the pipe vertically or horizontally around the duct.
        options.append({"action": "move_up", "x": x, "y": y, "z": z + VERTICAL_OFFSET})
        options.append({"action": "move_down", "x": x, "y": y, "z": z - VERTICAL_OFFSET})
        options.append({"action": "move_right", "x": x + HORIZONTAL_OFFSET, "y": y, "z": z})

    elif "pipe" in pair and "cabletray" in pair:
        # Best Practice: Pipes should generally NOT run directly above cable trays to avoid water drip hazards on electricals.
        # Prefer routing pipes below or to the sides of cable trays.
        options.append({"action": "move_right", "x": x + HORIZONTAL_OFFSET, "y": y, "z": z})
        options.append({"action": "move_left", "x": x - HORIZONTAL_OFFSET, "y": y, "z": z})
        options.append({"action": "move_down", "x": x, "y": y, "z": z - VERTICAL_OFFSET})

    elif "duct" in pair and "cabletray" in pair:
        # Ducts are massive; move the cable tray if possible, usually vertical separation.
        options.append({"action": "move_up", "x": x, "y": y, "z": z + VERTICAL_OFFSET})
        options.append({"action": "move_down", "x": x, "y": y, "z": z - VERTICAL_OFFSET})

    elif "pipe" in pair and "pipe" in pair:
        # Pipe vs Pipe: Easy to introduce a standard elevation difference.
        options.append({"action": "move_up", "x": x, "y": y, "z": z + VERTICAL_OFFSET})
        options.append({"action": "move_down", "x": x, "y": y, "z": z - VERTICAL_OFFSET})

    elif "duct" in pair and "duct" in pair:
        # Duct vs Duct: Avoid vertical crossing if ceiling void is tight; try side-by-side or up.
        options.append({"action": "move_up", "x": x, "y": y, "z": z + VERTICAL_OFFSET})
        options.append({"action": "move_right", "x": x + HORIZONTAL_OFFSET, "y": y, "z": z})

    elif "pipe" in pair:
        # Generic fallback for Pipe vs something unknown (e.g., Pipe vs Standard)
        options.append({"action": "move_right", "x": x + HORIZONTAL_OFFSET, "y": y, "z": z})
        options.append({"action": "move_up", "x": x, "y": y, "z": z + VERTICAL_OFFSET})

    elif "duct" in pair:
        # Generic fallback for Duct vs something unknown
        options.append({"action": "move_up", "x": x, "y": y, "z": z + VERTICAL_OFFSET})

    else:
        # Fallback when both types are completely unknown
        options.append({
            "action": "no_action",
            "x": x, "y": y, "z": z
        })

    return options