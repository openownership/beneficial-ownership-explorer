import json
from neofuzz import char_ngram_process

def load_data(file_name):
    file_path = f"boexplorer/data/sources/{file_name}"
    with open(file_path) as json_file:
        return json.load(json_file)

def extract_name(names, item):
    company_id = item['ariregistri_kood']
    for bo in item['kasusaajad']:
        first_name = bo['eesnimi']
        last_name = bo['nimi']
        name = f"{first_name.lower()} {last_name.lower()}"
        if name in names:
            names[name].append(company_id)
        else:
            names[name] = [company_id]

def extract_names(data):
    names = {}
    for item in data:
        extract_name(names, item)
    return names

def search_data(names, data, name):
    if name.lower() in names:
        company_ids = names[name.lower()]
    else:
        company_ids = []
    matches = [item for item in data if item['ariregistri_kood'] in company_ids]
    return matches
