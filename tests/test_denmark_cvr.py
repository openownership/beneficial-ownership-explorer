import json
import pytest

from boexplorer.search import fetch_all_data, fetch_person_data, process_data
from boexplorer.apis.denmark_cvr import DenmarkCVR

@pytest.mark.asyncio
async def test_denmark_cvr():
    api = DenmarkCVR()
    text = "Lundbeck"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    await fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_denmark_cvr_person_search():
    api = DenmarkCVR()
    text = "Povlsen"
    bods_data = {'persons': {}, 'sources': {}}
    await fetch_person_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False
