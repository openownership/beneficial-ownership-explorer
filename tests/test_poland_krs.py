import json
import pytest

from boexplorer.search import fetch_all_data, process_data
from boexplorer.apis.poland_krs import PolandKRS
from boexplorer import config

@pytest.mark.asyncio
async def test_poland_krs():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = PolandKRS()
    text = "TAURON POLSKA ENERGIA"
    bods_data = {'entities': {}, 'sources': {}}
    await fetch_all_data(api, text, bods_data)
    print(json.dumps(bods_data, indent=2))
    assert False

@pytest.mark.asyncio
async def test_poland_krs_2():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = PolandKRS()
    text = "GRUPA AZOTY"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False

