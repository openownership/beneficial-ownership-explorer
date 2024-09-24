import json
import pytest

from bodsexplorer.apis.gleif import GLEIF
from bodsexplorer.transforms.bods_0_2_0 import transform_relationship

@pytest.fixture
def relationship_json_data():
    """GLEIF LEI Record update"""
    with open("tests/fixtures/relationship_data.json", "r") as read_file:
        return json.load(read_file)

def test_transform_relationship(relationship_json_data):

    # Setup GLEIF api
    api = GLEIF()

    # Extract data
    data = api.extract_data(relationship_json_data)

    # Process data
    bods_data = []
    for item in data:
        bods_data.append(transform_relationship(item, api))

    assert len(bods_data) == 5

    print(json.dumps(bods_data[0]))
