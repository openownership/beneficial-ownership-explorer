import pycountry

from boexplorer.transforms.annotations import add_annotation
from boexplorer.transforms.utils import (
    current_date_iso,
    format_date,
    generate_statement_id,
)


def format_address(address_type, address, api):
    """Format address structure"""
    address_string = api.address_string(address)
    out = {'type': address_type,'address': address_string, 'country': api.address_country(address)}
    address_postcode = api.address_postcode(address)
    if address_postcode: out['postCode'] = address_postcode
    return out

def publication_details():
    """Generate publication details"""
    return {'publicationDate': current_date_iso(), # TODO: fix publication date
            'bodsVersion': "0.2",
            'license': "https://creativecommons.org/publicdomain/zero/1.0/",
            'publisher': {"name": "Open Ownership",
                          "url": "https://www.openownership.org"}}

def jurisdiction_name(jurisdiction_id):
    """Lookup jurisdiction name"""
    try:
        if "-" in jurisdiction_id:
            subdivision = pycountry.subdivisions.get(code=jurisdiction_id)
            name = f"{subdivision.name}, {subdivision.country.name}"
        else:
            name = pycountry.countries.get(alpha_2=jurisdiction_id).name
    except AttributeError:
        name = jurisdiction_id
    return name

def data_source(data, api):
    sourceType = api.source_type(data)
    sourceDescription = api.source_description
    return {'type': sourceType, 'description': sourceDescription}

def entity_id(item, api):
    lei = api.indentifier(item)
    last_update = api.update_date(item)
    return f"{lei}_{last_update}"

def transform_entity(data, api):
    """Transform into BODS v0.2 entity"""
    item = api.extract_entity_item(data)
    statementID = generate_statement_id(entity_id(data, api), 'entityStatement')
    statementType = 'entityStatement'
    statementDate = format_date(api.update_date(data))
    entityType = 'registeredEntity'
    name = api.entity_name(item)
    country = jurisdiction_name(api.jurisdiction(item))
    jurisdiction = {'name': country, 'code': api.jurisdiction(item)}
    identifiers = [{'id': api.indentifier(data),
                    'scheme': api.scheme,
                    'schemeName': api.scheme_name}]
    identifiers += api.additional_identifiers(item)
    registeredAddress = format_address('registered', api.registered_address(item), api)
    businessAddress = format_address('business', api.business_address(item), api)
    source = data_source(data, api)
    creation = api.creation_date(item)
    annotations = []
    annotation_text, annotation_pointer = api.entity_annotation(data)
    add_annotation(annotations, annotation_text, annotation_pointer)
    out = {'statementID': statementID,
           'statementType': statementType,
           'statementDate': statementDate,
           'entityType': entityType,
           'name': name,
           'incorporatedInJurisdiction': jurisdiction,
           'identifiers': identifiers,
           'addresses': [registeredAddress, businessAddress],
           'foundingDate': creation,
           'annotations': annotations,
           'publicationDetails': publication_details(),
           'source': source}
    return out

#def extract_relationships(data, api):
#    """Extract relationship links"""
#    item = api.extract_item(data)
#    api = api.extract_links(item)
#    for rel in item["relationships"]:
#        if rel.endswith("parent"):
#            rel_type = rel.split("-")[0]
#            if "reporting-exception" in item["relationships"][rel]["links"]:
#                rel_links[rel_type] = item["relationships"][rel]["links"]["reporting-exception"]
#            else:
#                rel_links[rel_type] = item["relationships"][rel]["links"]["relationship-record"]
#    return rel_links

def relationship_id(item, api):
    subject = api.subject_id(item)
    interested = api.interested_id(item)
    rel_type = api.relationship_type(item)
    last_update = api.update_date(item)
    return f"{subject}_{interested}_{rel_type}_{last_update}"

def transform_relationship(data, api):
    """Transform into BODS v0.2 relationship"""
    item = api.extract_relationship_item(data)
    statementID = generate_statement_id(relationship_id(data, api), 'ownershipOrControlStatement')
    statementType = 'ownershipOrControlStatement'
    statementDate = format_date(api.update_date(data))
    subjectDescribedByEntityStatement = calc_statement_id(api.subject_id(data), mapping)
    interestedPartyDescribedByEntityStatement = calc_statement_id(api.interested(data), mapping)
    interestType = 'other-influence-or-control'
    #interestLevel = interest_level(data['Relationship']['RelationshipType'], 'unknown')
    interestLevel = "unknown"
    interestStartDate = False
    interestDetails = api.interest_details(data)
    start_date = False
