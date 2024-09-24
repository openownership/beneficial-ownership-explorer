import json
import pytest

from boexplorer.search import fetch_all_data
from boexplorer.apis.france_inpi import FranceINPI

def test_france_inpi():
    api = FranceINPI()
    text = "LVMH"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
