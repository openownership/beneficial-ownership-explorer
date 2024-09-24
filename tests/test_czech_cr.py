import json
import pytest

from boexplorer.search import fetch_all_data
from boexplorer.apis.czech_cr import CzechCR

def test_czech_cr():
    api = CzechCR()
    text = "Skoda"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
