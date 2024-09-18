def not_none(value):
    return value if not value is None else ""

def list_all(records):
    if len(records) == 1:
        return records[0]["source"]["description"]
    else:
        return ", ".join([record["source"]["description"] for record in records])

def merge_records(record_id, records):
    name = records[0]["recordDetails"]["name"].title()
    jurisdiction = records[0]["recordDetails"]["jurisdiction"]["name"]
    founding_date = records[0]["recordDetails"]["foundingDate"]
    return [name, jurisdiction, record_id, not_none(founding_date), list_all(records)]

def construct_table(bods_data):
    table = []
    for record_id in bods_data['entities']:
        row = merge_records(record_id, bods_data['entities'][record_id])
        table.append(row)
    return table
