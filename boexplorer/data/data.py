import csv
import json
from pathlib import Path


def load_data():
    data = []
    with open("boexplorer/data/2022-03-23_ra_list_v1.7.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data

def lookup_scheme(country, structure):
    directory = Path(f"boexplorer/data/org-id-lists/{country.lower()}")
    schemes = directory.glob("*.json")
    for filename in schemes:
        with open(filename) as json_file:
            data = json.load(json_file)
            if (data["confirmed"] and (data['coverage'] and country in data['coverage']) and
                (data['structure'] and structure in data['structure'])):
                return data['code'], data["name"]["en"]
    return None, None
