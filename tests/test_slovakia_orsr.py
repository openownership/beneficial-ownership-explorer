import json
import pytest

from boexplorer.search import (fetch_all_data, fetch_person_data, process_data,
                               process_person_data)
from boexplorer.apis.slovakia_orsr import SlovakiaORSR
from boexplorer import config

@pytest.mark.asyncio
async def test_slovakia_orsr():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = SlovakiaORSR()
    text = "Tatra Banka"
    bods_data = {'entities': {}, 'sources': {}}
    await fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_slovakia_orsr():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = SlovakiaORSR()
    text = "Transpetrol"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_slovakia_orsr_person_search():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = SlovakiaORSR()
    text = "Pinke"
    bods_data = {'persons': {}, 'sources': {}}
    _, persons_data = await fetch_person_data(api, text, bods_data)
    process_person_data(persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
