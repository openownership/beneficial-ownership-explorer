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
    if address_string:
        out = {'type': address_type,'address': address_string, 'country': api.address_country(address)}
        address_postcode = api.address_postcode(address)
        if address_postcode: out['postCode'] = address_postcode
        return out
    else:
        return None

def format_name(name_type, name_data, api):
    """Format name structure"""
    full_name, famliy_name, first_name, patronymic_name = api.person_name_components(name_data)
    name = {'type': name_type, 'fullName': full_name, 'familyName': famliy_name,
           'givenName': first_name, 'patronymicName': patronymic_name}
    return name

def publication_details():
    """Generate publication details"""
    return {'publicationDate': current_date_iso(), # TODO: fix publication date
            'bodsVersion': "0.4",
            'license': "https://creativecommons.org/publicdomain/zero/1.0/",
            'publisher': {"name": "Open Ownership",
                          "url": "https://www.openownership.org"}}

def jurisdiction_name(jurisdiction_id):
    """Lookup jurisdiction name"""
    try:
        if "-" in jurisdiction_id:
            subdivision = pycountry.subdivisions.get(code=jurisdiction_id)
            name = f"{subdivision.name}, {subdivision.country.name}"
        elif "UK" in jurisdiction_id:
            name = "United Kingdom"
        else:
            name = pycountry.countries.get(alpha_2=jurisdiction_id).name
    except AttributeError:
        name = jurisdiction_id
    return name

def data_source(data, api):
    """Build data source"""
    sourceType = api.source_type(data)
    sourceDescription = api.source_description
    return {'type': sourceType, 'description': sourceDescription}

def entity_id(item, api):
    """Identifier for entity"""
    lei = api.identifier(item)
    last_update = api.update_date(item)
    return f"{lei}_{last_update}"

def build_addresses(registered, business):
    addresses = []
    if registered: addresses.append(registered)
    if business: addresses.append(business)
    return addresses

def transform_entity(data, api):
    """Transform into BODS v0.4 entity"""
    item = api.extract_entity_item(data)
    statementID = generate_statement_id(entity_id(data, api), 'entityStatement')
    recordType = 'entity'
    recordID = api.record_id(data)
    statementDate = format_date(api.update_date(data))
    entityType = 'registeredEntity'
    name = api.entity_name(item)
    country = jurisdiction_name(api.jurisdiction(item))
    jurisdiction = {'name': country, 'code': api.jurisdiction(item)}
    identifiers = [{'id': api.identifier(data),
                    'scheme': api.scheme,
                    'schemeName': api.scheme_name}]
    identifiers += api.additional_identifiers(item)
    registered = api.registered_address(item)
    if registered:
        registeredAddress = format_address('registered', registered, api)
    else:
        registeredAddress = None
    business = api.business_address(item)
    if business:
        businessAddress = format_address('business', api.business_address(item), api)
    else:
        businessAddress = None
    source = data_source(data, api)
    creation = api.creation_date(item)
    annotations = []
    annotation_text, annotation_pointer = api.entity_annotation(data)
    add_annotation(annotations, annotation_text, annotation_pointer)
    out = {"statementId": statementID,
           "declarationSubject": recordID,
           "statementDate": statementDate,
           "recordId": recordID,
           "recordStatus": "new",
           "recordType": recordType,
           "recordDetails": {
               "isComponent": False,
               "entityType": {
                   "type": entityType
               },
               #"unspecifiedEntityDetails": ,
               "name": name,
               "alternateNames": [],
               "jurisdiction": jurisdiction,
               "identifiers": identifiers,
               "foundingDate": creation,
               #"dissolutionDate": ,
               "addresses": build_addresses(registeredAddress, businessAddress)
               #"uri": ,
               #"publicListing": ,
               #"formedByStatute": ,
           },
           'annotations': annotations,
           'publicationDetails': publication_details(),
           'source': source
          }
    return out

def person_id(item, api):
    """Identifier for person"""
    ident = api.person_identifier(item)
    last_update = api.update_date(item)
    return f"{ident}_{last_update}"

def transform_person(data, api):
    """Transform into BODS v0.4 entity"""
    item = api.extract_person_item(data)
    statementID = generate_statement_id(person_id(data, api), 'person')
    recordType = 'person'
    recordID = api.record_id(data)
    statementDate = format_date(api.update_date(data))
    unspecified = api.unspecified_person(item)
    if not unspecified:
        legal_name = format_name('legal', data, api)
        identifiers = [{'id': api.person_identifier(data),
                    'scheme': api.scheme,
                    'schemeName': api.scheme_name}]
        address = api.person_address(item)
        if address:
            personAddress = format_address('residence', address, api)
        else:
            personAddress = None
        birth_date = api.person_birth_date(item)
        tax_residency = api.person_tax_residency(item)
    else:
        legal_name = None
        identifiers = None
        personAddress = None
        birth_date = None
        tax_residency = None
    #identifiers += api.additional_identifiers(item)
    source = data_source(data, api)
    country = jurisdiction_name(api.jurisdiction(item))
    jurisdiction = {'name': country, 'code': api.jurisdiction(item)}
    annotations = []
    annotation_text, annotation_pointer = api.person_annotation(data)
    add_annotation(annotations, annotation_text, annotation_pointer)
    out = {"statementId": statementID,
           "declarationSubject": recordID,
           "statementDate": statementDate,
           "recordId": recordID,
           "recordStatus": "new",
           "recordType": recordType,
           "recordDetails": {
               "isComponent": False,
               "personType": "knownPerson" if not unspecified else "unknownPerson",
               #"unspecifiedPersonDetails": ,
               "names": [legal_name] if legal_name else [],
               "identifiers": identifiers if identifiers else [],
               #"nationalities": ,
               #"placeOfBirthAddress": ,
               "birthDate": birth_date,
               #"deathDate": ,
               "taxResidencies": [tax_residency] if tax_residency else [],
               "addresses": build_addresses(personAddress, None) if personAddress else [],
               #"politicalExposure": ,
           },
           'annotations': annotations,
           'publicationDetails': publication_details(),
           'source': source
          }
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
