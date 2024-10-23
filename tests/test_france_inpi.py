import json
import pytest

from boexplorer.search import fetch_all_data, process_data
from boexplorer.apis.france_inpi import FranceINPI
from boexplorer import config

@pytest.mark.asyncio
async def test_france_inpi():
    config.app_config = {"caching": {"cache_dir": "cache"}}
    api = FranceINPI()
    text = "LVMH"
    bods_data = {'entities': {}, 'persons': {}, 'sources': {}}
    _, company_data, persons_data = await fetch_all_data(api, text, bods_data)
    process_data(company_data, persons_data, api, bods_data, search=text)

    print(json.dumps(bods_data, indent=2))
    assert False
