def apply_constraints(options, original_row):
    valid = []
    
    try:
        orig_x = float(original_row.get("x", 0))
        orig_y = float(original_row.get("y", 0))
        orig_z = float(original_row.get("z", 0))
    except (ValueError, TypeError):
        orig_x, orig_y, orig_z = 0.0, 0.0, 0.0
        
    unit_scale = 0.001 if (abs(orig_x) < 200 and abs(orig_y) < 200 and abs(orig_z) < 200) else 1.0

    # Maximum safe allowable deviation from original position to prevent architectural overlap
    MAX_DEVIATION_Z = 600.0 * unit_scale
    MAX_DEVIATION_XY = 1500.0 * unit_scale

    for opt in options:
        if opt.get("action") == "no_action" or "no" in opt.get("action", ""):
            valid.append(opt)
            continue
            
        z = opt.get("z", 0)
        x = opt.get("x", 0)
        y = opt.get("y", 0)

        # Violation: Element moves too far vertically from its origin
        if abs(z - orig_z) > MAX_DEVIATION_Z:
            continue
            
        # Violation: Element moves too far horizontally
        if abs(x - orig_x) > MAX_DEVIATION_XY or abs(y - orig_y) > MAX_DEVIATION_XY:
            continue

        valid.append(opt)

    return valid