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

def summary_columns(table_type="company"):
    if table_type == "person":
        return ["Country", "Source", "Individuals", "Companies", "Links"]
    else:
        return ["Country", "Source", "Companies", "Individuals", "Links"]

def source_summary(source_id, data, table_type="company"):
    if table_type == "person":
        return [data['country'], data['name'], data['person_count'], data['entity_count'], data['url']]
    else:
        return [data['country'], data['name'], data['entity_count'], data['person_count'], data['url']]

def construct_company_table(bods_data):
    table = []
    for record_id in bods_data['entities']:
        row = merge_records(record_id, bods_data['entities'][record_id])
        table.append(row)
    return table

def sort_table(table, column):
    """Sort table in reverse order on specified column"""
    return sorted(table, key=lambda row: row[column], reverse=True)

def construct_summary_table(bods_data, table_type="company"):
    """Construct summary table"""
    table = []
    for source_id in bods_data['sources']:
        row = source_summary(source_id, bods_data['sources'][source_id], table_type=table_type)
        table.append(row)
    table = sort_table(table, 2)
    return table
