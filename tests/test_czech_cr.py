import json
import pytest

from boexplorer.search import fetch_all_data, process_data
from boexplorer.apis.czech_cr import CzechCR
from boexplorer import config

@pytest.mark.asyncio
async def test_czech_cr():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = CzechCR()
    text = "Skoda"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
