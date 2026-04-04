import csv


def parcer_csv():
    with open("D:/My_Learning/Non-Coders/data/meshdata.csv", mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            print(row)

    return reader