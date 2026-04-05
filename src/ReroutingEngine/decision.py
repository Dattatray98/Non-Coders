def choose_best_option(options, original_row):
    if not options:
        return None

    best = None
    min_score = float("inf")

    try:
        orig_x = float(original_row.get("x", 0))
        orig_y = float(original_row.get("y", 0))
        orig_z = float(original_row.get("z", 0))
    except (ValueError, TypeError):
        orig_x, orig_y, orig_z = 0.0, 0.0, 0.0

    for opt in options:
        if opt.get("action") == "no_action" or opt.get("action") == "no-action":
            continue

        x, y, z = opt.get("x", 0), opt.get("y", 0), opt.get("z", 0)

        # 3D Manhattan Distance represents material cost / travel distance
        distance = abs(x - orig_x) + abs(y - orig_y) + abs(z - orig_z)
        
        # Penalties: Vertical rerouting (Z) often requires added hangers/supports 
        # and creates gravity/pressure drops. So apply a 1.5x penalty to z-moves.
        vertical_penalty = abs(z - orig_z) * 1.5 
        
        score = distance + vertical_penalty

        if score < min_score:
            min_score = score
            best = opt

    # If no action was preferable or valid, return the fallback no_action
    if best is None and options:
        best = next((o for o in options if "no" in o.get("action", "")), None)

    return best