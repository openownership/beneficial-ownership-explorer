import json
import pytest

from bodsexplorer.apis.gleif import GLEIF
from bodsexplorer.data.data import load_data
from bodsexplorer.transforms.bods_0_2_0 import transform_entity

from utils import date_now

@pytest.fixture
def entity_json_data():
    """GLEIF LEI Record update"""
    with open("tests/fixtures/entity_data.json", "r") as read_file:
        return json.load(read_file)

def test_transform_entities(entity_json_data):

    scheme_data = load_data()

    # Setup GLEIF api
    api = GLEIF(scheme_data=scheme_data)

    # Extract data
    data = api.extract_data(entity_json_data)

    # Process data
    bods_data = []
    for item in data:
        bods_data.append(transform_entity(item, api))

    assert len(bods_data) == 5

    print(json.dumps(bods_data[0], indent=2))

    assert bods_data[0]["statementID"] == "e219feb5-614e-7634-a657-d446870e9df1"
    assert bods_data[0]["statementType"] == "entityStatement"
    assert bods_data[0]["statementDate"] == "2024-04-08"
    assert bods_data[0]["entityType"] == "registeredEntity"
    assert bods_data[0]["name"] == "BRITISH COUNCIL(THE)"
    assert bods_data[0]["incorporatedInJurisdiction"] == {"name": "United Kingdom", "code": "GB"}
    assert bods_data[0]["identifiers"][0] == {"id": "213800S8DFQ6UFES2T83",
                                              "scheme": "XI-LEI",
                                              "schemeName": "Global Legal Entity Identifier Index"}
    for address in bods_data[0]["addresses"]:
        assert address in [{"type": "registered", "address": "1 REDMAN PLACE, STRATFORD, LONDON", "country": "GB"},
                            {"type": "business", "address": "1 REDMAN PLACE, STRATFORD, LONDON", "country": "GB"}]
    assert bods_data[0]["foundingDate"] == "1963-01-03"
    assert bods_data[0]["annotations"][0] == {"motivation": "commenting",
                                              "description": "GLEIF data for this entity - LEI: 213800S8DFQ6UFES2T83; Registration Status: ISSUED",
                                              "statementPointerTarget": "/",
                                              "creationDate": date_now(),
                                              "createdBy": {"name": "Open Ownership",
                                                            "uri": "https://www.openownership.org"}}
    assert bods_data[0]["publicationDetails"] == {"publicationDate": date_now(),
                                                  "bodsVersion": "0.2",
                                                  "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                                                  "publisher": {"name": "Open Ownership",
                                                                "url": "https://www.openownership.org"}}
    assert bods_data[0]["source"] == {"type": ["officialRegister", "verified"], "description": "GLEIF"}
