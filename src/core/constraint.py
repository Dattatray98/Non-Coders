def apply_constraints(options):
    valid = []

    for opt in options:
        if opt["z"] > 3000:
            continue
        if opt["x"] < 0:
            continue

        valid.append(opt)

    return valid