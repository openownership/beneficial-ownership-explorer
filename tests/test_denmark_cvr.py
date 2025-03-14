import json
import pytest

from boexplorer.search import (fetch_all_data, fetch_person_data, process_data,
                               process_person_data)
from boexplorer.apis.denmark_cvr import DenmarkCVR
from boexplorer import config

@pytest.fixture(scope="session")
def api():
    return DenmarkCVR()

@pytest.mark.asyncio
async def test_denmark_cvr(api):
    config.app_config = {"caching": {"cache_dir": "cache"}}
    text = "Lundbeck"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_denmark_cvr_person_search(api):
    config.app_config = {"caching": {"cache_dir": "cache"}}
    text = "Povlsen"
    bods_data = {'persons': {}, 'sources': {}}
    _, persons_data = await fetch_person_data(api, text, bods_data)
    process_person_data(persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_denmark_cvr_person_search_2(api):
    config.app_config = {"caching": {"cache_dir": "cache"}}
    text = "Jonas Schwarz Lausten"
    bods_data = {'persons': {}, 'sources': {}}
    _, persons_data = await fetch_person_data(api, text, bods_data)
    process_person_data(persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
