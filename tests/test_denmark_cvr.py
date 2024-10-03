import json
import pytest

from boexplorer.search import fetch_all_data, fetch_person_data
from boexplorer.apis.denmark_cvr import DenmarkCVR

def test_denmark_cvr():
    api = DenmarkCVR()
    text = "Lundbeck"
    bods_data = {'entities': {}, 'sources': {}}
    fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False

def test_denmark_cvr_person_search():
    api = DenmarkCVR()
    text = "Povlsen"
    bods_data = {'persons': {}, 'sources': {}}
    fetch_person_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
