import json
import pytest

from boexplorer.search import fetch_all_data
from boexplorer.apis.slovakia_orsr import SlovakiaORSR

def test_slovakia_orsr():
    api = SlovakiaORSR()
    text = "Tatra Banka"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
