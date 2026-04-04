import csv
import json


def parse_csv():

    csv_path = "D:/My_Learning/Non-Coders/data/meshdata.csv"
    json_path = "D:/My_Learning/Non-Coders/data/data.json"

    data = []

    with open(csv_path, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

    with open(json_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

    return data


# Run function
if __name__ == "__main__":
    result = parse_csv()
    print("Total rows:", len(result))