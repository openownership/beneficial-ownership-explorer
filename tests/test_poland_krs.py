import json
import pytest

from boexplorer.search import fetch_all_data
from boexplorer.apis.poland_krs import PolandKRS

def test_poland_krs():
    api = PolandKRS()
    text = "TAURON POLSKA ENERGIA"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
