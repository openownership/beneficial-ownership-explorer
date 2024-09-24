import json
import pytest

from boexplorer.search import fetch_all_data
from boexplorer.apis.estonia_rik import EstoniaRIK

def test_denmark_cvr():
    api = EstoniaRIK()
    text = "Alexela"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
