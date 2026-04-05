def choose_best_option(options, original_row):
    if not options:
        return None

    best = None
    min_distance = float("inf")

    for opt in options:
        dist = abs(opt["x"] - original_row["x"]) + \
               abs(opt["z"] - original_row["z"])

        if dist < min_distance:
            min_distance = dist
            best = opt

    return best