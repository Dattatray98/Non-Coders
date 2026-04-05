def Generaterules(row):
    pair = row["clash_pair"].lower()

    options = []
    if "pipe" in pair and "duct" in pair:
        options.append({
            "action":"move-up",
            "x":row["x"],
            "y":row["y"],
            "z":row["z"] + 100
        })

        options.append({
            "action":"move-right",
            "x":row["x"] + 100,
            "y":row["y"],
            "z":row["z"]
        })

    elif "pipe" in pair and "cabletray" in pair:
        options.append({
            "action":"move-right",
            "x":row["x"] + 100,
            "y":row["y"],
            "z":row["z"]
        })

    
    else:
        options.append({
            "action": "no-action",
            "x":row["x"],
            "y":row["y"],
            "z":row["z"]
        })
    

    return options