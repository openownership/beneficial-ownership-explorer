import json
import pytest

from boexplorer.search import fetch_all_data
from boexplorer.apis.nigeria_cac import NigerianCAC

def test_nigeria_cac():
    api = NigerianCAC()
    text = "Dangote Cement"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
